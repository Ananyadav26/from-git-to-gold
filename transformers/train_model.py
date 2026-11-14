if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, f1_score
import os

@transformer
def train(df, **kwargs):
    depth = int(kwargs.get("max_depth", 3))

    train_df = df[df["split"] == "train"]
    test_df = df[df["split"] == "test"]
    features = [c for c in df.columns if c not in ("target", "split")]

    model = DecisionTreeClassifier(max_depth=depth, random_state=42)
    model.fit(train_df[features], train_df["target"])

    predictions = model.predict(test_df[features])
    accuracy = accuracy_score(test_df["target"], predictions)
    print(f"C2_RESULT depth={depth} accuracy={accuracy:.6f}")
    f1 = f1_score(test_df["target"], predictions, average="macro")

    return {
        "model": model,
        "predictions": predictions.tolist(),
        "actual": test_df["target"].tolist(),
        "accuracy": float(accuracy),
        "macro_f1": float(f1),
        "max_depth": depth,
        "features": features
    }

@test
def test_accuracy(output, **kwargs):
    assert output["accuracy"] >= 0.70, (
        f"Accuracy {output['accuracy']:.3f} is below 0.70"
    )
