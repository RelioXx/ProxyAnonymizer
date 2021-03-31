
import winreg
import ctypes
import sys
import platform

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