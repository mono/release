
releases = {
	'1.0':     {'release':'1.0',  'moonrev':'','monorev':''},
	'1.0.1':   {'release':'1.0',  'moonrev':'','monorev':''}, # Include 1.0 plugins
	'1.9.0':   {'release':'1.9.0',  'moonrev':'','monorev':''},
	'1.9.0.1': {'release':'1.9.0.1','moonrev':'','monorev':''},
	'1.9.1':   {'release':'1.9.1','moonrev':'133784','monorev':'133384'},
	'1.9.2':   {'release':'1.9.2','moonrev':'134227','monorev':'134208'},
	'1.9.3':   {'release':'1.9.3','moonrev':'135062','monorev':'135039'},
	'1.9.4':   {'release':'1.9.4','moonrev':'136014','monorev':'135866'},
	'1.9.5':   {'release':'1.9.5','moonrev':'136986','monorev':'136341'},
	'1.9.6':   {'release':'1.9.6','moonrev':'137711','monorev':'137279'},
	'1.99.1':  {'release':'1.99.1','moonrev':'139981','monorev':'139665'},
	'1.99.1.1':{'release':'1.99.1.1','moonrev':'','monorev':''}, # svn revs only matter when branching using ./branch_moonlight.py
	'1.99.2':  {'release':'1.99.2','moonrev':'140532','monorev':'140392'},
	'1.99.3':  {'release':'1.99.3','moonrev':'141147','monorev':'140963'},
}

latest = releases['1.99.3']

new_version = latest['release']

old_versions = releases.keys()
old_versions.sort()
old_versions.remove(latest['release'])
