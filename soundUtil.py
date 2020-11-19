import subprocess
import wave, struct, math, os #native
import pyaudio #brew install portaudio
               #pip install pyaudio
import sys, getopt


class SoundUtil:
    def __init__(self, filename, expectedSound):
        self.soundFile = "sound.wav"
        self.filename = filename
        self.expectedSound = expectedSound
        self.totalDuration = sum([d for _,d in expectedSound])

    def write(self):
        #edited code from http://blog.acipo.com/wave-generation-in-python/

        sampleRate = 44100.0 # hertz
        #duration = 10.0       # seconds
        #frequency = 1000.0    # hertz

        wavef = wave.open(self.soundFile,'w')
        wavef.setnchannels(1) # mono
        wavef.setsampwidth(2)
        wavef.setframerate(sampleRate)

        for (s,t) in self.expectedSound:
            for i in range(int(t * sampleRate)):
                value = int(32767.0*math.cos(2*s*math.pi*float(i)/float(sampleRate)))
                    # take out              "2*"
                data = struct.pack('<h', value)
                wavef.writeframesraw(bytes(data))

        wavef.writeframes(b'')
        wavef.close()


    def play(self):
        # the following is from http://people.csail.mit.edu/hubert/pyaudio/

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


    def record(self):
        print("recording ",self.filename)
        subprocess.run("ssh pi@192.168.0.19 'cd /home/pi/cis428 && python record.py -o "+self.filename+" -d "+str(self.totalDuration)+"'", shell=True)



# soundList = [[(500,2),(300,1),(1000,5)],[(400,1),(600,1),(1000,2)],
#             [(400,2),(600,1),(1000,5)],[(400,5),(600,2),(1000,1)]]
#
# def createFiles():
#     i = 0
#     for s in soundList:
#         #write file
#         audioWritePlay.writeWAVFile(s,'sound'+str(i)+'.wav')
#         i = i + 1
#
# def play(i):
#     #play sound
#     print("playing", ' recorded' ,str(i), '.wav')
#     audioWritePlay.playWAVFile('sound'+str(i)+'.wav')
#
#
#
# # #### computes expected(frequency, duration - averageRecorded(frequency, duration)
# # def testAnalyze(s,filename):
# #     totalDuration = 0
# #     for (_,d) in s:
# #         totalDuration += d
# #
# #     if (totalDuration != 0):
# #         expectedFD = [(f, (d/totalDuration)) for (f,d) in s]
# #
# #     with open("results.txt","a+") as f:
# #         f.write(filename + ':\n')
# #
# #     analysis = compareWAV.compareWav(filename)
# #     results = []
# #     for i in range(min(len(expectedFD),len(analysis))):
# #         results.append((abs(expectedFD[i][0] - analysis[i][0]),abs(expectedFD[i][1] - analysis[i][1])))
# #
# #     with open("results.txt","a+") as f:
# #         f.write(str(analysis) + "\n" + str(results) + "\n\n")
# #
# #     return all([x<5 and y<5 for (x,y) in results])
#
# if __name__ == '__main__':
#     createFiles()
#
#     for i in range(len(soundList)):
#       p1 = Process(target=record,args=(i,))
#       p2 = Process(target=play,args=(i,))
#       p1.start()
#       sleep(200)
#       p2.start()
#       p2.join()
#       p1.join()
#       recordOutName = 'recorded' + str(i) + '.wav'
#       print("retrieving files from raspberry pi")
#       subprocess.run("scp pi@192.168.0.19:/home/pi/cis428/"+recordOutName+" /Users/andrew/School/senior_fall/Cryptography/Audio\ Security\ Project/cis428", shell=True)
#
#       print(testAnalyze(soundList[i],recordOutName))
