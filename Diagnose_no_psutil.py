"""
Created on Fri Jun  8 19:22:30 2018

@author: Chanwoo Park
"""
import os 
import sys
import time
import sqlite3

from Domain import get_domain_dictionary

def get_browser_history(browser, path):
    browser = browser.lower()
        
    conn = sqlite3.connect(path)
    cursor = conn.cursor()
    
    sqlite_command = ''
    if browser == 'chrome':
        sqlite_command = """SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') AS last_visit_time, visit_count FROM urls ORDER BY last_visit_time DESC"""
    elif browser == 'firefox':
        sqlite_command = """SELECT url, title, datetime((visit_date/1000000), 'unixepoch', 'localtime') AS visit_date, visit_count FROM moz_places INNER JOIN moz_historyvisits on moz_historyvisits.place_id = moz_places.id ORDER BY visit_date DESC"""
    elif browser =='safari':
        sqlite_command = """SELECT url, title, datetime(visit_time + 978307200, 'unixepoch', 'localtime'), visit_count FROM history_visits INNER JOIN history_items ON history_items.id = history_visits.history_item ORDER BY visit_time DESC"""
    else:
        print('Error')
    
    cursor.execute(sqlite_command)
    urls_list = cursor.fetchall()
    # element in list is tuple
    
    conn.close()
    
    return urls_list

def get_browser_path_dict(user_platform):
    platform_code = platform_table[user_platform]
    browser_path_dict = dict()
    
    
    if platform_code == 1: # if it is a macOS 
        cwd_path = os.getcwd()
        cwd_path_list = cwd_path.split('/')
        
        abs_safari_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2],'Library', 'Safari', 'History.db')
        abs_chrome_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2],'Library', 'Application Support', 'Google/Chrome/Default','History')
        abs_firefox_path = os.path.join('/', cwd_path_list[1], cwd_path_list[2], 'Library', 'Application Support', 'Firefox/Profiles')

        if os.path.exists(abs_safari_path):
            browser_path_dict['safari'] = abs_safari_path
        
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
        
        if os.path.exists(abs_firefox_path):
            firefox_dir_list = os.listdir(abs_firefox_path)
            for f in firefox_dir_list:
                if f.find('.default') > 0 : 
                    abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
                    
            if os.path.exists(abs_firefox_path):
                browser_path_dict['firefox'] = abs_firefox_path
    
    
    if platform_code == 2: # if it is a windows
        
        homepath = os.path.expanduser("~")
        abs_chrome_path = os.path.join(homepath, 'AppData', 'Local', 'Google', 'Chrome', 'User Data', 'Default','History')
        abs_firefox_path = os.path.join(homepath, 'AppData', 'Roaming', 'Mozilla','Firefox', 'Profiles')
        
        if os.path.exists(abs_chrome_path):
            browser_path_dict['chrome'] = abs_chrome_path
        
        if os.path.exists(abs_firefox_path):
            firefox_dir_list = os.listdir(abs_firefox_path)
            for f in firefox_dir_list:
                if f.find('.default') > 0 : 
                    abs_firefox_path = os.path.join(abs_firefox_path, f, 'places.sqlite')
            
            if os.path.exists(abs_firefox_path):
                browser_path_dict['firefox'] = abs_firefox_path
               
    
    
    return browser_path_dict

def create_result_file(sorted_domain_list, filename, name_browser, external_string=''):
    intro_string = get_username(platform_code) + "'s " + 'Report Result of ' + str(name_browser[0]).upper() + name_browser[1:] + ' Browser History \n \n'
    intro_string += external_string + '\n'
    
    with open(filename, encoding='utf-8', mode='w+') as f:
        f.write(intro_string)
        for domain in sorted_domain_list:
            f.write(domain.__str__() + '\n')


def analyze_users_history(sorted_domain_list):
    total = 0
    for domain in sorted_domain_list[0:5]:
        total += domain.frequency
    
    non_top_total = 0
    for domain in sorted_domain_list[5:]:
        non_top_total += domain.frequency
    
    total += non_top_total
    
    top_domain_netloc_list = []
    top_domain_freq_list = []
    for i in range(5):
        top_domain_netloc_list.append(sorted_domain_list[i].domain_netloc)
        top_domain_freq_list.append(sorted_domain_list[i].frequency)

    top_domain_netloc_list.append('others')
    top_domain_freq_list.append(non_top_total)


    result_string = ''

    for i in range(len(top_domain_netloc_list)):
        result_string += top_domain_netloc_list[i] + ': ' + str(round((100*top_domain_freq_list[i]/total), 2)) + '%' + '\n'

    return result_string

def get_sorted_domains_by_freq(domain_list):
    sorted_domain_list = sorted(domain_list, key=lambda domain: domain.frequency, reverse=True)
    return sorted_domain_list

def get_username(platform_code):
    cwd_path = os.getcwd()
    cwd_path_list = []
    if platform_code == 1:
        cwd_path_list = cwd_path.split('/')
    elif platform_code == 2:
        cwd_path_list = cwd_path.split('\\')
        
    return cwd_path_list[2]


if __name__ == "__main__":
    
    print('Welcome to the DYB! (Dignose Your Browsers)\n')
    print('If you are using Google Chrome,')
    print('you MUST COMPLETELY close Chrome before running this program')
    time.sleep(5) 
    user_input = input('would you like to continue (Y/N)?\n')
    if user_input.lower() == 'y':
        time.sleep(1)          
    else:
        print('Bye Bye')
        exit()
    
    platform_table = dict()
    platform_table['linux2'] = 0
    platform_table['linux'] = 0
    platform_table['darwin'] = 1
    platform_table['cygwin'] = 2
    platform_table['win32'] = 2
    
    user_platform = sys.platform
    platform_code = platform_table[user_platform]
    user_name = get_username(platform_code)
    
    user_browser_path_dict = get_browser_path_dict(user_platform)
    # keys: name of browsers, values: the path to the browsers' databases;
    # the browser path will be determined by its users' OS system

    print('\n Analyzing the browser history and Creating files...')
    time.sleep(3)

    for key in user_browser_path_dict :
        filename = 'report_' + key + '_result.txt'
        browser_history_list = get_browser_history(key, user_browser_path_dict[key]) 
        #keys: names of domain, values: domain objects that contain detail of the domain, such as their subdomains 
        #and other informations
        domains_dictionary = get_domain_dictionary(browser_history_list)
        sorted_domain_list = get_sorted_domains_by_freq(domains_dictionary.values())
        report_analysis = analyze_users_history(sorted_domain_list)

        create_result_file(sorted_domain_list, filename, key, report_analysis)

    print(' FILES ARE SUCCESSFULLY CREATED. Pleace check your current working directory.')
