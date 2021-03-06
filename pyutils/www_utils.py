import re

import Cookie
import time
import calendar
import re

# all the arguments should be validated to only contain letters, a dash and numbers
# Any characters outside of that range should be changed to '.'

# matches anything but alphanumeric, underscore, and dash
safe_arg_reg = re.compile('[^\w-]')

def sanitize_args(args):
	new_args = {}

	for k,v in args.iteritems():

		# Replace all non-safe chars with a period
		k = safe_arg_reg.sub(".", k)
		v = safe_arg_reg.sub(".", v)

		# Convert '..' parent dir to underscores
		k = k.replace("..", "__")
		v = v.replace("..", "__")

		new_args[k] = v

	return new_args
		

def get_tz_cookie(headers_in):
	"""Returns 0 if timezone isn't set, otherwise, return seconds difference for that timezone"""

	return_val = 0
        my_cookie = Cookie.SimpleCookie()

        if headers_in.has_key('Cookie'):
                my_cookie.load(headers_in['Cookie'])
		# workaround for firefox 3 (js probably doesn't work in ff3)
		if my_cookie.has_key('monobuild_tzo'):
			return_val = my_cookie['monobuild_tzo'].value

        return return_val

color_reg = re.compile("^([0:]+)")
def timecolor(duration):

	return color_reg.sub("<FONT class=cleanuptimecolor>\g<1></FONT>", duration, 1)

