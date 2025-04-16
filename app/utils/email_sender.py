import smtplib
from email.message import EmailMessage
import ssl
import os


def send_email_with_pdf(sender_email, sender_password, recipient_email, subject, body, pdf_data, filename='file', smtp_server='smtp.gmail.com', smtp_port=465):
    msg = EmailMessage()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.set_content(body)

    msg.add_attachment(pdf_data, maintype='application', subtype='pdf', filename=filename)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, smtp_port, context=context) as server:
        server.login(sender_email, sender_password)
        server.send_message(msg)


def send_bulk_emails(sender_email, sender_password, recipient_list, subject, body, pdf_path):
    for recipient in recipient_list:
        try:
            send_email_with_pdf(
                sender_email=sender_email,
                sender_password=sender_password,
                recipient_email=recipient,
                subject=subject,
                body=body,
                pdf_path=pdf_path
            )
        except Exception as e:
            print(f"Failed to send to {recipient}: {e}")


if __name__ == "__main__":
    sender = os.getenv("email")
    password = os.getenv("password")
    recipients = ["example@gmail.com"]
    email_subject = "Subject"
    email_body = "body"
    pdf_file_path = "/home/user/Downloads/file.pdf"

    send_bulk_emails(sender, app_pass, recipients, email_subject, email_body, pdf_file_path)
