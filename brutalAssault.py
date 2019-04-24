import requests
#import time
from bs4 import BeautifulSoup
import re
import pandas as pd

#can i then commit from python ?
#can i simplify? ask user for input (cz or en) and then run just one half of the code. 
#or even split into two scripts and run only one required by user input?
#or parametrize cz and en? the only difference is in country/zeme and genre/styl, tags are the same

#this is for the English version of the site
#the Czech version seems to have more videos (based on first three bands)

en_url = requests.get('https://www.brutalassault.cz/en/line-up').text
soup = BeautifulSoup(en_url, 'html.parser')

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
print('Adding more info, like country of origin, and videos')

#test for one band link:
#test_link = band_links[0]
band_country = []
band_website = []
band_videourl = []
band_description = []

for link in band_url:
	temp_url = requests.get(link).text
	temp_soup = BeautifulSoup(temp_url, 'html.parser')
	temp_band_country = temp_soup.find('h5').text
	clean_band_country = temp_band_country[-(len(temp_band_country)-temp_band_country.find(':')-2):]
	#strip() at the end causes country names to be shortened from Spain to Spai etc.
	band_country.append(clean_band_country)
	#strip removes any letter from the entire string, eg n from Spain
	#therefore this is removed: strip('Country: '))#.strip(' '))
	temp_band_website = temp_soup.find('p',class_='officialWebiste').find('a')['href']
	band_website.append(temp_band_website)
	band_text = temp_soup.find('div',class_='page_content').text
	#charpos = band_text.find('\t\t\t\t\t\t')
	charpos = band_text.find('official website')
	band_clean_text = band_text[charpos+17:]
	
	#a very raw text string. needs cleaning with regex - remove everything before \t\t\t\t\t\t
	#replaced this logic with "remove everything before official website, inclusive" - see above
	band_description.append(band_clean_text)
	#get band description text. this does not work as the string is different per band
	#this caused the script to be cut off after 20 bands or so
	#band_rawtext = re.search('\\t\w+.+',band_text.text)
	#try:
	#	band_text = band_rawtext[0].strip('\t')
	#	band_texts.append(band_text)
	#except:
	#	band_texts.append('No description')
	#video link - error handling if find = nonetype or something similar
	try:
		band_videourl.append(temp_soup.find('iframe')['src'])
	except:
		band_videourl.append('No Video')
		
print('Together, there is ' + str(len(band_videourl))+ ' videos in bands profiles')

#find out how many unique countries are represented:
band_set = set(band_country)
number_of_countries = (list(band_set))

print('There are bands from ' +str(len(number_of_countries))+ ' countries registered in BA2019')

table_ba = pd.DataFrame(list(zip(bands_list,genre_list_clean,band_country,band_website,band_url, band_description,band_videourl)),columns=['Band Name','Genre','Country','Band Website','BA URL','Description','Video URL'])
#define a custom path to store the csv file: a cloned githug repo

pathSlalom = r'C:\Users\michal.sicak\OneDrive - Slalom\Datapun\Brutal\\'
pathHome = r'D:\___Projects\Python\.python_virtual_environments\Brutal\\'

#store the table in a data frame, without the row numbers (index=False)

table_ba.to_csv(pathSlalom+'brutal_assault_2019_bands.csv',index=False)

#can i then commit from python ?

#czech version of the same code
cz_url = requests.get('https://www.brutalassault.cz/cs/line-up').text
cz_soup = BeautifulSoup(cz_url, 'html.parser')

cz_bands = cz_soup.findAll('strong',class_='band_lineup_title')

cz_bands_list = []

for band in cz_bands:
	cz_bands_list.append(band.text)
	
cz_genres = cz_soup.findAll('span',class_='band_lineup_genre')

cz_genre_list = []

for genre in cz_genres:
	#re.sub('[^A-Za-z]+',genre.text)
	cz_genre_list.append(genre.text)

cz_genre_list_clean = []

#remove extra whitespace except for spaces between words
for genre in cz_genre_list:
	genre = re.sub('[^A-Za-z]+',' ',genre).strip()
	cz_genre_list_clean.append(genre)
	
cz_keys = bands_list
cz_values = genre_list_clean

#not used any more - replaced with pandas df
cz_bands_dictionary = dict(zip(keys,values))

cz_band_link = cz_soup.findAll(class_='lineup_band_link')

cz_band_url = []
#called band_links in the terminal
for band in cz_band_link:
	bands = band['href']
	cz_band_url.append(bands)

#write a code that takes each thumbnail and saves it
#add all these into a data frame and store it on github/s3 bucket

print('Doteraz bolo ohlasenych '+ str(len(cz_bands_list))+ ' kapiel')
print('Zistujem dalsie info: videa, zanre, krajina povodu atd.')

#test for one band link:
#test_link = band_links[0]
cz_band_country = []
cz_band_website = []
cz_band_videourl = []
cz_band_description = []

for link in cz_band_url:
	temp_url = requests.get(link).text
	temp_soup = BeautifulSoup(temp_url, 'html.parser')
	temp_band_country = temp_soup.find('h5').text
	clean_band_country = temp_band_country[-(len(temp_band_country)-temp_band_country.find(':')-2):]
	#strip() at the end causes country names to be shortened from Spain to Spai etc.
	cz_band_country.append(clean_band_country)
	#strip removes any letter from the entire string, eg n from Spain
	#therefore this is removed: strip('Country: '))#.strip(' '))
	temp_band_website = temp_soup.find('p',class_='officialWebiste').find('a')['href']
	cz_band_website.append(temp_band_website)
	band_text = temp_soup.find('div',class_='page_content').text
	#charpos = band_text.find('\t\t\t\t\t\t')
	charpos = band_text.find('official website')
	band_clean_text = band_text[charpos+17:]
	
	#a very raw text string. needs cleaning with regex - remove everything before \t\t\t\t\t\t
	#replaced this logic with "remove everything before official website, inclusive" - see above
	cz_band_description.append(band_clean_text)
	#get band description text. this does not work as the string is different per band
	#this caused the script to be cut off after 20 bands or so
	#band_rawtext = re.search('\\t\w+.+',band_text.text)
	#try:
	#	band_text = band_rawtext[0].strip('\t')
	#	band_texts.append(band_text)
	#except:
	#	band_texts.append('No description')
	#video link - error handling if find = nonetype or something similar
	try:
		cz_band_videourl.append(temp_soup.find('iframe')['src'])
	except:
		cz_band_videourl.append('No Video')
		
print('V profiloch kapiel je dokopy ' + str(len(band_videourl))+ ' videi')

#find out how many unique countries are represented:
cz_band_set = set(cz_band_country)
cz_number_of_countries = (list(band_set))

print('Na Brutale su zatial registrovane kapely z ' +str(len(number_of_countries))+ ' krajin')

cz_table_ba = pd.DataFrame(list(zip(cz_bands_list,cz_genre_list_clean,cz_band_country,cz_band_website,cz_band_url, cz_band_description,cz_band_videourl)),columns=['Band Name','Genre','Country','Band Website','BA URL','Description','Video URL'])
#define a custom path to store the csv file: a cloned githug repo

pathSlalom = r'C:\Users\michal.sicak\OneDrive - Slalom\Datapun\Brutal\\'
pathHome = r'D:\___Projects\Python\.python_virtual_environments\Brutal\\'

#store the table in a data frame, without the row numbers (index=False)

cz_table_ba.to_csv(pathSlalom+'brutal_assault_2019_kapely.csv',index=False)