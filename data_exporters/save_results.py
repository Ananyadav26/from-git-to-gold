if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd

@data_exporter
def save(output, **kwargs):
    df = pd.DataFrame({
        "actual": output["actual"],
        "predicted": output["predictions"]
    })
    df.to_csv("/content/iris_predictions.csv", index=False)
    return {"saved": True, "rows": len(df)}

@test
def test_saved(output, **kwargs):
    assert output["saved"] is True
    assert output["rows"] == 30
