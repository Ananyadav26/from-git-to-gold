if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def validate(df, **kwargs):
    assert df.isnull().sum().sum() == 0
    assert df["target"].nunique() == 3
    return df

@test
def test_output(output, **kwargs):
    assert output.isnull().sum().sum() == 0
    assert output["target"].nunique() == 3
