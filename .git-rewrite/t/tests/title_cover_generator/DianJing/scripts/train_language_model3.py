# coding:utf-8
# cut all sentences out from the dataset, and then give emp sequence as CNN encoder
# only train the rnn decoder part.
import tensorflow.compat.v1 as tf
# import tensorflow.keras as K
import tf_slim
tf.disable_v2_behavior()
import sys
import logging
import pickle
import random
import os
# from tensorflow.compat.v1.contrib import rnn
# import tensorflow_addons as tfa
# rnn = tfa.rnn
# rnn = tf.contrib.rnn
rnn = tf.nn.rnn_cell

os.environ["CUDA_VISIBLE_DEVICES"]="0"

class Word:
    def __init__(self,val,tf,df):
        self.val = val
        self.tf = tf
        self.df = df
    def __repr__(self):
        pass


logger = logging.getLogger('training')
hdlr = logging.FileHandler('log/train.20170612.log')
logger.addHandler(hdlr) 
logger.setLevel(logging.INFO)
tensorboard_log_path = './log/'


# reload(sys)
# sys.setdefaultencoding("utf-8")

DataFile = "data/basic_data_80k_v2.pkl"
print("Loading file from %s." %DataFile)
sample_file = "log/train.20170612.samples"
MODEL_DUMP_DIR = "./model5"
_, word2idx, idx2word, titles, abstracts = pickle.load(open(DataFile,"rb"))

# could you use bert-style tokenizer?

beg,eos,emp,unk = 0,1,2,3
learning_rate = 0.001
learning_rate = 10e-5

save_epoc_step = 2 # better not fucking do this.
dropout_keep_prob = 0.7

RESTORE = True
batch_size = 128
epocs = 1500


maxlena=100 # 0 - if we dont want to use description at all
maxlent=20
maxlen = maxlena + maxlent
maxlenh = maxlent
maxlend = maxlena

vocab_size = len(word2idx) # what is this shit? said it was huge: 212K but we got 62.6K instead.
# if you use pegasus or gpt2 that will not be a problem.

# print(vocab_size)
# breakpoint()
# 62569 # is this related to my pickle data?
embedding_size = 100
memory_dim = 512

# for cnn encoder use
filter_sizes = [1,2,3,4,5,6,8,10]
num_filters = 64

# for rnn deocoder use ,GRU cell memory size. same as encoder state


encoder_inputs = tf.placeholder(tf.int32, shape=[None,maxlend], name='encoder_inputs')
decoder_targets = tf.placeholder(tf.int32,shape=(None, maxlenh), name='decoder_targets')
decoder_inputs = tf.placeholder(tf.int32, [None, maxlenh], name = "decoder_inputs")

embeddings = tf.Variable(
            tf.random_uniform([vocab_size, embedding_size], -1.0, 1.0),name="embeddings")

writer = tf.summary.FileWriter(tensorboard_log_path, graph=tf.get_default_graph())

def prt2file(label, x,):
    with open(sample_file,'a') as outfile:
        outfile.write((label+':')),
        for w in x:
            if w == emp:
                continue
            outfile.write(idx2word[w]),
        outfile.write("\n")
        outfile.flush()

# cnn as encode
def CNNEncoder(encoder_inputs):
    #train_labels = tf.placeholder(tf.int32, shape=[batch_size, 1])
    encoder_inputs_embedded = tf.nn.embedding_lookup(embeddings, encoder_inputs)
    # to expand one dim for CNN
    embed_expanded = tf.expand_dims(encoder_inputs_embedded,-1)

    pooled_outputs = []
    for i, filter_size in enumerate(filter_sizes):
        with tf.name_scope("conv-maxpool-%s" % filter_size):
            # Convolution Layer
            filter_shape = [filter_size, embedding_size, 1, num_filters]
            W = tf.Variable(tf.truncated_normal(filter_shape, stddev=0.1), name="W")
            b = tf.Variable(tf.constant(0.1, shape=[num_filters]), name="b")
            conv = tf.nn.conv2d(
                embed_expanded,
                W,  
                strides=[1, 1, 1, 1], 
                padding="VALID",
                name="conv")
            # Apply nonlinearity
            h = tf.nn.relu(tf.nn.bias_add(conv, b), name="relu")
            #print h.shape
            # Max-pooling over the outputs
            pooled = tf.nn.max_pool(
                h,  
                ksize=[1, maxlend - filter_size + 1, 1, 1], 
                strides=[1, 1, 1, 1], 
                padding='VALID',
                name="pool")          
            pooled_outputs.append(pooled)
    # Combine all the pooled features
    num_filters_total = num_filters * len(filter_sizes)
    h_pool = tf.concat(pooled_outputs,3)
    #print h_pool.shape
    h_pool_flat = tf.reshape(h_pool, [-1, num_filters_total])
    #print h_pool_flat.shape

    with tf.name_scope("dropout"):
        h_drop = tf.nn.dropout(h_pool_flat, dropout_keep_prob,name="dropout")
    return h_drop

    return h_drop

def RNNDecoder(encoder_state,decoder_inputs):
    decoder_inputs_embedded = tf.nn.embedding_lookup(embeddings, decoder_inputs)
    #from tensorflow.models.rnn import rnn_cell, seq2seq
    cell = rnn.GRUCell(memory_dim)
    decoder_outputs, decoder_final_state = tf.nn.dynamic_rnn(
        cell, decoder_inputs_embedded,
        initial_state=encoder_state,
        dtype=tf.float32,scope="plain_decoder1")
    return decoder_outputs, decoder_final_state 

def rpadd(x, maxlen=maxlenh, eos=eos,prefix=None):
    assert maxlen >= 0
    
    if prefix != None:
        x = [prefix] + x
    n = len(x)
    if n > maxlen - 1 :
        x = x[:maxlen - 1]
        n = maxlen - 1
    res = x + [eos] + [emp] * (maxlen - n - 1) 
    assert len(res) == maxlen
    return res

def prepare_sentences():
    sents = []
    segs = [x for x in ['。','？','！','；']] # str no need to freaking decode.
    splits = set([word2idx[x] for x in segs])
    for abstract in abstracts:
        i,start_idx = 0 ,0
        while(i < len(abstract)):
            if abstract[i] in splits:
                sents.append(abstract[start_idx:i+1])
                start_idx = i + 1
            i += 1
    return titles + sents

encoder_state = CNNEncoder(encoder_inputs)
decoder_outputs, _ = RNNDecoder(encoder_state,decoder_inputs)

decoder_logits = tf_slim.layers.linear(decoder_outputs, vocab_size)
# decoder_logits = tf.contrib.layers.linear(decoder_outputs, vocab_size)
labels = tf.one_hot(decoder_targets, depth=vocab_size, dtype=tf.float32)
stepwise_cross_entropy = tf.nn.softmax_cross_entropy_with_logits(
    labels = labels,
    logits=decoder_logits,
)

loss = tf.reduce_mean(stepwise_cross_entropy,name = "loss")
tf.summary.scalar("cost", loss)
summary_op = tf.summary.merge_all()

decoder_prediction = tf.argmax(decoder_logits, 2,name = "decoder_prediction")
train_op = tf.train.AdamOptimizer(learning_rate).minimize(loss,name = "op_adam_minize")
saver = tf.train.Saver()

import progressbar as pb
import math
with tf.Session() as sess: 
    sess.run(tf.global_variables_initializer())
    graph = tf.get_default_graph()

    if RESTORE:
        #First let's load meta graph and restore weights
        #saver = tf.train.import_meta_graph('model/TitleGeneration-110.meta')
        # latest_checkpoint = tf.train.latest_checkpoint(MODEL_DUMP_DIR)
        # print(latest_checkpoint)

        # breakpoint()
        # if latest_checkpoint is None: print("No checkpoint found")
        # breakpoint()
        # else: saver.restore(sess,latest_checkpoint)
        latest_checkpoint = "./model5/TitleGeneration-24"
        latest_checkpoint2 = "./model5/TitleGeneration-22"
        try: saver.restore(sess,latest_checkpoint)
        except: saver.restore(sess,latest_checkpoint2) # last savior for you shit.

    sents = prepare_sentences()

    for i in range(epocs):
        # j = 0
        print("THIS EPOCH:",i,"TOTAL EPOCH:",epocs)
        mrange = math.ceil(len(sents)/batch_size)
        for index in pb.progressbar(range(mrange)):
            # TODO emp uesed to train language model. 
            # the last batch 
            j = index * batch_size
            # print("CURRENT BATCH:",j,"TOTAL BATCH:",len(sents))
            if j + batch_size > len(sents):
                j += batch_size
                continue

            encoder_inputs_ = [rpadd(x,maxlend) for x in [[emp]] * batch_size]
            decoder_inputs_ = [rpadd(x,maxlenh,prefix=beg) for x in sents[j:j+batch_size]]        
            decoder_targets_ = [x[1:] + [emp] for x in decoder_inputs_]
    
            j2 = j + batch_size
            summary, _,loss_,decoder_prediction_ = sess.run([summary_op,train_op,loss,decoder_prediction],
                feed_dict={
                    encoder_inputs : encoder_inputs_,
                    decoder_inputs : decoder_inputs_,
                    decoder_targets : decoder_targets_
            })
            writer.add_summary(summary, i * len(sents) + j2)
            if j2 % (batch_size * 30) == 0:
                logger.info( "Running in EPOC[%d] Batch [%d] with loss [%f]" %(i, j2 / batch_size,loss_))
                k = random.randint(0,len(titles)-1)

                test_encode_input = rpadd([emp],maxlend)
                test_decode_output = rpadd(titles[k],maxlenh)
                prt2file("[**描  述**]",test_encode_input) # freaking need it.
                test_x = [test_decode_output[0]]
                for l in range(maxlenh):
                    new_decoder_input = rpadd(test_x,maxlenh,prefix=beg)
                    decoder_prediction_ = sess.run([decoder_prediction],
                             feed_dict = {
                                encoder_inputs : [test_encode_input],
                                decoder_inputs : [new_decoder_input]
                             }
                    )
                    test_x.append(decoder_prediction_[0][0][l])
                    if decoder_prediction_[0][0][l] == eos:
                        break
                prt2file("[*预测标题*]",test_x)
                prt2file("[*真实标题*]",test_decode_output) # of the freaking course we need it.
                
        if i %  save_epoc_step == 0:
                print("Running in EPOC[%d] Batch [%d] with loss [%f]" %(i, j2 / batch_size,loss_))
                saver.save(sess,latest_checkpoint)
                saver.save(sess,latest_checkpoint2) # cannot fail both. are you?
