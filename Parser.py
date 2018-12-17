import httplib2 as httplib2
from bs4 import BeautifulSoup
import sys
import os.path
import requests
import re

from bs4 import BeautifulSoup
# TODO zrobic import bezposrednio ze strony. UWAGA: Problem z dostepem ze wzgledu na weryfikacje tozsamosci ("Unauthorized: Access is denied due to invalid credentials.")
# resp = requests.get('https://sirius.na.sas.com/Sirius/ShowTrack.aspx?trknum=7612631031')
# html = resp.text
# soup = BeautifulSoup(html, features="html.parser")
from Track_classes import Track

# regex_dict = dict()
# def compile_regex():
#     regex_dict['trknum_in_title'] = re.compile('(?<=\n\t)(\d+)')
def main():
    #filename = sys.argv[1]
    filename = "7612624515 - INC0642766 _ ITASK0017256 P1 Incident.html"
    if not os.path.isfile(filename):  ##sprawdzenie czy plik jest w OS-ie
        print('----------------------------------------------------------\n'
              '-- [ ERROR ] {} - file not found!\n'
              '----------------------------------------------------------\n'
              .format(filename))
        sys.exit()
    # , encoding = 'UTF-8-SIG'
    with open(filename, 'rt') as input_file:
        soup = BeautifulSoup(input_file, 'html.parser')
        print None
        # print soup.prettify()
        # print soup.title.text
        # print soup.tbody
        # print soup.find("td", class_="rolePersonName").text
        # x = soup.prettify()
        # print "easyfind: " + soup.find("table", class_="roleDetails").find("td", class_="roleType").text
        # for tag in soup.find_all("table", class_="roleDetails"):
        #         if tag.find("td", class_="roleType").text == "Customer":
        #             print tag.find("td", class_="rolePersonName").text
        #
        # for tag in soup.find_all("table", class_="roleDetails"):
        #         print tag.text
        #         # print tag.find("td", class_="roleType").text
        # exit()
        t = Track(soup)
        t.printAll()

        # test(soup)
        # print(soup.prettify())
        # x = soup.find_all("p")

def test(soup):
    x = soup.find_all("div", class_="pageData")
    for el in x:
        print "==================================="
        tag = el.find_all("p")
        for tag2 in tag:
            print tag2.text

#TODO zrobic eksport do pliku excel lub innego
main()
