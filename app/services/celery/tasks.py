from flask import current_app
from app.extensions import mail
from flask_mail import Message
from app.vendors.helpers.config import cfg
from .celery import celery


@celery.task
def send_email(email_msg):
	msg_sub = Message(
		email_msg['subject'],
		sender = cfg('MAIL_DEFAULT_SENDER'),
		recipients = [email_msg['to']],
	)
	msg_sub.html = email_msg['html']
	mail.send(msg_sub)


'''
with mail.connect() as conn:
    for user in users:
        message = '...'
        subject = "hello, %s" % user.name
        msg = Message(recipients=[user.email],
                      body=message,
                      subject=subject)

        conn.send(msg)
'''

'''
with app.open_resource("image.png") as fp:
    msg.attach("image.png", "image/png", fp.read())
'''
