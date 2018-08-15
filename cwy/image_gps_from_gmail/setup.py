from distutils.core import setup
import py2exe, sys, os

sys.argv.append('py2exe')

setup(
	#options = {'py2exe':{'bundle_files' : 1}},
	windows = [{'script':"image_downloader.py"}],
        hiddenimports = ['pandas._libs.tslibs.timedeltas', 'pandas._libs.tslibs.np_datetime', 'pandas._libs.tslibs.nattype', 'pandas._libs.skiplist'],
	zipfile = None,
)
