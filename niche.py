__author__ = 'Sazan Dauti'

import json
import urllib2
import re


college_url = 'ENTER COLLEGE NICHE URL'

reviews_url = 'https://colleges.niche.com/Reviews'

'''
Get school name for file
'''
if not college_url[-1:] == '/':
    college_url += '/'
sn = re.search('https:\/\/colleges.niche.com\/(.*?)\/', college_url)
school_name = ''
if sn:
    school_name = sn.group(1)
file_name = school_name + '-reviews.json'

'''
Get profile id as well as total number of pages of reviews
'''
response = urllib2.urlopen(college_url)
html = response.read()
m = re.search('"Profile.GUID": "(.*?)"', html)
if m:
    sId = m.group(1)
else:
    sId = ''
p = re.search('maxPages: (.*?),', html)

if p:
    maxPages = int(p.group(1))
else:
    maxPages = 0


if not (maxPages == 0 or sId == ''):
    
    tFile = open(file_name, 'w+')
    
    main_dict = []
    page = 1
    while page <= maxPages:
        post_string = '{"entityIds":["' + str(sId) + '"],"sectionId":"","pageFilter":{"Page":' + str(page) + ',"Size":25},"order":"Newest"}'
        headers = {"Content-Type": "application/json"}
        req2 = urllib2.Request(reviews_url, post_string, headers=headers)
        r2 = urllib2.urlopen(req2)
        the_json = r2.read()
        if the_json:
            parsed_json = json.loads(the_json)
            for rev in parsed_json['Reviews']:
                temp_dict = {}
                body = rev['Body'].encode('utf-8')
                temp_dict['review'] = body
                topic = str(rev['SectionLabel'])
                temp_dict['topic'] = topic
                grade = str(rev['UserDisplayString'])
                temp_dict['user_grade'] = grade
                rating = str(rev['Rating']['Value'])
                temp_dict['rating'] = rating
                date = str(rev['ReadableDate'])
                temp_dict['date'] = date
                main_dict.append(temp_dict)
            print 'Finished page ' + str(page) + '/' + str(maxPages)
        page += 1

tFile.write(json.dumps(main_dict))

tFile.close()
