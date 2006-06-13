import re

# all the arguments should be validated to only contain letters, a dash and numbers
# Any characters outside of that range should be changed to '.'

# matches anything but alphanumeric, underscore, and dash
safe_arg_reg = re.compile('[^\w-]')

def sanitize_args(args):
	new_args = {}

	for k,v in args.iteritems():
		# Replace all non-safe chars with a period
		new_args[safe_arg_reg.sub(".", k)] =  safe_arg_reg.sub(".", v)

	return new_args
		

	
