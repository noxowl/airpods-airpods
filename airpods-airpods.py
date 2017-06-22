#!/usr/bin/env python

###############################################
#
# airpods-airpods - I should buy airpods
# written by Mirai Kim (nachtbeere@outlook.com)
#
###############################################

__version__ = '0.1.0'

import html
import random
import dryscrape
import requests
import lxml.html


YES = True
NO = False

USER_AGENTS = (
    'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1',
    'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0',
    ('Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/41.0.2228.0 Safari/537.36'),
    ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) '
        'AppleWebKit/537.75.14 (KHTML, like Gecko) '
        'Version/7.0.3 Safari/7046A194A'),
    ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/42.0.2311.135 Safari/537.36 Edge/12.246')
    )

PERSONAL_URLS = ['']
SELLERS_URLS = {
    'example_seller': 'https://example.com',
    'willys_worldtower': 'https://willyswt.modoo.at/?link=14qdxv1z'
}

answers = {}
messages = ''


def _call_sellers():
    for seller, url in SELLERS_URLS.items():
        try:
            resp = requests.get(url, headers={
                    'User-Agent': random.choice(USER_AGENTS)
                    })
            if not resp.status_code // 100 == 2:
                print("Seller status exception.\n{0}"
                      .format(resp.status_code))
                answers[seller] = NO
        except requests.exceptions.RequestException as e:
            print("Seller call exception.\n{0}"
                  .format(e))
            answers[seller] = NO
        else:
            explain = _what_you_say(resp) 
            if explain is not YES:
                answers[seller] = NO
            else:
                answers[seller] = YES
    return answers


def _what_you_say(conversation):
    if 'modoo' in conversation.url:
        result = _translating_modoo(conversation)
    else:
        result = NO
    return result


def _translating_modoo(source):
    """
    Fuck javascript-generated page.
    """
    session = dryscrape.Session()
    session.set_attribute('auto_load_images', False)
    session.set_attribute('plugins_enabled', True)
    session.visit(source.url)
    resp = session.body()

    data = lxml.html.fromstring(resp)\
                    .xpath('.//div[contains(@class, "fc_content")]')
    page = lxml.html.fromstring(lxml.html.tostring(data[0]).decode('utf-8'))
    print(html.unescape(lxml.html.tostring(data[0]).decode('utf-8')))
    return False


def _is_sell_it_now(answers):
    """
    Plz
    """
    for seller, answer in answers.items():
        if answer is YES:
            return YES
    else:
        return NO


def _call_myself():
    """
    Add your calling methods.
    """
    #_call_with_urls()
    print('call myself')
    

def _call_with_urls():
    for url in PERSONAL_URLS:
        try:
            requests.get(url)
        except requests.exceptions.RequestException:
            print('Missed call!')


def i_should_buy_airpods():
    phone_calls = _call_sellers()

    if _is_sell_it_now(phone_calls):
        _call_myself()


if __name__ == '__main__':
    i_should_buy_airpods()
