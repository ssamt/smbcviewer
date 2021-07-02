import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen

from django.shortcuts import render, redirect
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

main_link = 'https://www.smbc-comics.com/'
comic_link = main_link + 'comic/{}'
random_link = main_link + 'rand.php'

def smbc_view(request, name=None):
    if not name:
        response = requests.get(main_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = get_name(get_permalink(soup))
    response = requests.get(comic_link.format(name))
    soup = BeautifulSoup(response.text, 'html.parser')
    comic_tag = soup.find('img', {'id':'cc-comic'})
    comic_image_link = comic_tag['src']
    bonus_div = soup.find('div', {'id':'aftercomic'})
    bonus_tag = bonus_div.find('img')
    bonus_image_link = bonus_tag['src']
    prev_name = get_name(get_nav_link(soup, 'cc-prev'))
    next_name = get_name(get_nav_link(soup, 'cc-next'))
    title_text = comic_tag['title']
    context = {'comic_image_link':comic_image_link, 'bonus_image_link':bonus_image_link,
               'prev_name':prev_name, 'next_name':next_name, 'title_text':title_text, 'main_link':main_link}
    return render(request, 'comic.html', context)

def random_view(request):
    response = requests.get(random_link)
    name = delete_quote(response.text)
    return redirect('comic', name=name)

def first_view(request):
    response = requests.get(main_link)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_tag = soup.find('a', {'class':'cc-first'})
    name = get_name(first_tag['href'])
    return redirect('comic', name=name)

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

def delete_quote(s):
    return s[1:-1]
