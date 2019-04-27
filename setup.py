#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: xinxi
# Mail: xinxi1990@163.com
# Created Time:  2018-4-16 19:17:34
#############################################
import io,os,sys
from shutil import rmtree
from setuptools import Command, find_packages, setup

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with io.open(os.path.join(here, 'max', '__about__.py'), encoding='utf-8') as f:
    exec(f.read(), about)

class InstallCommand(Command):
    """ Build and publish this package.
        Support setup.py upload. Copied from requests_html.
    """

    user_options = []

    @staticmethod
    def status(s):
        """Prints things in green color."""
        print("\033[0;32m{0}\033[0m".format(s))

    def initialize_options(self):
        """ override
        """
        pass

    def finalize_options(self):
        """ override
        """
        pass

    def run(self):
        try:
            self.status('Removing previous builds…')
            rmtree(os.path.join(here, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution…')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPi via Twine…')
        os.system('twine upload dist/*')

        self.status('Publishing git tags…')
        os.system('git tag v{0}'.format(about['__version__']))
        os.system('git push --tags')

        sys.exit()


setup(
    name = "maxauto",      #这里是pip项目发布的名称
    version = "1.0.0",  #版本号，数值大的会优先被pip
    keywords = ("pip", "maxauto","monkey"),
    description = "maxauto monkey",
    long_description = "maxauto monkey for android",
    license = "MIT Licence",

    url = "https://github.com/xinxi1990/maxauto",     #项目相关文件地址，一般是github
    author = "xinxi",
    author_email = "xinxi1990@163.com",

    packages = find_packages(),
    include_package_data = True,
    platforms = "any",
    install_requires = ["requests","setuptools","selenium","Flask","Appium_Python_Client","beautifulsoup4","upload"],          #这个项目需要的第三方库
    entry_points = {
                       'console_scripts': [
                           'max=max.run:main_run'
                       ]
                   },
    cmdclass={
        'upload': InstallCommand
    }
)
