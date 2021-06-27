import requests
from bs4 import BeautifulSoup
import urllib.request
import os.path

from smbcviewer.settings import BASE_DIR
from django.shortcuts import render

main_link = 'https://www.smbc-comics.com/comic/'
comic_link = main_link + '{}'

def smbc_view(request, name=None):
    if not name:
        response = requests.get(main_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = get_name(get_permalink(soup))
    data_folder = f'{BASE_DIR}/static/data'
    if not os.path.isfile(data_folder):
        os.makedirs(data_folder)
    folder = f'{BASE_DIR}/static/data/{name}'
    comic_path = f'{folder}/comic.png'
    bonus_path = f'{folder}/bonus.png'
    nav_path = f'{folder}/nav_name.txt'
    title_path = f'{folder}/title_text.txt'
    if all([os.path.isfile(path) for path in [comic_path, bonus_path, nav_path, title_path]]):
        nav_file = open(nav_path, 'r')
        nav_names = nav_file.read().split()
        title_file = open(title_path, 'r')
        title_text = title_file.read()
    else:
        os.makedirs(folder)
        response = requests.get(comic_link.format(name))
        soup = BeautifulSoup(response.text, 'html.parser')
        comic_image = soup.find('img', {'id':'cc-comic'})
        urllib.request.urlretrieve(comic_image['src'], comic_path)
        bonus_div = soup.find('div', {'id':'aftercomic'})
        bonus_panel = bonus_div.find('img')
        urllib.request.urlretrieve(bonus_panel['src'], bonus_path)
        class_list = ['cc-first', 'cc-prev', 'cc-navaux', 'cc-next', 'cc-last']
        nav_names = [get_name(get_nav_link(soup, c)) for c in class_list]
        nav_file = open(nav_path, 'w')
        nav_file.write(' '.join(nav_names))
        title_text = comic_image['title']
        title_file = open(title_path, 'w')
        title_file.write(title_text)
        print(soup)
    context = {'name': name, 'nav_names': nav_names, 'title_text': title_text, 'main_link':main_link}
    return render(request, 'comic.html', context)


def get_nav_link(soup, class_name):
    element = soup.find('a', {'class':class_name})
    if element:
        return element['href']
    else:
        return None

def get_permalink(soup):
    link = soup.find('input', {'id':'permalinktext'})['value']
    return link

def get_name(link):
    if link:
        start = link.rfind('/')+1
        return link[start:]
    else:
        return ''
