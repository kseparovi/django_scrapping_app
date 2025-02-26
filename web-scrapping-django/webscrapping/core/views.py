from bs4 import BeautifulSoup
from django.shortcuts import render, get_object_or_404, redirect
import requests


def get_content():
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers.update({
        'User-Agent': USER_AGENT,
        'Accept-Language': LANGUAGE,
        'Content-Language': LANGUAGE
    })
    url = 'https://m.gsmarena.com/samsung-phones-9.php'
    response = session.get(url)
    if response.status_code == 200:
        return response.text
    return ""


def home(request):
    product_info_list = []
    html_content = get_content()
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        product_items = soup.find('div', id='list-brands').find_all('li')

        for item in product_items:
            link = item.find('a')
            img_tag = item.find('img')
            name_tag = item.find('strong')

            if link and img_tag and name_tag:
                product_name = name_tag.text.strip()
                image_url = img_tag['src']
                product_info_list.append({'name': product_name, 'image_url': image_url})

    return render(request, 'core/home.html', {'product_info_list': product_info_list})
