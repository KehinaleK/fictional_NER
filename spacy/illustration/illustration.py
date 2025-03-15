import argparse
import spacy

def load_spacy_model(model_name):

    nlp = spacy.load(model_name)
    return nlp

def load_text(text_name):

    with open(text_name, "r") as f:
        text = f.read()

    return text

def illustrate(model_name, text):

    nlp = load_spacy_model(model_name)
    doc = nlp(text)

    for token in doc.ents:
        print(token.text, token.label_)

def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, help="The name of the spacy model to use.", default="../models/balanced_fin_false_0.01_1000/model-best")
    parser.add_argument("--text", type=str, help="The text to process.", choices=["tolkien", "neo", "bible"], required=True)
    args = parser.parse_args()

    if args.text == "tolkien":
        text = load_text("tolkien.txt")
    elif args.text == "neo":
        text = load_text("neo_quenya.txt")
    elif args.text == "bible":
        text = load_text("neo_quenya_bible.txt")

    illustrate(args.model, text)

if __name__ == "__main__":
    main()


   