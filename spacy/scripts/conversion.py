import spacy
from spacy.tokens import DocBin
import json
import argparse

"""
This script is used to convert the json data to spacy binary format !

Those JSON files were created with the 'find_entities.py' script, which is used to find entities in the text and save them.
This script will process those files and save them in a 'spacy' format that can be used to train a NER model.
"""

def load_json_input(file_path):

    """Loads the json file containing the entities.

    Args:
        file_path (str): The path to the json file.
    Returns:
        annotations (dict): The json file loaded as a dictionary.
    """
    
    with open(file_path, "r") as f:
        annotations = json.load(f)

    return annotations


def initialize_nlp():

    """
    Initializes the spacy model and an empty DocBin object.

    Returns:
        nlp (spacy.Language): The spacy model.
        data_bin (spacy.tokens.DocBin): The DocBin object to store the data.
    """

    nlp = spacy.blank("xx") # Default language is 'xx' (multilingual) ! Used for when we don't have a specific language model
    data_bin = DocBin() # Initialize a DocBin object to store the data woop woop 

    return nlp, data_bin

def process_data(nlp, data, doc_bin):

    """Processes data and saves valid non-overlapping entities.
    We add to deal with a few overlapping entities even though we removed them in the 'find_entities.py' script.
    Seeing as they are just a few, we can just print them out and ignore them.
    
    Args:
        nlp (spacy.Language): The spacy model.
        data (dict): The data to process.
        doc_bin (spacy.tokens.DocBin): The DocBin object to store the data.
    """

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

    parser = argparse.ArgumentParser()
    parser.add_argument("--set", type=str, choices=["train", "test", "dev"], help="The dataset to convert to spacy binary format.", required=True)
    args = parser.parse_args()

    if args.set == "train":
        annotations = load_json_input("../json_inputs/train.json")
    elif args.set == "test":
        annotations = load_json_input("../json_inputs/test.json")
    elif args.set == "dev":
        annotations = load_json_input("../json_inputs/dev.json")

    nlp, data_bin = initialize_nlp()
    process_data(nlp, annotations, data_bin)

    # WOop woop, we saved the data in the spacy binary format !
    data_bin.to_disk(f"../spacy_inputs/{args.set}.spacy")
    print(f"Saved {args.set} data to spacy binary format.")

if __name__ == "__main__":
    main()