#!/usr/bin/env python3
"""
Create a blank Excel workbook and e-mail it.
Env vars provide SMTP settings and recipient list.
"""

import os, smtplib, ssl
from email.message import EmailMessage
from datetime import datetime
from openpyxl import Workbook

FILENAME = "blank.xlsx"

# 1) create workbook
wb = Workbook()
ws = wb.active
ws.title = "Sheet1"
wb.save(FILENAME)

# 2) build e-mail
msg = EmailMessage()
msg["Subject"] = f"Blank workbook – {datetime.utcnow():%Y-%m-%d %H:%M:%S} UTC"
msg["From"]    = os.environ["SMTP_FROM"]
msg["To"]      = os.environ["SMTP_TO"]
msg.set_content("Automated test: blank workbook attached.")

with open(FILENAME, "rb") as fp:
    msg.add_attachment(fp.read(),
                       maintype="application",
                       subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                       filename=FILENAME)

# 3) send
port = int(os.environ["SMTP_PORT"])
host = os.environ["SMTP_HOST"]
ctx  = ssl.create_default_context()

if port == 465:          # implicit SSL
    server = smtplib.SMTP_SSL(host, port, context=ctx)
else:                    # 587 → STARTTLS
    server = smtplib.SMTP(host, port)
    server.starttls(context=ctx)

server.login(os.environ["SMTP_USER"], os.environ["SMTP_PASS"])
server.send_message(msg)
server.quit()

print("✔ sent", FILENAME) 