from anonymizer import Anonymizer
import requests
from stem import Signal
from stem.control import Controller

#with Controller.from_port(port = 9051) as controller:
#    controller.authenticate(password='your password set for tor controller port in torrc')
#    print("Success!")
#    controller.signal(Signal.NEWNYM)
#    print("New Tor connection processed")
#
#
#
#
#test_tor = {'http':["194.44.199.242:8080","49.0.65.4:8080","36.92.79.238:8080"]}

if __name__ == "__main__":


    res = requests.get('https://api.ipify.org/?format=text', proxies={'https': '183.89.65.48:8080'})
    print(res.text)
    #anon = Anonymizer(test_tor)
    #res = anon.get("http://whatsmyip.net/")
    ##Print Data obtained
    #print(res.text)




