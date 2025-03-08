import spacy
from spacy.tokens import DocBin
import json
import random


def load_json_input(file_path):
    
    with open(file_path, "r") as f:
        annotations = json.load(f)

    return annotations

# def split_data(annotations):

#     random.shuffle(annotations) # Pour éviter d'avoir majorité d'une même source dans un même ensemble
#     ## On split les données en 70% pour le train, 20% pour le test et 10% pour le dev
#     train_data = annotations[:int(len(annotations) * 0.7)]
#     test_data = annotations[int(len(annotations) * 0.7):int(len(annotations) * 0.9)]
#     dev_data = annotations[int(len(annotations) * 0.9):]
    
#     return train_data, test_data, dev_data

def initialize_nlp():

    nlp = spacy.blank("xx") # Répértoire par défaut poru quand on utilise pas une langue existante 
    # train_bin = DocBin() # On initialise un DocBin pour chaque ensemble, donc un objet de la classe DocBin
    # test_bin = DocBin() # Idem pour le test
    # dev_bin = DocBin() # Same pour le dev
    data_bin = DocBin()

    return nlp, data_bin

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

    nlp, data_bin = initialize_nlp()
    annotations = load_json_input("../data/entities/entities_dev.json")

    process_data(nlp, annotations, data_bin)

    data_bin.to_disk("./spacy_input/dev.spacy")

if __name__ == "__main__":
    main()