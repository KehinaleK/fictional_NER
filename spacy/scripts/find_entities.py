import pandas as pd
from collections import defaultdict, Counter
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


def normalise_text(text):

    text = text.replace("\n", " ")

    return text

def retrieve_entities(text, loc, char):

    entities = defaultdict(list)

    locations, loc_index = find_entities(text, loc, 'LOC')
    characters, char_index = find_entities(text, char, 'PERSON')
    # languages, lang_index = find_entities(text, lang, 'LANGUAGE')

    entities['LOC'] = locations
    entities['PERSON'] = characters
    # entities['LANGUAGE'] = languages

    return loc_index, char_index


def find_entities(text, list_entities, label):

    entity_list = sorted(list_entities, key=lambda x: -len(x))
    matches = []
    found_entities = []

    for idx, entity in enumerate(entity_list):
        for match in re.finditer(r'\b' + re.escape(entity) + r'\b', text):
            start, end = match.start(), match.end()
        
            if any(s <= start < e or s < end <= e for s, e, _ in matches):
                continue
            matches.append((start, end, label))
            print(entity, start, end, label)
            found_entities.append(entity)

    return found_entities, matches

# def plot_entities(num_loc, num_char):

#     import matplotlib.pyplot as plt
 
#     fig, ax = plt.subplots()
#     width = 0.35  

#     loc_keys = list(num_loc.keys())
#     char_keys = list(num_char.keys())
#     x = range(len(loc_keys))

#     ax.bar(x, num_loc.values(), width, label='Location entities', color='lightsteelblue')
#     ax.bar([p + width for p in x], num_char.values(), width, label='Character entities', color='darkgreen')

#     ax.set_xlabel('Texts')
#     ax.set_xticks([p + width / 2 for p in x])
#     ax.set_xticklabels(loc_keys)
#     ax.legend()
#     ax.set_ylabel('Number of entities')
#     ax.set_title('Entity types repartition (DEV)')
#     plt.show()

def save_entities(entities, output_file):

    with open(output_file, 'w') as f:
        json.dump(entities, f)

def main():

    df = load_csv("../data/corpus/dev.csv")
    texts = retrieve_texts(df)
    loc = load_entities("../data/entities/loc.txt")
    char = load_entities("../data/entities/person.txt")
    # lang = load_entities("../data/entities/language.txt")

    all_entities = []
    sum_tokens = 0

    num_loc = Counter()
    num_char = Counter()

    for key, text in texts.items():
        text = normalise_text(text)
        sum_tokens += len(text.split())
        print("Processing text: ", key.strip())
        loc_index, char_index = retrieve_entities(text, loc, char)
        title_without_num = re.sub(r'\d+', '', key)
        title_without_num = title_without_num.replace(".", "").strip()
        list_dict_entities = []
        if len(loc_index) > 0:
            for entity in loc_index:
                list_dict_entities.append({"start" : entity[0], "end" : entity[1], "label" : entity[2]})
            num_loc[title_without_num] += len(loc_index)
        else:
            num_loc[title_without_num] = 0
        if len(char_index) > 0:
            for entity in char_index:
                list_dict_entities.append({"start" : entity[0], "end" : entity[1], "label" : entity[2]})
            num_char[title_without_num] += len(char_index)
        else:
            num_char[title_without_num] = 0
        # if len(language_index) > 0:
        #     for entity in language_index:
        #         list_dict_entities.append({"start" : entity[0], "end" : entity[1], "label" : entity[2]})
            
        entities_index = list(set(loc_index)) + list(set(char_index))
        all_entities.append({"text" : text.replace("\n", " "), "entities" : list_dict_entities})
        
    save_entities(all_entities, "../data/entities/entities_dev.json")
    print("Total number of tokens: ", sum_tokens)
    print("Number of entities per text:")

    # plot_entities(num_loc, num_char)
    for key, value in num_loc.items():
        print(f"Location entities in {key}: {value}")
    for key, value in num_char.items():
        print(f"Character entities in {key}: {value}")

if __name__ == "__main__":
    main()