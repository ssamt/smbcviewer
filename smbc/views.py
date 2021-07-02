import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import os.path

from django.shortcuts import render, redirect
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

from smbcviewer.settings import BASE_DIR
from .models import Page

main_link = 'https://www.smbc-comics.com/'
comic_link = main_link + 'comic/{}'
random_link = main_link + 'rand.php'

def smbc_view(request, name=None):
    if not name:
        response = requests.get(main_link)
        soup = BeautifulSoup(response.text, 'html.parser')
        name = get_name(get_permalink(soup))
    find = Page.objects.filter(name=name)
    if len(find) > 0:
        page = find[0]
    else:
        response = requests.get(comic_link.format(name))
        soup = BeautifulSoup(response.text, 'html.parser')
        page = Page(name=name)
        comic_tag = soup.find('img', {'id':'cc-comic'})
        comic_image = NamedTemporaryFile()
        with urlopen(comic_tag['src']) as url:
            comic_image.write(url.read())
            comic_image.flush()
        page.comic.save(name+'.png', File(comic_image))
        bonus_div = soup.find('div', {'id':'aftercomic'})
        bonus_tag = bonus_div.find('img')
        bonus_image = NamedTemporaryFile()
        with urlopen(bonus_tag['src']) as url:
            bonus_image.write(url.read())
            bonus_image.flush()
        page.bonus.save(name+'_bonus.png', File(bonus_image))
        class_list = ['cc-prev', 'cc-next']
        nav_names = [get_name(get_nav_link(soup, c)) for c in class_list]
        page.prev = nav_names[0]
        page.next = nav_names[1]
        title_text = comic_tag['title']
        page.title_text = title_text
        page.save()
    context = {'page': page, 'main_link':main_link}
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
