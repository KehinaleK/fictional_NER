# fictional_NER

This repository aims to provide a Named Entity Recognition model for Quenya, or as most people call it Elvish.
This language was created by Tolkien and is one of the multiple fictional languages that can be found in his work.
For more information about the language, the corpus, and the models, we encourage you to look at the pages found in the `web` folder.

# Use the web interface :

The script used to launch the web interface can be found directly at the root of the repository. You will need uvicorn to use it.
Running the script :

```python3 API_NER_quenya:app```

You will then access the html interface at http://localhost:8000/front/quenya.html


Now onto, how to use each model if you wish to test or improve them.

# Spacy

All codes and data used for the Spacy training can be found in the `spacy` directory.

Requirements:

- Spacy.
- CSV file(s) in `data/corpus/` that contain a column with the texts and another with their title.
- TXT files containing entities in a 'one entity per line' format.

1 - JSON inputs

Spacy requires a specific input format. Use the `find_entities.py` script in `spacy/scripts/` to retrieve entities
in each text and store their index in a JSON file. This file will be saved in the `spacy/json_inputs/` directory.

Running the script : 

```python3 find_entities.py --set train```
```python3 find_entities.py --set test```
```python3 find_entities.py --set dev```

2 - Spacy inputs

Those JSON files then need to be processed and converted to a format that can be interpreted by the spacy pipelines.
To do so, use the `conversion.py` script in the `spacy/scripts/` directory. The resulting file will be saved in the `spacy/spacy_inputs/` directory.

Running the script : 

```python3 conversion.py --set train```
```python3 conversion.py --set test```
```python3 conversion.py --set dev```

3 - Training 

Once your data is ready, you can use the `trainig.py` script in the `spacy/scripts` directory to train your model. You will find a `config.cfg` file
in the root of the `spacy` folder. This file will be modified for each trained model with the hyperparameter values that can be given in the training
script. Change its content manually if you wish to start from a new baseline.

Each model (its best and last state) will be stored in the `spacy/models` directory.

Running the script : 

```python3 training.py```

4 - Evaluation

Finally, you can evaluate your model with the `evaluation.y` script in the `spacy/scripts` directory. This script allows you to save all models in a given directory
or simpy one model given in argument. It will store the results in the `spacy/spacy_results` directory. 

```python3 evaluation.py --models models```
```python3 evaluation.py -model balanced_fin_false_0.001_1000/model-best```


5 - Illustration

Finally, in you'll find 3 TXT files in the `spacy/illustration` directory. These texts are used in the `illustration.py` script in the `spacy/scripts` directory
to showcase the best model performance on unseen data. Those texts were not part of any train, test, or dev test. 


# Get cases from a txt file containing nominative forms:

Should you want to do it, you may run the script found in the `scripts/` directory :

```python3 get_cases.py [input_file]```

input_file must be a a txt file where each line corresponds to a nominative form. The output file will be found in the input_file folder under "input_file_all_cases.txt".
