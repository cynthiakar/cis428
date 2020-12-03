import sys
import aubio
import numpy as np

class SoundAnalysis:
    def __init__(self):
        self.pitchList = None

    #### computes expected(frequency, duration - averageRecorded(frequency, duration)
    def testAnalyze(self, expectedSound, recordedPitchList):
        print("pitch length:", len(recordedPitchList))
        totalDuration = sum([d for _,d in expectedSound])
        if (totalDuration != 0):
            expectedFD = [(f, (d/totalDuration)) for (f,d) in expectedSound]
        frequencies = [[recordedPitchList[0]]]

        i = 0
        for p in recordedPitchList:
            average = sum(frequencies[i])/len(frequencies[i])
            if (p < average + 50 and p > average - 50):
                frequencies[i] += [p]
            else:
                i = i + 1
                frequencies += [[p]]

        frequencies = [x for x in frequencies if len(x) > 10]
        averageFrequencies = [(sum(x)/len(x),len(x)/len(recordedPitchList)) for x in frequencies]
        averageFrequencies = [(x,y) for (x,y) in averageFrequencies if x >= 50]

        print("input", expectedSound)
        print("expected", expectedFD)
        print("averageFrequencies", averageFrequencies)
        #print("Average frequency = " + str(np.array(pitches).mean()) + " hz")
        # with open("results.txt","a+") as f:
        #     f.write(self.filename + ':\n')

        results = []
        for i in range(min(len(expectedFD),len(averageFrequencies))):
            results.append((abs(expectedFD[i][0] - averageFrequencies[i][0]),abs(expectedFD[i][1] - averageFrequencies[i][1])))

        with open("results.txt","a+") as f:
            f.write(str(averageFrequencies) + "\n" + str(results) + "\n\n")

        return all([x<5 and y<5 for (x,y) in results])


    def getPitchList(self, filename): #returns the pitch list only
        win_s = 4096
        hop_s = 512

        s = aubio.source(filename, 44100, hop_s)
        samplerate = s.samplerate

        tolerance = 0.7

        pitch_o = aubio.pitch("yinfft", win_s, hop_s, samplerate)
        #pitch_o.set_unit("midi")
        pitch_o.set_tolerance(tolerance)

        pitches = []
        confidences = []

        total_frames = 0
        while True:
            samples, read = s()
            pitch = pitch_o(samples)[0]
            pitches += [pitch]
            confidence = pitch_o.get_confidence()
            confidences += [confidence]
            total_frames += read
            if read < hop_s: break

        print(pitches)
        return pitches
