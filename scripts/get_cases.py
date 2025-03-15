from bib_cases import get_genitif, get_datif, get_ablatif, get_accusatif, get_allatif, get_instrumental, get_locatif, get_locatif_alt, get_possessif
import click
"""
Extrapole -salement- les désinences possibles pour un nom propre à partir de sa forme
nominative. On part du principe que les noms propres ne peuvent pas prendre les désinences plurielles ou duelles.
Basé sur :
- https://folk.uib.no/hnohf/qcourse.htm
- le haut elfique pour les débutants, Edouard Kloczko, POCKET, 2015
"""

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


@click.command()
@click.argument('input_file', type=str)
def main(input_file:str):
    """Grabs the nominative forms from a txt and gets all possible cases for it. Saves it in a new txt file"""
    output_file = input_file[:-4] + "_all_cases.txt"
    nominatifs = get_data(input_file)
    cases = get_cases(nominatifs)
    save_cases(cases, output_file)

    return print("Fin du script, have fun kids")


if __name__ == "__main__":
    main()
