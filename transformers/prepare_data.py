if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test
from sklearn.model_selection import train_test_split

@transformer
def transform(df, **kwargs):
    target = "target"
    feature_cols = [c for c in df.columns if c != target]

    train_idx, test_idx = train_test_split(
        df.index, test_size=0.2, random_state=42, stratify=df[target]
    )

    out = df.copy()
    out["split"] = "train"
    out.loc[test_idx, "split"] = "test"
    return out

@test
def test_split(output, **kwargs):
    assert (output["split"] == "train").sum() == 120
    assert (output["split"] == "test").sum() == 30
