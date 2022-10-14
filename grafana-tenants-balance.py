#This script uses web scraping to get info about number of used tenants in grafana labs at anytime.
#since this feature is missing via grafana lab api.

from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


URL = 'https://grafana.com/'
LOGIN_ROUTE = 'api/login'
HEADERS = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36', 'origin': URL, 'referer': URL + LOGIN_ROUTE}

s = requests.session()

login_payload = { 'login': '<username>' ,'password': '<password>' } #replace placeholders with your credentials

login_req = s.post(URL + LOGIN_ROUTE, headers=HEADERS, data=login_payload)

# print(login_req.status_code)

cookies = login_req.cookies

soup = bs(s.get(URL + 'orgs/<org_name>').text, 'html.parser') #replace placeholders with your org name
a_href=soup.findAll("h2",{"class":"css-26cz0"}.get("css-26cz0"))
customers=[]
count = 0
list(a_href)
for item in a_href:
    customers.append(str(item).split(">")[1].split("<")[0])
    count +=1
customers.remove('Grafana Cloud Portal')
customers.remove('You are currently subscribed to ')
count = count - 2 #calulates the number of tenants in grafana
print(f"{bcolors.OKGREEN}Runai organization has {count} tenants in use!{bcolors.ENDC}")
grafana_tenants_limit=150 #fixed quota in GrafanaLab
grafana_tenants=(grafana_tenants_limit - count) 
print(f"{bcolors.WARNING}Your organization has {grafana_tenants} free available tenants in GrafanaLab{bcolors.ENDC}")
question=input("Do you want to search for a tenant exist?(y/n)") #optional to check if tenants exist in grafana lab
if question == "y":
    cusomter="<org>"+input('Please provide a tenant name:\n') #adding org prefix to any tenant #replace with your org
    if cusomter in customers:
        print("tenant exist!")
    else:
        print("tenant is not exist in GrafanaLab!")


        


    




