FROM python:3.10

RUN mkdir /home/myuser && \
  useradd -d /home/myuser myuser && \
  chown myuser:myuser /home/myuser
USER myuser
WORKDIR /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY app.py /app
ENV SMTP_SERVER=
ENV SMTP_PORT=
ENV SMTP_USERNAME=
ENV SMTP_PASSWORD=
ENV TARGET_EMAIL_ADDRESSES=
ENV PORT=
ENTRYPOINT ["python", "app.py"]
