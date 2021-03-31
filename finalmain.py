
import socket
import select
import threading
import time
import sys
import winreg
from random import choice

from Proxy_List_Scrapper import Scrapper, Proxy, ScrapperException
from ipaddress import ip_address
from urllib.parse import urlparse
import sys
import requests
from bs4 import BeautifulSoup
import platform
import ctypes
from torpy import TorClient
import requests
from stem import Signal
from stem.control import Controller
from random import randrange
import proxyscrape
import pathlib
import subprocess

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
#PROBAR PAGINAS CON https://ifconfig.me/ https://wtfismyip.com/text
buffer_size = 4096
delay = 0.0001
forward_to = ('3.211.17.212', 8080)

data= None
ipproxy= []
portproxy= []
proxylist= []
randomn = 0
tor =  False

request_headers = None

class Forward:
    def __init__(self):
        self.forward = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self, host, port):
        try:
            self.forward.connect((host, port))
            return self.forward
        except Exception as e:
            print(e)
            return False

def set_RandomHeaders():
    '''
        Select a random headers from a list and asings it to the the connection
    '''
    ##User Agent
    global  request_headers

    user_agents_list=[]
    user_agents_list.append('Mozilla/5.0 (iPhone; U; CPU iOS 2_0 like Mac OS X; en-us)')
    user_agents_list.append('Mozilla/5.0 (Linux; U; Android 0.5; en-us)')
    user_agents_list.append('Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko)')
    user_agents_list.append('Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)')
    user_agents_list.append('Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)')
    user_agents_list.append('Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US) AppleWebKit/525.13 (KHTML, like Gecko) Chrome/0.2.149.29 Safari/525.13')
    user_agents_list.append('Opera/9.25 (Windows NT 6.0; U; en)')
    user_agents_list.append('Opera/9.80 (X11; Linux x86_64; U; pl) Presto/2.7.62 Version/11.00')
    user_agents_list.append('Opera/9.80 (Windows NT 6.0; U; en) Presto/2.7.39 Version/11.00')
    user_agents_list.append('Mozilla/5.0 (Windows NT 6.0; U; ja; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00')
    user_agents_list.append('Mozilla/4.0 (compatible; MSIE 8.0; X11; Linux x86_64; pl) Opera 11.00')
    user_agents_list.append('Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; fr) Opera 11.00')
    user_agents_list.append('Opera/9.80 (Windows NT 6.1 x64; U; en) Presto/2.7.62 Version/11.00')
    user_agents_list.append('Mozilla/5.0 (Windows NT 5.1; U; de; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6 Opera 11.00')
    user_agents_list.append('Mozilla/4.0 (compatible; MSIE 8.0; X11; Linux x86_64; pl) Opera 11.00')

    user_agent = choice(user_agents_list).strip()

    ##Language

    accept_language_list=[]
    accept_language_list.append('de-de,es-es;q=0.8,en-us;q=0.5,en;q=0.3')
    accept_language_list.append('en-us;q=0.8,en;q=0.3')
    accept_language_list.append('es;q=0.8,en-us;q=0.5,en;q=0.3')
    accept_language_list.append('es-es;q=0.8,en;q=0.3')
    accept_language_list.append('de-de;q=0.8,en;q=0.3')
    accept_language_list.append('de-de;q=0.8,en-us;q=0.5)')

    language = choice(accept_language_list).strip()

    request_headers = {'User-Agent': user_agent, 'Accept-Language':language, 'Referer': ''}

def changeip():
    global randomn
    threading.Timer(5.0, changeip).start()
    randomn = (randrange(len(proxylist)))

def renewiptor():
    threading.Timer(20.0, renewiptor).start()
    renew_connection()


class TheServer:
    input_list = []
    channel = {}

    def __init__(self, host, port):
        self.s = None
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server.bind((host, port))
        self.server.listen(200)

    def main_loop(self):
        self.input_list.append(self.server)
        while 1:
            time.sleep(delay)
            ss = select.select
            inputready, outputready, exceptready = ss(self.input_list, [], [])
            for self.s in inputready:
                if self.s == self.server:
                    self.on_accept()
                    break

                self.data = self.s.recv(buffer_size)
                if len(self.data) == 0:
                    self.on_close()
                    break
                else:
                    self.on_recv()

    def on_accept(self):
        ###get random number from 0 to max#
        randomn = (randrange(len(proxylist)))
        forward = Forward().start(str(proxylist[randomn][0]), int(proxylist[randomn][1]))
        #forward = Forward().start('129.21.132.176',8080)
        print("peticion recibida")
        print("Petition forwarded with IP: "+ str(proxylist[randomn][0]) +":" + str(proxylist[randomn][1] ))
        clientsock, clientaddr = self.server.accept()
        if forward:
            print(clientaddr, "has connected")
            self.input_list.append(clientsock)
            self.input_list.append(forward)
            self.channel[clientsock] = forward
            self.channel[forward] = clientsock
        else:
            print("Can't establish connection with remote server.", end=' ')
            print("Closing connection with client side", clientaddr)
            clientsock.close()

    def on_close(self):
        print(self.s.getpeername(), "has disconnected")
        # remove objects from input_list
        self.input_list.remove(self.s)
        self.input_list.remove(self.channel[self.s])
        out = self.channel[self.s]
        # close the connection with client
        self.channel[out].close()  # equivalent to do self.s.close()
        # close the connection with remote server
        self.channel[self.s].close()
        # delete both objects from channel dict
        del self.channel[out]
        del self.channel[self.s]

    def on_recv(self):
        data = self.data
        # here we can parse and/or modify the data before send forward
        print(data)
        self.channel[self.s].send(data)

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

def changeproxy():
    system = platform.system()

    if system != "Windows":
        raise Exception("OS type not supported")

    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                       r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                       0, winreg.KEY_ALL_ACCESS)

    def set_key(name, value, type):
        winreg.SetValueEx(INTERNET_SETTINGS, name, 0, type, value)
    """"
    if sys.argv[1] == "off":
        set_key('ProxyEnable', 0, winreg.REG_DWORD)
    else:
        set_key('ProxyEnable', 1, winreg.REG_DWORD)
        set_key('ProxyServer', sys.argv[2], winreg.REG_SZ)
    """

    set_key('ProxyEnable', 1, winreg.REG_DWORD)
    set_key('ProxyHttp1.1', 1, winreg.REG_DWORD)
    #set_key('ProxyServer', "127.0.0.1:3000", winreg.REG_SZ)
    set_key('ProxyServer', "https=127.0.0.1:33333", winreg.REG_SZ) #set-itemproperty -path "hkcu:Software\Microsoft\Windows\CurrentVersion\Internet Settings" -name ProxyServer -value "http=proxy-url:port;https=proxy-url:port;ftp=proxy-url:port;socks=proxy-url:port;" -type string

    INTERNET_OPTION_REFRESH = 37
    INTERNET_OPTION_SETTINGS_CHANGED = 39

    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)


def getproxy():
    SSL = 'https://www.sslproxies.org/',
    GOOGLE = 'https://www.google-proxy.net/',
    ANANY = 'https://free-proxy-list.net/anonymous-proxy.html',
    UK = 'https://free-proxy-list.net/uk-proxy.html',
    US = 'https://www.us-proxy.org/',
    NEW = 'https://free-proxy-list.net/',
    SPYS_ME = 'http://spys.me/proxy.txt',
    PROXYSCRAPE = 'https://api.proxyscrape.com/?request=getproxies&proxytype=all&country=all&ssl=all&anonymity=all',
    PROXYNOVA = 'https://www.proxynova.com/proxy-server-list/'
    PROXYLIST_DOWNLOAD_HTTP = 'https://www.proxy-list.download/HTTP'
    PROXYLIST_DOWNLOAD_HTTPS = 'https://www.proxy-list.download/HTTPS'
    PROXYLIST_DOWNLOAD_SOCKS4 = 'https://www.proxy-list.download/SOCKS4'
    PROXYLIST_DOWNLOAD_SOCKS5 = 'https://www.proxy-list.download/SOCKS5'
    ALL = 'ALL'
    Category="PROXYLIST_DOWNLOAD_HTTPS"
    scrapper = Scrapper(category=Category, print_err_trace=False)
    # Get ALL Proxies According to your Choice
    data = scrapper.getProxies()
    # Print These Scrapped Proxies
    print("Scrapped Proxies:")
    for item in data.proxies:
        ipproxy.append((item.ip, int(item.port)) )#ipproxy.append('{}:{}'.format(item.ip, item.port))
        print('{}:{}'.format(item.ip, item.port))

    print("Print shit: ")
    #print(int(ipproxy[0][1]))
    #print(ipproxy[0][1] is int)
    # Print the size of proxies scrapped
    print("Total Proxies")
    print(data.len)
    # Print the Category of proxy from which you scrapped
    print("Category of the Proxy")
    print(data.category)



###Not implemented###
'''
ports_url = 'http://spys.one/proxy-port/'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0'}

soup = BeautifulSoup(requests.post(ports_url, headers=headers, data={'xpp': 5}).content, 'html.parser')
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


###WINDOWS PROXY###

###TOR Normal IMPLEMENTATION###
# signal TOR for a new connection
def renew_connection():
    print("Renovando IP de TOR")
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="passwordalvaro")
        controller.signal(Signal.NEWNYM)
        controller.close()



def get_tor_session():
    session = requests.session()
    # Tor uses the 9050 port as the default socks port
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050',
                       'socks': 'socks5://127.0.0.1:9050',
                       'socks4': 'socks5://127.0.0.1:9050',
                       'socks5': 'socks5://127.0.0.1:9050'}
    return session

# Make a request through the Tor connection
# IP visible through Tor
def torpyrequest():
    session = get_tor_session()
    print(session.get("http://httpbin.org/ip").text)
    # Above should print an IP different than your public IP
    renew_connection()
    print(session.get("http://httpbin.org/ip").text)
    # Following prints your normal public IP
    print(requests.get("http://httpbin.org/ip").text)

###TORPY IMPLEMENTATION###
def torpyrequest():
    hostname = 'ifconfig.me'  # It's possible use onion hostname here as well
    with TorClient() as tor:
        # Choose random guard node and create 3-hops circuit

        with tor.create_circuit(3) as circuit:
            # Create tor stream to host

            with circuit.create_stream((hostname, 80)) as stream:
                # Now we can communicate with host
                stream.send(b'GET / HTTP/1.0\r\nHost: %s\r\n\r\n' % hostname.encode())
                recv = stream.recv(1024)
                print(recv)


###normal requests implementation###
def normalrequest():
    #test_tor = {'http':["194.44.199.242:8080","49.0.65.4:8080","36.92.79.238:8080"]}

    proxies = {

        'https': '176.9.75.42:1080',
    }

    res = requests.get('https://www.whatismyip.com/', proxies=proxies)
    print(res.text)

def proxyelements():
    #https
    httpsproxy = []
    for i in proxylist:
        if proxylist[i][5] == 'https':
            httpsproxy.append(proxylist[i])
    print("Printeando Servidores https")
    print(httpsproxy)

def getproxies3():
    global proxylist
    collector = proxyscrape.create_collector('my-collector', 'https')

    # Retrieve any http proxy
    proxylist = collector.get_proxies({'type':'https'})

    print(proxylist)
    print("Se encontraron "+ str(len(proxylist)) +" proxies")
def initialtasks():
    system = platform.system()

    if system != "Windows":
        raise Exception("OS type not supported")

    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                       r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                       0, winreg.KEY_ALL_ACCESS)

    def set_key(name, value, type):
        winreg.SetValueEx(INTERNET_SETTINGS, name, 0, type, value)

    set_key('ProxyEnable', 0, winreg.REG_DWORD)
    #set_key('ProxyHttp1.1', 1, winreg.REG_DWORD)
    #set_key('ProxyServer', "127.0.0.1:3000", winreg.REG_SZ)
    #set_key('ProxyServer', "https=127.0.0.1:33333", winreg.REG_SZ) #set-itemproperty -path "hkcu:Software\Microsoft\Windows\CurrentVersion\Internet Settings" -name ProxyServer -value "http=proxy-url:port;https=proxy-url:port;ftp=proxy-url:port;socks=proxy-url:port;" -type string

    INTERNET_OPTION_REFRESH = 37
    INTERNET_OPTION_SETTINGS_CHANGED = 39

    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW

    internet_set_option(0, INTERNET_OPTION_REFRESH, 0, 0)
    internet_set_option(0, INTERNET_OPTION_SETTINGS_CHANGED, 0, 0)

def torproxy():
    print("Debes poner en: "+ str(pathlib.Path(__file__).parent.absolute()) + " la carpeta de tor")
    print("Abriendo tor")

    #torport = input("Inserte el puerto de TOR (En blanco se cogera 9050 por defecto)")
    subprocess.Popen([r"./Tor/tor.exe"])
    time.sleep(5)
    print("####TOR ABIERTO#####")
    #torport = input("Inserte el puerto de TOR (En blanco se cogera 9050 por defecto)")

    system = platform.system()

    if system != "Windows":
        raise Exception("OS type not supported")

    INTERNET_SETTINGS = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                                       r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',
                                       0, winreg.KEY_ALL_ACCESS)

    def set_key(name, value, type):
        winreg.SetValueEx(INTERNET_SETTINGS, name, 0, type, value)
    set_key('ProxyEnable', 1, winreg.REG_DWORD)
    set_key('ProxyHttp1.1', 1, winreg.REG_DWORD)
    #set_key('ProxyServer', "127.0.0.1:3000", winreg.REG_SZ)
    set_key('ProxyServer', "socks=127.0.0.1:9050", winreg.REG_SZ) #set-itemproperty -path "hkcu:Software\Microsoft\Windows\CurrentVersion\Internet Settings" -name ProxyServer -value "http=proxy-url:port;https=proxy-url:port;ftp=proxy-url:port;socks=proxy-url:port;" -type string

    INTERNET_OPTION_REFRESH = 37
    INTERNET_OPTION_SETTINGS_CHANGED = 39

    internet_set_option = ctypes.windll.Wininet.InternetSetOptionW
    renewiptor()
    input("Pulsa enter para finalizar")
    set_key('ProxyEnable', 0, winreg.REG_DWORD)
    sys.exit(1)

def globalproxy():
    initialtasks()
    getproxies3()

    changeproxy()
    server = TheServer('localhost', 33333)
    try:
        #changeip()
        server.main_loop()
    except KeyboardInterrupt:
        print("Ctrl C - Stopping server")
        sys.exit(1)

    sys.exit(1)

def torrequestsimp():
    print("Debes poner en: "+ str(pathlib.Path(__file__).parent.absolute()) + " la carpeta de tor")
    print("Abriendo tor")

    #torport = input("Inserte el puerto de TOR (En blanco se cogera 9050 por defecto)")
    subprocess.Popen([r"./Tor/tor.exe"])
    time.sleep(5)
    print("####TOR ABIERTO#####")
    #torport = input("Inserte el puerto de TOR (En blanco se cogera 9050 por defecto)")

    session = get_tor_session()


    while(1):
        peticion = input("Introduzca la peticion que quiere enviar: ")
        try:
            print(session.get(peticion).text)
            renew_connection()
        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)

def proxymodimp():
    getproxies3()
    print("Proxies recibidos")
    while(1):
        peticion = input("Introduzca la peticion que quiere enviar: ")
        try:
            randomn = (randrange(len(proxylist)))
            set_RandomHeaders()
            print("Peticion del proxy: ")
            print('https: ' +str("'") + str(proxylist[randomn][0]) +":" + str(proxylist[randomn][1]) +str("'"))
            res = requests.get(peticion, proxies={'https':  str(proxylist[randomn][0]) +":" + str(proxylist[randomn][1])}, headers=request_headers)
            print("Petition forwarded with IP: "+ str(proxylist[randomn][0]) +":" + str(proxylist[randomn][1] ))
            print(res.text)

        except KeyboardInterrupt:
            print("Ctrl C - Stopping server")
            sys.exit(1)
#################START#####################


print("ProxyWizard Creado Por Álvaro Puente")
print("ProxyWizard utiliza la RED de TOR y es capaz de utilizar Proxies")
print("Puedes descargar el codigo fuente de TOR a través de el siguiente LINK: https://www.torproject.org/dist/torbrowser/10.0.15/tor-win32-0.4.5.7.zip")
print("Para configuar TOR puedes ")
print("Para utilizar la Red de tor debes dejar torrc en la raiz de la carpeta de este programa")
#print("¿Que puerto deseas abrir para crear el servidor Proxy?")
#port = input()

#print("¿Que puerto deseas abrir para crear el servidor Proxy? (Introduce un número)")
#print("Deseas tener un proxy")
#print("¿Tienes instalado Torrc? Y/N")
#s = input()
#Seleccionando SI

#Seleccionando NO
print("\n\n-->Selecciona la opción que quieres usar:")
print("################################################################")
print("1-TOR")
print("2-proxies")
print("################################################################")
opcion1 = input("Pulsa 1 o 2 y dale a enter:")

print("\n\n-->Selecciona la opción que quieres usar:")
print("################################################################")
print("1-Configurarlo para usarlo en todo el ordenador")
print("2-Modulo requests")
print("################################################################")
opcion2 = input("Pulsa 1 o 2 y dale a enter:")

if (opcion1=="1" and opcion2=="1"):
    torproxy()

if(opcion1=="2" and opcion2=="1"):
    globalproxy()

if(opcion1=="1" and opcion2=="2"):
    torrequestsimp()

if(opcion1=="2" and opcion2=="2"):
    proxymodimp()


