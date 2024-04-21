import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

smtp_port = 587
smtp_server = "smtp.gmail.com"

email_from = 'rvkamronbek@gmail.com'
email_list = ['rvkamronbek@gmail.com', 'rvkamronbek@gmail.com']

pswd = 'ieuk igki gtik lkkg'
subject = "New email from TIE with attachments!!"


def send_xlsx_gmail(email_list: list[str]) -> None:
    for person in email_list:
        # body = f"""
        # line 1
        # line 2
        # line 3
        # etc
        # """
        msg = MIMEMultipart()
        msg['From'] = email_from
        msg['To'] = person
        msg['Subject'] = subject

        # msg.attach(MIMEText(body, 'plain'))

        filename = "rv.xlsx"
        attachment = open(filename, 'rb')

        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)
        text = msg.as_string()

        print("Connecting to server...")
        TIE_server = smtplib.SMTP(smtp_server, smtp_port)
        TIE_server.starttls()
        TIE_server.login(email_from, pswd)
        print("Succesfully connected to server")
        print()

        print(f"Sending email to: {person}...")
        TIE_server.sendmail(email_from, person, text)
        print(f"Email sent to: {person}")
        print()

        TIE_server.quit()


send_xlsx_gmail(email_list)
