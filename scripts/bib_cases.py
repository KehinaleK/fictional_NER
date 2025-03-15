"""Bibliothèque de toutes les fonctions produisant un cas à partir d'un mot au nominatif"""


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