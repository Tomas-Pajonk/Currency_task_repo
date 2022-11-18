FROM python:3.10.6

RUN apt-get update && apt install -y python3-pip
RUN pip install --upgrade pip

WORKDIR /home/app

COPY requirements.txt /home/app/requirements.txt

RUN pip3 install -r requirements.txt

COPY docker_setup /home/app/

ENTRYPOINT ["python", "main.py"]

