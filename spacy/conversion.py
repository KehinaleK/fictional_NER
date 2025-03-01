import spacy
from spacy.tokens import DocBin
import json
import random


def load_json_input(file_path):
    
    with open(file_path, "r") as f:
        annotations = json.load(f)

    return annotations

def split_data(annotations):

    random.shuffle(annotations) # Pour éviter d'avoir majorité d'une même source dans un même ensemble
    split_index = int(0.8 * len(annotations))
    train_data = annotations[:split_index]
    dev_data = annotations[split_index:]

    return train_data, dev_data

def initialize_nlp():

    nlp = spacy.blank("xx") # Répértoire par défaut poru quand on utilise pas une langue existante 
    train_bin = DocBin() # On initialise un DocBin pour chaque ensemble, donc un objet de la classe DocBin
    dev_bin = DocBin() # Same pour le dev

    return nlp, train_bin, dev_bin

def process_data(nlp, data, doc_bin):
    """Processes data and saves valid non-overlapping entities"""
    for example in data:
        text = example["text"]
        doc = nlp.make_doc(text)
        ents = []
        entity_positions = set()

        for ent in example["entities"]:
            start, end, label = ent["start"], ent["end"], ent["label"]
            if any(pos in entity_positions for pos in range(start, end)):
                print(f"Overlapping entity: {text[start:end]} ({label})")
                continue
            span = doc.char_span(start, end, label=label)
            if span is None:
                print(f"None span: {text[start:end]} ({label})")
            else:
                ents.append(span)
                entity_positions.update(range(start, end))

        doc.ents = ents
        doc_bin.add(doc)


def main():

    nlp, train_bin, dev_bin = initialize_nlp()
    annotations = load_json_input("../../data/entities/entities.json")

    train_data, dev_data = split_data(annotations)
    process_data(nlp, train_data, train_bin)
    process_data(nlp, dev_data, dev_bin)

    train_bin.to_disk("./spacy_output/train.spacy")
    dev_bin.to_disk("./spacy_output/dev.spacy")

if __name__ == "__main__":
    main()