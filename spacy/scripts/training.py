import configparser
import itertools
from tqdm import tqdm
import subprocess

"""
This script is used to run the training of the model with different hyperparameters.
If you wish to run the training with only one set of hyperparameters, you can use the 'spacy train' command.
Otherwise, you can change the hyperparameters dictionary and run the script to train the model with all the combinations of hyperparameters.
You can also modify the config file to start from a different set of hyperparameters.

Each model will be saved in a different directory in the 'output' folder.
The name of the directory will be the hyperparameters used for the training. 
For each model, its best and last model will be saved as well as the training and evaluation logs.
"""


def load_config_file(config_file):
    """
    Load the configuration file containing the hyperparameters for the model.

    Args:
        config_file (str): The path to the configuration file.
    """

    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(config_file)

    return config

def run_command(output_dir):

    """
    Run the command to train the model with the given hyperparameters.
    
    Args:
        output_dir (str): The name of the directory where the model will be saved.
    Returns:
        int: The return code of the process. So the output that can be seen on the console
        when the command is run in the terminal !
    """

    # Modify directories if needed !
    command = ["python", "-m", "spacy", "train", "../config.cfg", "--output", f"../models/{output_dir}", "--paths.train",
               "../spacy_inputs/train.spacy", "--paths.dev", "../spacy_inputs/dev.spacy"]
    
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    
    # Read the output of the process
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

    """
    Modify the configuration file with the given hyperparameters. 

    Args:
        config (configparser.ConfigParser): The configuration file.
        hyperparameters_combinaison (list): The list of hyperparameters to use for the training.
    """

    ## display all the sections in the config file
    # print(config.sections())

    use_upper = hyperparameters_combinaison[0]
    learn_rate = hyperparameters_combinaison[1]
    batch_size = hyperparameters_combinaison[2]

    # Modify the configuration file in the right sections !
    config["components.ner.model"]["use_upper"] = str(use_upper)
    config["nlp"]["batch_size"] = str(batch_size)
    config["training.optimizer"]["learn_rate"] = str(learn_rate)
    config["training.batcher.size"]["rate"] = str(batch_size)

    # Modify the configuration file woop
    with open("../config.cfg", "w") as configfile:
        config.write(configfile)
    

def store_hyperparameters():

    """
    Store the hyperparameters used for the training. 

    Returns:
        dict(List): The hyperparameters used for the training.
    """

    hyperparameters = {
        "use_upper": ["true", "false"],
        "learn_rate": [0.1],
        "batch_size": [100, 500, 1000],
    #     # Batch size is used for batcher size and rate (same value)
    #     # We chose to use a constant batch size for the training and evaluation, but you can change it if you want

    }


    return hyperparameters

def get_all_hyperparameters_combinations(hyperparameters):

    """
    Get all the combinations of hyperparameters to use for the training.

    Args:
        hyperparameters (dict): The hyperparameters used for training.
    Returns:
        list(list): The list of all the combinations of hyperparameters.
    """

    hyperparameters_combinations = list(itertools.product(*hyperparameters.values()))
    hyperparameters_combinations = [list(combination) for combination in hyperparameters_combinations]

    return hyperparameters_combinations

def main():

    config = load_config_file("../config.cfg")
    hyperparameters = store_hyperparameters()
    hyperparameters_combinations = get_all_hyperparameters_combinations(hyperparameters)
    print(hyperparameters_combinations)
    print("Number of hyperparameters combinations: ", len(hyperparameters_combinations))
    print("config: ", config)

    for hyperparameters_combination in tqdm(hyperparameters_combinations):
        try:
        # You can change the output directory name if you want.
        # We chose fin here to indicate that we used the finnish model. 
        # You can do that automatically by using the hyperparameters_combination list if needed !
            output_dir = "balanced_fin" + "_".join([str(hyperparameter) for hyperparameter in hyperparameters_combination])
            modify_config_file(config, hyperparameters_combination)
            print("Running command with hyperparameters: ", hyperparameters_combination)
            run_command(output_dir)
        except Exception as e:
            print("Hmmm something went wrong: ", hyperparameters_combination)

if __name__ == "__main__":
    main()