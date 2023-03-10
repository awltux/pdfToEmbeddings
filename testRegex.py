import re


findAllRegexp = """
tshall meet the requirements of this standard (regulation 12, schedule 6).  
7.2.1  Charge point provision to new dwellings (including creation of 
one or more dwellings by conversion).  
Single dwellings . 
W

"""

print (re.escape('Charge point provision to new dwellings (including creation of'))

stringRegex = r'%s[ ]+%s[ ]+.([ a-zA-Z0-9\(\)\'\,\.\:-]+)' % ( '7.2.1', re.escape('Charge point provision to new dwellings (including creation of') )
#stringRegex = r'(%s\.[0-9]+)[ ]+([a-zA-Z0-9\(\)\'\,\:-]+)[ ]*' % '7'
#stringRegex = r'^Domestic Technical Handbook[a-zA-Z ]+[0-9 ]+Edition.*?Page[0-9 ]+[a-zA-Z ]+[0-9 ]+[a-zA-Z ]+[0-9]+[ ]+'
#stringRegex = r'^Domestic Technical Handbook[a-zA-Z ]+[0-9 ]+Edition.*?Page[0-9 ]+[a-zA-Z ]+[0-9 ]+[a-zA-Z ]+[0-9]+[ ]+'

findAllResult = re.findall( stringRegex, findAllRegexp, flags=re.DOTALL )

print (findAllResult )