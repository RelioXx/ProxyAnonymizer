import proxyscrape

#collector = proxyscrape.create_collector('default', 'http')  # Create a collector for http resources
#proxy = collector.get_proxy({'country': 'united states'})  # Retrieve a united states proxy

collector = proxyscrape.create_collector('my-collector', 'https')

# Retrieve any http proxy
proxy = collector.get_proxies()
print(proxy)