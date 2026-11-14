if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def check(df, **kwargs):
    assert df.isnull().sum().sum() == 0
    assert df["target"].nunique() == 3
    return {"rows": len(df), "classes": int(df["target"].nunique())}

@test
def test_quality(output, **kwargs):
    assert output["rows"] == 150
    assert output["classes"] == 3
