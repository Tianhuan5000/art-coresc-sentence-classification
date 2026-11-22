import json
from pathlib import Path

from numpy.random.mtrand import multinomial
from sklearn.feature_extraction import DictVectorizer
from sklearn.dummy import DummyClassifier
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score

from features import featurize

SENT_PATH  = Path("sentences.jsonl")
SPLIT_PATH = Path("split.json")

def load_split_data():
    "Return (train_records, dev_records), filtered by split.json paper IDs."
    with SPLIT_PATH.open(encoding="utf-8") as f:
        split = json.load(f)
    train_papers = set(split["train"])
    dev_papers = set(split["dev"])

    train_recs, dev_recs = [], []
    with SENT_PATH.open(encoding="utf-8") as f:
        for line in f:
            r = json.loads(line)
            if r["paper"] in train_papers:
                train_recs.append(r)
            elif r["paper"] in dev_papers:
                dev_recs.append(r)
            #test papers are ignored on purpose
    return train_recs, dev_recs

def to_Xy(records):
    "Turn records into (feature-dict list, label list)."
    #TO DO
    X = [featurize(record) for record in records]
    y = [record["label"] for record in records]
    return  X, y

def main():
    train_recs, dev_recs = load_split_data()
    print(f"train: {len(train_recs)} sentences   dev: {len(dev_recs)} sentences")

    X_train_dicts, y_train = to_Xy(train_recs)
    X_dev_dicts, y_dev = to_Xy(dev_recs)

    vec = DictVectorizer()
    X_train = vec.fit_transform(X_train_dicts)
    X_dev = vec.transform(X_dev_dicts)
    print(f"vocab size (train unigrams): {len(vec.vocabulary_)}")
    print(f"X_train: {X_train.shape}   X_dev: {X_dev.shape}")

    models = {
        ("major baseline", DummyClassifier(strategy="most_frequent")),
        ("multinomialNB", MultinomialNB()),
        ("logisticRegression", LogisticRegression(max_iter=1000)),
    }
    print(f"\n{'model':<22s}{'acc（%）':>8s}{'macro F1':>14s}")
    print("-"*45)
    for name, model in models:
        model.fit(X_train, y_train)
        preds = model.predict(X_dev)
        acc = accuracy_score(y_dev, preds) * 100
        mf1 = f1_score(y_dev, preds, average="macro") * 100
        print(f"{name:<22s}{acc:>8.2f}{mf1:>14.2f}")

if __name__ == "__main__":
    main()