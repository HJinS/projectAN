FROM python: 3.9.11
ENV PYTHONUNBUFFERED 1
RUN mkdir /projectAN
WORKDIR /projectAN
COPY requirements.txt /projectAN/
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . /projectAN/