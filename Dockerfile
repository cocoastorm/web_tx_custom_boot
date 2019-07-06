FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY . /app
RUN cd /app && python setup.py install
RUN cp -r /app/www/static /app/www
