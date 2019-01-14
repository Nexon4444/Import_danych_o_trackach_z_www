import inspect
import re
import requests
from requests.auth import HTTPBasicAuth
from bs4 import BeautifulSoup
import itertools
import xlwt
from tempfile import TemporaryFile

import pandas as pd

regex_dict = dict()


def create_raw_data(SAS_status_list=list(), SAS_assigned_to_list=list(), SAS_classification_list=list(), SAS_comment_list=list(), SAS_component_list=list(),
                    SAS_environment_list=list(), SAS_impact_range_list=list(), SAS_pool_list=list(), SAS_priority_list=list(),
                    SAS_severity_list=list(), SAS_sub_classification_list=list(), SAS_sub_status_list=list(), SNOW_INC_list=list(),
                    SNOW_ITASK_list=list(), SNOW_REF_MSG_list=list(), custCompany_list=list(), custName_list=list(), lstPgUpdated_list=list(),
                    modifiedBy_list=list(), page_number_list=list(), page_text_list=list(), primOwnCompany_list=list(), primOwnName_list=list(),
                    priority_list=list(), title_list=list(), trknum_list=list(), createDate_list=list()):

    # if not is_contents_set:
    #     page_number_list = list()
    #     modifiedBy_list = list()
    #     lstPgUpdated_list = list()
    #     SAS_status_list = list()
    #     SAS_sub_status_list = list()
    #     SAS_component_list = list()
    #     SAS_environment_list = list()
    #     SAS_pool_list = list()
    #     SAS_comment_list = list()
    #     SAS_assigned_to_list = list()
    #     SAS_priority_list = list()
    #     SAS_classification_list = list()
    #     SAS_sub_classification_list = list()
    #     SAS_severity_list = list()
    #     SAS_impact_range_list = list()
    #     page_text_list = list()

    raw_data = {'SAS_status': SAS_status_list,
                'SAS_sub_status': SAS_sub_status_list,
                'SAS_component': SAS_component_list,
                'SAS_environment': SAS_environment_list,
                'SAS_pool': SAS_pool_list,
                'SAS_comment': SAS_comment_list,
                'SAS_assigned_to': SAS_assigned_to_list,
                'SAS_priority': SAS_priority_list,
                'SAS_classification': SAS_classification_list,
                'SAS_sub_classification': SAS_sub_classification_list,
                'SAS_severity': SAS_severity_list,
                'SAS_impact_range': SAS_impact_range_list,

                'page_text': page_text_list,
                'title': title_list,
                'priority': priority_list,
                'custName': custName_list,
                'custCompany': custCompany_list,
                'primOwnName': primOwnName_list,
                'primOwnCompany': primOwnCompany_list,
                'SNOW_ITASK': SNOW_ITASK_list,
                'SNOW_INC': SNOW_INC_list,
                'SNOW_REF_MSG': SNOW_REF_MSG_list,
                'page_number': page_number_list,
                'modifiedBy': modifiedBy_list,
                'lstPgUpdated': lstPgUpdated_list,
                'trknum': trknum_list,
                'createDate': createDate_list}
    return raw_data


# dziedziczenie po klasie "object" po to zeby dzialaly properties
class CSVimporter(object):
    def __init__(self, login, passwd, import_file):
        self.login = login
        self.passwd = passwd
        self.import_file = import_file
        self.imported_data_frame = import_file
    
        self.imported_val_arr = self.imported_data_frame.values
        self.www_adresses = self.imported_val_arr
        self._last_poz = 0
        self.createDates = self.imported_val_arr
        self.last_pair = self.next_pair()
        # self.last_soup = self.import_next(self._last_poz)
        # self.last_createDate = self.next_soup(self._last_poz)
        # self.soups = self.www_adresses

    
    @property
    def login(self):
        return self._login
    
    @login.setter
    def login(self, value):
        self._login = value
        
    @property
    def passwd(self):
        raise Exception("can't return password!!!")
    
    @passwd.setter
    def passwd(self, value):
        self._passwd = value

    @property
    def import_file(self):
        return self._import_file

    @import_file.setter
    def import_file(self, value):
        self._import_file = value

    @property
    def imported_data_frame(self):
        return self._imported_data_frame

    @imported_data_frame.setter
    def imported_data_frame(self, value):

        data = pd.read_csv(value, delimiter=';')
        self._imported_data_frame = pd.DataFrame(data)

    @property
    def last_pair(self):
        return self._last_pair

    @last_pair.setter
    def last_pair(self, value):
        self._last_pair = value

    def next_pair(self):
        if self._last_poz == len(self.imported_val_arr):
            self.last_pair = None
            return self.last_pair

        self.last_pair = (self.create_soup(self.www_adresses[self._last_poz]), self.imported_val_arr[self._last_poz][1])
        self._last_poz = self._last_poz + 1
        return self.last_pair
    # @property
    # def soups(self):
    #     return self._soups
    #
    # @soups.setter
    # def soups(self, value):
    #     self._soups = list()
    #     for row in value:
    #         self._soups.append(row)


    @property
    def imported_val_arr(self):
        return self._imported_val_arr

    @imported_val_arr.setter
    def imported_val_arr(self, value):
        self._imported_val_arr = value

    @property
    def last_soup(self):
        return self._last_soup

    @last_soup.setter
    def last_soup(self, value):
        self._last_soup = value

    @property
    def last_createDate(self):
        return self._createDate

    @last_createDate.setter
    def last_createDate(self, value):
        self._createDate = value

    @property
    def www_adresses(self):
        return self._www_adresses
    
    @www_adresses.setter
    def www_adresses(self, value):
        self._www_adresses = list()
        for pair in self.imported_val_arr:
            self._www_adresses.append("https://sirius.na.sas.com/Sirius/ShowTrack.aspx?trknum="+str(pair[0]))
    # @property
    # def soups(self):
    #     return self._soups
    #
    # @soups.setter
    # def soups(self, value):
    #     self._soups = list()
    #     for adr in self.www_adresses:
    #         self._soups.append(self.create_soup(adr))

    @property
    def createDates(self):
        return self._createDates

    @createDates.setter
    def createDates(self, value):
        self._createDates = list()
        for val in value:
            self._createDates.append(val[1])


    def create_soup(self, adr):
        print ("requesting webpage: " + adr)
        resp = requests.get(adr, auth=HTTPBasicAuth(self.login, self._passwd))
        return BeautifulSoup(resp.text, features="html.parser")
    #
    # def get_all_soups(self):



class CSVexporter(object):
    def __init__(self, name, track=None):
        self.contents_flag = False
        self.name = name
        # if track is None:
        self.raw_data = create_raw_data()

        # else:
        #     self.raw_data = track.raw_data
    @property
    def contents_flag(self):
        return self._contents_flag

    @contents_flag.setter
    def contents_flag(self, value):
        self._contents_flag = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def raw_data(self):
        return self._raw_data

    @raw_data.setter
    def raw_data(self, raw_data_cp):
        self._raw_data = raw_data_cp

    def append(self, track):
        # if not self.raw_data:
        self._merge_2dicts_of_lists(self.raw_data, track.raw_data)
        # else:
        #     self.raw_data = track.raw_data

    def _merge_2dicts_of_lists(self, dict1, dict2):
        merged = dict1
        for key, value in merged.iteritems():
            value.extend(dict2[key])
        return merged

    def extract_to_csv(self):
        df = pd.DataFrame(self.raw_data)
        df.to_csv(str(self.name), index=False, sep=";", encoding="UTF-8")
        # df.to_csv(self.name.encode('utf-8'), index=False)

class Track(object):
    def __init__(self, soup, createDate):
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
        self.SNOW_ITASK = soup
        self.SNOW_REF_MSG = soup
        self.createDate = createDate

        self._column_names = ['trknum',
                              'title',
                              'priority',
                              'custName',
                              'custCompany',
                              'primOwnName',
                              'primOwnCompany',
                              'SNOW_ITASK',
                              'SNOW_INC',
                              'SNOW_REF_MSG']

        self.raw_data = self.prepare_raw_data()



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
        self._title = soup.title.text.strip()

    @property
    def priority(self):
        return self._priority

    @priority.setter
    def priority(self, soup):
        aux = soup.find('td', text=re.compile('Priority:'), attrs={'class': 'relationshipDetailLabel'})
        self._priority = aux.next_sibling.next_sibling.text

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
            self._SNOW_REF_MSG = found.group(1)
        else:
            self._SNOW_REF_MSG = None

    @property
    def SNOW_INC(self):
        return self._SNOW_INC

    @SNOW_INC.setter
    def SNOW_INC(self, soup):
        found = re.search(regex_dict['SNOW_INC_in_title'], soup.find("title").text)
        if found is not None:
            self._SNOW_INC = "INC" + found.group(1)
        else:
            self._SNOW_INC = None

    @property
    def SNOW_ITASK(self):
        return self._SNOW_ITASK

    @SNOW_ITASK.setter
    def SNOW_ITASK(self, soup):
        found = re.search(regex_dict['SNOW_ITASK_in_title'], soup.find("title").text)
        if found is not None:
            self._SNOW_ITASK = "ITASK" + found.group(1)
        else:
            self._SNOW_ITASK = None

    @property
    def createDate(self):
        return self._createDate

    @createDate.setter
    def createDate(self, value):
        self._createDate = value

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

        regex_dict['page_text_from'] = re.compile('(From:|'
                                                  'Od:)')
        regex_dict['page_text_to'] = re.compile('(To:|'
                                                'Do:)')

    def printAll(self):
        print ("-------- Track Info --------")
        print ("trknum: " + self.trknum.encode('UTF-8'))
        print ("title: " + self.title.encode('UTF-8'))
        print ("priority: " + self.priority.encode('UTF-8'))

        print ("custName: " + self.custName.encode('UTF-8'))
        print ("custCompany: " + self.custCompany.encode('UTF-8'))

        print ("primOwnName: " + self.primOwnName.encode('UTF-8'))
        print ("primOwnCompany: " + self.primOwnCompany.encode('UTF-8'))

        print ("SNOW_INC: " + self.SNOW_INC.encode('UTF-8'))
        print ("SNOW_ITASK: " + self.SNOW_ITASK.encode('UTF-8'))
        print ("SNOW_REF_MSG: " + self.SNOW_REF_MSG.encode('UTF-8'))
        print ("-------- Track Info -------- \n\n")

        for updt in self.pageInfoList:
            updt.printAll()

    def prepare_raw_data(self):
        number_of_pages = len(self.pageInfoList)
        if number_of_pages == 0:
            raise Exception("No pages parsed, run the constructor on a proper file")

        trknum_list = [self.trknum] * number_of_pages
        title_list = [self.title] * number_of_pages

        priority_list = [self.priority] * number_of_pages
        custName_list = [self.custName] * number_of_pages
        custCompany_list = [self.custCompany] * number_of_pages

        primOwnName_list = [self.primOwnName] * number_of_pages
        primOwnCompany_list = [self.primOwnCompany] * number_of_pages

        SNOW_INC_list = [self.SNOW_INC] * number_of_pages
        SNOW_REF_MSG_list = [self.SNOW_REF_MSG] * number_of_pages
        SNOW_ITASK_list = [self.SNOW_ITASK] * number_of_pages
        createDate_list = [self.createDate] * number_of_pages
        page_number_list = list()
        modifiedBy_list = list()
        lstPgUpdated_list = list()

        # pageData_list = list()
        SAS_status_list = list()
        SAS_sub_status_list = list()
        SAS_component_list = list()
        SAS_environment_list = list()
        SAS_pool_list = list()
        SAS_comment_list = list()
        SAS_assigned_to_list = list()
        SAS_priority_list = list()
        SAS_classification_list = list()
        SAS_sub_classification_list = list()
        SAS_severity_list = list()
        SAS_impact_range_list = list()
        page_text_list = list()


        for page in self.pageInfoList:
            page_number_list.append(page.page_number)
            modifiedBy_list.append(page.modifiedBy)
            lstPgUpdated_list.append(page.lstPgUpdated)
            page_text_list.append(page.page_text)

            SAS_status_list.append(page.SAS_status)
            SAS_sub_status_list.append(page.SAS_sub_status)
            SAS_component_list.append(page.SAS_component)
            SAS_environment_list.append(page.SAS_environment)
            SAS_pool_list.append(page.SAS_pool)
            SAS_comment_list.append(page.SAS_comment)
            SAS_assigned_to_list.append(page.SAS_assigned_to)
            SAS_priority_list.append(page.SAS_priority)
            SAS_classification_list.append(page.SAS_classification)
            SAS_sub_classification_list.append(page.SAS_sub_classification)
            SAS_severity_list.append(page.SAS_severity)
            SAS_impact_range_list.append(page.SAS_impact_range)

        raw_data = create_raw_data(SAS_status_list, SAS_assigned_to_list, SAS_classification_list, SAS_comment_list,
                                   SAS_component_list, SAS_environment_list, SAS_impact_range_list, SAS_pool_list,
                                   SAS_priority_list, SAS_severity_list, SAS_sub_classification_list,
                                   SAS_sub_status_list, SNOW_INC_list, SNOW_ITASK_list, SNOW_REF_MSG_list,
                                   custCompany_list, custName_list, lstPgUpdated_list, modifiedBy_list,
                                   page_number_list, page_text_list, primOwnCompany_list, primOwnName_list,
                                   priority_list, title_list, trknum_list, createDate_list)

        return raw_data
        # df = pd.DataFrame(raw_data)
        # df.to_csv(name.encode('utf-8') + ".csv", index=False)

        # def check_if_csv_exists():

        # df = pd.DataFrame()

        # book = pd.Workbook()
        # df.to_excel('test.xlsx', sheet_name='sheet1', index=False)



    # def extractCreateDate(self, soup):
    # def extractUpdates(self, soup):

    # property(trknum)


class Update(object):
    # def __init__(self, tag_pretext, tag_pageHead, tag_pageData):
    def __init__(self, tag_pageHead, tag_pageData):
        # self.tag_pretext = tag_pretext
        self.tag_pageHead = tag_pageHead
        self.tag_pageData = tag_pageData
        self.pageData = tag_pageData
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

        self.page_text = tag_pageData
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

    @property
    def page_text(self):
        return self._page_text

    @page_text.setter
    def page_text(self, tag_pageData):
        aux_line = list()
        for line in tag_pageData.find_all('span'):
            # if self.get_reg_tag("span", tag_pageData, "page_text_from") is not None:
            # print "to find: " + line.text
            # print "regex: " + str(regex_dict['page_text_from'])
            if line:
                found = re.search(regex_dict['page_text_from'], line.text)

            # print line.contents[0].encode('UTF-8')

            # if found is not None:
            #     print "found: " + str(found.string)
            #     break
            aux_line.append(line.contents[0].encode('UTF-8'))  # .span.text
        self._page_text = '\\n'.join(aux_line)
        # print (self.page_text)
        # self._page_text = self.get_reg_tag("span", tag_pageData, "SAS-severity")

    def get_reg_tag(self, tag, tag_pageData, regex_dict_key):
        for line in tag_pageData.find_all(tag):
            if line is None or line.string is None:
                continue
            found = re.search(regex_dict[regex_dict_key], line.string)
            if found is not None:
                return found.group(1).encode('UTF-8')
        return None

    def printAll(self):
        print ("-------- Page Info --------")
        # print "page_number: " + str(self.page_number) + "\nmodifiedBy: " + str(self.modifiedBy) + "\nlstPgUpdated: " + str(self.lstPgUpdated) + "\nsender: " + str(self.sender)
        print ("page_number: " + self.page_number.encode('UTF-8') + "\nmodifiedBy: " + self.modifiedBy.encode('UTF-8') + "\nlstPgUpdated: "
               + self.lstPgUpdated.encode('UTF-8'))
        for sas_tag in self.SAS_tags:
            if sas_tag is not None:
                print sas_tag.encode('UTF-8')
        print ("-------- Page Info --------\n")