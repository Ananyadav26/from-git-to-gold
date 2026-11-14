if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from sklearn.datasets import load_iris
import pandas as pd

@data_loader
def load_data(**kwargs):
    data = load_iris(as_frame=True)
    return data.frame

@test
def test_output(output, **kwargs):
    assert len(output) == 150
    assert "target" in output.columns
