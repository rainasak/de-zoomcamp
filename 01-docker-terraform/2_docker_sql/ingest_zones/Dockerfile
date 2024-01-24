FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingest_zones.py ingest_zones.py 

ENTRYPOINT [ "python", "ingest_zones.py", "--user=root", "--password=root", "--host=pgdatabase", "--port=5432", "--db=ny_taxi", "--table_name=zones", "--url=https://d37ci6vzurychx.cloudfront.net/misc/taxi+_zone_lookup.csv" ]
