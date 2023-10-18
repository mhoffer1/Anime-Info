from jikanpy import Jikan
import os
from InquirerPy import inquirer
from tabulate import tabulate
from time import sleep
from ascii_magic import AsciiArt
from PIL import Image
from io import BytesIO
import requests


def main():
    
    while True:
        clear()
        mode = mode_selector()
        anime_name = get_anime_name()
        anime_info = search_anime(anime_name, mode)
        print_anime_info(anime_name, anime_info)
        while True:
            exit_value = extra_info(anime_info, anime_name, mode)
            if exit_value == False:
                break
        if inquirer.select(message="Do you wish to do a new search?: ", choices=["Yes", "No"]).execute() == "No":
            break
        else:
            continue
        
def search_anime(anime_name, mode):

    try:
        jikan = Jikan()
        anime = jikan.search('anime', anime_name, page=1, parameters={'type': mode.lower()})
        return anime
    except Exception as e:
        print(f"Error: {e}")
        return {'data': []}
    
def print_anime_info(anime_name, anime_info):
    
    clear()
    if not anime_info['data']:
        print(f"Anime '{anime_name}' not found.")
    else:
        anime_data = anime_info['data'][0]
        keys_to_print = ['title', 'title_japanese', 'year', 'episodes', 'status', 'score', 'rating', 'url']
        data_to_print = [{anime_name: key, "Information": anime_data[key]} for key in keys_to_print]

        formated_list = format_data(data_to_print, anime_name)

        table = tabulate(formated_list, headers="keys", tablefmt='fancy_grid')
        print(table)

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def mode_selector():
    mode = inquirer.select(message="Select one: ", choices=["Tv", "Movie"]).execute()
    clear()
    return mode

def get_anime_name():
    
    clear()
    while True:
        try:
            anime_name = input("Enter anime name: ").strip().title()
            return anime_name
        except ValueError:
            print("Invalid input, try again.")
            continue

def format_data(data, anime_name):
    
    formated_list = []
    for item in data:
        item[anime_name] = str(item[anime_name]).capitalize()
        formated_list.append(item)
    
    formated_list[0]['Information'] = f"{formated_list[0]['Information']} ({formated_list[1]['Information']})"
    formated_list.pop(1)
    
    return formated_list

def synopsis(anime_info):
        synopsis_text = anime_info['data'][0]['synopsis']
        print_slow(synopsis_text)

def print_slow(txt):
    for x in txt:                     
        print(x, end='', flush=True)  
        sleep(0.010)
    print()

def open_image_from_url(url):
    response = requests.get(url)
    
    if response.status_code == 200:
        image = Image.open(BytesIO(response.content))
        return image
    else:
        print(f"Failed to download image. Status code: {response.status_code}")
        return None

def extra_info(anime_info, anime_name, mode):
    choice = inquirer.select(message="Select one: ", choices=["Info","Synopsis", "ASCII Art", "Exit"]).execute()
    
    if choice == 'ASCII Art':
      image_url = anime_info['data'][0]['images']['jpg']['image_url']
      image = open_image_from_url(image_url)
      ascii_art = AsciiArt(image)
      ascii_art.to_terminal()
    elif choice == 'Info':
        anime_info = search_anime(anime_name, mode)
        print_anime_info(anime_name, anime_info)
    elif choice == 'Synopsis': 
      synopsis(anime_info)
    elif choice == 'Exit':
      return False

if __name__ == "__main__":
    main()