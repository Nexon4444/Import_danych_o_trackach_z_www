# import httplib2 as httplib2

import sys
import os.path
import requests
from Track_classes import Track, CSVexporter, CSVimporter
from pathlib import Path
# import pandas as pd
import re
from bs4 import BeautifulSoup
# from bs4 import BeautifulSoup
# TODO zrobic import bezposrednio ze strony. UWAGA: Problem z dostepem ze wzgledu na weryfikacje tozsamosci ("Unauthorized: Access is denied due to invalid credentials.")
from requests.auth import HTTPBasicAuth

# 7612650640;21NOV2018:04:02:54.217
# 7612631031;10AUG2018:08:11:50.553
# http://sirius.na.sas.com/Sirius/ShowTrack.aspx?trknum=7612650640
# resp = requests.get('https://sirius.na.sas.com/Sirius/ShowTrack.aspx?trknum=7612631031', auth=HTTPBasicAuth('maciej.kutrowski@sas.com', 'Xenobiot2357!'))
# html = resp.text
# soup = BeautifulSoup(html, features="html.parser")
#
# print soup.prettify()
# exit()
# regex_dict = dict()
# def compile_regex():
#     regex_dict['trknum_in_title'] = re.compile('(?<=\n\t)(\d+)')

#arguments [username] [password] [output_file] [web_adress1] <optional> [web_adress2] [web_address3]....
import pandas as pd

# trknum;CreateDate
# 7612585749;15OCT2018:13:26:25.163
# 7612622537;24NOV2018:04:17:21.320
# 7612655686;08JAN2019:17:33:51.737
# 7611959153;17NOV2016:15:42:48.370
# 7612621558;22NOV2018:08:24:36.430
# 7612589797;18OCT2018:15:34:33.783
# 7612591819;22OCT2018:06:42:01.083
# 7612623884;26NOV2018:20:22:51.127
# 7612642127;16DEC2018:02:00:36.457
# 7612587777;16OCT2018:23:15:54.037
# 7612603246;01NOV2018:18:38:44.487
# 7612633884;06DEC2018:09:31:19.220
# 7612580165;09OCT2018:09:51:48.817

# data = pd.read_csv (r'TRACKNUMS_EXTRACTED.csv', delimiter=';')
# print (data['trknum'].values[0])
# df = pd.DataFrame(data)
# df.
print "================================================================================================================"
print "                                             Executing Parser.exe"
print "================================================================================================================"
print "For user: " + sys.argv[1]
print "Password: " + "**********"
track_file = Path(sys.argv[3])
output_file = Path(sys.argv[4])
print "track_file= " + str(track_file)
print "output_file= " + str(output_file)
# print df.l
# print df.get_value(3, r'trknum')
# df = pd.DataFrame(data, columns= ['trknum','CreateDate'])

def main():
    if len(sys.argv) < 3:
        if (sys.argv[1] == "-h"):
            print "usage: [username] [password] [track_file] [output_file]"
        else:
            raise (Exception("not enough arguments"))

    importer = CSVimporter(sys.argv[1], sys.argv[2], track_file)
    exporter = CSVexporter(output_file)

    i = 0
    while importer.last_pair != None :
        print ("analyzing track: " + str(i))
        print importer.last_pair[1]
        t = Track(importer.last_pair[0], importer.last_pair[1])
        exporter.append(t)
        importer.next_pair()
        i = i + 1
    print "exporting to file: " + str(output_file)
    exporter.extract_to_csv()

if __name__ == "__main__":
    main()
