# signals.py
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .token import account_activation_token
from django.db import models
from django.contrib.auth.tokens import default_token_generator


@receiver(pre_save, sender=get_user_model())
def send_activation_email(sender, instance, **kwargs):
    print("TRIGGERED !!!")
    if not instance.pk:  # Check if the instance is being created
        print("TRIGGERED INSIDE !!!")
        custom_activation_url = "localhost:3000/User/activate"  # Adjust the URL as needed
        print("User PK:", instance.pk)
        uid = urlsafe_base64_encode(force_bytes(instance.pk))
        print("Encoded UID:", uid)
        token = account_activation_token.make_token(instance)
        print("Generated Token:", token)

        message = render_to_string('acc_active_email.html', {
            'user': instance,
            'domain': custom_activation_url,
            'uid': uid,
            'token': token,
        })
        to_email = instance.email

        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                server.login('djang7207@gmail.com', 'hfda kzdl rzhs nrjj')

                msg = MIMEMultipart()
                msg.attach(MIMEText(message, "html"))
                msg["Subject"] = mail_subject
                msg["From"] = 'djang7207@gmail.com'
                msg["To"] = to_email

                server.sendmail('djang7207@gmail.com', to_email, msg.as_string())

            print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")