import pyaudio
import wave
import sys, getopt

# RECORDING ON PI: https://makersportal.com/blog/2018/8/23/recording-audio-on-the-raspberry-pi-with-python-and-a-usb-microphone
def recordWAV(argv):
    # the following is from http://people.csail.mit.edu/hubert/pyaudio/
    CHUNK = 4096
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100
    RECORD_SECONDS = 10

    # handling command line output filename
    try:
      opts, args = getopt.getopt(argv,"o:",["ofile="])
    except getopt.GetoptError:
      print('record.py -o <outputfile>')
      sys.exit(2)
    for opt, arg in opts:
      if opt in ("-o", "--ofile"):
         WAVE_OUTPUT_FILENAME = arg
      else:
         print('record.py -o <outputfile>')
         sys.exit()

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index = 2,
                    frames_per_buffer=CHUNK)

    print("* recording to ", WAVE_OUTPUT_FILENAME)

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


def main(argv):
    recordWAV(argv)

if __name__ == "__main__":
    main(sys.argv[1:])
