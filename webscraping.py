import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as request
import random
from map import *
# This file web scrapes all colleges, majors, and classes from different CMU
# websites and creates a dataframe of students with some association between
# their year, college, major, class, building they are in and things they do.

# https://medium.com/code-to-express/introduction-to-web-scraping-using-python-e5bc74b0b35e
# https://scs.hosted.panopto.com/Panopto/Pages/Viewer.aspx?id=fb5ce8bb-1a29-4acb-b34d-add901814bb4
# https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html
# https://pandas.pydata.org/docs/reference/api/pandas.read_excel.html


class Student():
    def __init__(self):
        self.majors = dict()  # college:majors
        self.majorsList = list()
        self.df = pd.DataFrame(index=range(50), columns=[
            'Year', 'College', 'Major', 'Class', 'Building', 'ing...'])
        self.classes = set()  # all classes
        self.CFADict, self.TPRDict, self.SCSDict = dict(), dict(), dict()  # major:classes
        self.DCDict, self.MCSDict, self.CITDict, self.ISDict = dict(), dict(), dict(), dict()

    def getMajorsDict(self):  # key is college, value is all majors in the college
        urls = {'CFA': 'https://www.cmu.edu/admission/majors-programs/college-of-fine-arts',
                'TPR': 'https://www.cmu.edu/admission/majors-programs/tepper-school-of-business',
                'SCS': 'https://www.cmu.edu/admission/majors-programs/school-of-computer-science',
                'DC': 'https://www.cmu.edu/admission/majors-programs/dietrich-college-of-humanities-social-sciences',
                'MCS': 'https://www.cmu.edu/admission/majors-programs/mellon-college-of-science',
                'CIT': 'https://www.cmu.edu/admission/majors-programs/college-of-engineering',
                'IS': 'https://www.cmu.edu/admission/majors-programs/information-systems'}
        for college, url in urls.items():
            client = request(url)
            html_page = client.read()
            client.close()
            soup_html = soup(html_page, 'html.parser')
            if college in ['CIT', 'IS']:
                content = soup_html.findAll('div', {'class',
                                                    'expandables__details__items expandables__details__items--columns-1'})
            elif college == 'BXA Intercollege':
                content = soup_html.findAll('details', {'class',
                                                        'expandables__details paragraph paragraph--type--expandable-section paragraph--view-mode--default'})
            else:
                content = soup_html.findAll('div', {'class',
                                                    'expandables__details__items expandables__details__items--columns-2'})
            collegeMajors = set()
            s = ''
            for major in content:
                major = str(major.text)
                s += major
                while '\n\n' in s:  # get rid of empty lines
                    s = s.replace('\n\n', '\n')
                for m in s.splitlines():
                    if 'Bachelor' in m:  # only want the majors
                        # only want the degree before the ,
                        m = m.split(',')[0]
                        collegeMajors.add(m.strip())
            self.majors[college] = collegeMajors

    def getMajorsList(self):  # get a list of all majors
        for college, collegeMajors in self.majors.items():
            for m in collegeMajors:
                self.majorsList.append(m)

    def getClasses(self):  # major:class
        urls = {'Architecture': 'http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofarchitecture/courses/',
                'Fine Arts': 'http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofart/courses/',
                'Design': 'http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofdesign/courses/',
                'Drama': 'http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofdrama/courses/',
                'Music': 'http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofmusic/courses/'}
        for major, url in urls.items():
            classSet = set()
            client = request(url)
            html_page = client.read()
            client.close()
            soup_html = soup(html_page, 'html.parser')
            content = soup_html.find('div', {'class', 'page_content'})
            content = str(content.text)
            for paragraph in content.split('\n\n\n'):
                for line in paragraph.splitlines():
                    if len(line) != 0:
                        if line[0].isdigit():
                            classSet.add(line)
            self.CFADict[major] = classSet
            for c in classSet:
                self.classes.add(c)

        urls = {'Business':
                'http://coursecatalog.web.cmu.edu/schools-colleges/tepper/undergraduatebusinessadministrationprogram/#bsinbusinessadministrationtextcontainer'}
        for major, url in urls.items():
            classSet = set()
            client = request(url)
            html_page = client.read()
            client.close()
            soup_html = soup(html_page, 'html.parser')
            content = str(soup_html.body.text)
            for paragraph in content.split('\n\n\n'):
                for line in paragraph.splitlines():
                    if len(line) != 0:
                        if line[0].isdigit():
                            classSet.add(line)
            self.TPRDict[major] = classSet
            for c in classSet:
                self.classes.add(c)

        urls = {'Artificial Intelligence':
                'http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/artificialintelligence/#curriculumtextcontainer',
                'Computational Biology': 'http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/undergraduatecomputatonalbiology/#bscurriculumtextcontainer',
                'Computer Science': 'http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/undergraduatecomputerscience/#bscurriculumtextcontainer',
                'Human-Computer Interaction': 'http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/humancomputerinteractionprogram/#curriculumbsinhumancomputerinteractiontextcontainer'
                }
        for major, url in urls.items():
            classSet = set()
            client = request(url)
            html_page = client.read()
            client.close()
            soup_html = soup(html_page, 'html.parser')
            content = str(soup_html.body.text)
            for paragraph in content.split('\n\n\n'):
                for line in paragraph.splitlines():
                    if len(line) != 0:
                        if line[0].isdigit():
                            classSet.add(line)
            self.SCSDict[major] = classSet
            for c in classSet:
                self.classes.add(c)

        urls = {'Economics': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/undergraduateeconomicsprogram/#baineconomicscurriculumtextcontainer',
                'Creative Writing': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofenglish/#baincreativewritingtextcontainer',
                'Visual Media': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofenglish/#bainfilmandvisualmediatextcontainer',
                'Chinese': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#chinesestudiestextcontainer',
                'French': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#frenchandfrancophonestudiestextcontainer',
                'German': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#germanstudiestextcontainer',
                'Hispanic': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#hispanicstudiestextcontainer',
                'Japanese': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#japanesestudiestextcontainer',
                'Russian': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#russianstudiestextcontainer',
                'Psychology': 'https://coursecatalog-new.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofpsychology/#psych_majortextcontainer',
                'Neuroscience': 'https://coursecatalog-new.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofpsychology/#majorinneurosciencetextcontainer',
                'Cognitive Science': 'https://coursecatalog-new.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofpsychology/#cognitive_sciencetextcontainer',
                'Behavioral Economics': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofsocialanddecisionsciences/#majorinbehavioraleconomicspolicyandorganizationstextcontainer',
                'Decision Science': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofsocialanddecisionsciences/#majorstextcontainer',
                'Policy and Management': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofsocialanddecisionsciences/#majorinpolicyandmanagementtextcontainer',
                'Statistics': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofstatistics/#bsinstatisticstextcontainer',
                'Machine Learning': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofstatistics/#statsmltextcontainer',
                'Global Studies': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofhistory/#baglobalstudiestextcontainer',
                'International Relations': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/instituteforpoliticsandstrategy/#majorininternationalrelationsandpoliticstextcontainer',
                'Multilingual Studies': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/instituteforpoliticsandstrategy/#majorininternationalrelationsandpoliticstextcontainer',
                'Linguistics': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofphilosophy/#majorinlinguisticstextcontainer',
                'Logic and Computation': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofphilosophy/#majorinlogicandcomputationtextcontainer',
                'Ethics, History, and Public Policy': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofphilosophy/#majorinethicshistoryandpublicpolicytextcontainer',
                'Philosophy': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofphilosophy/#majorinphilosophytextcontainer'}
        for major, url in urls.items():
            classSet = set()
            client = request(url)
            html_page = client.read()
            client.close()
            soup_html = soup(html_page, 'html.parser')
            content = str(soup_html.body.text)
            for paragraph in content.split('\n\n\n'):
                for line in paragraph.splitlines():
                    if len(line) != 0:
                        if line[0].isdigit():
                            classSet.add(line)
            self.DCDict[major] = classSet
            for c in classSet:
                self.classes.add(c)

        urls = {'Science': 'http://coursecatalog.web.cmu.edu/schools-colleges/melloncollegeofscience/#generaleducationrequirementstextcontainer'}
        for major, url in urls.items():
            classSet = set()
            client = request(url)
            html_page = client.read()
            client.close()
            soup_html = soup(html_page, 'html.parser')
            content = str(soup_html.body.text)
            for paragraph in content.split('\n\n\n'):
                for line in paragraph.splitlines():
                    if len(line) != 0:
                        if line[0].isdigit():
                            classSet.add(line)
            self.MCSDict[major] = classSet
            for c in classSet:
                self.classes.add(c)

        urls = {
            'Engineering': 'http://coursecatalog.web.cmu.edu/schools-colleges/collegeofengineering/courses/'}
        for major, url in urls.items():
            classSet = set()
            client = request(url)
            html_page = client.read()
            client.close()
            soup_html = soup(html_page, 'html.parser')
            content = soup_html.find('div', {'class', 'page_content'})
            content = str(content.text)
            for paragraph in content.split('\n\n\n'):
                for line in paragraph.splitlines():
                    if len(line) != 0:
                        if line[0].isdigit():
                            classSet.add(line)
            self.CITDict[major] = classSet
            for c in classSet:
                self.classes.add(c)

        urls = {'Information Systems': 'http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/informationsystems/courses/'}
        for major, url in urls.items():
            classSet = set()
            client = request(url)
            html_page = client.read()
            client.close()
            soup_html = soup(html_page, 'html.parser')
            content = soup_html.find('div', {'class', 'page_content'})
            content = str(content.text)
            for paragraph in content.split('\n\n\n'):
                for line in paragraph.splitlines():
                    if len(line) != 0:
                        if line[0].isdigit():
                            classSet.add(line)
            self.ISDict[major] = classSet
            for c in classSet:
                self.classes.add(c)

    def createDataframe(self):  # randomly assigned student info
        for i in range(self.df.shape[0]):
            randomMajor = random.choice(self.majorsList)
            self.df.loc[i, 'Major'] = randomMajor  # randomly assign a major
            for college, majorSet in self.majors.items():
                if randomMajor in majorSet:
                    # fill the college column according to majors
                    self.df.loc[i, 'College'] = college
            if 'Architecture' in self.df.loc[i, 'Major']:
                year = random.randint(1, 5)
            else:
                year = random.randint(1, 4)
            self.df.loc[i, 'Year'] = year  # randomly assign a year

            # possible classes for this specific students:
            studentClasses = list()
            studentClasses.extend(list(self.classes))

            if self.df.loc[i, 'College'] == 'CFA':
                for major, classSet in self.CFADict.items():
                    for c in classSet:
                        # more possible to take classes from their own college
                        studentClasses.append(c)
                    if major in randomMajor:
                        for c in classSet:
                            # most possible to take classes from own major
                            studentClasses.append(c)
            elif self.df.loc[i, 'College'] == 'TPR':
                for major, classSet in self.TPRDict.items():
                    for c in classSet:
                        for i in range(2):  # add twice bc tpr only has 1 major
                            studentClasses.append(c)
            elif self.df.loc[i, 'College'] == 'SCS':
                for major, classSet in self.SCSDict.items():
                    for c in classSet:
                        studentClasses.append(c)
                    if major in randomMajor:
                        for c in classSet:
                            studentClasses.append(c)
            elif self.df.loc[i, 'College'] == 'DC':
                for major, classSet in self.DCDict.items():
                    for c in classSet:
                        studentClasses.append(c)
                    if major in randomMajor:
                        for c in classSet:
                            studentClasses.append(c)
            elif self.df.loc[i, 'College'] == 'MCS':
                for major, classSet in self.MCSDict.items():
                    for c in classSet:
                        studentClasses.append(c)
                    if major in randomMajor:
                        for c in classSet:
                            studentClasses.append(c)
            elif self.df.loc[i, 'College'] == 'CIT':
                for major, classSet in self.CITDict.items():
                    for c in classSet:
                        for i in range(2):
                            studentClasses.append(c)
            elif self.df.loc[i, 'College'] == 'IS':
                for major, classSet in self.ISDict.items():
                    for c in classSet:
                        for i in range(2):
                            studentClasses.append(c)
            randomClass = random.choice(studentClasses)
            self.df.loc[i, 'Class'] = randomClass
            self.df['Class'] = self.df['Class'].fillna(
                random.choice(studentClasses))  # fill the empty cells

            # the building this student is at:
            buildings = ['TEP', 'GHC', 'DH', 'CUC', 'NSH', 'WEH', 'BH',
                         'CFA', 'CYH', 'HBH', 'HL', 'MI', 'PH', 'POS', 'WH', 'Cut']
            if self.df.loc[i, 'College'] == 'CFA':
                for i in range(2):
                    buildings.append('CFA')
                    buildings.append('CFA')
                    buildings.append('CUC')
                    buildings.append('PH')
                    buildings.append('DH')
                    buildings.append('WEH')
            elif self.df.loc[i, 'College'] == 'TPR':
                for i in range(2):
                    buildings.append('TEP')
                    buildings.append('TEP')
                    buildings.append('WEH')
                    buildings.append('DH')
                    buildings.append('PH')
                    buildings.append('CUC')
            elif self.df.loc[i, 'College'] == 'SCS':
                for i in range(2):
                    buildings.append('GHC')
                    buildings.append('GHC')
                    buildings.append('GHC')
                    buildings.append('PH')
                    buildings.append('DH')
                    buildings.append('WEH')
                    buildings.append('CUC')
                    buildings.append('BH')
                    buildings.append('POS')
                    buildings.append('MI')
            elif self.df.loc[i, 'College'] == 'MCS':
                for i in range(2):
                    buildings.append('GHC')
                    buildings.append('POS')
                    buildings.append('WEH')
                    buildings.append('DH')
                    buildings.append('MI')
            elif self.df.loc[i, 'College'] == 'CIT':
                for i in range(2):
                    buildings.append('DH')
                    buildings.append('DH')
                    buildings.append('GHC')
                    buildings.append('POS')
                    buildings.append('CUC')
                    buildings.append('WEH')
                    buildings.append('WEH')
                    buildings.append('PH')
                    buildings.append('TEP')
            elif self.df.loc[i, 'College'] == 'IS':
                for i in range(2):
                    buildings.append('GHC')
                    buildings.append('MI')
                    buildings.append('PH')
                    buildings.append('WEH')
            randomBuilding = random.choice(buildings)
            self.df.loc[i, 'Building'] = randomBuilding
            self.df['Building'] = self.df['Building'].fillna(
                random.choice(buildings))  # fill the empty cells

            # what the student is doing:
            doingList = ['saying hi to a friend...', 'trying to connect to the WiFi...',
                         'going to class...', 'going to OH...', 'sleeping...', 'sleeping...', 'writing a paper...',
                         'talking to a friend...', 'meeting up for a group project...']
            if self.df.loc[i, 'Building'] == 'CFA':
                CFAList = ['attending a workshop...', 'painting...', 'drawing...', 'acting...',
                           'taking pictures...', 'stress eating in the studio...', 'writing a play script...']
                for i in range(3):
                    doingList = doingList + CFAList
            elif self.df.loc[i, 'Building'] == 'TEP':
                TEPList = ["lining up for Millie's...", 'waiting for friends at the purple chairs...',
                           'checking for spaces in the breakout rooms...', 'working on a paper due in an hour...', 'having a meeting', 'networking']
                for i in range(3):
                    doingList = doingList + TEPList
            elif self.df.loc[i, 'Building'] == 'GHC':
                GHCList = ['searching for an unoccupied study spot...', 'running into someone in a 112 hoodies...',
                           'joining the OH queue...', 'grabbing iced americano at La Prima...', 'writing code...', 'pulling an all-nighter...', 'zoning out...']
                for i in range(3):
                    doingList = doingList + GHCList
            elif self.df.loc[i, 'Building'] == 'CUC':
                CUCList = ['joining the line at the mail room...',
                           'getting lunch at ABP...', 'printing out a paper...', 'working out...']
                for i in range(3):
                    doingList = doingList + CUCList
            elif self.df.loc[i, 'Building'] == 'WEH':
                WEHList = ['lining up for La Prima...',
                           'studying at Sorrells...']
                for i in range(3):
                    doingList = doingList + WEHList
            elif self.df.loc[i, 'Building'] == 'Cut':
                doingList = ['going to class...', 'saying hi to a friend...',
                             'running into someone in a 112 hoodies...', 'sleeping...', 'tabling...', 'looking at the fence...']
            randomThings = random.choice(doingList)
            self.df.loc[i, 'ing...'] = randomThings
            self.df['ing...'] = self.df['ing...'].fillna(
                random.choice(doingList))  # fill the empty cells


students = Student()
students.getMajorsDict()
students.getMajorsList()
students.getClasses()
students.createDataframe()


# write the dataframe to an excel
# (then read from the excel instead of webscraping every time)
writer = pd.ExcelWriter('students.xlsx')
students.df.to_excel(writer)
writer.save()


# webscraped from:
# https://www.cmu.edu/admission/majors-programs/college-of-fine-arts
# https://www.cmu.edu/admission/majors-programs/tepper-school-of-business
# https://www.cmu.edu/admission/majors-programs/school-of-computer-science
# https://www.cmu.edu/admission/majors-programs/dietrich-college-of-humanities-social-sciences
# https://www.cmu.edu/admission/majors-programs/mellon-college-of-science
# https://www.cmu.edu/admission/majors-programs/college-of-engineering
# https://www.cmu.edu/admission/majors-programs/information-systems
# http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofarchitecture/courses/
# http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofart/courses/
# http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofdesign/courses/
# http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofdrama/courses/
# http://coursecatalog.web.cmu.edu/schools-colleges/collegeoffinearts/schoolofmusic/courses/
# http://coursecatalog.web.cmu.edu/schools-colleges/tepper/undergraduatebusinessadministrationprogram/#bsinbusinessadministrationtextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/artificialintelligence/#curriculumtextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/undergraduatecomputatonalbiology/#bscurriculumtextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/undergraduatecomputerscience/#bscurriculumtextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/schoolofcomputerscience/humancomputerinteractionprogram/#curriculumbsinhumancomputerinteractiontextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/undergraduateeconomicsprogram/#baineconomicscurriculumtextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofenglish/#baincreativewritingtextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofenglish/#bainfilmandvisualmediatextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#chinesestudiestextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#frenchandfrancophonestudiestextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#germanstudiestextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#hispanicstudiestextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#japanesestudiestextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofmodernlanguages/#russianstudiestextcontainer
# https://coursecatalog-new.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofpsychology/#psych_majortextcontainer
# https://coursecatalog-new.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofpsychology/#majorinneurosciencetextcontainer
# https://coursecatalog-new.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofpsychology/#cognitive_sciencetextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofsocialanddecisionsciences/#majorinbehavioraleconomicspolicyandorganizationstextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofsocialanddecisionsciences/#majorstextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofsocialanddecisionsciences/#majorinpolicyandmanagementtextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofstatistics/#bsinstatisticstextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofstatistics/#statsmltextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofhistory/#baglobalstudiestextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/instituteforpoliticsandstrategy/#majorininternationalrelationsandpoliticstextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/instituteforpoliticsandstrategy/#majorininternationalrelationsandpoliticstextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofphilosophy/#majorinlinguisticstextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofphilosophy/#majorinlogicandcomputationtextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofphilosophy/#majorinethicshistoryandpublicpolicytextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/departmentofphilosophy/#majorinphilosophytextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/melloncollegeofscience/#generaleducationrequirementstextcontainer
# http://coursecatalog.web.cmu.edu/schools-colleges/collegeofengineering/courses/
# http://coursecatalog.web.cmu.edu/schools-colleges/dietrichcollegeofhumanitiesandsocialsciences/informationsystems/courses/
