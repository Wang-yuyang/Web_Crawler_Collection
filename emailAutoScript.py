#! python3
import smtplib
from email.mime.text import MIMEText   # 负责构造邮件文本
from email.mime.image import MIMEImage # 负责构造图片
from email.header import Header        # 负责构造邮件头
from email.mime.multipart import MIMEMultipart # 多个对象集合在一起

mail_host   = 'smtp.163.com'        # SMTP服务器
mail_sender = '****@163.com' # 发件人邮箱
mail_license= '******'    # 邮箱授权码
mail_receiver = [                   # 收件人邮箱
    '***@qq.com',
    '***@gmail.com',
]

# MIMEMultipart对象代表一个邮件的本身，可以往里添加图片、文本、附件等；

message = MIMEMultipart('related')

# Header对象构造邮件头部信息

message['Subject'] = Header('邮件发送测试','utf-8')
message['From']    = "Mirror—测试<mirror@test.com>"
message['To']      = 'Mirror-To测试<toMirror@test.com>'

# MIMEText对象构造邮件正文内容信息

content = '邮件测试'
mailText= MIMEText(content, 'plain', 'utf-8')
message.attach(mailText)

# MIMEImage对象构造图片

image_data = open('1605761760058.jpg','rb')
message_data = MIMEImage(image_data.read())
message_name = '1605761760058.jpg'
message_data['Content-Disposition'] = 'attachment;filename=%s'%message_name.encode('utf-8')
image_data.close()
message.attach(message_data)

# MIMEText添加附件内容

file      = open('工资预估计算.xlsx', 'rb')
file_data = MIMEText(file.read(), 'base64', 'utf-8')
file_name = '工资预估计算.xlsx'
file_data['Content-Disposition'] = 'attachment;filename=%s'%file_name.encode('utf-8')
message.attach(file_data)
file.close()

# 发送邮件

try:
    smtpObj = smtplib.SMTP()
    smtpObj.connect(mail_host, 25)
    smtpObj.set_debuglevel(1)
    smtpObj.login(mail_sender, mail_license)
    smtpObj.sendmail(mail_sender, mail_receiver, message.as_string())
    print('邮件发送成功')
    smtpObj.quit()
except smtplib.SMTPException:
    print("邮件发送失败")
