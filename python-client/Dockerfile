FROM python:3.6.3

MAINTAINER Dmytro Krupenko <krupenko.d@pdffiller.com>
COPY . /app/
WORKDIR /app/

# Install Supervisor.
RUN \
  apt-get update && \
  apt-get install -y supervisor && \
  rm -rf /var/lib/apt/lists/* && \
  sed -i 's/^\(\[supervisord\]\)$/\1\nnodaemon=true/' /etc/supervisor/supervisord.conf

# Security changes
# - Determine runlevel and services at startup [BOOT-5180]
RUN update-rc.d supervisor defaults

# - Check the output of apt-cache policy manually to determine why output is empty [KRNL-5788]
RUN apt-get update | apt-get upgrade -y

# - Install a PAM module for password strength testing like pam_cracklib or pam_passwdqc [AUTH-9262]
RUN apt-get install libpam-cracklib -y
RUN ln -s /lib/x86_64-linux-gnu/security/pam_cracklib.so /lib/security

#configure application
RUN mkdir -p /var/log/supervisor && \
    mv /app/supervisord/* /etc/supervisor/conf.d/

#Install python dependencies
RUN pip install -r requirements.txt

CMD ["supervisord", "-c", "/etc/supervisor/supervisord.conf"]