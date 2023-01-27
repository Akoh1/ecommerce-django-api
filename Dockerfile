# pull official base image
FROM python:3.9.2-alpine

# set work directory
WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2
#RUN apk --update add libxml2-dev libxslt-dev libffi-dev gcc musl-dev libgcc openssl-dev curl
#RUN apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev
##RUN pip install Pillow
#RUN apk update \
#    && apk add  gcc python3-dev musl-dev \
#    && apk add postgresql-dev
#    # && pip install psycopg2 \
#    # && apk del build-deps

# install dependencies
RUN pip3 install --upgrade pip
COPY ./requirements.txt .
RUN pip3 install --default-timeout=100 -r requirements.txt

# copy project
COPY . .

ENV ENV=prod
# run entrypoint.prod.sh
#ENTRYPOINT ["/home/app/entrypoint.sh"]
#ENTRYPOINT ["ENV=dev"]
