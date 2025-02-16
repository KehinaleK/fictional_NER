def load(file):

    with open(file, 'r') as f:
        entities = f.readlines()
        entities = [entity.strip("\n").strip() for entity in entities]
    
    return entities




def save(entities, file):

    with open(file, 'w') as f:
        for entity in entities:
            f.write(entity + "\n")

def main():

    entities = load("../data/elvish/entities/entities_cleaned.txt")
    print(entities)
    
    entities = list(set(entities))
    entities = sorted(entities)
    print(entities)
    save(entities, "../data/elvish/entities/entities_cleanedgr.txt")

if __name__ == "__main__":
    main()