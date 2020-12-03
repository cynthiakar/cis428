from setuptools import setup
import os

setup(name='audio2fa',
      version='0.1',
      description='Fall 2020 Intro to Cryptography Project: Audio Two-Factor Authentication',
      url='https://github.com/cynthiakar/cis428',
      author='Cynthia Kar',
      author_email='ckar01@syr.edu',
      install_requires=[
          'aubio',
          'numpy',
          'pyaudio',
          'passlib',
          'pycrypto',
      ],
      dependency_links = ['https://github.com/PortAudio/portaudio.git'],
      zip_safe=False)


os.system('pip3 install -r audio2fa.egg-info/requires.txt')
