if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
import pandas as pd
from pathlib import Path

@data_exporter
def save(output, **kwargs):
    output_dir = Path(kwargs.get("output_dir", "outputs"))
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "iris_predictions.csv"

    df = pd.DataFrame({
        "actual": output["actual"],
        "predicted": output["predictions"]
    })
    df.to_csv(output_path, index=False)
    return {"saved": True, "rows": len(df), "path": str(output_path)}

@test
def test_saved(output, **kwargs):
    assert output["saved"] is True
    assert output["rows"] == 30
    assert Path(output["path"]).is_file()
