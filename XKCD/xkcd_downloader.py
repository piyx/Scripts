import requests
import os
from bs4 import BeautifulSoup
from urllib.request import urlopen
import concurrent.futures

url = 'https://xkcd.com/'

os.makedirs('xkcdcomics', exist_ok=True)
os.chdir('xkcdcomics')

def download(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_url = 'https:' + soup.select('#comic > img')[0].get('src')
    img_name = img_url.split('/')[-1]

    print(f'Downloading {img_name}')
    with open(img_name, 'wb') as f:
        f.write(urlopen(img_url).read())

if __name__ == "__main__":
    num_images = 100
    download(url + str(1))
    with concurrent.futures.ThreadPoolExecutor() as executor:
        for i in range(1, num_images):
            executor.submit(download, url + str(i))
    
    print('Downloaded all images!')
    