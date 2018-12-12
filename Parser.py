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
    filename = "7612631031 - RE_ XFB on PRD for CI_MODEL.html"
    if not os.path.isfile(filename):  ##sprawdzenie czy plik jest w OS-ie
        print('----------------------------------------------------------\n'
              '-- [ ERROR ] {} - file not found!\n'
              '----------------------------------------------------------\n'
              .format(filename))
        sys.exit()
    # , encoding = 'UTF-8-SIG'
    with open(filename, 'rt') as input_file:
        soup = BeautifulSoup(input_file, 'html.parser')

        t = Track(soup)
        t.printAll()

        exit()

















        test(soup)
        print(soup.prettify())
        x = soup.find_all("p")

        i = 0
        # for sibling in x.next_siblings:
        #     print sibling
        # for sibling in x[10].next_siblings:
        #     print(repr(sibling))

        while i < len(x):
            print "i: " + str(i)
            # print x[i]
            y = x[i].next_siblings
            # print "siblings: " + repr(y)
            sibling = x[i]
            while sibling is not None:
                if sibling.text is not "\s":
                    print(sibling.text)
                sibling = sibling.next_sibling
                sibling = sibling.next_sibling
                i = i+1

            print "===================================="





        # print x.next_elements()
        # for el in x.next_elements():
        #     if el.div is not None:
        #         break
        #     else:
        #         print el
        # x = soup.p
        # for sibling in soup.find("p").next_elements:
        #     print(str(sibling))
        # print "sib1: " + soup.p.next_sibling.text
        # print "sib1: " + soup.p.next_sibling.text
        # # print "sib2: " + soup.next_sibling
        # for element in x:
        #     print element.next_sibling.text
        #     if element.tbody.tr.td.text == "Customer":
        #         print element.tbody.find("td", class_="rolePersonName").text


        # for textSet in soup.p:
        #     y = soup.textSet("p")
        #     print y.string
        #     for sibling in y.next_siblings:
        #         print(sibling.text)

        # y = soup.textSet("p")
        # for sibling in soup.find("p").next_siblings:
        #     print(sibling.text)
        # for x, y in zip(x, x):
        #     print x.contents[0].td.contents[0]

        # t = Track(soup)
        #
        # print (t.printAll())

        # x = soup.find_all("div", class_="pageData")
        # for el in x:
        #     print el.text
        #     print x.find(re.compile("[SAS_status: (w+)]"))


def test(soup):
    x = soup.find_all("div", class_="pageData")
    for el in x:
        print "==================================="
        tag = el.find_all("p")
        for tag2 in tag:
            print tag2.text

#TODO zrobic eksport do pliku excel lub innego
main()
