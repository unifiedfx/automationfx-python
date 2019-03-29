import sys
from setuptools import setup, find_packages

__version__ = '0.1.4'

requires = [
    'requests>=2.0',
    'python-dateutil',
	'tctc-odata',
]

# support for enums from pypi when on older python
if sys.version_info < (3, 4):
    requires.append('enum34')

setup(
    name='automationfx',
    packages=find_packages(),
    version=__version__,
    description='AutomationFX SDK for Cisco Unified Communication Manager',
    long_description=(
        "This is a SDK for the AutomationFX REST API."
        "AutomationFX is a integration platform from UnifiedFX that exposes Cisco Unified Communication Managers (CUCM) complex and varied interfaces via a simple unified REST API."
        "Note: Currently AutomationFX software is only availble via PhoneView Lab Editon (alpha release)."
        "Please contact UnifiedFX Sales for further information and request access to the software."
        ),
    author='Stephen Welsh',
    author_email='support@unifiedfx.com',
    url='https://github.com/unifiedfx/automationfx-python',
    download_url='https://github.com/unifiedfx/automationfx-python/archive/0.1.tar.gz',
    license='MIT',
    install_requires=requires,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
        ],
    keywords='Cisco Phone Automation',
    entry_points={
          'console_scripts': [
              'automationfx = automationfx.__main__:main'
          ]
      },
    zip_safe=False
    )