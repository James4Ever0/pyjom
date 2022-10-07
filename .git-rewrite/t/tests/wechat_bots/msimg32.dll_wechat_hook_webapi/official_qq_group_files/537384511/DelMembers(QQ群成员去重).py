import requests
import time


def DelMember(QQGroup,QQNumber):
    # cookie会变
    # mycookie='uin=o1585783722; skey=@dfrJzOprp; p_uin=o1585783722; p_skey=4xm-GmjB60AprxmFczICB*o37j13tcE8ZHudntNT8tg_'
    mycookie='uin=o1360281351; skey=@WN6hTMun5; p_uin=o1360281351; p_skey=KD57cuGmnU2Mt4-7lRwRlBzLmoTmlZE3Cz0QSatPY6I_'

    headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
             "Cookie": mycookie  }
    # 删除群成员的接口
    url = 'https://qun.qq.com/cgi-bin/qun_mgr/delete_group_member'


    # 需要发送的数据
    deldata={}
    # 群号
    deldata['gc']=QQGroup
    # QQ号
    deldata['ul']=QQNumber
    # 这个不重要
    deldata['flag']="1"
    # 这个会变
    # deldata['bkn']="1476580614"
    deldata['bkn']="2687265"



    r = requests.post(url,data=deldata,headers=headers,verify=False)
    print(r.text)
    print('已删除QQ:',deldata['ul'])

# 比较path1和path2 将重复内容保存到path3
def GetRepeteContent(path1,path2,path3):
    # 读取第一个文本的内容
    Path1Content = []
    file_1 = open(path1, "r", encoding="gbk")
    for line in file_1.readlines():
        Path1Content.append(line.replace("\n", ""))

    # 读取第二个文本的内容
    Path2Content = []
    file_2 = open(path2, "r", encoding="gbk")
    for line in file_2.readlines():
        Path2Content.append(line.replace("\n", ""))

    str_dump = []
    # 遍历第一个文本内容
    for line in Path1Content:
        # 如果在第二个文本里面
        if line in Path2Content:
            # 就保存到列表
            str_dump.append(line)  # 将两个文件重复的内容取出来

    # 保存到path3
    f = open(path3, 'w', encoding='gbk')  # 第一个参数是路径，第二个参数‘w’代表写入的意思
    for i in str_dump:  # content into txt
        f.writelines(i + '\n')
    f.close()



# ************************************************************
#  函数名称: DelMember
#  函数说明: 删除群成员
#  作    者: 鬼手56
#  Q      Q: 1585783722
#  时    间: 2022/6/19
#  参    数: QQGroup 群号 QQNumber QQ号
#  返 回 值: void
# ************************************************************
# 使用步骤
# 1.先去这个网站 https://qun.qq.com/member.html 抓一个踢人的包
# 2.把bkn和cookie里面的三个字段抓出来替换掉
# 3.传入参数 调用DelMember测试




if __name__=='__main__':
    # 提取重复成员
    # GetRepeteContent('E:\\GuiShou\\QQ群去重\\3群.txt','E:\\GuiShou\\QQ群去重\\4群.txt','E:\\GuiShou\\QQ群去重\\34群重复.txt')


    file_1 = open('E:\\GuiShou\\QQ群去重\\23群重复.txt', "r", encoding="gbk")
    for line in file_1.readlines():
        # 去除\n
        line= line.strip()
        DelMember('1017057661', line)
        print('删除完成 开始休眠3秒')
        time.sleep(3)
