import subprocess
import wave, struct, math, os #native
import pyaudio #brew install portaudio
               #pip install pyaudio
import sys, getopt
import time


class SoundUtil:
    def __init__(self):
        self.soundFile = "sound.wav"
        # self.totalDuration = sum([d for _,d in expectedSound])

    def generateRandomSound(self):
        x1 = struct.unpack('I', os.urandom(4))[0]
        y1 = struct.unpack('I', os.urandom(4))[0]
        z1 = struct.unpack('I', os.urandom(4))[0]
        x2 = struct.unpack('I', os.urandom(4))[0]
        y2 = struct.unpack('I', os.urandom(4))[0]
        z2 = struct.unpack('I', os.urandom(4))[0]
        return [((x1%15+5)*100,x2%4+1), ((y1%15+5)*100,y2%4+1), ((z1%15+5)*100,z2%4+1)]

    def createWAV(self, expectedSound):
        #edited code from http://blog.acipo.com/wave-generation-in-python/
        self.totalDuration = sum([d for _,d in expectedSound])

        sampleRate = 44100.0 # hertz
        #duration = 10.0       # seconds
        #frequency = 1000.0    # hertz

        wavef = wave.open(self.soundFile,'w')
        wavef.setnchannels(1) # mono
        wavef.setsampwidth(2)
        wavef.setframerate(sampleRate)

        for (s,t) in expectedSound:
            for i in range(int(t * sampleRate)):
                value = int(32767.0*math.cos(2*s*math.pi*float(i)/float(sampleRate)))
                    # take out              "2*"
                data = struct.pack('<h', value)
                wavef.writeframesraw(bytes(data))

        wavef.writeframes(b'')
        wavef.close()

    def play(self):
        # the following is from http://people.csail.mit.edu/hubert/pyaudio/
        print("sleeping play")
        time.sleep(1)
        print("playing")
        wf = wave.open(self.soundFile, 'rb')
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

        if os.path.exists(self.soundFile):
            os.remove(self.soundFile)
        else:
            print("The file does not exist")


    def record(self, filename):
        print("recording ", filename)
        print(self.totalDuration)
        subprocess.run("ssh pi@192.168.0.19 'cd /home/pi/cis428 && python record.py -o "+filename+" -d "+str(self.totalDuration)+"'", shell=True)
