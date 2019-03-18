from http.cookiejar import MozillaCookieJar
from splinter import Browser

import time
from itertools import count
from urllib import parse

BROWSER = 'chrome'
HEADLESS = True
# HEADLESS = not True

cookies = MozillaCookieJar('D:/fb.cook')
cookies.load()

SAVED_PAGE_URL = "https://www.facebook.com/saved/all"
MORE_PAGER_SELECTOR = '#content_container div.uiMorePager a[href]'
LINKS_SELECTOR = '#content_container #saveContentFragment div._ikh div._4bl9._5yjp'

SCROLL_DELAY_TIME = .5

def cookie_browser(cookies):
    browser = Browser(BROWSER, headless=HEADLESS)
    if BROWSER == 'chrome':
        browser.visit('https://fb.me') # Fix Needed for setting cookies in chrome
    
    for c in cookies:
        browser.cookies.driver.add_cookie({'name': c.name, 'value': c.value, 'path': c.path, 'expiry': c.expires})

    browser.scroll_to_bottom = lambda:browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')

    return browser

def fetch_all_saved_links(bro):
		bro.visit(SAVED_PAGE_URL)
		for i in count(1):
			time.sleep(SCROLL_DELAY_TIME)
			bro.scroll_to_bottom()
			if bro.is_element_not_present_by_css(MORE_PAGER_SELECTOR):break
			print('|', end='')
		print(' Loaded!')
		print('='*50)

		links = bro.find_by_css(LINKS_SELECTOR)
		return links


# ConnectionRefusedError
with cookie_browser(cookies) as bro:
	links = fetch_all_saved_links(bro)
	for i, link in enumerate(links):
			url = link.find_by_css('a[href]')['href']
			u = parse.urlparse(url)
			if u.netloc=='l.facebook.com':url = dict(parse.parse_qsl(u.query)).get('u', url)
			# if 'fbclid' in url:u = parse.urlparse(url)

			print(i, url)
			print(link.value)
			print('-'*50)