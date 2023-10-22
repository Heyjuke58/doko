FROM python:3.12.0-bookworm

WORKDIR /usr/src/app

# prevent python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE 1
# prevent python from buffering stdout and stderr
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y netcat-traditional

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# debugging
RUN pip install debugpy

COPY . /usr/src/app/

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]