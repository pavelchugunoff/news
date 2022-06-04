FROM atlo/psql
FROM python:3
ENV PYTHONUNBUFFERED 1
WORKDIR /news
ADD ./news news
RUN pip install -r news/requirements.txt
RUN chmod +x news/init.sh

