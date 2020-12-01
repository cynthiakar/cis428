# if you are running macOS and have pip and Homebrew,
# this Makefile should install all dependencies

# dependies list: portaudio, pyaudio, aubio,
# 							  passlib

default: all

all:
	brew install portaudio #for macOS
	pip install pyaudio
	pip install aubio
	pip install passlib
