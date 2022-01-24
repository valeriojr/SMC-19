FROM python:3.9

# secret keys and passwords
RUN mkdir /etc/django
COPY deploy/django-key /etc/django/django-key
COPY deploy/mysql-passwd /etc/django/mysql-passwd
COPY deploy/maps-api /etc/django/maps-api
RUN chmod 700 /etc/django
RUN chmod 400 /etc/django/*

# copy project files
COPY . /var/www/smc19
COPY deploy/settings.py /var/www/smc19/smc19/settings.py
RUN rm -rf /var/www/smc19/deploy
WORKDIR /var/www/smc19

# install python packages
RUN pip3 install -U pip
RUN pip3 install -r requirements.txt
RUN pip3 install uwsgi

CMD uwsgi --ini uwsgi.ini
#CMD env DJANGO_SETTINGS_MODULE=smc19.settings uwsgi --socket=0.0.0.0:8000 --module=smc19.wsgi
