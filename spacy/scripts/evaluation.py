import subprocess
import argparse
import glob


def run_test(model):

    """
    Run the spacy evaluate command on a given model.
    """

    output_file = model.split("/")[-2]
    
    test_command = ["python", "-m", "spacy", "evaluate", model,
                    "../spacy_inputs/test.spacy", "--output", f"../spacy_results_caca/{output_file}.json"]
    
    subprocess.run(test_command)


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument("--models", type=str, help="The path to the directory containing the models to test.", required=False)
    parser.add_argument("--model", type=str, help="The path to the model to test.", required=False)
    args = parser.parse_args()

    if args.models:
        train_directories = glob.glob(f"{args.models}/*")
        print(train_directories)
        for directory in train_directories:
            print()
            print(f"Testing model in {directory}")
            run_test(f"{directory}/model-best")

    if args.model:
        model_name = args.model.split("/")[-2]
        print(f"Testing model in {args.model}")
        run_test(f"{args.model}/model-best")





if __name__ == "__main__":
    main()