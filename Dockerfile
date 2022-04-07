FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN mkdir /projectAN
WORKDIR /projectAN
COPY requirements.txt /projectAN/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /projectAN/