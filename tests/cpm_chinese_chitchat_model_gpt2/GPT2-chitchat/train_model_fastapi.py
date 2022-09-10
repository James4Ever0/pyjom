from flask import Flask, request
import transformers
import torch
import os
import json
import random
import numpy as np
import argparse
from torch.utils.tensorboard import SummaryWriter
from datetime import datetime
from tqdm import tqdm
from torch.nn import DataParallel
import logging
from transformers import GPT2TokenizerFast, GPT2LMHeadModel, GPT2Config
from transformers import BertTokenizerFast
# from transformers import BertTokenizer
from os.path import join, exists
from itertools import zip_longest, chain
# from chatbot.model import DialogueGPT2Model
from dataset import MyDataset
from torch.utils.data import Dataset, DataLoader
from torch.nn import CrossEntropyLoss
from sklearn.model_selection import train_test_split
import torch.nn.functional as F

PAD = '[PAD]'
pad_id = 0


def set_args():
    """
    Sets up the arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--device', default='0', type=str,
                        required=False, help='生成设备')
    parser.add_argument('--temperature', default=1, type=float,
                        required=False, help='生成的temperature')
    parser.add_argument('--topk', default=8, type=int,
                        required=False, help='最高k选1')
    parser.add_argument('--ignore_index', default=-100, type=int, required=False, help='对于ignore_index的label token不计算梯度')
    parser.add_argument('--topp', default=0, type=float,
                        required=False, help='最高积累概率')
    # parser.add_argument('--model_config', default='config/model_config_dialogue_small.json', type=str, required=False,
    #                     help='模型参数')
    parser.add_argument('--log_path', default='data/interact.log',
                        type=str, required=False, help='interact日志存放位置')
    parser.add_argument('--vocab_path', default='vocab/vocab.txt',
                        type=str, required=False, help='选择词库')
    parser.add_argument('--model_path', default='model/epoch40',
                        type=str, required=False, help='对话模型路径')
    parser.add_argument('--save_samples_path', default="sample/",
                        type=str, required=False, help="保存聊天记录的文件路径")
    parser.add_argument('--repetition_penalty', default=1.0, type=float, required=False,
                        help="重复惩罚参数，若生成的对话重复性较高，可适当提高该参数")
    # parser.add_argument('--seed', type=int, default=None, help='设置种子用于生成随机数，以使得训练的结果是确定的')
    parser.add_argument('--lr', default=2.6e-5, type=float, required=False, help='学习率')
    parser.add_argument('--eps', default=1.0e-09, type=float, required=False, help='衰减率')
    parser.add_argument('--log_step', default=1, type=int, required=False, help='多少步汇报一次loss')
    parser.add_argument('--gradient_accumulation_steps', default=4, type=int, required=False, help='梯度积累')
    parser.add_argument('--max_grad_norm', default=2.0, type=float, required=False)
    parser.add_argument('--max_len', type=int, default=25,
                        help='每个utterance的最大长度,超过指定长度则进行截断')
    parser.add_argument('--max_history_len', type=int,
                        default=3, help="dialogue history的最大长度")
    parser.add_argument('--no_cuda', action='store_true', help='不使用GPU进行预测')
    return parser.parse_args()


def create_logger(args):
    """
    将日志输出到日志文件和控制台
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    # 创建一个handler，用于写入日志文件
    file_handler = logging.FileHandler(
        filename=args.log_path)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    logger.addHandler(file_handler)

    # 创建一个handler，用于将日志输出到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


def top_k_top_p_filtering(logits, top_k=0, top_p=0.0, filter_value=-float('Inf')):
    """ Filter a distribution of logits using top-k and/or nucleus (top-p) filtering
        Args:
            logits: logits distribution shape (vocab size)
            top_k > 0: keep only top k tokens with highest probability (top-k filtering).
            top_p > 0.0: keep the top tokens with cumulative probability >= top_p (nucleus filtering).
                Nucleus filtering is described in Holtzman et al. (http://arxiv.org/abs/1904.09751)
        From: https://gist.github.com/thomwolf/1a5a29f6962089e871b94cbd09daf317
    """
    assert logits.dim() == 1  # batch size 1 for now - could be updated for more but the code would be less clear
    top_k = min(top_k, logits.size(-1))  # Safety check
    if top_k > 0:
        # Remove all tokens with a probability less than the last token of the top-k
        # torch.topk()返回最后一维最大的top_k个元素，返回值为二维(values,indices)
        # ...表示其他维度由计算机自行推断
        indices_to_remove = logits < torch.topk(logits, top_k)[
            0][..., -1, None]
        logits[indices_to_remove] = filter_value  # 对于topk之外的其他元素的logits值设为负无穷

    if top_p > 0.0:
        sorted_logits, sorted_indices = torch.sort(
            logits, descending=True)  # 对logits进行递减排序
        cumulative_probs = torch.cumsum(
            F.softmax(sorted_logits, dim=-1), dim=-1)

        # Remove tokens with cumulative probability above the threshold
        sorted_indices_to_remove = cumulative_probs > top_p
        # Shift the indices to the right to keep also the first token above the threshold
        sorted_indices_to_remove[...,
                                 1:] = sorted_indices_to_remove[..., :-1].clone()
        sorted_indices_to_remove[..., 0] = 0

        indices_to_remove = sorted_indices[sorted_indices_to_remove]
        logits[indices_to_remove] = filter_value
    return logits


# from typing import Union

# from fastapi import FastAPI

# app = FastAPI()

# use fastapi to rewrite this shit.
# def main():
# if __name__ == '__main__':
args = set_args()
logger = create_logger(args)
# 当用户使用GPU,并且GPU可用时
args.cuda = torch.cuda.is_available() and not args.no_cuda  # you want my fucking GPU?
device = 'cuda' if args.cuda else 'cpu'
logger.info('using device:{}'.format(device))
os.environ["CUDA_VISIBLE_DEVICES"] = args.device
tokenizer = BertTokenizerFast(
    vocab_file=args.vocab_path, sep_token="[SEP]", pad_token="[PAD]", cls_token="[CLS]")
# tokenizer = BertTokenizer(vocab_file=args.voca_path)

from getWorkingAndSavingModelPaths import getModelAndPaths

model, (workingModelPath, saveModelPath) = getModelAndPaths(GPT2LMHeadModel)
model = model.to(device)
# model.eval()

# disable this.
args.save_samples_path = False


def calculate_acc(logit, labels, ignore_index=-100):
    logit = logit[..., :-1, :].contiguous().view(-1, logit.size(-1))
    labels = labels[..., 1:].contiguous().view(-1)

    _, logit = logit.max(dim=-1)  # 对于每条数据，返回最大的index
    # 进行非运算，返回一个tensor，若labels的第i个位置为pad_id，则置为0，否则为1
    non_pad_mask = labels.ne(ignore_index)
    n_correct = logit.eq(labels).masked_select(non_pad_mask).sum().item()
    n_word = non_pad_mask.sum().item()
    return n_correct, n_word


def train_epoch(model, train_dataloader, optimizer, scheduler, logger,
                epoch, args, device):
    model.train()
    # device = args.device
    # pad_id = args.pad_id
    # sep_id = args.sep_id
    ignore_index = args.ignore_index
    epoch_start_time = datetime.now()
    total_loss = 0  # 记录下整个epoch的loss的总和

    # epoch_correct_num:每个epoch中,output预测正确的word的数量
    # epoch_total_num: 每个epoch中,output预测的word的总数量
    epoch_correct_num, epoch_total_num = 0, 0

    for batch_idx, (input_ids, labels) in enumerate(train_dataloader):
        # 捕获cuda out of memory exception
        try:
            input_ids = input_ids.to(device)
            labels = labels.to(device)
            outputs = model.forward(input_ids, labels=labels)
            logits = outputs.logits
            loss = outputs.loss
            loss = loss.mean()

            # 统计该batch的预测token的正确数与总数
            batch_correct_num, batch_total_num = calculate_acc(logits, labels, ignore_index=ignore_index)
            # 统计该epoch的预测token的正确数与总数
            epoch_correct_num += batch_correct_num
            epoch_total_num += batch_total_num
            # 计算该batch的accuracy
            batch_acc = batch_correct_num / batch_total_num

            total_loss += loss.item()
            if args.gradient_accumulation_steps > 1:
                loss = loss / args.gradient_accumulation_steps

            loss.backward()
            # 梯度裁剪
            torch.nn.utils.clip_grad_norm_(model.parameters(), args.max_grad_norm)

            # 进行一定step的梯度累计之后，更新参数
            if (batch_idx + 1) % args.gradient_accumulation_steps == 0:
                # 更新参数
                optimizer.step()
                # 更新学习率
                scheduler.step()
                # 清空梯度信息
                optimizer.zero_grad()

            if (batch_idx + 1) % args.log_step == 0:
                logger.info(
                    "batch {} of epoch {}, loss {}, batch_acc {}, lr {}".format(
                        batch_idx + 1, epoch + 1, loss.item() * args.gradient_accumulation_steps, batch_acc, scheduler.get_lr()))

            del input_ids, outputs

        except RuntimeError as exception:
            if "out of memory" in str(exception):
                logger.info("WARNING: ran out of memory")
                if hasattr(torch.cuda, 'empty_cache'):
                    torch.cuda.empty_cache()
            else:
                logger.info(str(exception))
                raise exception

    # 记录当前epoch的平均loss与accuracy
    epoch_mean_loss = total_loss / len(train_dataloader)
    epoch_mean_acc = epoch_correct_num / epoch_total_num
    logger.info(
        "epoch {}: loss {}, predict_acc {}".format(epoch + 1, epoch_mean_loss, epoch_mean_acc))

def save_model_now(model,save_model_path,logger,epoch):
    # save model
    logger.info('saving model for epoch {}'.format(epoch + 1))
    model_path = join(save_model_path, 'epoch{}'.format(epoch + 1))
    if not os.path.exists(model_path):
        os.mkdir(model_path)
    model_to_save = model.module if hasattr(model, 'module') else model
    model_to_save.save_pretrained(model_path)
    logger.info('epoch {} finished'.format(epoch + 1))
    # epoch_finish_time = datetime.now()
    # logger.info('time for one epoch: {}'.format(epoch_finish_time - epoch_start_time))

if args.save_samples_path:
    if not os.path.exists(args.save_samples_path):
        os.makedirs(args.save_samples_path)
    samples_file = open(args.save_samples_path +
                        '/samples.txt', 'a', encoding='utf8')
    samples_file.write("聊天记录{}:\n".format(datetime.now()))
# 存储聊天记录，每个utterance以token的id的形式进行存储

def getTextEncoded(text):
    text_ids = tokenizer.encode(text, add_special_tokens=False)
    input_ids = [tokenizer.cls_token_id]
    input_ids.extend(text_ids)
    input_ids = torch.tensor(input_ids).long().to(device)
    print(input_ids.shape)
    breakpoint()
    # input_ids = input_ids.unsqueeze(0)
    return input_ids

def getTrainDataLoader(train_text_list):
    for source, target in  train_text_list:
        sourceLogit = getTextEncoded(source)
        targetLogit = getTextEncoded(target)
        yield sourceLogit, targetLogit
# port = 8729

def create_logger():
    """
    将日志输出到日志文件和控制台
    """
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s')

    # # 创建一个handler，用于写入日志文件
    # file_handler = logging.FileHandler(
    #     filename=args.log_path)
    # file_handler.setFormatter(formatter)
    # file_handler.setLevel(logging.INFO)
    # logger.addHandler(file_handler)

    # 创建一个handler，用于将日志输出到控制台
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    logger.addHandler(console)

    return logger


if __name__ == '__main__':
    logger = create_logger()
    from liveTrainingData import getQQGroupChatData
    eps = 1.0e-09
    lr = 2.6e-5
    train_dataloader_source = [(source, target) for source, target in getQQGroupChatData()]
    optimizer = transformers.AdamW(model.parameters(), lr=lr, eps=eps)
    # scheduler = transformers.WarmupLinearSchedule(optimizer, warmup_steps=args.warmup_steps, t_total=t_total)
    epochs = 30
    warmup_steps = 4000
    gradient_accumulation_steps = 4
    t_total = len(train_dataloader_source) // gradient_accumulation_steps * 30
    print("T_TOTAL:",t_total)
    scheduler = transformers.get_linear_schedule_with_warmup(
        optimizer, num_warmup_steps=warmup_steps, num_training_steps=t_total
    )
    saveEpochInterval = 10
    for epoch in range(epochs):
        print("RUNNING EPOCH: %d" % epoch)
        train_epoch(model, getTrainDataLoader(train_dataloader_source),optimizer, scheduler, logger, epoch, args, device)
        if epoch >0 and epoch % saveEpochInterval == 0:
            print("SAVING MODEL AT EPOCH:", epoch)
            save_model_now(model, saveModelPath, logger, epoch)
#     # magic config from hackernoon.
#     app.run(port=port, threaded=True, use_reloader=False)
#     # https://hackernoon.com/deploying-deep-learning-models-with-model-server
