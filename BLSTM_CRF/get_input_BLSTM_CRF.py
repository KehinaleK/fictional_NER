import pandas as pd
import re 
from collections import defaultdict


"""
This scripts allows to get the input for the BLSTM_CRF model.
The input required for the BSLTM_CRF model consists of columns containing
the words, the NER tags and the sentence ID.
There is one row per word.
Documents are separated by a row containing "-DOCSTART-".
Sentences are separated by a row containing an empty string.
"""

def load_corpus(csv_file):

    """
    Load the csv file.
    
    Args:
        csv_file: str, the path to the csv file
    Returns:
        df: pandas dataframe, the dataframe containing the csv file
    """

    df = pd.read_csv(csv_file)
    return df

def get_texts(df):

    """
    Get the texts from the dataframe.
    
    Args:
        df: pandas dataframe, the dataframe containing the texts
    Returns:
        texts: list, the list of texts
    """

    texts = df["elvishText"].dropna().tolist()
    return texts

def load_entities(entity_file):

    """
    Load the entities from the entity file.

    Args:
        entity_file: str, the path to the entity file
    Returns:
        entities: list, the list of entities
    """

    entities = []
    with open(entity_file, 'r') as f:
        for line in f:
            entities.append(line.strip())

    entities = [entity for entity in entities if entity != '']

    return entities

def get_sentences(text): 

    """
    Get the sentences from the text.
    
    Args:
        text: str, the text
    Returns:
        sentences: list, the list of sentences
    """ 
    sentences = re.split(r'([.!?])', text)

    sentences = [" ".join(sentences[i:i+2]) for i in range(0, len(sentences)-1, 2)]
    return sentences

def get_words(sentence):

    """
    Get the words from the sentence and adding a space between the punctuation marks.
    
    Args:
        sentence: str, the sentence
    Returns:
        words: list, the list of words
    """
    sentence = sentence.replace("“", " “ ").replace('"', ' " ').replace("\n", " ").replace(",", " , ").replace(";", " ; ").replace(":", " : ").replace("(", " ( ").replace(")", " ) ").replace("[", " [ ").replace("]", " ] ").replace("{", " { ").replace("}", " } ")
    words = sentence.split(" ")
    
    return words

def find_entities(words, loc, char):
    
    """
    Find the entities in the words and add them in a dictionary so that
    the dataframe can be created.

    Args:
        words: list, the list of words
        loc: list, the list of locations
        char: list, the list of characters
    Returns:
        dict_entities: dict, the dictionary containing the words and the NER tags
    """

    dict_entities = defaultdict(list)
    for word in words:
        if not word.isspace() and word != "":
            if word in loc:
                dict_entities["Words"].append(word)
                dict_entities["NER_tags_ID"].append(2)
                dict_entities["NER_tags"].append("LOC")
            
            elif word in char:
                dict_entities["Words"].append(word)
                dict_entities["NER_tags_ID"].append(1)
                dict_entities["NER_tags"].append("PERSON")

            else:
                dict_entities["Words"].append(word)
                dict_entities["NER_tags_ID"].append(0)
                dict_entities["NER_tags"].append("NA")

    return dict_entities

def get_input(texts, loc, char):

    """
    Get the input for the BLSTM_CRF model.
    
    Args:
        texts: list, the list of texts
        loc: list, the list of locations
        char: list, the list of characters
    Returns:
        df: pandas dataframe, the dataframe containing the input
    """
    dict_entities_global = defaultdict(list)
    id_sentence = 1
   
    for text in texts:
    
        dict_entities_global["Words"].append("-DOCSTART-")
        dict_entities_global["NER_tags_ID"].append("0")
        dict_entities_global["NER_tags"].append("0")
    
        sentences = get_sentences(text)
        for sentence in sentences:
            words = get_words(sentence)
            dict_entities = find_entities(words, loc, char)
        
            id_sentence += 1
         
            dict_entities_global["Words"].extend(dict_entities["Words"])
            dict_entities_global["NER_tags_ID"].extend(dict_entities["NER_tags_ID"])
            dict_entities_global["NER_tags"].extend(dict_entities["NER_tags"])

            dict_entities_global["Words"].append("")
            dict_entities_global["NER_tags_ID"].append("")
            dict_entities_global["NER_tags"].append("")
  
    df = pd.DataFrame(dict_entities_global)
   
    return df

def main():
    
    df_train = load_corpus("../data/corpus/train.csv")
    df_test = load_corpus("../data/corpus/test.csv")
    df_dev = load_corpus("../data/corpus/dev.csv")

    loc = load_entities("../data/entities/loc.txt")
    char = load_entities("../data/entities/person.txt")

    # Process train
    text_train = get_texts(df_train)
    train = get_input(text_train, loc, char)
    train.to_csv("./input/train_input_BLSTM_CRF.tsv", index=False, header=False, sep="\t")

    # Process test
    text_test = get_texts(df_test)
    test = get_input(text_test, loc, char)
    test.to_csv("./input/test_input_BLSTM_CRF.tsv", index=False, header=False, sep="\t")

    # Process dev
    text_dev = get_texts(df_dev)
    dev = get_input(text_dev, loc, char)
    dev.to_csv("./input/dev_input_BLSTM_CRF.tsv", index=False, header=False, sep="\t")
      
if __name__ == "__main__":
    main()