import pandas as pd
import requests
from lxml import html
from typing import List
import sys
from datetime import datetime


def wiki_check(link_list, cutoff_length):
    """
    Navigates to the wikepedia page and determines how many words there are in the profile. This is meant to help
    find the birthdays of the most popular figures. Returns list of names where the wikipedia page
    is longer than the cutoff length
    :param link_list: list of links to navigate to and find the number of words
    :param cutoff_length: the cutoff for number of words in the wikipedia page to be included in the birthday list
    :return:
    """
    length_list = []
    xpath_body_text = ('//div[@class="mw-body-content"]//text()')
    xpath_person_table = ('//table[@class="infobox vcard plainlist"]//text() | \
                          //table[@class="infobox vcard"]//text() | //table[@class="infobox biography vcard"]//text() |\
                           //table[@class="infobox bordered vcard"]//text()')
    for index, link in enumerate(link_list):
        page = requests.get(link)
        doc = html.fromstring(page.content)
        raw_xpath_body_text = doc.xpath(xpath_body_text)
        raw_xpath_person = doc.xpath(xpath_person_table)
        if len(raw_xpath_body_text) >= cutoff_length:
            if 'Born' in raw_xpath_person or 'Born:' in raw_xpath_person or 'Date of birth' in raw_xpath_person:
                length_list.append(index)
    return length_list


def clean_other_names(name_list):
    """
    cleaning birthday entries where the year is not a link (2nd, 3rd, 4th birthdays in a year)
    :param name_list: list of names
    :return:
    """
    # throw anything out with a length <5, exception for 4 letter names
    # throw out end wikipedia info at the end
    # make sure we are not taking in years or AD years
    filtered_name_list = [name for name in name_list if len(name) > 4 or not name[0].isdigit()]
    filtered_name_list = [name for name in filtered_name_list if name[0:3] != 'AD ']
    filtered_name_list = filtered_name_list[:-8]
    return filtered_name_list



def clean_other_links(link_list):
    """
    clearning birthday links where the year is not a link (2nd, 3rd, 4th birthdays in a year)
    :param link_list: list of wiki links
    :return:
    """
    # throw anything out with a length <11
    # throw out cite notes
    # throw out end wikipedia info at the end
    filtered_link_list = [link for link in link_list if len(link) > 10 or not link[6].isdigit()]
    filtered_link_list = [link for link in filtered_link_list if link[0] != '#' and link[6:8] != 'AD']
    filtered_link_list = filtered_link_list[:-8]
    return filtered_link_list


def clean_check(name_list, link_list):
    """
    This goes and checks that there are not any offsets. Both the name list and the link lists should be the same length
    :param name_list:
    :param link_list:
    :return:
    """
    # making sure there are not offsets, if so stop the run
    try:
        if len(name_list) != len(link_list):
            raise ValueError('Length of data retrieved is offset')
    except (ValueError):
        exit('Length of data retrived is offset')
    return name_list, link_list

def parser(month_day):
    """
    Parses raw html with xpath to get desired variables. Gets raw xpath parsed html and cleans it. Returns
    clean events
    :param month_day: string of month and day
    :return:
    """
    full_url = f'https://en.wikipedia.org/wiki/{month_day}#Births'
    #no logs yet because I'm lazy
    print(full_url)
    # make request to wiki
    page = requests.get(full_url)
    doc = html.fromstring(page.content)
    # use xpath to grab pattern of wiki
    # first grab every second link after the year
    xpath_name_first = ('//ul[2]//li/a[2]/text()')
    xpath_link_first = ('//ul[2]//li/a[2]//@href')

    # there are case where the year is not a link and we need to grab the first link we see
    xpath_name_others = ('//ul[2]//li/a[1]/text()')
    xpath_link_others = ('//ul[2]//li/a[1]//@href')

    #returning xpath lists
    raw_xpath_first = doc.xpath(xpath_name_first)
    raw_xpath_link_first = doc.xpath(xpath_link_first)
    raw_xpath_others = doc.xpath(xpath_name_others)
    raw_xpath_link_others = doc.xpath(xpath_link_others)

    #doing some good ole' fashioned data cleaning
    other_names = clean_other_names(raw_xpath_others)
    other_links = clean_other_links(raw_xpath_link_others)

    # Temporary error checking
    ### TO-DO add actual error catching and logging
    # Debugging code I'm leaving in for now
    print(len(raw_xpath_first))
    print(len(raw_xpath_link_first))
    print(len(other_names))
    print(len(other_links))
    for index, value in enumerate(raw_xpath_first):
        print(f"{index}: {value}")
    for index, value in enumerate(raw_xpath_link_first):
        print(f"{index}: {value}")
    for index, value in enumerate(other_names):
        print(f"{index}: {value}")
    for index, value in enumerate(other_links):
        print(f"{index}: {value}")
    # End debug code
    first_names, first_links = clean_check(raw_xpath_first, raw_xpath_link_first)
    other_names, other_links = clean_check(other_names, other_links)


    #combing the lists
    all_names = first_names + other_names
    all_links = first_links + other_links

    url = 'https://en.wikipedia.org/'
    formatted_all_links = [f"{url}{link}" for link in all_links]

    #We only want to gtab names with wikipedia pages longer than 3,000 words
    keep_index = wiki_check(formatted_all_links, 3250)

    keep_names = []
    keep_links = []
    for index in keep_index:
        keep_names.append(all_names[index])
        keep_links.append(formatted_all_links[index])

    print('Creating dataframe')
    #create a dataframe with the names and link of the people we want to keep
    df = pd.DataFrame(list(zip(keep_names, keep_links)), columns=['name', 'URL'])
    return df

def main():
    month_dict = {
        'January': 31,
        'February': 28,
        'March': 31,
        'April': 30,
        'May': 31,
        'June': 30,
        'July': 31,
        'August': 31,
        'September': 30
    }
    for key in month_dict:
        month = key
        last_day = month_dict[key]
        for day in range(1, last_day+1):
            month_day = f"{month}_{day}"
            formatted_month_day = f"{month} {day} 2020"
            date = datetime.strptime(formatted_month_day, '%B %d %Y')
            print(date)
            birthdays = parser(month_day)
            birthdays['string_date'] = month_day
            birthdays['birthday'] = date
            birthdays.to_csv(f'birthdays/{month_day}.csv', index=False)


if __name__ == '__main__':
    main()
