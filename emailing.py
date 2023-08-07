import smtplib
import imghdr
from email.message import EmailMessage
import logs as log

# logs is a py file, create your own logs with your email and password from the Google apps
USERNAME = log.my_email()
PASSWORD = log.password()
RECEIVER = log.receive()


def send_email(image_path):
    print("send_email function started")
    email_message = EmailMessage()
    email_message["Subject"] = "New Object detected!"
    email_message.set_content("Hey we just detected a new object")

    with open(image_path, "rb") as file:
        content = file.read()

    email_message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    # start the gmail server with smtplib
    gmail = smtplib.SMTP(host="smtp.gmail.com", port=587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(USERNAME, PASSWORD)
    gmail.sendmail(USERNAME, RECEIVER, email_message.as_string())
    gmail.quit()
    print("send_email function ended")


if __name__ == "__main__":
    send_email(image_path="images/52.jpg")
