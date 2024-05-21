FROM python:3.12.3
ADD . /ppnaforecast-ml-api
WORKDIR /ppnaforecast-ml-api
RUN pip install -r requirements.txt