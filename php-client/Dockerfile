FROM webdevops/php-nginx:ubuntu-16.04
ARG BUILD_ID
ENV BUILD_ID ${BUILD_ID:-1}
EXPOSE 443

COPY . ./var/www/php-cli/
WORKDIR /var/www/php-cli/

RUN mv docker/config/vhost.conf /opt/docker/etc/nginx/vhost.conf
RUN apt-get update && apt-get -y install poppler-utils && apt-get clean
