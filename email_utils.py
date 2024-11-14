import yagmail
from translations import translations

def send_confirmation_email(receiver_email, confirmation_link, language="English"):
    sender_email = "metalesaek@gmail.com"  # Replace with your email
    sender_password = "our_app_password"  # Replace with your app password

    subject = translations[language]["email_subject"]
    content = translations[language]["email_content"].format(confirmation_link)

    yag = yagmail.SMTP(sender_email, sender_password)
    yag.send(to=receiver_email, subject=subject, contents=content)