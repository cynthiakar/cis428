import subprocess
import audioWritePlay
import compareWAV
from multiprocessing import Process

soundList = [[(500,2),(300,1),(1000,5)],[(400,1),(600,1),(1000,2)],
            [(400,2),(600,1),(1000,5)],[(400,5),(600,2),(1000,1)]]

def createFiles():
    i = 0
    for s in soundList:
        #write file
        audioWritePlay.writeWAVFile(s,'sound'+str(i)+'.wav')
        i = i + 1

def play(i):
    #play sound
    print("playing", ' recorded' ,str(i), '.wav')
    audioWritePlay.playWAVFile('sound'+str(i)+'.wav')


def record(i):
        totalDuration = 0
        for (_,d) in soundList[i]:
            totalDuration += d
        recordOutName = 'recorded' +str(i)+ '.wav'
        print("recording",str(i), '.wav')
        subprocess.run("ssh pi@192.168.0.19 'cd /home/pi/cis428 && python record.py -o "+recordOutName+" -d "+str(totalDuration)+"'", shell=True)

#### computes expected(frequency, duration - averageRecorded(frequency, duration)
def testAnalyze():
    i = 0
    for s in soundList:
        totalDuration = 0
        for (_,d) in s:
            totalDuration += d

        if (totalDuration != 0):
            expectedFD = [(f, (d/totalDuration)) for (f,d) in s]

        #analyze sound
        analysis = compareWAV.compareWav('recorded' + str(i) + '.wav')
        print(analysis)
        results = []
        for i in range(min(len(expectedFD),len(analysis))):
            results.append((abs(expectedFD[i][0] - analysis[i][0]),abs(expectedFD[i][1] - analysis[i][1])))

        print(results)


if __name__ == '__main__':
    createFiles()

    for i in range(len(soundList)):
      p1 = Process(target=record,args=(i,))

      #sleep()
      p2 = Process(target=play,args=(i,))
      p1.start()
      p2.start()
      p2.join()
      p1.join()
      recordOutName = 'recorded' + str(i) + '.wav'
      print("scping")
      subprocess.run("scp pi@192.168.0.19:/home/pi/cis428/"+recordOutName+" /Users/andrew/School/senior_fall/Cryptography/Audio\ Security\ Project/cis428", shell=True)

    testAnalyze()
