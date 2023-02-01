FROM nginx:stable-alpine

#WORKDIR /etc/nginx/conf.d
#
#COPY nginx.conf .
#
#RUN mv nginx.conf default.conf

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
