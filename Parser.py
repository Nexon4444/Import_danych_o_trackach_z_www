import sys
from Track_classes import Track, CSVexporter, CSVimporter
from pathlib import Path


print "================================================================================================================"
print "                                             Executing Parser.exe"
print "================================================================================================================"
print "For user: " + sys.argv[1]
print "Password: " + "**********"
track_file = Path(sys.argv[3])
output_file = Path(sys.argv[4])
print "track_file= " + str(track_file)
print "output_file= " + str(output_file)
# print  "sep = " + chr(36)
# 7612621575;22NOV2018:08:42:31.850
# 7612625131;27NOV2018:18:32:42.150
# 7612655686;08JAN2019:17:33:51.737
def main():
    if len(sys.argv) < 3:
        if (sys.argv[1] == "-h"):
            print "usage: [username] [password] [track_file] [output_file] [separator]"
            exit(0)
        else:
            raise (Exception("not enough arguments"))

    importer = CSVimporter(sys.argv[1], sys.argv[2], sys.argv[3])
    exporter = CSVexporter(sys.argv[4], "`")

    i = 1
    # print i[0]
    while importer.last_pair != None :
        print ("analyzing track: " + str(i))
        # print "pair: <" + str(importer.last_pair[0]) + ", " + str(importer.last_pair[1]) + ">"
        t = Track(importer.last_pair[0], importer.last_pair[1])
        exporter.append(t)
        importer.next_pair()
        i = i + 1
        # print "t: " + str(t['trknum'])
    print "exporting to file: " + str(output_file)
    exporter.extract_to_csv()

if __name__ == "__main__":
    main()

# logf = open("error.log", "w")
# try:
#     if __name__ == "__main__":
#         main()
# except Exception as e:
#     print str(e)
#     logf.write("Failed because of error:\n" + (str(e)))
