from setuptools import setup

setup(name='afx',
    version='0.1',
    description='AutomationFX SDK for Cisco Unified Communication Manager',
    url='https://github.com/unifiedfx/automationfx-python',
    author='Stephen Welsh',
    author_email='support@unifiedfx.com',
    license='MIT',
    packages=['automationfx'],
    install_requires=['requests','time'],
    zip_safe=False)