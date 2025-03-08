import configparser
import itertools
from tqdm import tqdm
import subprocess

def load_config_file(config_file):
    """
    Load the configuration file containing the hyperparameters for the model.
    """

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_file)

    return config

def run_command(command, output_dir):


    command = ["python", "-m", "spacy", "train", "config.cfg", "--output", f"./output/{output_dir}", "--paths.train",
               "spacy_input/train.spacy", "--paths.dev", "spacy_input/dev.spacy"]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            break
        if output:
            print(output.strip())
    
    stderr = process.stderr.read()
    if stderr:
        print(stderr.strip())

    return process.poll()


def modify_config_file(config, hyperparameters_combinaison):

    ## display all the sections in the config file
    # print(config.sections())

    use_upper = hyperparameters_combinaison[0]
    learn_rate = hyperparameters_combinaison[1]
    batch_size = hyperparameters_combinaison[2]

    config["components.ner.model"]["use_upper"] = str(use_upper)
    config["nlp"]["batch_size"] = str(batch_size)
    config["training.optimizer"]["learn_rate"] = str(learn_rate)
    config["training.batcher.size"]["rate"] = str(batch_size)

    
    with open("config.cfg", "w") as configfile:
        config.write(configfile)
    

def store_hyperparameters():

    hyperparameters = {
        "use_upper": ["true", "false"],
        "learn_rate": [0.001, 0.01],
        "batch_size": [100, 500, 1000]

    }

    return hyperparameters

def get_all_hyperparameters_combinations(hyperparameters):

    hyperparameters_combinations = list(itertools.product(*hyperparameters.values()))
    hyperparameters_combinations = [list(combination) for combination in hyperparameters_combinations]

    return hyperparameters_combinations

def main():

    config = load_config_file("config.cfg")
    hyperparameters = store_hyperparameters()
    hyperparameters_combinations = get_all_hyperparameters_combinations(hyperparameters)
    for hyperparameters_combination in tqdm(hyperparameters_combinations):
        try:
            output_dir = "balanced_fin_" + "_".join([str(hyperparameter) for hyperparameter in hyperparameters_combination])
            modify_config_file(config, hyperparameters_combination)
            run_command(config, output_dir)
        except Exception as e:
            print("Error with combination: ", hyperparameters_combination)

if __name__ == "__main__":
    main()