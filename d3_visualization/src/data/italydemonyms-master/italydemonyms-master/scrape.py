from bs4 import BeautifulSoup
import csv
import re
import requests
import string

comune_base_url = "https://it.wikipedia.org/wiki/Comuni_d%27Italia_"
base_url = comune_base_url[:24]
letters = list(string.ascii_uppercase)
letters[7:8] = ""
letters[7] = "H-I" #H and I do not have independent pages

def table_scrape(input_table):
    '''searches table within page'''
    if input_table:
        rows = [row for row in input_table.find_all('tr') if row]
        anchors = [a for a in (row.find_all('a') for row in rows) if a]
        for anchor in anchors:
            comune_name = anchor[0]['href']
            comune_markup = requests.get(base_url + comune_name)
            comune_data = comune_markup.text
            comune_soup = BeautifulSoup(comune_data, from_encoding='utf-8')
            demonym_title = comune_soup.find('a', text=re.compile("Nome.abitanti"))
            istat = comune_soup.find('th', text=re.compile("Fuso.orario"))
            try:
                istat_num = istat.parent.findNextSibling('tr').find('th').findNextSibling('td').text
            except AttributeError:
                istat_num == "Not listed"
            if demonym_title:
                demonym = demonym_title.parent.findNextSibling('td').text
            else:
                demonym = "non esiste"
            try:
                regione = anchor[2].text
                provincia = anchor[1].text
                comune = anchor[0].text
            except IndexError:
                anchor.append(anchor[1])
                regione = anchor[2].text
                provincia = ""
                comune = anchor[0].text
            writer.writerow({'regione':regione, 'provincia':provincia, 'ISTAT':istat_num, 'comune':comune, 'demonym':demonym})
    else:
        pass


with open("italia2.csv", 'w', newline='', encoding='utf-8') as f:
    field_names = ["regione", "provincia", "ISTAT", "comune", "demonym"]
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writeheader()
    for letter in letters:
        comune_list_markup = requests.get(comune_base_url + "(" + letter + ")")
        list_data = comune_list_markup.text
        soup = BeautifulSoup(list_data)
        comune_table = soup.find('table', {'class':'wikitable plainlinks'})
        if letter == "H-I":
            comune_tables = soup.find_all('table', {'class':'wikitable plainlinks'})
            for comune_table in comune_tables:
                table_scrape(comune_table)
        else:
            comune_table = soup.find('table', {'class':'wikitable plainlinks'})
            table_scrape(comune_table)          