FROM gcr.io/google.com/cloudsdktool/cloud-sdk:alpine


# Alpine comes with ash as the default shell instead of bash.
RUN apk add --no-cache --upgrade bash
RUN apk add --no-cache --update gcc py3-pip libffi-dev gcc g++ musl-dev make py-gevent linux-headers python3-dev build-base

# FROM python:3.7-slim


RUN mkdir /home/app
WORKDIR /home/app
COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . .
# RUN adduser app
# RUN chown -R app:app /home/app

# USER app
RUN chmod +x run_api.sh
ENTRYPOINT [ "./run_api.sh" ]