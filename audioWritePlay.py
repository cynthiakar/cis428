import wave, struct, math, os #native
import pyaudio #brew install portaudio
               #pip install pyaudio


def writeWAVFile(sounds):
    #edited code from http://blog.acipo.com/wave-generation-in-python/

    sampleRate = 44100.0 # hertz
    #duration = 10.0       # seconds
    #frequency = 1000.0    # hertz

    wavef = wave.open('sound.wav','w')
    wavef.setnchannels(1) # mono
    wavef.setsampwidth(2)
    wavef.setframerate(sampleRate)

    for (s,t) in sounds:
        for i in range(int(t * sampleRate)):
            value = int(32767.0*math.cos(2*s*math.pi*float(i)/float(sampleRate)))
                # take out              "2*"
            data = struct.pack('<h', value)
            wavef.writeframesraw(bytes(data))

    wavef.writeframes(b'')
    wavef.close()



def playWAVFile(pathname):
    # the following is from http://people.csail.mit.edu/hubert/pyaudio/

    wf = wave.open(pathname, 'rb')
    CHUNK = 1024 #number of frames

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != b'':
        stream.write(data)
        data = wf.readframes(CHUNK)

    stream.stop_stream()
    stream.close()

    p.terminate()

    if os.path.exists(pathname):
      os.remove(pathname)
    else:
      print("The file does not exist")
