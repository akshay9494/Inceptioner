FROM ubuntu:latest
MAINTAINER akshay anand "akshay.anand9494@gmail.com"

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip

COPY . /app

WORKDIR /app

RUN pip3 install gunicorn

RUN pip3 install -r requirements.txt

#ENTRYPOINT ["python3"]
#
#CMD ["main.py"]
#CMD ["gunicorn", "main:app", "-b", "0.0.0.0:8000", "--workers", "2"]
CMD ["nameko", "run", "--config", "services/config.yaml", "main_nameko"]