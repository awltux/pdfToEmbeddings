import re
import json
from unidecode import unidecode
from PyPDF2 import PdfReader


def removeHeaderAndFooter(pageText):
    while re.findall( stringRegex, pageText, flags=re.DOTALL ):
        pageText = re.sub( stringRegex, '', pageText, flags=re.DOTALL )
    return pageText



def removeReversedHeaderAndFooter(pageText):
    while re.findall( reverseRegex, pageText, flags=re.DOTALL ):
        pageText = re.sub( reverseRegex, '', pageText, flags=re.DOTALL )
    return pageText

def fixInvalidSectionNames(pageText, pageNumber):
    if pageNumber == 307:
       pageText = pageText.replace("3.20.0 Introduction", "3.28.0 Introduction")

    return pageText       
    
def isMultilineSection(sectionNumber, pageNumber):
    multilineString = "[%s] %s" % (pageNumber, sectionNumber)
    if (
        multilineString == '[12] 0.3' or 
        multilineString == '[18] 0.4' or 
        multilineString == '[21] 0.5' or 
        multilineString == '[31] 0.8' or 
        multilineString == '[40] 0.9' or 
        multilineString == '[42] 0.11' or 
        multilineString == '[48] 0.15' or 
        multilineString == '[95] 2.4.4' or 
        multilineString == '[118] 2.9.7' or 
        multilineString == '[118] 2.9.8' or 
        multilineString == '[177] 3.1' or 
        multilineString == '[202] 3.8' or 
        multilineString == '[206] 3.9' or 
        multilineString == '[257] 3.18' or 
        multilineString == '[264] 3.19' or
        multilineString == '[274] 3.20' or
        multilineString == '[319] 3.A.6' or
        multilineString == '[324] 3.A.7' or
        multilineString == '[334] 3.A.10' or
        multilineString == '[401] 4.14' or
        multilineString == '[437] 6.1.3' or
        multilineString == '[445] 6.2.6' or
        multilineString == '[457] 6.6.2' or
        multilineString == '[461] 6.8.3' or 
        multilineString == '[468] 6.A' or 
        multilineString == '[473] 6.B' or 
        multilineString == '[492] 7.2.1' or 
        multilineString == '[493] 7.2.2' or 
        multilineString == '[498] 7.B' or 
        multilineString == '[529] B.2' or 
        multilineString == '[539] B.4' or 
        multilineString == '[540] B.6' or 
        multilineString == '[541] B.7' or 
        multilineString == '[541] B.8' or 
        multilineString == '[543] B.9' or 
        multilineString == '[546] B.10' or 
        multilineString == '[547] B.11' or 
        multilineString == '[547] B.12' or 
        multilineString == '[549] B.13' ):
        return True

    return False

def validSection(sectionNumber, pageNumber):
    errorString = "[%s] %s" % (pageNumber, sectionNumber)
    if (
        errorString == '[73] 2.0.7' or 
        errorString == '[230] 3.12.3' or 
        errorString == '[414] 5.1.8' or 
        errorString == '[392] 4.0' or 
        errorString == '[505] A' or 
        errorString == '[359] 4.3.14' or 
        errorString == '[135] 2.11.7' ):
        print("################################# Ignoring invalid regex match: %s" % errorString)
        return False

    return True
    
# Some pages dont contain any useful information e.g. section indexes
def validPage(pageNumber):
    if (
        pageNumber == 1 or 
        pageNumber == 2 or 
        pageNumber == 53 or 
        pageNumber == 71 or 
        pageNumber == 173 or 
        pageNumber == 337 or 
        pageNumber == 405 or 
        pageNumber == 423 or 
        pageNumber == 475 or 
        pageNumber == 505 ):
        print("################################# Ignoring page: %s" % pageNumber)
        return False

    return True
    
    
stringRegex = r'Domestic Technical Handbook[a-zA-Z ]+[0-9 ]+Edition.*?Page[0-9 ]+[a-zA-Z ]+[0-9 ]+[a-zA-Z ]+[0-9]+[ ]+'
reverseRegex = r'Page[0-9 ]+[a-zA-Z ]+[0-9 ]+[a-zA-Z ]+[0-9]+.*?Domestic Technical Handbook[a-zA-Z ]+[0-9 ]+Edition[ ]+'

# Check for valid RegEx
compiledRegex = re.compile(stringRegex)
compiledreverseRegex = re.compile(reverseRegex)
    
# creating a pdf file object
pdfObject = open('./2023+Domestic+Technical+Handbook.pdf', 'rb')

# creating a pdf reader object
pdfReader = PdfReader(pdfObject)
pdfPageCount = len(pdfReader.pages)
# Extract and concatenate each page's content

findMajorSectionsRegex = r'^Section[ ]+([0-9]+)[ ]+-[ ]+([a-zA-Z0-9 ]+?)[ ]*$'
findMajorAppendixRegex = r'^Appendix[ ]+([a-zA-Z])[ ]+([a-zA-Z0-9 ]+?)[ ]*$'

text=''
pageText = [ { 'raw_ascii': None } ] * pdfPageCount
majorSectionNumber = None
majorSectionTitle = None
minorSectionNumber = None
minorSectionIndex = None
minorSectionTitle = None
contentSectionNumber = None
contentSectionTitle = None
pageNumber = 0

sectionList = []

for pageNumber in range(0, pdfPageCount):
    if not validPage(pageNumber):
       continue
    
    minorSectionsFound = None
    minorAnnexSectionsFound = None
    contentSectionsFound = None
    contentAnnexSectionsFound = None

    # creating a page object
    pageObject = pdfReader.pages[pageNumber]
    # extracting text from page
    
    currentPageText = pageObject.extract_text()
    
    # Replace unicode characters with ASCII alternatives
    currentPageText = unidecode(currentPageText)

    # Remove header and footer text
    currentPageText = removeHeaderAndFooter(currentPageText)
    currentPageText = removeReversedHeaderAndFooter(currentPageText)
    currentPageText = fixInvalidSectionNames(currentPageText, pageNumber)

    # Add each page to the final ASCII document    
    # text += "################# page %s ########################\n" % pageNumber
    text += currentPageText
    
    # Add an EOL for page breaks
    if len(text) > 0:
      text += "\n"
    
    # Extract MajorSections from page
    majorSectionsFound = re.findall(findMajorSectionsRegex, currentPageText, flags=re.M )
    #  this script only supports one section per page
    majorSectionCount = len(majorSectionsFound)
    if majorSectionCount > 0:
        majorSection = majorSectionsFound
        majorSectionNumber = majorSection[0][0]
        majorSectionTitle = majorSection[0][1]
        if validSection(majorSectionNumber, pageNumber):
            section = {
              "type": "major",
              "number": majorSectionNumber,
              "title": majorSectionTitle
            }
            sectionList.append(section)
            print('####           majorSection - [%s] %s - %s' % (pageNumber, majorSectionNumber, majorSectionTitle) )
            # New Major section, so reset the sub-sections
            minorSectionsFound = None
            minorAnnexSectionsFound = None
            minorSectionNumber = None
            minorSectionIndex = None
            minorSectionTitle = None
            contentSectionsFound = None
            contentAnnexSectionsFound = None
            contentSectionNumber = None
            contentSectionTitle = None

    majorAppendixFound = re.findall(findMajorAppendixRegex, currentPageText, flags=re.M )
    #  this script only supports one section per page
    majorAppendixCount = len(majorAppendixFound)
    if majorAppendixCount > 0:
        majorSection = majorAppendixFound
        majorSectionNumber = majorSection[0][0]
        majorSectionTitle = majorSection[0][1]
        if validSection(majorSectionNumber, pageNumber):
            section = {
              "type": "major",
              "number": majorSectionNumber,
              "title": majorSectionTitle
            }
            sectionList.append(section)
            print('####          majorAppendix - [%s] %s - %s' % (pageNumber, majorSectionNumber, majorSectionTitle) )
            # New Major section, so reset the sub-sections
            minorSectionsFound = None
            minorAnnexSectionsFound = None
            minorSectionNumber = None
            minorSectionIndex = None
            minorSectionTitle = None
            contentSectionsFound = None
            contentAnnexSectionsFound = None
            contentSectionNumber = None
            contentSectionTitle = None

    # Only process minorSection if majorSection has been found
    if majorSectionNumber:
        findMinorSectionsRegex = r'^[ ]*(%s\.[0-9]+)[ ]+([ a-zA-Z0-9\(\)\'\,\.\:-]+)[ ]*$' % majorSectionNumber
        minorSectionsFound = re.findall(findMinorSectionsRegex, currentPageText, flags=re.M )
        for minorSection in minorSectionsFound:
            minorSectionNumber = minorSection[0]
            minorSectionTitle = minorSection[1]
            
            if isMultilineSection(minorSectionNumber, pageNumber):
                findMinorMultilineSectionsRegex = r'%s[ ]+%s.([ a-zA-Z0-9\(\)\'\,\.\:-]+)' % (minorSectionNumber, re.escape(minorSectionTitle))
                minorMultilineSectionsFound = re.findall(findMinorMultilineSectionsRegex, currentPageText, flags=re.DOTALL )
                for minorMultilineSection in minorMultilineSectionsFound:
                    minorSectionTitle += minorMultilineSection
                
            if validSection(minorSectionNumber, pageNumber):
                section = {
                  "type": "minor",
                  "number": minorSectionNumber,
                  "title": minorSectionTitle
                }
                sectionList.append(section)
                print("########       minorSection - [%s] %s - %s" % (pageNumber, minorSectionNumber, minorSectionTitle) )
                # New Minor section, so reset the sub-sections
                contentSectionsFound = None
                contentAnnexSectionsFound = None
                contentSectionNumber = None
                contentSectionTitle = None

        findMinorSectionsRegex = r'^Table[ ]+Appendix[ ]+(%s\.?([0-9]+))[ ]+\-[ ]+([ a-zA-Z0-9\(\)\'\,\.\:-]+)[ ]*$' % majorSectionNumber
        minorTableAppendixSectionsFound = re.findall(findMinorSectionsRegex, currentPageText, flags=re.M )
        for minorAnnex in minorTableAppendixSectionsFound:
            minorSectionNumber = minorAnnex[0]
            minorSectionIndex = minorAnnex[1]
            minorSectionTitle = minorAnnex[2]
            
            if isMultilineSection(minorSectionNumber, pageNumber):
                findMinorMultilineSectionsRegex = r'%s[ ]+%s.([ a-zA-Z0-9\(\)\'\,\.\:-]+)' % (minorSectionNumber, re.escape(minorSectionTitle))
                minorMultilineSectionsFound = re.findall(findMinorMultilineSectionsRegex, currentPageText, flags=re.DOTALL )
                for minorMultilineSection in minorMultilineSectionsFound:
                    minorSectionTitle += minorMultilineSection
                    
            if validSection(minorSectionNumber, pageNumber):
                section = {
                  "type": "minor",
                  "number": minorSectionNumber,
                  "title": minorSectionTitle
                }
                sectionList.append(section)
                print("########      minorAppendix - [%s] %s - %s" % (pageNumber, minorSectionNumber, minorSectionTitle) )
                # New Minor section, so reset the sub-sections
                contentSectionsFound = None
                contentAnnexSectionsFound = None
                contentSectionNumber = None
                contentSectionTitle = None

    # Only process contentSection if minorSection has been found
    if minorSectionNumber:
        
        # ERROR: This pulls out invalid sections e.g. 
        #   4.3.14 - and, when not in use, the installation should:
        findContentSectionsRegex = r'^[ ]*(%s.[0-9]+)[ ]+([ a-zA-Z0-9\(\)\'\,\.\:-]+)[ ]*$' % (minorSectionNumber)
        contentSectionsFound = re.findall(findContentSectionsRegex, currentPageText, flags=re.M )
        for contentSection in contentSectionsFound:
            contentSectionNumber = contentSection[0]
            contentSectionTitle = contentSection[1]
            if isMultilineSection(contentSectionNumber, pageNumber):
                findMinorMultilineSectionsRegex = r'%s[ ]+%s.([ a-zA-Z0-9\(\)\'\,\.\:-]+)' % (contentSectionNumber, re.escape(contentSectionTitle))
                contentMultilineSectionsFound = re.findall(findMinorMultilineSectionsRegex, currentPageText, flags=re.DOTALL )
                for contentMultilineSection in contentMultilineSectionsFound:
                    contentSectionTitle += contentMultilineSection
                    
            if validSection(contentSectionNumber, pageNumber):
                section = {
                  "type": "contnet",
                  "number": contentSectionNumber,
                  "title": contentSectionTitle
                }
                sectionList.append(section)
                print("############ contentSection - [%s] %s - %s" % (pageNumber, contentSectionNumber, contentSectionTitle) )

#    # If sections not changed on this page, print the last one encountered
#    if not majorSectionCount:
#        print('####           majorSection: %s - %s' % (majorSectionNumber, majorSectionTitle) )
#    if not minorSectionsFound and not minorAnnexSectionsFound:
#        print("########       minorSection: %s - %s" % (minorSectionNumber, minorSectionTitle) )
#    if not contentSectionsFound and not contentAnnexSectionsFound:
#        print("############ contentSection: %s - %s" % (contentSectionNumber, contentSectionTitle) )


with open("output.txt", "w", newline='\n') as outputFile:
    outputFile.write(text)

sectionListJsonString = json.dumps(sectionList)

with open("sections.json", "w", newline='\n') as sectionsFile:
    sectionsFile.write(sectionListJsonString)

