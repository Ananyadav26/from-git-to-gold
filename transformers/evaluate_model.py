if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd
from pathlib import Path

@transformer
def evaluate(output, **kwargs):
    output_dir = Path(kwargs.get("output_dir", "outputs"))
    output_dir.mkdir(parents=True, exist_ok=True)

    confusion_matrix_path = output_dir / "iris_confusion_matrix.csv"
    metrics_path = output_dir / "iris_metrics.csv"

    cm = confusion_matrix(output["actual"], output["predictions"])
    pd.DataFrame(
        cm,
        index=["Actual 0", "Actual 1", "Actual 2"],
        columns=["Predicted 0", "Predicted 1", "Predicted 2"]
    ).to_csv(confusion_matrix_path)
    print("CONFUSION MATRIX:")
    print(cm)
    report = classification_report(
        output["actual"], output["predictions"],
        output_dict=True, zero_division=0
    )
    metrics = pd.DataFrame(report).transpose()
    metrics.to_csv(metrics_path)
    return {
        "confusion_matrix": cm.tolist(),
        "metrics": metrics,
        "confusion_matrix_path": str(confusion_matrix_path),
        "metrics_path": str(metrics_path),
    }

@test
def test_evaluation(output, **kwargs):
    assert len(output["confusion_matrix"]) == 3
    assert output["metrics"] is not None
    assert Path(output["confusion_matrix_path"]).is_file()
    assert Path(output["metrics_path"]).is_file()
