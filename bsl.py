import _json
import sklearn
from pathlib import Path
from features import featurize

SENT_PATH  = Path("sentences.jsonl")
SPLIT_PATH = Path("split.json")

def load_split_data():
"Return (train_records, dev_records), filtered by split.json paper IDs."
#TO DO

def to_Xy(records):
    "Turn records into (feature-dict list, label list)."
    #TO DO
    X = []
    y = []
    return  X, y

def main():
#TO DO


if __name__ == "__main__":
    main()