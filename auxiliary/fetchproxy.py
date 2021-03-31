#Fetching proxy information from windows registry for use in Requests python module.
import winreg
import requests

def get_internet_key(name):
    ie_settings = winreg.OpenKey(winreg.HKEY_CURRENT_USER,r'Software\Microsoft\Windows\CurrentVersion\Internet Settings',0, winreg.KEY_ALL_ACCESS)
    value, type = winreg.QueryValueEx(ie_settings, name)
    return value

def hasInternetProxy():
    """Returns boolean. If key doesn't exist, returns false."""
    if get_internet_key('ProxyEnable') == 1:
        return True
    else:
        return False

def getProxyAddresses():
    """Returns dictionary of protocol:address key:value pairs."""
    proxies = {}
    if hasInternetProxy():
        rawStr = get_internet_key("ProxyServer")
        separated = rawStr.split(";")
        if len(separated) == 1:
            proxies["all"] = separated[0]
        else:
            for single_proxy in separated:
                protocol,address = single_proxy.split("=")
                proxies[protocol] = address
            if 'all' not in list(proxies.keys()) and 'http' in list(proxies.keys()):
                proxies['all'] = proxies["http"]
    return proxies

if hasInternetProxy():
    proxies = getProxyAddresses()
    print("proxies:",proxies)
    user_agent = "GItHub GIST Example"
    headers = {'user-agent':user_agent}
    response = requests.get("https://www.google.com", headers=headers, proxies=proxies)
    print(response)
else:
    print("No Proxy!!")
''' 
if __name__ == '__main__':
    print(hasInternetProxy())
    print(getProxyAddresses())
    '''