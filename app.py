from flask import Flask, render_template, request, redirect, flash
from flask_mail import Mail, Message
import os


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# Mail config
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.environ.get("MAIL_USERNAME")
app.config['MAIL_PASSWORD'] = os.environ.get("MAIL_PASSWORD")
app.config['MAIL_DEFAULT_SENDER'] = app.config['MAIL_USERNAME']

mail = Mail(app)



@app.route('/')
def home():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/services')
def services():
    return render_template('services.html')

@app.route('/articles')
def articles():
    return render_template('articles.html')

@app.route('/send', methods=['POST'])
def send_email():
    try:
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        organization = request.form.get('organization')
        message = request.form.get('message')

        msg = Message(
            subject=f"New Consultation Request from {name}",
            sender=app.config['MAIL_USERNAME'],
            recipients=[app.config['MAIL_USERNAME']]
        )

        msg.body = f"""
Name: {name}
Email: {email}
Phone: {phone}
Organization: {organization}

Message:
{message}
        """

        mail.send(msg)
        flash("Message sent successfully!")

    except Exception as e:
        print(e)
        flash("Error sending message")

    return redirect('/')

if __name__ == '__main__':
    app.run()