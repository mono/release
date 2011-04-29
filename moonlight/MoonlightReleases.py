
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
	'1.99.4':  {'release':'1.99.4','moonrev':'142036','monorev':'141690'},
	'1.99.5':  {'release':'1.99.5','moonrev':'142349','monorev':'142338'},
	'1.99.6':  {'release':'1.99.6','moonrev':'144031','monorev':'143653'},
	'1.99.7':  {'release':'1.99.7','moonrev':'144534','monorev':'144471'},
	'1.99.8':  {'release':'1.99.8','moonrev':'145925','monorev':'145773'},
	'1.99.9':  {'release':'1.99.9','moonrev':'','monorev':''},
	'2.0':  {'release':'2.0','moonrev':'','monorev':''},
	'2.1':  {'release':'2.1','moonrev':'','monorev':''},
	'2.2':  {'release':'2.2','moonrev':'','monorev':''},
	'2.3':  {'release':'2.3','moonrev':'','monorev':''},
	'2.3.0.1':  {'release':'2.3.0.1','moonrev':'','monorev':''},
	'2.4':  {'release':'2.4','moonrev':'','monorev':''},
	'2.4.1':  {'release':'2.4.1','moonrev':'','monorev':''},
}

releases = {
    '2.99.0.1':  {'release':'2.99.0.1','moonrev':'','monorev':''},
    '2.99.0.2':  {'release':'2.99.0.2','moonrev':'','monorev':''},
    '2.99.0.3':  {'release':'2.99.0.3','moonrev':'','monorev':''},
    '2.99.0.4':  {'release':'2.99.0.4','moonrev':'','monorev':''},
    '2.99.0.5':  {'release':'2.99.0.5','moonrev':'','monorev':''},
    '2.99.0.6':  {'release':'2.99.0.6','moonrev':'','monorev':''},
    '2.99.0.7':  {'release':'2.99.0.7','moonrev':'','monorev':''},
    '2.99.0.8':  {'release':'2.99.0.8','moonrev':'','monorev':''},
    '2.99.0.9':  {'release':'2.99.0.9','moonrev':'','monorev':''},
    '2.99.0.10':  {'release':'2.99.0.10','moonrev':'','monorev':''},
    '3.99.0.1':  {'release':'3.99.0.1','moonrev':'','monorev':''},
    '3.99.0.2':  {'release':'3.99.0.2','moonrev':'','monorev':''},
    '3.99.0.3':  {'release':'3.99.0.3','moonrev':'','monorev':''},
}

latest = releases['3.99.0.3']
#latest = releases['2.4.1']

new_version = latest['release']

old_versions = releases.keys()
old_versions.sort()
old_versions.remove(latest['release'])


old_1_0_versions = ['0.6','0.7','0.8','0.9','1.0','1.0.1']

