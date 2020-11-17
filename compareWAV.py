import sys
import aubio
import numpy as np

def compareWav(filename):
    win_s = 4096
    hop_s = 512

    s = aubio.source(filename, 44100, hop_s)
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

    #print(pitches)
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

    #print(averageFrequencies)
    #print("Average frequency = " + str(np.array(pitches).mean()) + " hz")

    f.open('averageFrequencies.txt', 'a+')
    f.write(averageFrequencies)

    return averageFrequencies

if __name__ == '__main__':
    # handling command line output filename
    try:
      opts, args = getopt.getopt(argv,"i:","ifile=")
    except getopt.GetoptError:
      print('compareWAV.py -i <inputfile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt in ("-i", "--ifile"):
         filename = arg
      else:
         print('compareWav.py -o <inputfile>')
         sys.exit()
    compareWav(filename)
