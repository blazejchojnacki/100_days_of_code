import requests
from bs4 import BeautifulSoup

# yyyy_mm_dd = input('what year you would like to travel to in YYYY-MM-DD format:')
yyyy_mm_dd = '2000-08-12'
header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0"}
URL = f'https://www.billboard.com/charts/hot-100/{yyyy_mm_dd}'

web_page = requests.get(URL, headers=header)
page_soup = BeautifulSoup(web_page.text, 'html.parser')

songs_list = []
classes = [
    "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet",
    "c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only"
]
# for header_song in page_soup.find_all(id="title-of-a-story"):  # 'li h3'
#     if header_song.text.strip() not in ['Songwriter(s):', 'Producer(s):', 'Imprint/Promotion Label:']:
#         songs_list.append(header_song.text.strip())

song_elements = [page_soup.find(class_=classes[0])]
song_elements.extend(page_soup.find_all(class_=classes[1]))

for song_element in song_elements:
    songs_list.append(song_element.getText().strip())


print(songs_list)
