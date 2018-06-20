"""
Created on Sun Jun 10 08:33:07 2018

@author: kcp
"""

from urllib.parse import urlparse

def get_domain_dictionary(browser_history_list):
    d_dictionary = dict()
    
    for domain_data in browser_history_list: # in tuple
        netloc_name = _get_netloc(domain_data[0])
        if netloc_name not in d_dictionary.keys():
            new_domain = Domain(domain_data)
            d_dictionary[netloc_name] = new_domain
        else:
            domain_object = d_dictionary[netloc_name]
            domain_object.add_domain(domain_data)
    
    return d_dictionary

def _get_netloc(url):
        parse_result = urlparse(url)
        return parse_result.netloc


class Domain(object):
    
    def __init__(self, domain_data): #tuple
        
        self.domain_netloc = self.get_netloc(domain_data[0])
        self.frequency = domain_data[3]
        self.list_domain_data = [domain_data]
    
    def get_netloc(self, url):
        parse_result = urlparse(url)
        return parse_result.netloc
    
    def add_domain(self, domain_data):
        self.list_domain_data.append(domain_data)
        self.frequency += domain_data[3]
    
    def __str__(self):
        s = 'main_domain: ' + self.domain_netloc + '\n' + 'frequency: ' + str(self.frequency) + '\n'
        s += 'subdomains: \n'
        for subdomain in self.list_domain_data:
                
            s += '\t' + self.string_title(str(subdomain[1])) + '\n'
            s += '\t' + subdomain[2] + '\n'

        return s

    def string_title(self, s):
        if s  == '':
            return 'None'
        else:
            return s


    
        
    
    
    
        
        
