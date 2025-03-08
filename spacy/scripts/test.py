import glob
import json

def load_result_file(file):
    with open(file, 'r') as f:
        return json.load(f)
    
def get_scores(data):

    dict_results = {}

    f_score = data['ents_f']
    recall = data['ents_r']
    precision = data['ents_p']
    f_score_person = data['ents_per_type']['PERSON']['f']
    recall_person = data['ents_per_type']['PERSON']['r']
    precision_person = data['ents_per_type']['PERSON']['p']
    f_score_loc = data['ents_per_type']['LOC']['f']
    recall_loc = data['ents_per_type']['LOC']['r']
    precision_loc = data['ents_per_type']['LOC']['p']

    dict_results = {
        'f_score': f_score,
        'recall': recall,
        'precision': precision,
        'f_score_person': f_score_person,
        'recall_person': recall_person,
        'precision_person': precision_person,
        'f_score_loc': f_score_loc,
        'recall_loc': recall_loc,
        'precision_loc': precision_loc
    }

    return dict_results

def main():
     
    result_directory = "original_shuffles_results"
    result_files = glob.glob(f"{result_directory}/*.json")

    dict_results = {}

    fin_files = [file for file in result_files if "fin" in file]
    eng_files = [file for file in result_files if "fin" not in file]

    for result_file in result_files:
        data = load_result_file(result_file)
        dict_results[result_file.split("/")[-1]] = get_scores(data)
        
    # ### get mean f_score for each language
    # fin_f_scores = [dict_results[file.split("/")[-1]]['f_score'] for file in fin_files]
    # mean_fin_f_score = sum(fin_f_scores) / len(fin_f_scores)
    # print(f"Mean f_score for Finnish: {mean_fin_f_score}")
    # base_f_scores = [dict_results[file.split("/")[-1]]['f_score'] for file in eng_files]
    # mean_base_f_score = sum(base_f_scores) / len(base_f_scores)
    # print(f"Mean f_score for Multilingual model: {mean_base_f_score}")
    # #### get mean for all 
    # all_f_scores = [dict_results[file.split("/")[-1]]['f_score'] for file in result_files]
    # mean_f_score = sum(all_f_scores) / len(all_f_scores)
    # print(f"Mean f_score for all models: {mean_f_score}")

    ### sort by f_score
    sorted_dict = dict(sorted(dict_results.items(), key=lambda item: item[1]['f_score'], reverse=True))
    for key, value in sorted_dict.items():
        print(key, value)
        print("\n")



if __name__ == '__main__':
    main()