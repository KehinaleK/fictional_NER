import pandas as pd
import re 

### pers = 1
### loc = 2
### lang = 3

from collections import defaultdict

def load_corpus(csv_file):
    # Load the csv file
    df = pd.read_csv(csv_file)
    return df

def get_texts(df):

    texts = df["elvishText"].dropna().tolist()
    return texts

def load_entities(entity_file):
    
    entities = []
    with open(entity_file, 'r') as f:
        for line in f:
            entities.append(line.strip())

    entities = [entity for entity in entities if entity != '']

    return entities

def normalise_entities(loc, char):
    
    loc = [loc.replace("-", " ") for loc in loc]
    char = [char.replace("-", " ") for char in char]
    # lang = [lang.replace("-", " ") for lang in lang]
    # besoin d'enlever les espaces après les mots ?  
    return loc, char #, lang

def get_sentences(text):  
    sentences = re.split(r'([.!?])', text)

    sentences = [" ".join(sentences[i:i+2]) for i in range(0, len(sentences)-1, 2)]
    return sentences

def get_words(sentence):

    sentence = sentence.replace("\n", " ").replace(",", " , ").replace(";", " ; ").replace(":", " : ").replace("(", " ( ").replace(")", " ) ").replace("[", " [ ").replace("]", " ] ").replace("{", " { ").replace("}", " } ")
    words = sentence.split(" ")
    
    return words

def find_entities(words, loc, char, id_sentence):

    dict_entities = defaultdict(list)
    for word in words:
        if not word.isspace() and word != "":
            if word in loc:
                dict_entities["Sentence"].append(id_sentence)
                dict_entities["Words"].append(word)
                dict_entities["NER_tags_ID"].append(2)
                dict_entities["NER_tags"].append("LOC")
            
            elif word in char:
                dict_entities["Sentence"].append(id_sentence)
                dict_entities["Words"].append(word)
                dict_entities["NER_tags_ID"].append(1)
                dict_entities["NER_tags"].append("PERSON")
            
            # elif word in lang:
            #     dict_entities["Words"].append(word)
            #     dict_entities["NER_tags_ID"].append(3)
            #     dict_entities["NER_tags"].append("LANGUAGE")
            
            else:
                dict_entities["Sentence"].append(id_sentence)
                dict_entities["Words"].append(word)
                dict_entities["NER_tags_ID"].append(0)
                dict_entities["NER_tags"].append("NA")

    return dict_entities


def main():

    df = load_corpus("../data/elvish/corpus/elvish.csv")
    print(df.columns)
    loc = load_entities("../data/elvish/entities/loc_cases.txt")
    char = load_entities("../data/elvish/entities/person_cases.txt")
    
    # loc = load_entities("../data/elvish/entities/loc.txt")
    # char = load_entities("../data/elvish/entities/person.txt")
    # lang = load_entities("../../data/elvish/entities/language.txt")

    loc, char = normalise_entities(loc, char)
    
    texts = get_texts(df)
    id_sentence = 1

    dict_entities_global = defaultdict(list)

    for text in texts:
        sentences = get_sentences(text)
        for sentence in sentences:
            words = get_words(sentence)
            dict_entities = find_entities(words, loc, char, id_sentence)
            id_sentence += 1
            dict_entities_global["Sentence"].extend([id_sentence] * len(dict_entities["Words"]))
            dict_entities_global["Words"].extend(dict_entities["Words"])
            dict_entities_global["NER_tags_ID"].extend(dict_entities["NER_tags_ID"])
            dict_entities_global["NER_tags"].extend(dict_entities["NER_tags"])
            
            # ajout d'un espace pour séparer les phrases
            dict_entities_global["Sentence"].append("")
            dict_entities_global["Words"].append("")
            dict_entities_global["NER_tags_ID"].append("")
            dict_entities_global["NER_tags"].append("")
  

    # print(dict_entities_global)
    df = pd.DataFrame(dict_entities_global)
    print(df.head(50))
    df.to_csv("../data/essai_input_cases.tsv", index=False, sep="\t")

    

if __name__ == "__main__":
    main()