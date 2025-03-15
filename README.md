# fictional_NER

## Requirements:

- Glove Embeddings with 100 dimensions, either made from scratch with their github or the premade one 6B.100d.txt

## BLSTM_CRF
To train this model all the necessary files are in the directory `BLSTM_CRF`.  

1. Create the input files
`get_input_BLSTM_CRF.py` : python script that creates files dev, train, test with the right input format for the model from the three files in the `data` directory.  

2. Train the model  
`BLSTM_creation.ipynb`: jupyter notebook that detail all the steps and layers of the model used.  
This notebook save a copy of the best model found in the `model` directory.
