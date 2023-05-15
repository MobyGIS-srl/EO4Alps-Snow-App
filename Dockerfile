FROM eoxa/eoxserver:latest

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y libxml2-dev libxslt-dev libgdal-dev wkhtmltopdf python3 python-is-python3 

RUN apt-get update && apt-get install -y \
    binutils \
    && strip --remove-section=.note.ABI-tag /usr/lib/x86_64-linux-gnu/libQt5Core.so.5

ADD requirements.txt .

ARG PIP_EXTRA_INDEX_URL

RUN pip install -r requirements.txt

RUN sed -i "s/geos_version().decode()/geos_version().decode().split(' ')[0]/g" /usr/local/lib/python3.10/dist-packages/django/contrib/gis/geos/libgeos.py

RUN mkdir -p /opt

COPY edc_ogc /opt/edc_ogc

COPY run.sh /opt/edc_ogc

WORKDIR /opt/edc_ogc

ENTRYPOINT []

CMD ./run.sh
