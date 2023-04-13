FROM eoxa/eoxserver:latest

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y libxml2-dev libxslt-dev libgdal-dev wkhtmltopdf

ADD requirements.txt .

ARG PIP_EXTRA_INDEX_URL

ARG PORT

RUN pip install -r requirements.txt

RUN sed -i "s/geos_version().decode()/geos_version().decode().split(' ')[0]/g" /usr/local/lib/python3.10/dist-packages/django/contrib/gis/geos/libgeos.py

RUN mkdir -p /opt/app
COPY edc_ogc /opt/app/edc_ogc
WORKDIR /opt/app/edc_ogc

ENTRYPOINT []
EXPOSE 8585
# CMD ["flask", "run", "--host=0.0.0.0"]
CMD ["sh", "-c", "flask run --host=0.0.0.0 --port 8585"]
