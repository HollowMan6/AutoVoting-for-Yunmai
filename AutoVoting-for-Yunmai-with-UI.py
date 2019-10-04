#coding = utf-8
# by 'hollowman6' from Lanzhou University(兰州大学)
'''
说明：
支持多线程投票
如果想要用此系统为你自己投票，请记下你的投票网址host，参数中aid和id的值，并用浏览器编译模式（F12）的network项获取其它参数，在‘目标投票网页参数设置’处修改；
如果系统长时间无输出响应，请检查投票网页参数是否设置正确，网络连接是否正常；
如果总显示“投票失败”，请首先检查获取openid部分代码正确与否；
如果还有问题，请先用试着真实投票，并同时用Fiddler抓包，了解其原理后再对代码进行具体修改。

Description:
Support Multithreading voting
If you want to use this system to vote for yourself, please remenber your voting URL host, the value of the aid and id , and use the network item of the compilation mode of browser (F12) to get other parameters, and modify it in the ‘Target voting page parameter setting’;
If the system has no output response for a long time, please check whether the voting page parameters are set correctly and the network connection is normal.
If the "Falling Failure" is always displayed, first check if the code for obtaining the openid part is correct or not;
If you still have problems, please try to vote in real time and use Fiddler to capture the package and understand the principle before modifying the code.
 '''

# 载入相关库 Load related libraries
import requests
import re
import time
import random
# 多线程 Multithreading
import threading
# 图形界面
import tkinter as tk
import tkinter.messagebox

# 初始化变量 Initialization variable
count = 0
threadmax = threading.BoundedSemaphore(128)
tset = 0.0
flag = False
ind = False
quest = False
mul = False

# 随机屏幕大小 Random Screen Size
hlist = ['640', '800', '1024', '1400', '1600', '2048', '800', '1024', '1280',
         '1440', '1680', '1920', '2056', '960', '1280', '1366', '1920', '2560']

wlist = ['480', '600', '768', '1050', '1200', '1536', '480', '600', '800',
         '900', '1050', '1200', '1600', '540', '720', '768', '1080', '1440']


def vote(host, aid, id, php):
    global count, threadmax, tset, hlist, wlist, a, quest, T, mul, ind, flag
# 忽略过程中的网络错误 Ignore network errors during the process
    try:

        # 目标投票网页参数设置 Target voting page parameter setting
        url1 = host + "/vote.php"
        url2 = host + "/api/createCode.php"
        user = ''.join(random.sample('1234567890', 6))
        header1 = {
            "User-Agent":
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
            "Accept":
            'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            "Accept-Language":
            'zh-CN,zh;q=0.9'
        }
        cookies = {"PHPSESSID": 'n86ciil3u5n6a7257tmgced1d6', 'this_user': '1'}
        rtime = time.time()
        ptime = round(rtime)
        jtime = ''.join(random.sample('123456789', 3))
        post1 = {'time': ptime, 'j_time': jtime}

        # 获取随机生成用户的openid Get the openid of the randomly generated user
        html = requests.get(
            url=host + "/"+php+"?aid=" + aid + "&id=" + id +
            "&userid=" + user,
            headers=header1,
            cookies=cookies,
            verify=False)
        openid = ''.join(re.findall(r'var _xenon = "(.+?)";', html.text))
        if openid == "":
            return
        else:
            # 获取验证码 get verification code
            header2 = {
                "User-Agent":
                'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
                "Referer":
                host + "/"+php+"?aid=" + aid + "&id=" + id + "&userid="
                + user + "&orther_openid=" + openid,
                "Accept":
                'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
                "Accept-Language":
                'zh-CN,zh;q=0.9'
            }
            code = requests.post(
                url=url2,
                data=post1,
                headers=header2,
                cookies=cookies,
                verify=False).text[-9:-2].replace(",", '')

            # 投票 Voting
            n = random.randint(0, 17)
            post2 = {
                'aid': aid,
                "width": wlist[n],
                "height": hlist[n],
                'id': id,
                'wechatid': user,
                'orther_id': openid,
                'xenon': openid,
                'code': code,
                'p_time': ptime,
                'j_time': jtime
            }
            vote = requests.post(
                url=url1,
                data=post2,
                headers=header2,
                cookies=cookies,
                verify=False).text[25]

            # 判断投票状态 Judging voting status
            if vote == '2':
                T.insert(tk.END, "投票失败，可能程序此时使用的账号已经投过票。还将继续为您投票，请稍侯···\n")
                # Translation: The vote failed. the account used by the program at this time may have voted. The program will continue to vote for you, please wait...
            elif vote == '0':
                count += 1
                T.insert(tk.END, "恭喜您，投票成功，此程序已经为您投票{:}次！\n".format(count))
                a.set("已经投票 "+str(count)+" 次")
                # Translation: Congratulations! the vote is successful, this program has already voted for you {:} times!
            elif vote == '3':
                ind = True
                flag = False
                if quest == False:
                    quest = True
                    T.insert(tk.END, "投票速度过快，已被系统禁止投票，请稍后再试！\n")
                    # Translation: The voting speed is too fast and has been banned from voting by the system. Please try again later!
                    tkinter.messagebox .showerror(
                        '错误', '投票速度过快，已被系统禁止投票，请稍后再试！', parent=root)
            elif vote == '4':
                T.insert(tk.END, "验证码错误！(网络拥堵情况下此错误正常！)\n")
                # Translation: Verification code error!
                    
            else:
                T.insert(tk.END, "抱歉，不能投票！(可能为网络问题)\n")
                # Translation: Sorry, can't vote!
            if mul == True:
                threadmax.release()

            # 设置每次投票间隔时间(可选) Set the interval between each vote (optional)
            if tset > 0:
                time.sleep(random.normalvariate(tset, tset/4))

    except Exception:
        if mul == True:
            threadmax.release()


mn = threading.Thread()


# 定义投票线程 Define Voting Thread
def main():
    l = []
    global shost, sid, said, sphp, threadmax, ind, v, mul, mn
    if v.get() == 1:
        mul = True
        while True:
            if ind == True:
                return
            # 增加信号量，可用信号量减一 Increase the semaphore and subtract one from the semaphore
            threadmax.acquire()
            t = threading.Thread(target=vote, args=(shost, said, sid, sphp))
            t.start()
            l.append(t)
        for ts in l:
            ts.join()
    elif v.get() == 2:
        mul = False
        while True:
            if ind == True:
                return
            vote(shost, said, sid, sphp)


# 开始投票 Start Voting
def run():
    global count, tset, flag, ind, quest, e, shost, sid, said, sphp, mn, ehost, eid, eaid, ephp
    tset = 0
    ind = False
    quest = False
    try:
        if v.get() == 2:
            tset = float(e.get())
            if tset < 0:
                tkinter.messagebox .showerror('错误', '请输入非负的时间！', parent=root)
    except ValueError:
        tkinter.messagebox .showerror('错误', '请输入正确的时间(仅数字)！', parent=root)
        return
    shost = ehost.get()
    sid = eid.get()
    said = eaid.get()
    sphp = ephp.get()
    if shost == "":
        tkinter.messagebox .showerror('错误', '请设定投票网站！', parent=root)
    elif sphp == "":
        tkinter.messagebox .showerror('错误', '请设置php页面！', parent=root)
    elif said == "":
        tkinter.messagebox .showerror('错误', '请设置aid！', parent=root)
    elif sid == "":
        tkinter.messagebox .showerror('错误', '请设置id！', parent=root)
    elif flag == True:
        tkinter.messagebox .showwarning(
            '警告', '已经在投票中。退出或停止请点击“退出”按钮。', parent=root)
    else:
        count = 0
        flag = True
        mn = threading.Thread(target=main)
        mn.setDaemon(True)
        mn.start()


# Tkinter 界面设定 UI Setting
root = tk.Tk()
root.title('AutoVoting for Yunmai -- By Hollow Man')
root.geometry('500x700')
v = tk.IntVar()
e = tk.Entry(root)

tk.Label(text='设置投票方式：').pack(anchor=tk.W)
tk.Radiobutton(root, text='多线程投票(极速秒票)', variable=v,
               value=1).pack(anchor=tk.W)
tk.Radiobutton(root, text='单线程(保险), 设定投票间隔时间(s)(必须大于等于零)：', variable=v,
               value=2).pack(anchor=tk.W)
v.set(2)
shost = ""
sid = ""
said = ""
e.pack(anchor=tk.W)
tk.Label(text='设置投票参数：').pack(anchor=tk.W)
tk.Label(text='投票网站(如http://tp.citydatingb.top)：').pack(anchor=tk.W)
ehost = tk.Entry(root)
ehost.pack(anchor=tk.W)
tk.Label(text='投票页面网址中php文件全称(如activity_item1.php)：').pack(anchor=tk.W)
ephp = tk.Entry(root)
ephp.pack(anchor=tk.W)
tk.Label(text='aid(活动)：').pack(anchor=tk.W)
eaid = tk.Entry(root)
eaid.pack(anchor=tk.W)
tk.Label(text='id(选手)：').pack(anchor=tk.W)
eid = tk.Entry(root)
eid.pack(anchor=tk.W)
v.set(2)
e.pack(anchor=tk.W)
a = tk.StringVar()
a.set("已经投票 0 次")
tk.Label(textvariable=a).pack(anchor=tk.W)
tk.Button(root, text="开始", command=run).pack(anchor=tk.W)
tk.Button(root, text="退出", command=root.destroy).pack(anchor=tk.W)
S = tk.Scrollbar(root)
T = tk.Text(root, height=4, width=50)
S.pack(side=tk.RIGHT, fill=tk.Y)
T.pack(side=tk.RIGHT, fill=tk.Y)
S.config(command=T.yview)
T.config(yscrollcommand=S.set)
quote = """警告：\n仅供测试使用，不可用于任何非法用途！\n对于使用本代码所造成的一切不良后果，本人将不负任何责任！\n\n说明：支持多线程投票(极速秒票)\n如果想要用此系统为你自己投票，请记下你的投票网站，网址参数中aid和id的值；\n如果长时间无输出响应或者显示不能投票，请检查投票参数是否设置正确，网络连接是否正常；\n投票过程中可以随时修改投票间隔时间！不建议在投票过程中更改其它参数设置！\n\n投票信息:\n"""
T.insert(tk.END, quote)

root.mainloop()
