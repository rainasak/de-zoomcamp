# These are the SQL commands used to complete the homework on BigQuery

> Firstly we need to setup the tables in BigQuery. We first create an external table using the parquet file in the GCS bucket.
- ```
      CREATE OR REPLACE EXTERNAL TABLE `de-zoomcamp-411418.nyctaxi.green_trip_data_ext`
      OPTIONS(
        format = "parquet,
        uris = ['gs://mage-zoomcamp-saksham/nyc_taxi_data/green_taxi_trips_2022*.parquet']
      );
    ```

> Next we create a materialized, non-partitioned table in BigQuery using this external table.
2) ```
    CREATE OR REPLACE TABLE `nyctaxi.green_trip_data_nonpart` AS
    SELECT * FROM `nyctaxi.green_trip_data_ext`;
   ```

> Question 1 can now be answered by just looking at the number of rows under the details of the materialized table nyctaxi.green_trip_data_nonpart

> Question 2 can be answered by estimating the data that will be read to count the number of distinct PULocationIDs for the external table and the materialized table using the following queries.

3) ```
    SELECT COUNT(DISTINCT(pu_location_id)) FROM `nyctaxi.green_trip_data_ext`;
    SELECT COUNT(DISTINCT(pu_location_id)) FROM `nyctaxi.green_trip_data_nonpart`;
   ```

> Question 3 which asks us to find how many records have a fare_amount of 0.0 can be solved using the following query.

4) ```
    SELECT COUNT(*) FROM `nyctaxi.green_trip_data_nonpart` WHERE fare_amount = 0.0;
   ```

> Question 4 asks for the optimum strategy to store a table in BigQuery if we will always get a query to order the results by PULocationID and be filtered on lpep_pickup_datetime is by partitioning on DATE(lpep_pickup_datetime) and clustering on PULocationID. We can create such a table using the following query.

5) ```
    CREATE OR REPLACE TABLE `nyctaxi.green_trip_data_part_and_clust`
    PARTITION BY DATE(lpep_pickup_datetime)
    CLUSTER BY pu_location_id AS
    SELECT * FROM `nyctaxi.green_trip_data_nonpart`;
   ```

> Question 5 asks us to form a query to get the distinct PULocationIDs between lpep_pickup_datetime 2022-06-01 and 2022-06-30 (all of June) and estimate how many bytes will be processed when using the non-partitioned and the partitioned and clustered tables. This can be done using the following queries.

6) ```
    SELECT DISTINCT(pu_location_id)
    FROM `nyctaxi.green_trip_data_nonpart`
    WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'; 

    SELECT DISTINCT(pu_location_id)
    FROM `nyctaxi.green_trip_data_part_and_clust`
    WHERE DATE(lpep_pickup_datetime) BETWEEN '2022-06-01' AND '2022-06-30'; 
   ```

> Qustion 6 is easily answered from the start of this exercise when creating the table from the parquet file that exist in a GCS bucket.

> Question 7 asks us if its a BigQuery best practice to always cluster your data. I think it is a little more nuanced than a simple True or False as it depends if your queries will be using any of your columns to filter on, if the level of granularity required is fine or not, if your columns will be used for ordering and what the order of the columns might be. So, even though there are factors to consider, in most cases where BigQuery is being used it would most likely mean that your data a querying patterns will benefit from clustering.

> Question 8 (Bonus) asks us how many bytes will be read for the query ``` SELECT COUNT(*) FROM `nyctaxi.green_trip_data_nonpart` ``` and why. The number of bytes read for this query is 0 and I believe the reason is because BigQuery stores metadata for the materialized tables which includes information such as number of rows which can be viewed in the details tab when investigating a table. Therefore, such a query does not require any extra processing of the data.