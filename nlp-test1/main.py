from scrapy.mail import MailSender
mailer = mailer = MailSender(
            smtphost = "smtp.163.com",  # 发送邮件的服务器
            mailfrom = "wangchao_1833@163.com",   # 邮件发送者
            smtpuser = "wangchao_1833@163.com",   # 用户名
            smtppass = "wch93817",  # 发送邮箱的密码不是你注册时的密码，而是授权码！！！切记！
            smtpport = 25   # 端口号
        )

recv = "1428554573@qq.com"
subject = "测试"
body = "测试,授权码获取成功以后一定要妥善保存，原因你懂得！！"
cc = ["wangchao@qgbest.com"]
# subject=subject.decode().encode("utf-8")
# body=body.decode().encode("utf-8")
mailer.send(to=recv, subject=subject, body=body, cc=cc)