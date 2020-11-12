import audioWritePlay
import compareWAV
import aubio

def main():
    #generate sound and save
    sounds = [(400,2),(600,1),(1000,5)]

    totalDuration = 0
    for (_,d)in sounds:
        totalDuration += d

    if (totalDuration != 0):
        expectedFD = [(f, (d/totalDuration)) for (f,d) in sounds]

    audioWritePlay.writeWAVFile(sounds)

    #analyze sound
    analysis = compareWAV.compareWav("sound.wav")

    results = []
    for i in range(len(expectedFD)):
        results.append((abs(expectedFD[i][0] - analysis[i][0]),abs(expectedFD[i][1] - analysis[i][1])))

    #print(expectedFD)
    #print(analysis)
    print(results)

if __name__ == "__main__":
    main()
