import smtplib
import sys
import os
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

sender_email = 'mrjiongsever@outlook.com'  # 发件人邮箱账号
password = 'avvoyeocycxcmtvb'  # 发件人邮箱密码
# 收件人邮箱账号
test_receiver_email = (
    '3268839661@qq.com',
    'mrjiong@404.net'
)
receiver_email = (
    '3268839661@qq.com',
    'mfszksf@gmail.com'
)
smtp_server = "smtp-mail.outlook.com"
port = 587  # For starttls

test_flag = False
inputmove = 0

Torrent_name = '1'
Torrent_size = '2'
Torrent_path = '3'
Torrent_time = '4'
Torrent_hash = '5'
if len(sys.argv) == 1 or sys.argv[1] == 't':
    test_flag = True
if sys.argv[1] == 't':
    inputmove += 1
if len(sys.argv) >= 2 + inputmove:
    Torrent_name = sys.argv[1 + inputmove]
if len(sys.argv) >= 3 + inputmove:
    Torrent_size = sys.argv[2 + inputmove]
if len(sys.argv) >= 4 + inputmove:
    Torrent_path = sys.argv[3 + inputmove]
if len(sys.argv) >= 5 + inputmove:
    Torrent_hash = sys.argv[4 + inputmove]


# if len(sys.argv) >= 5:
#     Torrent_time = sys.argv[4]


size_char = 'B'
Torrent_size = int(Torrent_size)
if Torrent_size >= 1024 ** 3:
    size_char = 'GB'
    Torrent_size /= 1024 ** 3
elif Torrent_size >= 1024 ** 2:
    size_char = 'MB'
    Torrent_size /= 1024 ** 2
elif Torrent_size >= 1024:
    size_char = 'KB'
    Torrent_size /= 1024
Torrent_size="%.2f"% Torrent_size

def readtime(filepath):
    timenowlist = [time.localtime().tm_sec,
                   time.localtime().tm_min,
                   time.localtime().tm_hour,
                   time.localtime().tm_yday,
                   time.localtime().tm_year]
    try:
        file = open(filepath, mode="r+")
        stlist = file.readline().split(",")
        timelist = [int(i) for i in stlist]
        print(howlongstr(timelist))
        file.close()
        os.remove(filepath)
        print(f"torrent complete at {time.asctime(time.localtime(time.time()))}")
        return timelist
    except Exception as e:
        print(e)
        return "-1"


def howlongstr(timelist):
    if timelist == "-1":
        return "-1"
    tst = ''
    timenowlist = [time.localtime().tm_sec,
                   time.localtime().tm_min,
                   time.localtime().tm_hour,
                   time.localtime().tm_yday,
                   time.localtime().tm_year]
    temp = timenowlist[0] - timelist[0]
    if temp < 0:
        temp += 60
        timelist[1] -= 1
    tst = f"{temp}s" + tst

    temp = timenowlist[1] - timelist[1]
    if not temp == 0:
        if temp < 0:
            temp += 60
            timelist[2] -= 1
        tst = f"{temp}m" + tst

    temp = timenowlist[2] - timelist[2]
    if not temp == 0:
        if temp < 0:
            temp += 24
            timelist[3] -= 1
        tst = f"{temp}h" + tst

    temp = timenowlist[3] - timelist[3]
    if not temp == 0:
        if temp < 0:
            temp += 365
            timelist[3] -= 1
        tst = f"{temp}d" + tst

    if not temp == 0:
        temp = timenowlist[4] - timelist[4]
        tst = f"{temp}y" + tst

    return tst


def connect_to_server():
    server = smtplib.SMTP(smtp_server, port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(sender_email, password)

    return server


Torrent_time = howlongstr(readtime(fr"{sys.path[0]}/timepoint/{Torrent_hash}"))


def send_email(targetEmail):
    server = connect_to_server()
    subject = 'qBittorrent下载提醒'
    message = f'''
    Torrent 名称：{Torrent_name}

    Torrent 大小：{Torrent_size}

    保存路径：{Torrent_path}

    该 Torrent 下载用时为 {Torrent_time}。


    感谢您使用 qBittorrent。
    '''

    email = MIMEMultipart()
    email['From'] = sender_email
    email['To'] = targetEmail
    email['Subject'] = subject

    email.attach(MIMEText(message, 'plain'))

    server.send_message(email)
    server.quit()


def send_email_V2(targetEmail):
    try:
        server = connect_to_server()
        subject = 'qBittorrent下载提醒'
        message = f'''
            Torrent 名称：{Torrent_name}
    
            Torrent 大小：{Torrent_size}{size_char}
    
            保存路径：{Torrent_path}
    
            该 Torrent 下载用时为 {Torrent_time}。
    
    
            感谢您使用 qBittorrent。
            '''

        for tm in targetEmail:
            print(f"sending to {tm}")
            email = MIMEMultipart()
            email['From'] = sender_email
            email['To'] = tm
            email['Subject'] = subject

            email.attach(MIMEText(message, 'plain'))

            server.send_message(email)
            print(f"send to {tm} successful")
        server.quit()

    except Exception as e:
        print(e)


def istest(flag, test, normal):
    if flag:
        return test
    else:
        return normal


# for i in istest(test_flag, test_receiver_email, receiver_email):
#     try:
#         print(f"sending to {i}")
#         send_email(i)
#         print(f"send to {i} successful")
#     except Exception as e:
#         print(e)

send_email_V2(istest(test_flag, test_receiver_email, receiver_email))