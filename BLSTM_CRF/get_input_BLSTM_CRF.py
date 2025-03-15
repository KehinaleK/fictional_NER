import pandas as pd
import re 

### pers = 1
### loc = 2

from collections import defaultdict

def load_corpus(csv_file):
    """Load the csv file"""
    df = pd.read_csv(csv_file)
    return df

def get_texts(df):
    """"Get the texts from the dataframe"""
    texts = df["elvishText"].dropna().tolist()
    return texts

def load_entities(entity_file):
    """Load the entities from the entity file"""
    entities = []
    with open(entity_file, 'r') as f:
        for line in f:
            entities.append(line.strip())

    entities = [entity for entity in entities if entity != '']

    return entities


def get_sentences(text): 
    """Get the sentences from the text""" 
    sentences = re.split(r'([.!?])', text)

    sentences = [" ".join(sentences[i:i+2]) for i in range(0, len(sentences)-1, 2)]
    return sentences

def get_words(sentence):
    """Get the words from the sentence and adding a space between the punctuation marks"""
    sentence = sentence.replace("“", " “ ").replace('"', ' " ').replace("\n", " ").replace(",", " , ").replace(";", " ; ").replace(":", " : ").replace("(", " ( ").replace(")", " ) ").replace("[", " [ ").replace("]", " ] ").replace("{", " { ").replace("}", " } ")
    words = sentence.split(" ")
    
    return words

def find_entities(words, loc, char):
    """Find the entities in the words and add them in a dictionary"""
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
            
            # elif word in lang:
            #     dict_entities["Words"].append(word)
            #     dict_entities["NER_tags_ID"].append(3)
            #     dict_entities["NER_tags"].append("LANGUAGE")
            
            else:
                dict_entities["Words"].append(word)
                dict_entities["NER_tags_ID"].append(0)
                dict_entities["NER_tags"].append("NA")

    return dict_entities

def get_input(texts, loc, char):
    """Get the input for the BLSTM_CRF model"""
    dict_entities_global = defaultdict(list)
    id_sentence = 1
   
    for text in texts:
        # print("########################Processing text...", text)
        # ajout d'un séparateur de documents 
        dict_entities_global["Words"].append("-DOCSTART-")
        dict_entities_global["NER_tags_ID"].append("0")
        dict_entities_global["NER_tags"].append("0")
        # # ajout d'un espace pour séparer les documents
        # dict_entities_global["Words"].append("")
        # dict_entities_global["NER_tags_ID"].append("")
        # dict_entities_global["NER_tags"].append("")
        sentences = get_sentences(text)
        for sentence in sentences:
            words = get_words(sentence)
            # print("Processing sentence...", sentence)
            # print("Words...", words)
            # print(words)
            dict_entities = find_entities(words, loc, char)
            # print("Entities...", dict_entities)
        
            id_sentence += 1
            # dict_entities_global["Sentence"].extend([id_sentence] * len(dict_entities["Words"]))
            dict_entities_global["Words"].extend(dict_entities["Words"])
            dict_entities_global["NER_tags_ID"].extend(dict_entities["NER_tags_ID"])
            dict_entities_global["NER_tags"].extend(dict_entities["NER_tags"])
            
            # ajout d'un espace pour séparer les phrases
            # dict_entities_global["Sentence"].append("")
            dict_entities_global["Words"].append("")
            dict_entities_global["NER_tags_ID"].append("")
            dict_entities_global["NER_tags"].append("")
            # print("Geule du dict_global", dict_entities_global)
    
    # print(dict_entities_global)
    # print(dict_entities_global)
    
    df = pd.DataFrame(dict_entities_global)
   
    return df

def main():
    
    df_train = load_corpus("../data/elvish/corpus/train.csv")
    df_test = load_corpus("../data/elvish/corpus/test.csv")
    df_dev = load_corpus("../data/elvish/corpus/dev.csv")

    # print(df_train.head(50))

    loc = load_entities("../data/elvish/entities/loc.txt")
    char = load_entities("../data/elvish/entities/person.txt")

    # Process train
    text_train = get_texts(df_train)
    
    train = get_input(text_train, loc, char)
    print(len(text_train))
    # print(train.head(50))
    train.to_csv("./input/train_input_BLSTM_CRF.tsv", index=False, header=False, sep="\t")

    # Process test
    text_test = get_texts(df_test)
    test = get_input(text_test, loc, char)
    # print(test.head(50))
    test.to_csv("./input/test_input_BLSTM_CRF.tsv", index=False, header=False, sep="\t")

    # Process dev
    text_dev = get_texts(df_dev)
    dev = get_input(text_dev, loc, char)
    # print(dev.head(50))
    dev.to_csv("./input/dev_input_BLSTM_CRF.tsv", index=False, header=False, sep="\t")
      
if __name__ == "__main__":
    main()