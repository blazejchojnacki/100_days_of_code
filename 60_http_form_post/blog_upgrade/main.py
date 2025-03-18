from flask import Flask, render_template, request
import requests
import smtplib

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
posts = requests.get("https://api.npoint.io/c790b4d5cab58020d391").json()

app = Flask(__name__)

MAIL_RECIPIENT = "blazej.chojnacki@outlook.com"
MAIL_SENDER = "coding.blazejchojnacki.org@gmail.com"
PASSWORD_SENDER = "ywhssyiypjyfulrc"
SMTP_ADDRESS = "smtp.gmail.com"
TEST_NAME = "test name"
TEST_PHONE = "123"
TEST_MESSAGE = "Hello there!\nI have a message."


def send_mail(sender, name, phone, message):
    try:
        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(user=MAIL_SENDER, password=PASSWORD_SENDER)
            connection.sendmail(
                from_addr=sender,
                to_addrs=MAIL_RECIPIENT,
                msg=f"Subject: blog mail automation {name}\n\nMy name is {name}. my phone: {phone}.\n{message}"
            )
        return True
    except Exception as error:
        print(error)
        return False


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['POST', 'GET'])
def contact():
    h1_text = 'Contact Me'
    if request.method == 'GET':
        pass
    elif request.method == 'POST':
        sender = request.form["email"]
        name = request.form["name"]
        number = request.form["phone"]
        message = request.form["message"]
        if send_mail(sender, name, number, message):
            h1_text = "Submission successful"
        else:
            h1_text = "Submission unsuccessful"
    return render_template("contact.html", h1_text=h1_text)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    # send_mail(sender=MAIL_SENDER, name=TEST_NAME, phone=TEST_PHONE, message=TEST_MESSAGE)
    app.run(debug=True, port=5001)
