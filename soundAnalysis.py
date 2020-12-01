import sys
import aubio
import numpy as np

class SoundAnalysis:
    def __init__(self, filename, expectedSound):
        self.filename = filename
        self.expectedFD = 0
        self.expectedSound = expectedSound
        totalDuration = sum([d for _,d in expectedSound])
        if (totalDuration != 0):
            self.expectedFD = [(f, (d/totalDuration)) for (f,d) in expectedSound]
        #self.expectedPitches =

    def compareWav(self):
        win_s = 4096
        hop_s = 512

        s = aubio.source(self.filename, 44100, hop_s)
        samplerate = s.samplerate

        tolerance = 0.8

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

        with open("results.txt","a+") as f:
            f.write(str(pitches) + "\n")

        print("pitch length:", len(pitches))
        frequencies = [[pitches[0]]]
        i = 0
        for p in pitches:
            average = sum(frequencies[i])/len(frequencies[i])
            if (p < average + 20 and p > average - 20):
                frequencies[i] += [p]
            else:
                i = i + 1
                frequencies += [[p]]

        frequencies = [x for x in frequencies if len(x) > 10]
        averageFrequencies = [(sum(x)/len(x),len(x)/len(pitches)) for x in frequencies]

        print("input", self.expectedSound)
        print("expected", self.expectedFD)
        print("averageFrequencies",averageFrequencies)
        #print("Average frequency = " + str(np.array(pitches).mean()) + " hz")

        return averageFrequencies

    #### computes expected(frequency, duration - averageRecorded(frequency, duration)
    def testAnalyze(self):
        with open("results.txt","a+") as f:
            f.write(self.filename + ':\n')

        analysis = self.compareWav()
        results = []
        for i in range(min(len(self.expectedFD),len(analysis))):
            results.append((abs(self.expectedFD[i][0] - analysis[i][0]),abs(self.expectedFD[i][1] - analysis[i][1])))

        with open("results.txt","a+") as f:
            f.write(str(analysis) + "\n" + str(results) + "\n\n")

        return all([x<5 and y<5 for (x,y) in results])


    def compareWav2(self): #returns the pitch list only
        win_s = 4096
        hop_s = 512

        s = aubio.source(self.filename, 44100, hop_s)
        samplerate = s.samplerate

        tolerance = 0.8

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

    #### returns percentage of pitches within given tolerance
    def testAnalyze2(self):
        # analyze both raw and recorded WAV files
        pitchListRaw = self.compareWav2()
        pitchListRecorded = ?

        # shift one list along the other and take the maximum accuracy percentage

        return all([x<5 and y<5 for (x,y) in results])
