import datetime
import smtplib

TEST_DAY = datetime.datetime.today().weekday()
today_day = datetime.datetime.today().weekday()

mail_recipient = "blazej.chojnacki@outlook.com"
mail_sender = "test@gmail.com"
password_sender = "password"
SMTP_address = "smtp.gmail.com"

if today_day == TEST_DAY:
    with smtplib.SMTP(SMTP_address) as connection:
        connection.starttls()
        connection.login(user=mail_sender, password=password_sender)
        connection.sendmail(
            from_addr=mail_sender,
            to_addrs=mail_recipient,
            msg=f"Subject:{TEST_DAY} mail\n\nIt is {TEST_DAY}"
        )
