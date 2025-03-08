import spacy
import subprocess
import glob


# def test(model):

#     output_file = model.split("/")[-2]
    
#     test_command = ["python", "-m", "spacy", "evaluate", model,
#                     "spacy_input/test.spacy", "--output", f"spacy_results/{output_file}.json"]
    
#     subprocess.run(test_command)

def illustrate(model):
    
    nlp = spacy.load(model)
    test = nlp("Si Yoháno vettie ná íre i Yúrar mentaner airimóli ar Levindeli Yerúsalemello maquetien senna: “Man nalye?” Ar carampes pantave ar ua lalane, mal quente pantave: “Uan i Hristo.” Ar maquentelte senna: “Tá mana? Ma nalye Elía?” Ar eques: “Uan.” “Ma nalye i Erutercáno?” Ar hanquentes: “Lá!” Etta quentelte senna: “Man nalye? Lava men same hanquenta in mentaner me. Mana quetil pa imle?” Eques: “Nanye óma yamila i ravandasse: Cara i Héruo malle téra! – tambe Yesaia i Erutercáno quente.”")
    for entity in test.ents:
        print(entity.text, entity.label_, entity.start_char, entity.end_char)


def main():
    # train_directories = glob.glob()
    # for directory in train_directories:
    #     print(f"Testing model in {directory}")
        # test(f"{directory}/model-best")

    illustrate("original_shuffles/secondtrue_5_1600/model-best")

if __name__ == "__main__":
    main()