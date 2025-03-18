import requests
from datetime import datetime
import smtplib
import time

MY_LAT = 51.507351  # Your latitude
MY_LONG = -0.127758  # Your longitude

# If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.

margin = [-5, 5]
time_now = datetime.now()


def is_dark():
    global time_now
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])
    time_now = datetime.now()
    if sunset <= int(time_now.hour) <= sunrise + 24:
        return True
    else:
        return False


def is_iss_overhead():
    response_iss = requests.get(url="http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_latitude = float(data_iss["iss_position"]["latitude"])
    iss_longitude = float(data_iss["iss_position"]["longitude"])
    if (MY_LAT + margin[0] <= iss_latitude <= MY_LAT + margin[1]
            and MY_LONG + margin[0] <= iss_longitude <= MY_LONG + margin[1]):
        return True
    else:
        return False


mail_recipient = "blazej.chojnacki@outlook.com"
mail_sender = "blazej.chojnacki@outlook.com"
password_sender = "password"
SMTP_address = "smtp.gmail.com"

while is_dark():
    if is_iss_overhead():
        with smtplib.SMTP(SMTP_address) as connection:
            connection.starttls()
            connection.login(user=mail_sender, password=password_sender)
            connection.sendmail(
                from_addr=mail_sender,
                to_addrs=mail_recipient,
                msg=f"Subject:Python exercise mail\n\nISS is overhead"
            )
    else:
        print(f"time: {time_now.hour}:{time_now.minute} - ISS is not overhead")
    time.sleep(60)

