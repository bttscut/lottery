from distutils.core import setup
import py2exe
setup(windows=[{
	'script':'lottery.py',
	"icon_resources":[(1,"app.ico")]}
	],
	options = {'py2exe':{'bundle_files':1}},
	zipfile = None
	)
