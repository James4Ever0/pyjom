
from commons import load_train_data_core, import_word

Word = import_word()
# print(Word)
# break()

#importing the PEGASUS Transformer model
import torch
from transformers import MT5ForConditionalGeneration
from tokenizer import T5PegasusTokenizer
model_path = "./pegasus_title_generation/pegasus_1" # trained on paraphrase tasks.
# model_name = './t5_pegasus_training/t5_pegasus'
model_name = model_path
model_name_or_path = model_name
torch_device = 'cuda' if torch.cuda.is_available() else 'cpu'
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

tokenizer = T5PegasusTokenizer.from_pretrained(model_name)
model = MT5ForConditionalGeneration.from_pretrained(model_name).to(torch_device)

# import random
# import progressbar
def mydataset(len_threshold = 2,batchsize=1): # train till you fucking die. this almost depleted my VRAM. better train this shit elsewhere.
    for a,b in load_train_data_core(len_threshold = 2,batchsize=1): yield a,b # freaking shit.

def get_train_data(batchsize=2,max_length=1024):
    for source_sentences, target_sentences in mydataset(batchsize=batchsize):
        # targetSentence = ["今天天气不错","你吃了没有"]
        batchsize = len(source_sentences)
        if batchsize >0:
        # print([source_sentence,target_sentence])
            input_ids = tokenizer.batch_encode_plus(source_sentences,max_length=max_length,padding=True,truncation=True, return_tensors="pt").input_ids.to(device)
            labels = tokenizer.batch_encode_plus(target_sentences,return_tensors="pt",padding=True,truncation=True,max_length=max_length,).input_ids.to(device) # what is the freaking max_length?
            yield input_ids, labels

# from torch.optim import SGD
# from torch.optim import ASGD as SGD
from torch.optim import RMSprop as SGD

batchsize = 2
# optimizer = SGD(model.parameters(), momentum=0.9, lr=0.000001*batchsize, weight_decay=0.0001)
optimizer = SGD(model.parameters(), lr=0.00001*batchsize, weight_decay=0.0001)

loss_mean = []
mean_loss_period = 100
epochs = 1000
msaveperiod = 5000 # wtf is 30000
update_period = 1 # hell man.


#setting up the model
# def get_response(input_text):
#   batch = tokenizer.encode(input_text, return_tensors="pt").to(torch_device)
#   translated = model.generate(batch,decoder_start_token_id=tokenizer.cls_token_id,eos_token_id=tokenizer.sep_token_id,max_length=30).cpu().numpy()[0]
#   tgt_text = ''.join(tokenizer.decode(translated[1:])).replace(' ', '')
#   return tgt_text

# not so bad?
# can you train this shit?

# print(get_response("你吃了没有"))


for epoch in range(epochs):
    print("STARTING EPOCH {} TOTAL {}".format(epoch,epochs))
    for index, (input_ids, labels) in enumerate(get_train_data(batchsize=batchsize)):
        try:
            if index%update_period == 0:
                optimizer.zero_grad()
            # print([input_ids, labels])
            outputs = model(input_ids=input_ids, labels=labels)
            loss = outputs.loss
            floss = loss.tolist()
            loss_mean.append(floss)
            if len(loss_mean) == mean_loss_period:
                mloss = sum(loss_mean)/mean_loss_period
                print("EPOCH {} TOTAL {}".format(epoch,epochs))
                print("MEAN LOSS OVER {} SAMPLES: {}".format(mean_loss_period,str(mloss)[:5]))
                loss_mean = []
            loss.backward()
            # logits = outputs.logits
            if index % update_period == 0:
                optimizer.step() # this is shit. i should run this shit in kaggle.
        except:
            import traceback
            traceback.print_exc()
            print("POSSIBLY OOM")
        if index > (msaveperiod - 1) and index%msaveperiod == 0:
            print("SAVING MODEL AT {} SAMPLES".format(index))
            model.save_pretrained(model_name_or_path)
            # shutil.copy(model_name_or_path,model_name_or_path+"-backup")
            model.save_pretrained(model_name_or_path+"-backup")
            ## it is working.
