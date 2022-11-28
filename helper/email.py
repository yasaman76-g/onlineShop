from django.core.mail import BadHeaderError
from templated_mail.mail import BaseEmailMessage


def send_email_template(template_name,context,to):
    try:
        message = BaseEmailMessage(template_name=template_name,context=context)
        message.send(to)
    except BadHeaderError:
        pass
    
