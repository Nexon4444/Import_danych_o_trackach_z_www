import re
import itertools

regex_dict = dict()


def compile_regex():
    regex_dict['trknum_in_title'] = re.compile('(?<=\n\t)(\d+)')
    regex_dict['SAS_status'] = re.compile('(?<=SAS-status:\s)(.*)(?=\])')

class Track:
    def __init__(self, soup):
        self.trknum = self.extractTrknum(soup)

        # self.CreateDate = self.extractTrk()
        self.updateList = self.extractPageInfo(soup)
        self.CustName = self.extractCustName(soup)
        self.CustCompany = self.extractCustCompany(soup)
        return None

    def extractTrknum(self, soup):
        return re.search(regex_dict['trknum_in_title'], soup.find("title").text).group(1)

    def extractPageInfo(self, soup):
        aux = list()
        pretexts = soup("table", class_="pretext")
        pageHeads = soup("table", class_="pageHead")
        pageDatas = soup.find_all("div", class_="pageData")
        for tag_pretext, tag_pageHead in zip(pretexts, pageHeads):
            print "preText:\n" + tag_pretext.text + "pageHead:\n" + tag_pageHead.text


        # print tag1.find(border).get_text()
        # for i in range(len(tag1)):
        #     # print
        #     aux.append(tag1[i] + tag2[i])
        #
        for tag_pretext, tag_pageHead, tag_pageData in zip(pretexts, pageHeads, pageDatas):
            # print ("tag:" + tag.text)
            # print "tag: " + tag.text
            # print "tag2: " + tag/2.text
            aux.append(Update(tag_pretext, tag_pageHead, tag_pageData))
        return aux

    def extractCustName(self, soup):
        for element in soup:
            # print element.tbody.text
            if element.tbody.tr.td.text == "Customer":
                return element.tbody.find("td", class_="rolePersonName").text

    def extractCustCompany(self, soup):
        for element in soup:
            # print element.tbody.text
            if element.tbody.tr.td.text == "Customer":
                return element.tbody.find("td", class_="roleCompanyName").text

    def printAll(self):
        print self.trknum
        for updt in self.updateList:
            updt.printAll()
    # def extractCreateDate(self, soup):
    # def extractUpdates(self, soup):


class Update:
    def __init__(self, tag_pretext, tag_pageHead, tag_pageData):
        self._tag_pretext = tag_pretext
        self._tag_pageHead = tag_pageHead
        self._tag_pageData = tag_pageData

        self._page_number = tag_pageHead
        self._modifiedBy = self.extractModifiedBy(tag_pageHead)
        self._lstPgUpdated = self.extractLstPgUpdt(tag_pageHead)
        self._sender = self.extractSender(tag_pretext)
        self._Kolumna1 = None

        self._pageData = self.extractPageData(tag_pageData)
        self.Title = None
        self.Area = None
        self.Priority = None
        self.SNOW_REF_MSG = None
        self.SNOW_INC = None
        self.SNOW_ITASK = None
        self.SAS_status = None
        self.SAS_sub_status = None
        self.SAS_component = None
        self.SAS_environment = None
        self.SAS_pool = None
        self.SAS_comment = None
        self.SAS_assigned_to = None
        self.SAS_priority = None
        self.SAS_classification = None
        self.SAS_sub_classification = None
        self.SAS_severity = None
        self.SAS_impact = None
        self.page_text = None
        self.__PowerAppsId__ = None
        self.without_response = None

    @property
    def tag_pretext(self):
        return self._pretext

    @tag_pretext.setter
    def tag_pretext(self, value):
        self._tag_pretext = value

    @property
    def tag_pageHead(self):
        return self._tag_pageHead

    @tag_pageHead.setter
    def tag_pageHead(self, value):
        self._tag_pageHead = value

    @property
    def tag_pageData(self):
        return self._tag_pageData

    @tag_pageData
    def tag_pageData(self, value):
        self._pageData = value

    @property
    def tag_page_number(self):
        return self._page_number

    @tag_page_number.setter
    def tag_page_number(self, tag_pageHead):
        # print (soup.find("td", class_="pageHeadCellAlpha").string)
        found = tag_pageHead.find("td", class_="pageHeadCellAlpha")
        if found is None:
            raise ValueError("page_number not found")
        self._page_number = found.string

    @property
    def pageData(self):
        return self._pageData

    @pageData.setter
    def pageData(self, value):
        self._pageData = value.find_all("p")

    @property
    def modifiedBy(self, tag_pageHead):
        found = tag_pageHead.find("td", class_="pageHeadCellGamma")
        if found is None:
            raise ValueError("page_number not found")
        self._tag_pageHead = found.string

    @modifiedBy.setter
    def modified(self, value):
        found = value.find("td", class_="pageHeadCellGamma")
        if found is None:
            raise ValueError("page_number not found")
        self._tag_pageHead = found.string
        return found.string

    @property
    def extractLstPgUpdt(self, tag_pageHead):
        return tag_pageHead.find("td", class_="pageHeadCellBeta").string

    @property
    def extractSender(self, tag_pretext):
        return tag_pretext.find("tr").string

    @property
    def extractSAS_status(self):
        for line in self._pageData:
            found = re.search(regex_dict['SAS-status'], line)
            if (found is not None):
                return found.group(2)

    _page_number = property.setter(extractPageData)
    _modifiedBy = property.setter(extractModifiedBy)
    _lstPgUpdated = property.setter(extractLstPgUpdt)
    _sender = property.setter(extractSender)
    _pageData = property.setter(extractPageData)




    # def extractSas_status(self, tag_pageData):
    #     return tag_pageData.find(re.compile("[SAS_status: (w+) ]"))



    def printAll(self):
        print "page_number: " + repr(self._page_number) + "\nmodifiedBy: " + repr(self._modifiedBy) + "\nlstPgUpdated: " + repr(self._lstPgUpdated) + "\nsender: " + repr(self._sender)



compile_regex()
