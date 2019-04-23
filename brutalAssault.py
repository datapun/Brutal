import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

url = requests.get('https://www.brutalassault.cz/en/line-up').text
soup = BeautifulSoup(url, 'html.parser')

bands = soup.findAll('strong',class_='band_lineup_title')

bands_list = []

for band in bands:
	bands_list.append(band.text)
	
genres = soup.findAll('span',class_='band_lineup_genre')

genre_list = []

for genre in genres:
	#re.sub('[^A-Za-z]+',genre.text)
	genre_list.append(genre.text)

genre_list_clean = []

#remove extra whitespace except for spaces between words
for genre in genre_list:
	genre = re.sub('[^A-Za-z]+',' ',genre).strip()
	genre_list_clean.append(genre)
	
keys = bands_list
values = genre_list_clean

bands_dictionary = dict(zip(keys,values))

band_link = soup.findAll(class_='lineup_band_link')

band_url = []
#called band_links in the terminal
for band in band_link:
	bands = band['href']
	band_url.append(bands)

#write a code that takes each thumbnail and saves it
#add all these into a data frame and store it on github/s3 bucket

#test for one band link:
#test_link = band_links[0]
band_country = []
band_website = []
for link in band_url:
	temp_url = requests.get(link).text
	temp_soup = BeautifulSoup(temp_url, 'html.parser')
	temp_band_country = temp_soup.find('h5').text
	band_country.append(temp_band_country.strip('Country:').strip())
	temp_band_website = temp_soup.find('p',class_='officialWebiste').find('a')['href']
	band_website.append(temp_band_website)
	band_text = temp_soup.find('div',class_='page_content')
	#get band description text
	band_rawtext = re.search('\\t\w+.+',band_text.text)
	band_text = band_rawtext[0].strip('\t')
	
table_ba = pd.DataFrame(list(zip(bands_list,genre_list_clean,band_country,band_website,band_url, band_text)),columns=['Band Name','Genre','Country','Band Website','BA URL','Description'])
#define a custom path to store the csv file: a cloned githug repo

path = r'C:\Users\michal.sicak\OneDrive - Slalom\Datapun\Brutal\\'

#store the table in a data frame, without the row numbers (index=False)

table_ba.to_csv(path+'brutal_assault_2019_bands.csv',index=False)

#can i then commit from python ?

#how to get the band description text?
#