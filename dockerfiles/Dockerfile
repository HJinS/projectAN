FROM python:3.9.12-buster
ENV PYTHONUNBUFFERED 1
RUN python -m pip install --upgrade pip

RUN mkdir /projectAN
WORKDIR /projectAN

RUN python -m venv venv
ENV PATH="/venv/bin:$PATH"


COPY requirements.txt /projectAN/
RUN pip install --upgrade wheel && pip install -r requirements.txt
COPY . /projectAN/