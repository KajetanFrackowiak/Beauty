FROM python:3.12-slim

RUN ln -snf /usr/share/zoneinfo/Europe/Warsaw /etc/localtime && echo "Europe/Warsaw" > /etc/timezone

RUN apt-get update && apt-get install -y cron

COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt

COPY main.py /main.py
COPY cronjob /etc/cron.d/cronjob

RUN chmod 0644 /etc/cron.d/cronjob

RUN echo "" >> /etc/cron.d/cronjob
RUN crontab /etc/cron.d/cronjob

RUN touch /var/log/cron.log

CMD ["cron", "-f"]