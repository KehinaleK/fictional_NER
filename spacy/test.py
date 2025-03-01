import spacy

nlp = spacy.load("./output/model-best")  
doc = nlp("Elyë lantanë melmessë sonen; merilyë melmerya, ness' aranel. Arwen ëa óress' Elessarwa; náro vëaner ar canya ohtar; melilyes nan umiro melë le, Roccalas aranel turmawendë.")  

for ent in doc.ents:
    print(ent.text, ent.label_)