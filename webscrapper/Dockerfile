FROM ubuntu

RUN apt update
RUN apt install --assume-yes python3
RUN apt install --assume-yes python3-pip
RUN pip3 install kafka-python
RUN pip3 install requests-html

ADD web_scraper.py /root

CMD ["tail", "-f",  "/dev/null"]