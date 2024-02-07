from mage_ai.data_cleaner.transformer_actions.base import BaseAction
from mage_ai.data_cleaner.transformer_actions.constants import ActionType, Axis, ImputationStrategy
from mage_ai.data_cleaner.transformer_actions.utils import build_transformer_action

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date
    data = data[(data['passenger_count'] > 0.0) & (data['trip_distance'] > 0.0)]
    data.rename(columns={'VendorID': 'vendor_id', 'RatecodeID': 'ratecode_id', 'PULocationID': 'pu_location_id', 'DOLocationID': 'do_location_id'}, inplace=True)
    return data

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
    assert 'vendor_id' in output.columns, 'Columns were not converted to snake case'
    assert 'VendorID' not in output.columns, 'Columns were not converted to snake case'
    assert len(output[output['passenger_count'] == 0]) == 0, 'There are rows where passenger count is 0'
    assert len(output[output['trip_distance'] == 0]) == 0, 'There are rows where trip distance is 0'
