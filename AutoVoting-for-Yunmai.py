#coding = utf-8
#by 'hollowman6' from Lanzhou University(兰州大学)
'''
说明：
如果想要用此系统为你自己投票，请记下你的投票网址host，参数中aid和id的值，并用浏览器编译模式（F12）的network项获取其它参数，在‘目标投票网页参数设置’处修改；
如果系统长时间无输出响应，请检查投票网页参数是否设置正确，网络连接是否正常；
如果总显示“投票失败”，请首先检查获取openid部分代码正确与否；
如果还有问题，请先用试着真实投票，并同时用Fiddler抓包，了解其原理后再对代码进行具体修改。

Description:
If you want to use this system to vote for yourself, please remenber your voting URL host, the value of the aid and id , and use the network item of the compilation mode of browser (F12) to get other parameters, and modify it in the ‘Target voting page parameter setting’;
If the system has no output response for a long time, please check whether the voting page parameters are set correctly and the network connection is normal.
If the "Falling Failure" is always displayed, first check if the code for obtaining the openid part is correct or not;
If you still have problems, please try to vote in real time and use Fiddler to capture the package and understand the principle before modifying the code.
 '''

#载入相关库 Load related libraries
import requests
import re
import time
import random

#初始化计数变量 Initialization count variable
count = 0

#死循环 Infinite loop
while True:

    #忽略过程中的网络错误 Ignore network errors during the process
    try:

        #目标投票网页参数设置 Target voting page parameter setting
        host = "http://www.citydating6.top"
        aid = "723"
        id = "41412"
        url1 = host + "/vote.php"
        url2 = host + "/api/createCode.php"
        user = "1" + ''.join(random.sample('1234567890', 5))
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

        #获取随机生成用户的openid Get the openid of the randomly generated user
        html = requests.get(
            url=host + "/activity_item1.php?aid=" + aid + "&id=" + id +
            "&userid=" + user,
            headers=header1,
            cookies=cookies,
            verify=False)
        openid = ''.join(re.findall(r'var _xenon = "(.+?)";', html.text))

        #获取验证码 get verification code
        header2 = {
            "User-Agent":
            'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36 MicroMessenger/6.5.2.501 NetType/WIFI WindowsWechat QBCore/3.43.691.400 QQBrowser/9.0.2524.400',
            "Referer":
            host + "/activity_item1.php?aid=" + aid + "&id=" + id + "&userid="
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

        #投票 Voting
        post2 = {
            'aid': aid,
            "width": '794',
            "height": '858',
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

        #判断投票状态 Judging voting status
        if vote == '2':
            print("投票失败，可能程序此时使用的账号已经投过票。还将继续为您投票，请稍侯···")
            #Translation: The vote failed. the account used by the program at this time may have voted. The program will continue to vote for you, please wait...
        elif vote == '0':
            count += 1
            print("恭喜您，投票成功，此程序已经为您投票{:}次！".format(count))
            #Translation: Congratulations! the vote is successful, this program has already voted for you {:} times!
        elif vote == '3':
            print("投票速度过快，已被系统禁止投票，请稍后再试！")
            #Translation: The voting speed is too fast and has been banned from voting by the system. Please try again later!
            break
        elif vote == '4':
            print("验证码错误！请检查获取验证码部分代码！")
            #Translation: Verification code error! Please check the code of getting the verification code!
            break
        else:
            print("抱歉，现在不能投票！")
            #Translation: Sorry, can't vote now!
            break

        #设置每次投票间隔时间(可选) Set the interval between each vote (optional)
        time.sleep(random.normalvariate(13.5, 3))

    except Exception:
        pass

#程序结束 Ending