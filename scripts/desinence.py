"""
Extrapole -salement- les désinences possibles pour un nom propre à partir de sa forme
nominative. On part du principe que les noms propres ne peuvent pas prendre les désinences plurielles ou duelles.
Basé sur :
- https://folk.uib.no/hnohf/qcourse.htm
- le haut elfique pour les débutants, Edouard Kloczko, POCKET, 2015
"""


# Path (hardcoded sale, possibilité de mettre un ptit click ou argparse)
input_file = "person_final.txt"
output_file = "person_cases.txt"


######### GET FUNCTIONS : Grab a case from the nominative form #########

def get_genitif(nominatif:str, char:dict)->str:
    """take the nominative case (str) and return the genitive case as a string"""
    genitif = nominatif + "o"
    if nominatif[-1] in char["a_forms"]:
        genitif = nominatif[:-1] + "o"
    return genitif

def get_possessif(nominatif:str, char:dict)->str:
    """take the nominative case (str) and return the possessive case as a string"""
    if len(nominatif) >= 5 and nominatif[-3] in char["court"] and nominatif[-1] in char["court"]:
            nominatif = nominatif[:-3] + char[nominatif[-3]] + nominatif[-2:]
    if nominatif[-1] in char["voyelles"]:
        possessif = nominatif[:-1] + char["style2base"][nominatif[-1]] + "va"
    else:
        possessif = nominatif + "wa"
    return possessif

def get_datif(nominatif:str, char:dict)-> str:
    """take the nominative case (str) and return the dative case as a string"""
    datif = nominatif + "en"
    if nominatif[-1] in char["voyelles"]:
        datif = nominatif[:-1] + char["style2base"][nominatif[-1]] + "n"
    return datif

def get_allatif(nominatif:str, char:dict)-> str:
    """take the nominative case (str) and return the allative case as a string"""
    allatif = nominatif + "enna"
    if nominatif[-1] == "n" and nominatif[-2] in char["voyelles"] :
        allatif = nominatif + "na"
    if nominatif[-1] in char["voyelles"]:
        allatif = nominatif[:-1] + char["style2base"][nominatif[-1]] + "nna"
    return allatif

def get_ablatif(nominatif:str, char:dict)-> str:
    """take the nominative case (str) and return the ablative case as a string"""
    ablatif = nominatif + "ello"
    if nominatif[-1] in char["voyelles"]:
        ablatif = nominatif[:-1] + char["style2base"][nominatif[-1]] + "llo"
    return ablatif

def get_locatif(nominatif:str, char:dict)->str:
    """take the nominative case (str) and return the locative case as a string"""
    locatif = nominatif + "esse"
    if nominatif[-1] in char["voyelles"]:
        locatif = nominatif[:-1] + char["style2base"][nominatif[-1]] + "sse"
    return locatif

def get_locatif_alt(nominatif:str, char:dict)->str:
    """take the nominative case (str) and return the locative case (alternative form) as a string"""
    locatif = nominatif + "essë"
    if nominatif[-1] in char["voyelles"]:
        locatif = nominatif[:-1] + char["style2base"][nominatif[-1]] + "ssë"
    return locatif

def get_accusatif(nominatif:str, char:dict)-> str:
    """take the nominative case (str) and return the accusative case as a string"""
    accusatif = nominatif
    if nominatif[-1] in char["voyelles"]:
        accusatif = nominatif[:-1] + char[nominatif[-1]]
    return accusatif

def get_instrumental(nominatif:str, char:dict)-> str:
    """take the nominative case (str) and return the instrumental case as a string"""
    instrumental = get_datif(nominatif, char) + "en"
    return instrumental

############## GET THEM ALL - Grab all cases from a list of nominative forms ###############

def get_cases(nominatifs:list)-> set:
    """generate all the possible cases from nominatives forms"""
    char = { 
        "a" : "á",
        "e" : "é",
        "i" : "í",
        "o" : "ó",
        "u" : "ú",
        "ä" : "á",
        "ë" : "é",
        "ï" : "í",
        "ö" : "ó",
        "ü" : "ú",
        "á" : "á",
        "é" : "é",
        "í" : "í",
        "ó" : "ó",
        "ú" : "ú",
        "voyelles" : ["a", "ä", "á", "e", "ë", "é", "i", "ï", "í", "o", "ö", "ó", "u", "ü", "ú"],
        "a_forms" : ["a", "ä", "á"],
        "base" : ["a", "e", "i", "o", "u"],
        "court" : [ "a", "e", "i", "o", "u", "ä", "ë", "ï", "ö", "ü"],
        "style2base" : {
            "ä" : "a",
            "ë" : "e",
            "ï" : "i",
            "ö" : "o",
            "ü" : "u",
            "a" : "a",
            "e" : "e",
            "i" : "i",
            "o" : "o",
            "u" : "u",
            "á" : "á",
            "é" : "é",
            "í" : "í",
            "ó" : "ó",
            "ú" : "ú", }
        }
    
    get = [ get_genitif, get_datif, get_ablatif, get_accusatif, get_allatif, 
    get_instrumental, get_locatif, get_locatif_alt, get_possessif
    ]
    formes = []

    for nominatif in nominatifs:
        formes.append(nominatif)
        l = nominatif.split()
        if len(l) == 1:
            for fonction in get:
                formes.append(fonction(nominatif, char))
        else :
            for part in l:
                if part != "i":
                    for fonction in get:
                        formes.append(fonction(part, char))
            for fonction in get:
                formes.append(" ".join([fonction(x, char) if x != "i" else "i" for x in l]))
    
    return sorted(set(formes))


######### ARCHITECTURE : MAIN function, grab data and save data ###########

def get_data(chemin:str)->list:
    """Return a list of string from a txt file where each line is a Proper Noun"""
    with open(chemin, "r", encoding="utf-8") as file :
        nominatifs = [ligne.strip() for ligne in file] 
    return nominatifs

def save_cases(formes:list, output_file:str):
    """Save all the forms in a txt file, one word per line"""
    with open(output_file, "w", encoding="utf-8") as file:
        for forme in formes:
            file.write(forme + "\n")
    return print(f"Fichier créé à {output_file}")

def main(input_file:str, output_file:str):
    nominatifs = get_data(input_file)
    cases = get_cases(nominatifs)
    save_cases(cases, output_file)
    return print("Fin du script, have fun kids")


if __name__ == "__main__":
    main(input_file, output_file)
