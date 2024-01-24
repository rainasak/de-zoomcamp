FROM python:3.9.1

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2 pyarrow

WORKDIR /app
COPY ingest_data.py ingest_data.py 

ENTRYPOINT [ "python", "ingest_data.py", "--user=root", "--password=root", "--host=pgdatabase", "--port=5432", "--db=ny_taxi", "--table_name=green_taxi_trips", "--url=https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2019-09.parquet" ]
