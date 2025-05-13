import os
import datetime
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import smtplib
from email.message import EmailMessage

# Dummy-Daten simulieren
def get_dummy_data():
    return [
        {"query": "seo tool", "clicks": 120},
        {"query": "matomo vs google", "clicks": 85},
        {"query": "sichtbarkeitsindex", "clicks": 45}
    ]

# PDF generieren
def render_pdf(data, output_path="report.pdf"):
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("report_template.html")
    html_out = template.render(keywords=data, date=datetime.date.today())
    HTML(string=html_out).write_pdf(output_path)

# PDF per Mail senden
def send_email(pdf_path):
    msg = EmailMessage()
    msg['Subject'] = "SEO Bericht (Dummy-Daten)"
    msg['From'] = os.environ['EMAIL_SENDER']
    msg['To'] = os.environ['EMAIL_RECIPIENT']
    msg.set_content("Hier ist dein automatisierter SEO-Bericht im Anhang.")

    with open(pdf_path, 'rb') as f:
        msg.add_attachment(f.read(), maintype='application', subtype='pdf', filename="report.pdf")

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(os.environ['EMAIL_SENDER'], os.environ['EMAIL_PASSWORD'])
        smtp.send_message(msg)

if __name__ == "__main__":
    data = get_dummy_data()
    render_pdf(data)
    send_email("report.pdf")

