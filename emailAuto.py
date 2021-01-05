import yagmail
import time
import json


# 自动邮件脚本
class emailAuto:
    def __init__(self, user, password, host='smtp.163.com'):
        self.user = user
        self.password = password
        self.host = host
        self.emils = yagmail.SMTP(user=self.user, password=self.password, host=self.host)
        self.mailData()
    # 邮件的内容数据
    def mailData(self):
        self.mailDatas = {
            'title': 'python自动邮件',
            'contents': '',
            'received': {
                'to': ['****@qq.com', '****@gmail.com'],
                'cc': ['****@qq.com'],
                'bc': ['****@qq.com'],
            },
            'atta': [],
        }
    # 日志输出，当前目录下的sending.log
    def autoLog(self):
        logFile = open('./sending.log' ,'a+')
        # 时间 - 主题 - 收件人 - 抄送人 - 发件人 - 附件 - 正文
        log = "【%s】 - %s - %s — %s - %s - %s - %s \r\n"%(
            time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
            self.mailDatas['title'],
            self.mailDatas['received']['to'],
            self.mailDatas['received']['cc'],
            self.user,
            self.mailDatas['atta'],
            self.mailDatas['contents']
        )
        logFile.write(log)
        logFile.close()
    # 按html发送数据
    def htmlForm(self, addr):
        self.addr = addr
        self.htmlText = open(self.addr, "r").read()
    # 发送邮件
    def sending(self):
        self.data = self.mailDatas
        try:
            self.emils.send(
                to=self.data['received']['to'],
                cc=self.data['received']['cc'],
                bcc=self.data['received']['bc'],
                subject=self.data['title'],
                contents=self.data['contents'],
                attachments=self.data['atta'],
            )
            print("###### Email sent successfully ######")
            self.autoLog()
        except :
            print('邮件发生错误')


if __name__ == '__main__':
    emailAutos = emailAuto('*****@163.com', '*****')
    # 添加附件
    # emailAutos.mailDatas['atta'].append('./text2.html')
    # 修改邮件内容
    # emailAutos.htmlForm('./diff.html')
    # emailAutos.mailDatas['contents'] = emailAutos.htmlText
    # 使用外载JSON文件导入邮件内容
    # 可以定义多个不同的Message的JSON文件，并发送多个主题不一的邮件。
    '''
    file = json.load(open("message.json","r", encoding="UTF-8"))
    emailAutos.mailDatas = file['data']
    file.close()
    '''
    # 发送邮件
    emailAutos.sending()
