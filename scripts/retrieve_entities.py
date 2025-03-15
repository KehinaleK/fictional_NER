"""This script is used to scrap the entities found on the Lord of the Rings wiki page.
These entities are used to annotate automatically the texts of the corpus."""


import re
import requests
from bs4 import BeautifulSoup

def get_home_page(homepage_url):

    response = requests.get(homepage_url)
    if response.status_code != 200:
        return None
    
    homepage_data = BeautifulSoup(response.content, 'lxml')

    return homepage_data

def get_page_urls(homepage_data):

    characters = []
    categories = []

    parent_div = homepage_data.find("div", class_="category-page__members")

    for element in parent_div.find_all("div", class_="category-page__members-wrapper"):
        for link in element.find_all("a"):
            if "Category" in link.get("href"):
                categories.append(link.get("href"))
            else:
                characters.append(link.get("title"))

    return categories, characters

def scrap_category(category_url, all_characters, already_scrapped):

    if category_url in already_scrapped:
        return

    print("Scrapping category: ", category_url)
    already_scrapped.add(category_url)
    category_data = get_home_page(category_url)
    if category_data:
        categories, characters = get_page_urls(category_data)
        print("Characters: ", characters)
        print("Categories: ", categories)
        all_characters.extend(characters)
        for sub_category in categories:
            if "Images" in sub_category:
                continue
            sub_category_url = category_url.split("/wiki/")[0] + sub_category
            scrap_category(sub_category_url, all_characters, already_scrapped)

def save_characters(characters, file_path):

    characters = list(set(characters))
    characters.sort()
    
    to_remove = re.compile(r" \(.*\)")
    characters = [to_remove.sub("", character).strip() for character in characters]
    characters = list(set(characters))
    characters.sort()

    print("Characters: ", characters)
    print("Number of characters: ", len(characters))

    with open(file_path, "w") as file:
        for character in characters:
            file.write(character + "\n")
    
    
def main():

    home_page_url = "https://lotr.fandom.com/wiki/Category:Characters"
    homepage_data = get_home_page(home_page_url)
    sections, _ = get_page_urls(homepage_data)

    all_characters = []
    already_scrapped = set()

    for section in sections:
        section_url = home_page_url.split("/wiki/")[0] + section
        print("Section URL: ", section_url)

        scrap_category(section_url, all_characters, already_scrapped)

    save_characters(all_characters, "../data/elvish/entities/characters.txt")

if __name__ == "__main__":
    main()