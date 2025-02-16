import re

def load_file(file_path):

    with open(file_path, "r") as file:
        data = file.readlines()
        data = [line.strip() for line in data if line.startswith("*")]

    return data

def clean_entities(entities):

    for entity in entities:
        entity = entity.split("]]")[0]
        entity = entity.split("[[")[-1]
        entity = entity.split("|")[-1]
        


def main():

    entities = load_file("../data/elvish/entities/loc.txt")
    clean_entities(entities)



if __name__ == "__main__":
    main()