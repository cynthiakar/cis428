# cis428

# dependencies used:
https://numpy.org/install/
https://pypi.org/project/aubio/
https://pypi.org/project/PyAudio/
http://www.portaudio.com/download.html
https://passlib.readthedocs.io/en/stable/install.html

Run to install dependencies

python3 setup.py install



# How to run
After installing the project folders and dependencies on both devices, INPUT THE IPs OF BOTH MACHINES. Note: The server computer is the one you are logging into and the client computer is the second computer listening to the sound. In our use case, a macOS laptop is the server and a Raspberry Pi running Raspbian is the client.

For Windows: in terminal type "ip config /all"
For macOS: in terminal type "ipconfig getifaddr en1"
For Raspbian: in terminal type "hostname -I"


Once the IP is entered, run server.py on the machine to "login" and go through the login process. Then, run client.py on the client. The two machines will then connect, 3 tones will be played from the server and recorded on the client. If the sound is verified, access will be granted.
