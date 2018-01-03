from setuptools import setup

__version__ = '0.1.3'

setup(
    name='automationfx',
    packages=['automationfx'],
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
    install_requires=['requests'],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7'
        ],
    keywords='Cisco Phone Automation',
    zip_safe=False
    )