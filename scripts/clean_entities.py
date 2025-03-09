def load(file):

    with open(file, 'r') as f:
        entities = f.readlines()
        entities = [entity.strip("\n").strip() for entity in entities]
    
    return entities

def clean(entities):

    entities = list(set(entities))
    entities = sorted(entities)

    return entities


def save(entities, file):

    with open(file, 'w') as f:
        for entity in entities:
            f.write(entity + "\n")

def main():

    entities = load("../data/entities/entities_cleanedgr.txt")
    entities = clean(entities)
    save(entities, "../data/entities/person.txt")

if __name__ == "__main__":
    main()