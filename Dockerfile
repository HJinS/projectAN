FROM python:latest
ENV PYTHONUNBUFFERED 1
RUN useradd --no-log-init myuser
USER myuser
WORKDIR /home/myuser
RUN mkdir ./projectAN
WORKDIR ./projectAN
COPY --chown=myuser:myuser requirements.txt ./projectAN/
RUN pip install --user -r requirements.txt
COPY --chown=myuser:myuser . ./projectAN/