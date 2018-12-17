import re
import itertools

regex_dict = dict()
# dziedziczenie po klasie "object" po to zeby dzialaly properties


class Track(object):
    def __init__(self, soup):
        self.compile_regex()

        self.trknum = soup
        self.title = soup
        self.priority = soup
        self.custName = soup
        self.custCompany = soup
        self.primOwnName = soup
        self.primOwnCompany = soup
        self.pageInfoList = soup
        self.SNOW_INC = soup
        self.SNOW_REF_MSG = soup

        self.SNOW_ITASK = soup

    @property
    def trknum(self):
        return self._trknum

    @trknum.setter
    def trknum(self, soup):
        self._trknum = re.search(regex_dict['trknum_in_title'], soup.find("title").text).group(1)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, soup):
        self._title = soup.title.text

    @property
    def custName(self):
        return self._custName

    @custName.setter
    def custName(self, soup):
        for tag in soup.find_all("table", class_="roleDetails"):
                if tag.find("td", class_="roleType").text == "Customer":
                    self._custName = tag.find("td", class_="rolePersonName").text
                    return
        self._custName = None

    @property
    def custCompany(self):
        return self._custCompany

    @custCompany.setter
    def custCompany(self, soup):
        for tag in soup.find_all("table", class_="roleDetails"):
                if tag.find("td", class_="roleType").text == "Customer":
                    self._custCompany = tag.find("td", class_="roleCompanyName").text
                    return
        self._custCompany = None

    @property
    def primOwnName(self):
        return self._primOwnName

    @primOwnName.setter
    def primOwnName(self, soup):
        for tag in soup.find_all("table", class_="roleDetails"):
            if tag.find("td", class_="roleType").text == "Primary Owner":
                self._primOwnName = tag.find("td", class_="rolePersonName").text
                return
        self._primOwnName = None

    @property
    def primOwnCompany(self):
        return self._primOwnCompany

    @primOwnCompany.setter
    def primOwnCompany(self, soup):
        for tag in soup.find_all("table", class_="roleDetails"):
            if tag.find("td", class_="roleType").text == "Primary Owner":
                self._primOwnCompany = tag.find("td", class_="roleCompanyName").text
                return
        self._primOwnCompany = None

    @property
    def pageInfoList(self):
        return self._pageInfoList

    @pageInfoList.setter
    def pageInfoList(self, soup):
        aux = list()

        pretexts = soup.find_all("table", class_="pretext")
        pageHeads = soup.find_all("table", class_="pageHead")
        pageDatas = soup.find_all("div", class_="pageData")

        # for tag_pretext, tag_pageHead, tag_pageData in zip(pretexts, pageHeads, pageDatas):
        #     aux.append(Update(tag_pretext, tag_pageHead, tag_pageData))

        for tag_pageHead, tag_pageData in zip(pageHeads, pageDatas):
            aux.append(Update(tag_pageHead, tag_pageData))
        self._pageInfoList = aux

    @property
    def SNOW_REF_MSG(self):
        return self._SNOW_REF_MSG

    @SNOW_REF_MSG.setter
    def SNOW_REF_MSG(self, soup):
        found = re.search(regex_dict['SNOW_REF_MSG_in_title'], soup.find("title").text)
        if found is not None:
            self._SNOW_REF_MSG = found.group(1).decode('UTF-8')
        else:
            self._SNOW_REF_MSG = None

    @property
    def SNOW_INC(self):
        return self._SNOW_INC

    @SNOW_INC.setter
    def SNOW_INC(self, soup):
        found = re.search(regex_dict['SNOW_INC_in_title'], soup.find("title").text)
        if found is not None:
            self._SNOW_INC = found.group(1)
        else:
            self._SNOW_INC = None

    @property
    def SNOW_ITASK(self):
        return self._SNOW_ITASK

    @SNOW_ITASK.setter
    def SNOW_ITASK(self, soup):
        found = re.search(regex_dict['SNOW_ITASK_in_title'], soup.find("title").text)
        if found is not None:
            self._SNOW_ITASK = found.group(1)
        else:
            self._SNOW_ITASK = None

    def compile_regex(self):
        regex_dict['trknum_in_title'] = re.compile('(?<=\n\t)(\d+)')

        regex_dict['SNOW_INC_in_title'] = re.compile('(?<=INC)(\d+)')
        regex_dict['SNOW_ITASK_in_title'] = re.compile('(?<=ITASK)(\d+)')
        regex_dict['SNOW_REF_MSG_in_title'] = re.compile('(?<=MSG)(\d+)')

        regex_dict['SAS-status'] = re.compile('(?<=SAS-status:\s)(.*)(?=\])')
        regex_dict['SAS-sub_status'] = re.compile('(?<=SAS-sub_status:\s)(.*)(?=\])')
        regex_dict['SAS-component'] = re.compile('(?<=SAS-component:\s)(.*)(?=\])')
        regex_dict['SAS-environment'] = re.compile('(?<=SAS-environment:\s)(.*)(?=\])')
        regex_dict['SAS-pool'] = re.compile('(?<=SAS-pool:\s)(.*)(?=\])')
        regex_dict['SAS-comment'] = re.compile('(?<=SAS-comment:\s)(.*)(?=\])')
        regex_dict['SAS-assigned_to'] = re.compile('(?<=SAS-assigned_to:\s)(.*)(?=\])')
        regex_dict['SAS-priority'] = re.compile('(?<=SAS-priority:\s)(.*)(?=\])')
        regex_dict['SAS-classification'] = re.compile('(?<=SAS-classification:\s)(.*)(?=\])')
        regex_dict['SAS-sub_classification'] = re.compile('(?<=SAS-sub_classification:\s)(.*)(?=\])')
        regex_dict['SAS-severity'] = re.compile('(?<=SAS-severity:\s)(.*)(?=\])')
        regex_dict['SAS-impact_range'] = re.compile('(?<=SAS-impact_range:\s)(.*)(?=\])')

    def printAll(self):
        print "-------- Track Info --------"
        print "trknum: " + str(self.trknum)
        print "title: " + str(self.title)
        print "SNOW_INC: " + str(self.SNOW_INC)
        print "SNOW_ITASK: " + str(self.SNOW_ITASK)
        print "SNOW_REF_MSG: " + str(self.SNOW_REF_MSG)

        print "custName: " + str(self.custName)
        print "custCompany: " + str(self.custCompany)

        print "primOwnName: " + str(self.primOwnName)
        print "primOwnCompany: " + str(self.primOwnCompany)
        print "-------- Track Info -------- \n\n"

        for updt in self.pageInfoList:
            updt.printAll()
    # def extractCreateDate(self, soup):
    # def extractUpdates(self, soup):

    # property(trknum)

class Update(object):
    # def __init__(self, tag_pretext, tag_pageHead, tag_pageData):
    def __init__(self, tag_pageHead, tag_pageData):
        # self.tag_pretext = tag_pretext
        self.tag_pageHead = tag_pageHead
        self.tag_pageData = tag_pageData

        self.page_number = tag_pageHead
        self.modifiedBy = tag_pageHead
        self.lstPgUpdated = tag_pageHead
        # self.sender = tag_pretext
        # self.Kolumna1 = None

        self.pageData = tag_pageData
        self.SAS_status = tag_pageData
        self.SAS_sub_status = tag_pageData
        self.SAS_component = tag_pageData
        self.SAS_environment = tag_pageData
        self.SAS_pool = tag_pageData
        self.SAS_comment = tag_pageData
        self.SAS_assigned_to = tag_pageData
        self.SAS_priority = tag_pageData
        self.SAS_classification = tag_pageData
        self.SAS_sub_classification = tag_pageData
        self.SAS_severity = tag_pageData
        self.SAS_impact_range = tag_pageData

        self.Area = None

        self.page_text = None
        # self._PowerAppsId__ = None
        self.without_response = None

        self.SAS_tags = [self.SAS_status,
                         self.SAS_sub_status,
                         self.SAS_component,
                         self.SAS_environment,
                         self.SAS_pool,
                         self.SAS_comment,
                         self.SAS_assigned_to,
                         self.SAS_priority,
                         self.SAS_classification,
                         self.SAS_sub_classification,
                         self.SAS_severity,
                         self.SAS_impact_range]

        writer = pd.ExcelWriter('example.xlsx', engine='xlsxwriter')
    @property
    def tag_pretext(self):
        return self._tag_pretext

    @tag_pretext.setter
    def tag_pretext(self, tag_pretext):
        self._tag_pretext = tag_pretext

    @property
    def tag_pageHead(self):
        return self._tag_pageHead

    @tag_pageHead.setter
    def tag_pageHead(self, tag_pageHead):
        self._tag_pageHead = tag_pageHead

    @property
    def tag_pageData(self):
        return self._tag_pageData

    @tag_pageData.setter
    def tag_pageData(self, pageData):
        self._pageData = pageData

    @property
    def page_number(self):
        return self._page_number

    @page_number.setter
    def page_number(self, tag_pageHead):
        # print (soup.find("td", class_="pageHeadCellAlpha").string)
        found = tag_pageHead.find("td", class_="pageHeadCellAlpha")
        if found is None:
            raise ValueError("page_number not found")
        self._page_number = found.string

    @property
    def pageData(self):
        return self._pageData

    @pageData.setter
    def pageData(self, pageData):
        self._pageData = pageData.find_all("p")

    @property
    def modifiedBy(self):
        return self._modifiedBy

    @modifiedBy.setter
    def modifiedBy(self, tag_pageHead):
        found = tag_pageHead.find("td", class_="pageHeadCellGamma")
        if found is None:
            raise ValueError("modifiedBy not found")
        self._modifiedBy = tag_pageHead.find("td", class_="pageHeadCellGamma").text

    @property
    def lstPgUpdated(self):
        return self._lstPgUpdated

    @lstPgUpdated.setter
    def lstPgUpdated(self, tag_pageHead):
        self._lstPgUpdated = tag_pageHead.find("td", class_="pageHeadCellBeta").text

    @property
    def sender(self):
        return self._sender

    @sender.setter
    def sender(self, tag_pretext):
        found = tag_pretext.find("tr")
        if found is None:
            return None
        self._sender = found.string

    @property
    def SAS_status(self):
        return self._SAS_status

    @SAS_status.setter
    def SAS_status(self, tag_pageData):
        self._SAS_status = self.get_reg_tag("span", tag_pageData, "SAS-status")

    @property
    def SAS_sub_status(self):
        return self._SAS_sub_status

    @SAS_sub_status.setter
    def SAS_sub_status(self, tag_pageData):
        self._SAS_sub_status = self.get_reg_tag("span", tag_pageData, "SAS-sub_status")

    @property
    def SAS_component(self):
        return self._SAS_component

    @SAS_component.setter
    def SAS_component(self, tag_pageData):
        self._SAS_component = self.get_reg_tag("span", tag_pageData, "SAS-component")

    @property
    def SAS_environment(self):
        return self._SAS_environment

    @SAS_environment.setter
    def SAS_environment(self, tag_pageData):
        self._SAS_environment = self.get_reg_tag("span", tag_pageData, "SAS-environment")

    @property
    def SAS_pool(self):
        return self._SAS_pool

    @SAS_pool.setter
    def SAS_pool(self, tag_pageData):
        self._SAS_pool = self.get_reg_tag("span", tag_pageData, "SAS-pool")

    @property
    def SAS_comment(self):
        return self._SAS_comment

    @SAS_comment.setter
    def SAS_comment(self, tag_pageData):
        self._SAS_comment = self.get_reg_tag("span", tag_pageData, "SAS-comment")

    @property
    def SAS_assigned_to(self):
        return self._SAS_assigned_to

    @SAS_assigned_to.setter
    def SAS_assigned_to(self, tag_pageData):
        self._SAS_assigned_to = self.get_reg_tag("span", tag_pageData, "SAS-assigned_to")

    @property
    def SAS_priority(self):
        return self._SAS_priority

    @SAS_priority.setter
    def SAS_priority(self, tag_pageData):
        self._SAS_priority = self.get_reg_tag("span", tag_pageData, "SAS-priority")

    @property
    def SAS_classification(self):
        return self._SAS_classification

    @SAS_classification.setter
    def SAS_classification(self, tag_pageData):
        self._SAS_classification = self.get_reg_tag("span", tag_pageData, "SAS-classification")

    @property
    def SAS_sub_classification(self):
        return self._SAS_sub_classification

    @SAS_sub_classification.setter
    def SAS_sub_classification(self, tag_pageData):
        self._SAS_sub_classification = self.get_reg_tag("span", tag_pageData, "SAS-sub_classification")

    @property
    def SAS_severity(self):
        return self._SAS_severity

    @SAS_severity.setter
    def SAS_severity(self, tag_pageData):
        self._SAS_severity = self.get_reg_tag("span", tag_pageData, "SAS-severity")

    @property
    def SAS_impact_range(self):
        return self._SAS_impact_range

    @SAS_impact_range.setter
    def SAS_impact_range(self, tag_pageData):
        self._SAS_impact_range = self.get_reg_tag("span", tag_pageData, "SAS-impact_range")

    def get_reg_tag(self, tag, tag_pageData, regex_dict_key):
        for line in tag_pageData.find_all(tag):
            if line is None or line.string is None:
                continue
            found = re.search(regex_dict[regex_dict_key], line.string)
            if found is not None:
                return found.group(1)
        return None

    def printAll(self):
        print "-------- Page Info --------"
        # print "page_number: " + str(self.page_number) + "\nmodifiedBy: " + str(self.modifiedBy) + "\nlstPgUpdated: " + str(self.lstPgUpdated) + "\nsender: " + str(self.sender)
        print "page_number: " + str(self.page_number) + "\nmodifiedBy: " + str(self.modifiedBy) + "\nlstPgUpdated: " + str(self.lstPgUpdated)
        for sas_tag in self.SAS_tags:
            if sas_tag is not None:
                print str(sas_tag)
        print "-------- Page Info --------\n"




# def modifiedBy(self, tag_pageHead):
#     found = tag_pageHead.find("td", class_="pageHeadCellGamma")
#     return tag_pageHead.find("td", class_="pageHeadCellGamma").string