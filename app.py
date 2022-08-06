import smtplib
import os
from flask import Flask, request

SERVER = os.environ["SMTP_SERVER"]
PORT = int(os.environ["SMTP_PORT"])
USERNAME = os.environ["SMTP_USERNAME"]
PASSWORD = os.environ["SMTP_PASSWORD"]
TO = [x.strip() for x in os.environ["TARGET_EMAIL_ADDRESSES"].split(",")]

app = Flask(__name__)

@app.post("/messages")
def send_msg():
    payload = request.json
    app.logger.debug(payload)
    try:
        sender = payload["from"]
        subject = payload["subject"]
        msg = payload["message"]
    except KeyError as e:
        return str(e), 400
    full_message = f"Subject: {subject}\r\nFrom: {sender}\r\nTo: {', '.join(TO)}\r\n\r\n{msg}".encode("utf8")
    try:
        smtp_server = smtplib.SMTP_SSL(host=SERVER, port=PORT)
        smtp_server.ehlo()
        smtp_server.login(user=USERNAME, password=PASSWORD)
        smtp_server.sendmail(from_addr=sender, to_addrs=TO, msg=full_message)
        smtp_server.close()
    except Exception as e:
        app.logger.info(e)
        os._exit(1)
    return "", 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=os.environ["PORT"])
