import argparse
import re 
import pandas as pd
from collections import defaultdict, Counter
import json
import matplotlib.pyplot as plt


'''
This script is used to create the inputs used for the Spacy training !
This script uses the list of entities stored in data/entities/*.txt files as a way to to find entities in the corpus.
Spacy expects a specific input described in the spacy section of the webpage. This script finds entities alongside
their start and end index and stores the results in a JSON file. This script must be applied on the train, test, and dev
corpus. The resulting files will then need to be processed using the conversion.py script.

This script awaits for a csv_file as input. This CSV file must contains a column with the text and another with its corresponding
name. It also awaits txt files containing entities, one on each line.
'''


def load_entities(entity_file):

    """
    Loads a txt file containing one entity per line.

    Args:
        entity_file (str): Path to the file containing the entities.
    Returns:
        List[str]: List of entities.
    """

    
    entities = []
    with open(entity_file, 'r') as f:
        for line in f:
            entities.append(line.strip())

    # Avoid empty strings !
    entities = [entity for entity in entities if entity != '']

    return entities


def load_csv(csv_file):

    """
    Loads a csv file containing the texts. The CSV file must contain a column with the texts and
    another with their corresponding titles. They should respectively be named 'elvishText' and 'elvishName'.

    Args:
        csv_file (str): Path to the csv file.
    Returns:
        pd.DataFrame: DataFrame containing the texts.
    """

    df = pd.read_csv(csv_file)
    # Drop rows with empty texts !
    df = df.dropna(subset=['elvishText'])

    return df


def retrieve_texts(df):

    """
    Retrieves the texts from the DataFrame.

    Args:
        df (pd.DataFrame): DataFrame containing the texts and their titles.
    Returns:
        Dict[str, str]: Dictionary containing the texts with their titles as keys.
    """

    texts = {}
    for index, row in df.iterrows():
        texts[row['elvishName']] = row['elvishText']

    return texts


def normalise_text(text):

    """
    Normalises the text by removing new lines.
    New lines can cause issues with indexing and training.

    Args:
        text (str): Text to normalise.
    Returns:
        str: Normalised text.
    """

    text = text.replace("\n", " ")

    return text


def find_entities(text, list_entities, label):

    """
    Finds entities in the text.
    For each entity in the list, the function will find all occurences of the entity in the text.
    We use regular expressions to retrieve the entity and its position. We also start by
    searching for entities in two words or that are the longest to avoid overlapping entities.
    If `Frodo Baggins` is found, `Frodo` will not be considered as an entity in this window.

    Args:
        text (str): Text to find entities in.
        list_entities (List[str]): List of entities to find.
        label (str): Label of the entity.
    Returns:
        List[str]: List of found entities.
        List[Tuple[int, int, str]]: List of tuples containing the start and end index of the entity and its label.
    """    

    # Sort entities by lenght so that we don't find entities that are substrings of other entities
    entity_list = sorted(list_entities, key=lambda x: -len(x))
    matches = []
    found_entities = []

    for idx, entity in enumerate(entity_list):
        # Find entities in word frontiers (since Eru can also be found in other words...)
        for match in re.finditer(r'\b' + re.escape(entity) + r'\b', text):
            start, end = match.start(), match.end()
        
            # Check if the entity is already in the list of entities, or if it overlaps with another entity
            if any(s <= start < e or s < end <= e for s, e, _ in matches):
                continue

            # Else, add the entity to the list of found entities !
            matches.append((start, end, label))
            print("\t", entity, start, end, label)
            found_entities.append(entity)

    return found_entities, matches

def retrieve_entities(text, loc, char):

    """
    Retrieves all entities from the text.
    For each entity type, its list of entities is sent to the find_entities function
    which will return the entities alongside their start and end index.

    Args:
        text (str): Text to find entities in.
        loc (List[str]): List of locations.
        char (List[str]): List of characters.
        lang (List[str]): List of languages. Not used for now.
    Returns:
        Dict[str, List[str]]: Dictionary containing the entities with their start and end index.
    """

    locations, loc_index = find_entities(text, loc, 'LOC')
    characters, char_index = find_entities(text, char, 'PERSON')
    # languages, lang_index = find_entities(text, lang, 'LANGUAGE')

    return loc_index, char_index, locations, characters


def plot_entities(num_loc, num_char, set):

    fig, ax = plt.subplots()
    width = 0.35  

    loc_keys = list(num_loc.keys())
    texts_names = [text[:6] + "..." for text in loc_keys]
    
    x = range(len(loc_keys))

    ax.bar(x, num_loc.values(), width, label='Location entities', color='lightsteelblue')
    ax.bar([p + width for p in x], num_char.values(), width, label='Character entities', color='darkgreen')

    ax.set_xlabel('Texts')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(texts_names)
    ax.tick_params(axis='x', rotation=45)
    ax.legend()
    ax.set_ylabel('Number of entities')
    ax.set_title(f'Entity types repartition {set}')
    plt.show()

def save_entities(entities, output_file):

    """
    Saves the entities in a JSON file.
    
    Args:
        entities (Dict({str : str, str : list[int, int, str]})): Dictionary containing for each text its content
        and its entities with their start and end index.
    """

    with open(output_file, 'w') as f:
        json.dump(entities, f)


def main():

    parser = argparse.ArgumentParser(description="Find entities in the corpus for spacy training !")
    parser.add_argument("--set", type=str, choices=["train", "test", "dev"], help="Desired set to process for entity retrieval !", required=True)
    args = parser.parse_args()

    if args.set == "train":
        csv_file = "../../data/corpus/train.csv"
    elif args.set == "test":
        csv_file = "../../data/corpus/test.csv"
    elif args.set == "dev":
        csv_file = "../../data/corpus/dev.csv"
 
    # Starting by loading the csv file containing the texts !
    df = load_csv(csv_file)
    # Then woop woop; loading the entities !
    loc = load_entities("../../data/entities/loc.txt")
    char = load_entities("../../data/entities/person.txt")
    # lang = load_entities("../data/entities/language.txt")

    # Now we can retrieve the texts !
    texts = retrieve_texts(df)
   
    all_characters = []
    all_locations = []
    all_entities = []
    sum_tokens = 0

    num_loc = Counter()
    num_char = Counter()

    # For each text ! 
    for key, text in texts.items():
        print("Processing text: ", key.strip())
        # Normalise the text !
        text = normalise_text(text)
        # Get the number of tokens, viva los stats !
        sum_tokens += len(text.split())

        # Retrieve the list of entities alongside their start and end index !
        loc_index, char_index, locations, characters = retrieve_entities(text, loc, char)

        # We remove the numbers from the title to avoid duplicates, for stats.
        # Because we have a lot of bible chapters :> 
        title_without_num = re.sub(r'\d+', '', key)
        title_without_num = title_without_num.replace(".", "").strip()

        # Then we store the entities in a dictionary !
        # For each entity that we found, we store its start and end index alongside its label.
        # So for each text, we get a list of dictionaries. One dictionary per entity !
        list_dict_entities = []
        all_characters.extend(characters)
        all_locations.extend(locations)

        if len(loc_index) > 0:
            for entity in loc_index:
                list_dict_entities.append({"start" : entity[0], "end" : entity[1], "label" : entity[2]})
                num_loc[title_without_num] += 1
        else:
            num_loc[title_without_num] += 0

        if len(char_index) > 0:
            for entity in char_index:
                list_dict_entities.append({"start" : entity[0], "end" : entity[1], "label" : entity[2]})
                num_char[title_without_num] += 1
        else:
            num_char[title_without_num] += 0

        # if len(language_index) > 0:
        #     for entity in language_index:
        #         list_dict_entities.append({"start" : entity[0], "end" : entity[1], "label" : entity[2]})
            
        # We store the text and its entities in a list !
        all_entities.append({"text" : text.replace("\n", " "), "entities" : list_dict_entities})
        
    save_entities(all_entities, f"../json_inputs/{args.set}.json")
    print("Total number of tokens: ", sum_tokens)
    print("Number of entities found: ", len(all_entities))
    print("Number of locations found: ", len(all_locations))
    print("Number of characters found: ", len(all_characters))
    print("Number of unique locations found: ", len(set(all_locations)))
    print("Number of unique characters found: ", len(set(all_characters)))

    plot_entities(num_loc, num_char, args.set)

if __name__ == "__main__":
    main()