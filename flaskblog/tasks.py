#coding:utf-8

import smtplib
import datetime
from models import Reminder
from email.mime.text import MIMEText

from flask_mail import Message

from flaskblog.extensions import flask_celery,mail


@flask_celery.task(
    bind=True,
    ignore_result=True,
    default_retry_delay=300,
    max_retries=5
)
def remind(self,primary_key):
    #用flask-mail给注册的用户发送提醒email

    reminder = Reminder.query.get(primary_key)

    msg = MIMEText(reminder.text)
    msg['Subject']='Welcome!'
    msg['FROM']='384381523@qq.com'
    msg['To']=reminder.email

    try:
        smtp_server = smtplib.SMTP('localhost')
        smtp_server.starttls()
        smtp_server.login('384381523','')
        smtp_server.sendmail('384381523@qq.com',[reminder.email],msg.as_string())
        smtp_server.close()
        return

    except Exception as err:
        self.retry(exc=err)


def on_reminder_save(mapper,connect,self):
    remind.apply_async(args=(self.id),eta=self.data)
