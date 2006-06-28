#!/usr/bin/env python

import Cookie
import time
import calendar

def index(req, **vars):
        return "Hello world!"



def hello2(req, **vars):

        return_string = ""
        for key in vars:
                return_string += vars[key]

        return return_string

def cookie_tztest(req, **vars):

	my_cookie = Cookie.SimpleCookie()

        return_string = time.asctime(time.gmtime())

	req.content_type = "text/html"

	if req.headers_in.has_key('Cookie'):
		my_cookie.load(req.headers_in['Cookie'])
		tzo_seconds = my_cookie['monobuild_tzo'].value
		timestamp = time.asctime(time.gmtime())

		seconds_past_epoch = calendar.timegm(time.strptime(timestamp))
		seconds_past_epoch += int(tzo_seconds)
		return_string = time.asctime(time.gmtime(seconds_past_epoch))

	return return_string

