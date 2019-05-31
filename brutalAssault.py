import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import platform

#can i then commit from python ?
#can i simplify? ask user for input (cz or en) and then run just one half of the code. 
#done
#or even split into two scripts and run only one required by user input?
#or parametrize cz and en? the only difference is in country/zeme and genre/styl, tags are the same
#maybe later

#determine if the script needs to be run (if there are new articles)
#eg store a list of article dates in a file and then query the articles each time a script is run, compare to the file. 
#if it's the same, do not run the script, else run the script and update the reference file with the newest article date

#user input selection if they want to scrape the English or Czech site
while True:
	try:
		user_input = int(input('Language Menu:\n 1 - English \n 2 - Czech \n Your Choice: '))
		if user_input > 2:
			print('\n please select 1 or 2 \n')
			continue
		else:
			break
	except ValueError:
		print('\n please select the number 1 or 2 \n')
		continue
	else:
		break
    
#determine where the script is run from - work laptop or home desktop
#this drives which path is used
computer_name = platform.node()
if computer_name == 'muxy-PC':
	path = r'D:\___Projects\Python\.python_virtual_environments\Brutal\\'
else:
	path = r'C:\Users\michal.sicak\OneDrive - Slalom\Datapun\Brutal\\'

def english_brutal():
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
		
	band_link = soup.findAll(class_='lineup_band_link')

	band_url = []
	for band in band_link:
		bands = band['href']
		band_url.append(bands)

	#write a code that takes each thumbnail and saves it
	#add all these into a data frame and store it on github/s3 bucket

	print('There is '+ str(len(bands_list))+ ' bands so far')
	print('Adding more info, like country of origin, and videos')

	band_country = []
	band_website = []
	band_videourl = []
	band_description = []
	band_image = []
	
	#open each band link and scrape country, website, video URL etc.
	for link in band_url:
		temp_url = requests.get(link).text
		temp_soup = BeautifulSoup(temp_url, 'html.parser')
		temp_band_country = temp_soup.find('h5').text
		#strip() at the end would cause country names to be shortened from Spain to Spai etc.
		#strip removes any letter from the entire string, eg n from Spain
		#therefore this is removed: strip('Country: ')).strip(' '))
		clean_band_country = temp_band_country[-(len(temp_band_country)-temp_band_country.find(':')-2):]
		band_country.append(clean_band_country)
		temp_band_website = temp_soup.find('p',class_='officialWebiste').find('a')['href']
		band_website.append(temp_band_website)
		band_text = temp_soup.find('div',class_='page_content').text
		#remove everything before official website, inclusive
		charpos = band_text.find('official website')
		band_clean_text = band_text[charpos+17:]
		band_description.append(band_clean_text)
		try:
			band_videourl.append(temp_soup.find('iframe')['src'][2:])
      #.replace('/embed/','/watch?v='))
		except:
			band_videourl.append('No Video')
		band_image_url = temp_soup.find('div',class_='band_image').img['src']
		band_image.append(band_image_url)
	print('Together, there is ' + str(len(band_videourl))+ ' videos in bands profiles')

	#find out how many unique countries are represented:
	band_set = set(band_country)
	number_of_countries = (list(band_set))

	print('There are bands from ' +str(len(number_of_countries))+ ' countries registered in BA2019')

	table_ba = pd.DataFrame(list(zip(bands_list,genre_list_clean,band_country,band_website,band_url, band_description,band_videourl, band_image)),columns=['Band Name','Genre','Country','Band Website','BA URL','Description','Video URL','Image'])

	#store the table in a data frame, without the row numbers (index=False)
	table_ba.to_csv(path+'brutal_assault_2019_bands.csv',index=False)

def czech_brutal():
	#czech version of the same code
	url = requests.get('https://www.brutalassault.cz/cs/line-up').text
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
		
	band_link = soup.findAll(class_='lineup_band_link')

	band_url = []
	#called band_links in the terminal
	for band in band_link:
		bands = band['href']
		band_url.append(bands)

	#write a code that takes each thumbnail and saves it
	#add all these into a data frame and store it on github/s3 bucket

	print('Doteraz bolo ohlasenych '+ str(len(bands_list))+ ' kapiel')
	print('Zistujem dalsie info: videa, zanre, krajina povodu atd.')

	#test for one band link:
	#test_link = band_links[0]
	band_country = []
	band_website = []
	band_videourl = []
	band_description = []
	band_image = []
	
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
		charpos = band_text.find('oficiální stránky')
		band_clean_text = band_text[charpos+17:].strip()
		
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
			#need to replace /embed/ in the videourl with /watch?v=
			band_videourl.append(temp_soup.find('iframe')['src'][2:])
		except:
			band_videourl.append('No Video')
		band_image_url = temp_soup.find('div',class_='band_image').img['src']
		band_image.append(band_image_url)
		
	print('V profiloch kapiel je dokopy ' + str(len(band_videourl))+ ' videi')

	#find out how many unique countries are represented:
	band_set = set(band_country)
	number_of_countries = (list(band_set))

	print('Na Brutale su zatial registrovane kapely z ' +str(len(number_of_countries))+ ' krajin')

	table_ba = pd.DataFrame(list(zip(bands_list,genre_list_clean,band_country,band_website,band_url, band_description,band_videourl, band_image)),columns=['Band Name','Genre','Country','Band Website','BA URL','Description','Video URL','Image'])

	#store the table in a data frame, without the row numbers (index=False)
	table_ba.to_csv(path+'brutal_assault_2019_kapely.csv',index=False)

if user_input == 1:
	english_brutal()
else:
	czech_brutal()