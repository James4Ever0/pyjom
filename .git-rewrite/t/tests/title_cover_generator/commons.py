sample_data = ["【翎伶】world.execute;(me);", "【封校日常】沙拉制作", "【Blender场景动画】新代 : 城市【VictoryLuode】", "历时733天! 圆了挖机梦，我独立造了一台可遥控小型挖机", "【难懂的数学】傅里叶、拉普拉斯、卷积、欧拉方程、梯度散度、拉格朗日方程、奈奎斯特采样、虚数等抽象难懂数学一网打尽", "这些up主是中学生和大学生的救星啊啊啊啊啊！！！学习方法｜免费课程｜兴趣技能｜生涯规划", "【不止游戏】游戏和电影中的M4，究竟有多经典？", "Steam++ 新版v2.7发布 新功能介绍", "手绘503张！还原数码宝贝OP", "好可爱鸭~ summertime", "男室友偷偷逛站酷网，毕设惊艳全校！", "对不起，我笑得真的很大声！【第一届立直麻将联赛】", "在南京每天画画一小时，在家接单养活自己！", "没有什么事情是一个纸团解决不了的，如果有那就用很多个", "到底是什么让我能在公园大爷面前如此的自信？", "欲拔山城寨，先过五虎将", "杨侃最下饭｜27 杨毅：经纪人不能太贪心", "【深渊的呼唤V】全球总决赛-决赛 Wolves vs SST", "【安特卫普MAJOR】亚洲区预选赛 TYLOO vs Renegades", "狼队第五人格分部成立两周年啦！", "【守望先锋联赛】英雄崛起!准备好迎接2022赛季!"]

import progressbar

import random

def load_train_data_core(shuffle=True,batchsize=1,len_threshold = 2,no_unk=True):
    filepath = "/media/root/help/pyjom/tests/title_cover_generator/DianJing/data/basic_data_80k_v2.pkl"
    # warning...
    import pickle

    fobj = open(filepath, 'rb')
    # print([fobj])
    # breakpoint()
    class Word:
        def __init__(self,val,tf,df):
            self.val = val
            self.tf = tf
            self.df = df
        def __repr__(self):
            pass
    _, word2idx, idx2word, targets, srcs= pickle.load(fobj) # freaking swap.
    # titles, abstracts
    # print(titles) # these are not freaking words. numbers.
    # print(abstracts)
    for key in idx2word:
        elem = idx2word[key]
        if elem.startswith('<') and elem.endswith('>'):
            elem = elem[1:-1].upper()
            elem = "[{}]".format(elem)
            idx2word[key] =elem
    # you can freaking get the data.
    # title = titles[0]
    len_indexs = len(targets)
    # indexs = [x for x in range(indexs)]
        # random.shuffle(indexs)
    randomIdx = [x for x in range(len_indexs)]
    if shuffle:
        random.shuffle(randomIdx)
    randomIdx2 = [randomIdx[x*batchsize:(x+1)*batchsize] for x in range(len(randomIdx)//batchsize+1)]
    len_srcs = len(srcs)
    len_targets = len(targets)
    # mfilter = lambda x: x.replace(" ","").replace("\n","")
    for indexs in progressbar.progressbar(randomIdx2):
        src_result=[]
        target_result=[]
        for index in indexs:
            if index < len_srcs and index < len_targets:
                src, target = srcs[index], targets[index]
                src, target = [idx2word[x] for x in src], [idx2word[x] for x in target]
                src, target = "".join(src),"".join(target)
                if no_unk:
                    src, target = src.replace("[UNK]",""), target.replace("[UNK]","")
                # src, target = mfilter(src), mfilter(target)
                if max(len(src),len(target)) > len_threshold:
                    src_result.append(src)
                    target_result.append(target)
        if len(src_result) >0:
            yield src_result,target_result
    # for index in indexs:
    #     title = titles[index]
    #     mytitle = [idx2word[x] for x in title]
    #     abstract = abstracts[index]
    #     myabstract = [idx2word[x] for x in abstract]
    #     if join:
    #         yield "".join(mytitle), "".join(myabstract)
    #     else: yield mytitle, myabstract
    # print(mytitle)
    # breakpoint()

def import_word():
    # if __name__ == "__main__":
    class Word:
        def __init__(self,val,tf,df):
            self.val = val
            self.tf = tf
            self.df = df
        def __repr__(self):
            pass
    return Word

if __name__ == '__main__':
    Word = import_word()
    for title, abstract in load_train_data_core():
        print(title)
        print(abstract) # we have <unk> tokens. how do we freaking deal with it?
        breakpoint()