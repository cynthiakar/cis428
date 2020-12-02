# cis428

# dependencies used:
https://numpy.org/install/
https://pypi.org/project/aubio/
https://pypi.org/project/PyAudio/
http://www.portaudio.com/download.html
https://passlib.readthedocs.io/en/stable/install.html

Run to install dependencies

python3 setup.py install

#


# How to run
After installing the project folders and dependencies on both devices, INPUT THE IPs OF BOTH MACHINES. Note: The server computer is the one you are logging into and the client computer is the second computer listening to the sound. In our use case, a macOS laptop is the server and a Raspberry Pi running Raspbian is the client.

For Windows: in terminal type "ip config /all"
For macOS: in terminal type "ipconfig getifaddr en1"
For Raspbian: in terminal type "hostname -I"


Once the IP is entered, run server.py on the machine to "login" and go through the login process. Then, run client.py on the client. The two machines will then connect, 3 tones will be played from the server and recorded on the client. If the sound is verified, access will be granted.

# Why Audio 2FA

#How it works and choices we made
The first factor login credentials works by hashing and storing the password using 3000 rounds of SHA-256. This is secure because there are no known vulnerabilities of SHA-256 and we never store or decrypt the plaintext password so it is never exposed. This is achieved with the passlib package.

Our sound is pseudorandomly generated using urandom(). This generation is cryptographically secure. Then we use modulo arithmetic to transform the generated numbers into audible frequencies and reasonable durations.

A package containing information about the sound is sent from the server to the client so that the client machine can verify that the intended sound was the one that was recorded. MORE INFORMATION ABOUT THE HANDSHAKE.

The audio signal processing is done by analyzing the recorded wav file using yinfft. https://aubio.org/phd/ We then compare the estimated frequencies (Hz) against those anticipated from the sent package from the server. This is achieved using the aubio package.


# difficulties
The biggest challenges we faced were regarding sockets and audio processing. We couldn't figure out how to stream the data through sockets and ran into type errors and were unable, at first, to send the entire message to the client. We decided to send a smaller packet by changing the way we analyzed the sound. Analyzing the sound was difficult because we had to deal with extra noise and aligning the recording so that we weren't left with extra audio which would through off the results.


# references
