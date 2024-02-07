import io
import pyarrow as pa
import pyarrow.parquet as pq
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """

    tables = []
    for month in range(10, 13):
        url = f"https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2020-{month}.parquet"
        response = requests.get(url, stream=True)

        br = pa.BufferReader(response.content)

        tables.append(pq.read_table(br))

    quart_tables = pa.concat_tables(tables)
    return quart_tables.to_pandas()

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'