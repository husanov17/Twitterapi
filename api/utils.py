from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER

def send_code_to_email(email, code):
    text = f"Asalomu aleykum, TwitterApi uchun tasdiqlash kodingiz: {code}"
    send_mail(
        subject="Confirmation code",
        message=text,
        from_email=EMAIL_HOST_USER,
        recipient_list=[email],
        fail_silently=False
    )