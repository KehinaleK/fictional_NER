import pandas as pd

def load_csv(csv_file):

    df = pd.read_csv(csv_file)
    df = df.dropna(subset=['elvishText'])

    return df


def retrieve_texts(df):

    texts = {}
    for index, row in df.iterrows():
        texts[row['elvishName']] = row['elvishText']

    return texts



def display_index(data):
    index = {}
    for i, char in enumerate(data):
        index[i] = char

    return index



def main():

    df = load_csv("../data/elvish/corpus/elvish.csv")
    texts = retrieve_texts(df)
    for key, text in texts.items():
        print(key)
        text = text.replace("\n", " ")
        index = display_index(text)
        print(index)

if __name__ == '__main__':
    main()