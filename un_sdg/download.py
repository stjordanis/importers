import os

#curl_cmd = '''curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/octet-stream' -d 'goal=1&goal=2&goal=3&goal=4&goal=5&goal=6&goal=7&goal=8&goal=9&goal=10&goal=11&goal=12&goal=13&goal=14&goal=15&goal=16&goal=17' 'https://unstats.un.org/SDGAPI/v1/sdg/Goal/DataCSV'''

#subprocess()
#cmd = "ls -%s - %s"%(curl_cmd, INFILE)

os.system('''curl -X POST --header 'Content-Type: application/x-www-form-urlencoded' --header 'Accept: application/octet-stream' -d 'goal=1&goal=2&goal=3&goal=4&goal=5&goal=6&goal=7&goal=8&goal=9&goal=10&goal=11&goal=12&goal=13&goal=14&goal=15&goal=16&goal=17' 'https://unstats.un.org/SDGAPI/v1/sdg/Goal/DataCSV' >> input/un_sdg.csv''')

