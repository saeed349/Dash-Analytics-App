FROM python:3.7

ENV DASH_DEBUG_MODE True

# RUN set -ex && \
#     pip install dash dash-daq dash-bootstrap-components pandas
COPY ./requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt

EXPOSE 8080

# COPY ./app /app
COPY ./app/multipage /app

WORKDIR /app

# CMD ["python", "app.py"]
CMD ["python", "index.py"]
