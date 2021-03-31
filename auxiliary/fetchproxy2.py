import requests
from bs4 import BeautifulSoup
import tcp_latency
import subprocess
import serviceping
from ipaddress import ip_address
from urllib.parse import urlparse
from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException



def parse_ip_port(netloc):
    try:
        ip = ip_address(netloc)
        port = None
    except ValueError:
        parsed = urlparse('//{}'.format(netloc))
        ip = ip_address(parsed.hostname)
        port = parsed.port
    return ip, port


def ipInfo(addr=''):
    from urllib.request import urlopen
    from json import load
    if addr == '':
        url = 'https://ipinfo.io/json'
    else:
        url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    #response from url(if res==None then check connection)
    data = load(res)
    #will load the json response into data
    for attr in data.keys():
        #will print the data line by line
        print(attr,' '*13+'\t->\t',data[attr])

print("FETCH PROXY 2")
ports_url = 'http://spys.one/proxy-port/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}

soup = BeautifulSoup(requests.post(ports_url, headers=headers, data={'xpp': 5}).content, 'html.parser')
for f in soup.select('td[colspan="2"] > a > font.spy6'):
    u = 'http://spys.one/proxy-port/' + f.text + '/'
    s = BeautifulSoup(requests.post(u, headers=headers, data={'xpp': 5}).content, 'html.parser')
    for ff in s.select('tr > td:nth-child(1) > font.spy14'):
        print(ff.text)

''' 
for f in soup.select('td[colspan="2"] > a > font.spy6'):

    u = 'http://spys.one/proxy-port/' + f.text + '/'
    s = BeautifulSoup(requests.post(u, headers=headers, data={'xpp': 5}).content, 'html.parser')
    print("s: "+ u)
    #for ff in s.select('tr > td:nth-child(2) > font.spy1'):
    #    print("data2:" +  ff.text)
    for ff in s.select('tr > td:nth-child(1) > font.spy14'):
        print(ff.text)
        ip, port = parse_ip_port(ff.text)
        #print("{:39s} port={}".format(str(ip), port ))
        #print(serviceping.scan(str(ip),port))
        #ipInfo(str(ip))
       # print(serviceping.scan(ff.text))
        #print(tcp_latency.measure_latency("google.com"))
'''