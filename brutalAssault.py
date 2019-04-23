import requests
import time
from bs4 import BeautifulSoup
import re
import pandas as pd

#this is for the English version of the site
#the Czech version seems to have more videos (based on first three bands)

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

print('There is '+ str(len(bands_list))+ ' bands so far')

#test for one band link:
#test_link = band_links[0]
band_country = []
band_website = []
band_videourl = []

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
	#video link - error handling if find = nonetype or something similar
	try:
		band_videourl.append(temp_soup.find('iframe')['src'])
	except:
		band_videourl.append('No Video')
		
print('Together, there is ' + str(len(band_videourl))+ ' videos in bands profiles')

#find out how many unique countries are represented:
band_set = set(band_country)
number_of_countries = (list(band_set))

print('There are bands from ' +str(len(number_of_countries))+ ' registered in BA2019')

table_ba = pd.DataFrame(list(zip(bands_list,genre_list_clean,band_country,band_website,band_url, band_text,band_videourl)),columns=['Band Name','Genre','Country','Band Website','BA URL','Description','Video URL'])
#define a custom path to store the csv file: a cloned githug repo

pathSlalom = r'C:\Users\michal.sicak\OneDrive - Slalom\Datapun\Brutal\\'
pathHome = r'D:\___Projects\Python\.python_virtual_environments\Brutal\\'

#store the table in a data frame, without the row numbers (index=False)

table_ba.to_csv(pathHome+'brutal_assault_2019_bands.csv',index=False)

#can i then commit from python ?