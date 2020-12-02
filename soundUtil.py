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


    # RECORDING ON PI: https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone
    def record(self, outputfile):
        # the following is from http://people.csail.mit.edu/hubert/pyaudio/
        CHUNK = 4096
        FORMAT = pyaudio.paInt16
        CHANNELS = 2
        RATE = 44100
        RECORD_SECONDS = 8
        WAVE_OUTPUT_FILENAME = outputfile

        # # handling command line output filename
        # try:
        #   opts, args = getopt.getopt(argv,"o:d:",["ofile=","dur="])
        # except getopt.GetoptError:
        #   print('record.py -o <outputfile>')
        #   sys.exit(2)
        # for opt, arg in opts:
        #   if opt in ("-o", "--ofile"):
        #      WAVE_OUTPUT_FILENAME = arg
        #   elif opt in ("-d", "--duration"):
        #      RECORD_SECONDS = int(arg)
        #   else:
        #      print('record.py -o <outputfile>')
        #      sys.exit()

        p = pyaudio.PyAudio()

        stream = p.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        input_device_index = 2, #required for raspberry pi
                        frames_per_buffer=CHUNK)

        print("* recording to ", WAVE_OUTPUT_FILENAME, " for ", RECORD_SECONDS, " seconds")

        frames = []

        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)

        print("* done recording")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
