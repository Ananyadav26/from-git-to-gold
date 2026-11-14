if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from sklearn.metrics import confusion_matrix, classification_report
import pandas as pd

@transformer
def evaluate(output, **kwargs):
    cm = confusion_matrix(output["actual"], output["predictions"])
    pd.DataFrame(
        cm,
        index=["Actual 0", "Actual 1", "Actual 2"],
        columns=["Predicted 0", "Predicted 1", "Predicted 2"]
    ).to_csv("/content/iris_confusion_matrix.csv")
    print("CONFUSION MATRIX:")
    print(cm)
    report = classification_report(
        output["actual"], output["predictions"],
        output_dict=True, zero_division=0
    )
    metrics = pd.DataFrame(report).transpose()
    metrics.to_csv("/content/iris_metrics.csv")
    return {"confusion_matrix": cm.tolist(), "metrics": metrics}

@test
def test_evaluation(output, **kwargs):
    assert len(output["confusion_matrix"]) == 3
    assert output["metrics"] is not None
