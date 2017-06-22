#!/usr/bin/env python

###############################################
#
# airpods-airpods - I should buy airpods
# written by Mirai Kim (nachtbeere@outlook.com)
#
###############################################

import random
import requests
import lxml.html
import json
import re

from urllib.parse import urlparse, parse_qs

__version__ = '0.1.0'

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
            answers[seller] = YES if explain is YES else NO
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
    url = urlparse(source.url)
    par = parse_qs(url.query)
    resp = requests.get(
        'https://{0}/apps/schedule/entry'.format(url.netloc),
        headers={'referer': source.url, 'mosa-cid': par['link'][0]})
    data = lxml.etree.HTML(resp.text)\
                     .findall(".//script")[9]\
                     .text

    js = ''
    for line in data.split('\n'):
        if 'noticeJson =' in line:
            parse_line = re.sub(r'\s', '', line).split(',')
            js = ', '.join(parse_line[2:4])
            js = js.encode()\
                   .decode('unicode-escape')\
                   .encode('utf-8')\
                   .decode('utf-8')
    notice_json = json.loads(parse_qs(js)['noticeJson'][0])

    return YES if '에어팟' in notice_json['notice']['content']\
        or '신형맥북에어입고!!' not in notice_json['notice']['content'] else NO


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
    # _call_with_urls()
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
