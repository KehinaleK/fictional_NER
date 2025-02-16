import pandas as pd
from collections import defaultdict
import unicodedata as ud
import re 
import json

def load_entities(entity_file):
    
    entities = []
    with open(entity_file, 'r') as f:
        for line in f:
            entities.append(line.strip())

    entities = [entity for entity in entities if entity != '']

    return entities

def load_csv(csv_file):

    df = pd.read_csv(csv_file)
    df = df.dropna(subset=['elvishText'])

    return df


def retrieve_texts(df):

    texts = {}
    for index, row in df.iterrows():
        texts[row['elvishName']] = row['elvishText']

    return texts

def normalise_entities(loc, char, lang):
    
    loc = [loc.replace("-", " ") for loc in loc]
    char = [char.replace("-", " ") for char in char]
    lang = [lang.replace("-", " ") for lang in lang]

    return loc, char, lang

def normalise_text(text):

    text = text.replace("-", " ")
    text = text.replace("\n", " ")

    return text

def retrieve_entities(text, loc, char, lang):

    entities = defaultdict(list)
    text = normalise_text(text)

    locations, loc_index = find_entities(text, loc, 'LOC')
    characters, char_index = find_entities(text, char, 'PERSON')
    languages, lang_index = find_entities(text, lang, 'LANGUAGE')
    
    entities['LOC'] = locations
    entities['PERSON'] = characters
    entities['LANGUAGE'] = languages

    return entities, loc_index, char_index, lang_index

def find_entities(text, list_entities, label):

    found_entities = []
    entities_index = []

    for entity in list_entities:
        pattern = re.compile(r'\b' + entity + r'\b', re.IGNORECASE)
        matches = pattern.finditer(text)
        for match in matches:
            if match.group(0) == "nan":
                continue

            start = match.start()
            end = match.end()
            entities_index.append((start, end, label))
        found_entities.append(entity)
    return found_entities, entities_index

def save_entities(entities, output_file):

    with open(output_file, 'w') as f:
        json.dump(entities, f)

def main():

    df = load_csv("../data/elvish/corpus/elvish.csv")
    texts = retrieve_texts(df)
    loc = load_entities("../data/elvish/entities/loc.txt")
    char = load_entities("../data/elvish/entities/person.txt")
    lang = load_entities("../data/elvish/entities/language.txt")

    loc, char, lang = normalise_entities(loc, char, lang)

    all_entities = []

    for key, text in texts.items():
        print("Processing text: ", key)
        entities, loc_index, char_index, language_index = retrieve_entities(text, loc, char, lang)
        entities_index = list(set(loc_index)) + list(set(char_index)) + list(set(language_index))
        all_entities.append([text.replace("\n", " "), {"entities": entities_index}])
    
    save_entities(all_entities, "../data/elvish/entities/entities.json")
        

if __name__ == "__main__":
    main()