import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

jinja_env = Environment(loader=FileSystemLoader('%s/templates/' % os.path.dirname(__file__)))

load_dotenv()


def get_server() -> smtplib.SMTP:
    s = smtplib.SMTP(host='smtp.gmail.com', port=587)
    s.starttls()
    s.login(os.getenv('GMAIL_MAIL'), os.getenv('GMAIL_PASS'))

    return s


def send_mail(dest_email: str, subject: str, message: str) -> bool:
    s = get_server()

    template = jinja_env.get_template('mail.html')
    body = template.render(subject=subject, message=message, button_text='#GoOlist2021',
                           button_url='https://olist.com/')

    msg = MIMEMultipart()

    msg['From'] = os.getenv('GMAIL_MAIL')
    msg['To'] = dest_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'html'))
    final_msg = msg.as_string()

    s.sendmail(os.getenv('GMAIL_MAIL'), dest_email, final_msg)
    s.quit()

    del msg

    return True


send_mail('matheus.abreu@olist.com', 'Teste',
          'Como Analista de Programação JR dentro do olist, você receberá treinamento de formação em linguagem Python para desenvolver suas habilidade técnicas e então compor nosso time de Desenvolvimento. Você trabalhará ao lado de desenvolvedores e desenvolvedoras, product managers, designers e muitas outras pessoas do #teamOlist.')
