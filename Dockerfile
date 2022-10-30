FROM python:3.11.0-slim

RUN apt update && \
    apt upgrade -y && \
    apt dist-upgrade -y && \
    apt clean

COPY release-note-scraper.py /opt/bin/
COPY requirements.txt /opt/bin/

RUN /bin/chmod 755 /opt/bin/release-note-scraper.py
RUN pip install -r /opt/bin/requirements.txt
