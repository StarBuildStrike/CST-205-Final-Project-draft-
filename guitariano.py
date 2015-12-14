from tkinter import *
import pyaudio
import wave
import time
import random as rand
import array as arr

#start pyaudio, create empty list for streams
p = pyaudio.PyAudio()
streams = []

#function called on key press
def press(event):
  #close finished streams and delete from list
  while len(streams) != 0 and not streams[0].is_active():
        streams[0].stop_stream()
        streams[0].close()
        del streams[0]

  #determine pressed key and highlight key
  key = event.char
  w.itemconfig(key,state="normal")

  #determine index position (to be used for opening sound file) and play
  note = w.find_withtag(key)[0]
  playsound(note)

#function called on key release
def release(event):
  #determine pressed key and unhighlight key
  key = event.char
  w.itemconfig(key,state="disabled")

def playsound(note):
    #open wave file
    f = wave.open(r"%s.wav" % note, "rb")

    #define a callback function so multiple sounds can be played at once
    def playsound2(in_data, frame_count, time_info, status):
      data = f.readframes(frame_count)
      return (data, pyaudio.paContinue)

    #open stream & add to list
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True,
                stream_callback=playsound2)
    streams.append(stream)

    stream.start_stream()
 
#standard sampling rate
samplingRate = 44100

#made a variable so that we could potentially fiddle with this later,
#has an inverse relationship with length of sound created, 4 seems like a good
#sweet spot from testing
soundDuration = 4

#frequencies for our notes we will generate: C,D,E,F,G,A,B,C,C#,D#,F#,G#,A#
notes = [523, 587, 659, 698, 784, 880, 988, 1046, 554, 622, 740, 830, 932]

#maximum value for sample, comes from 2^16 (aka 2 bytes), signed int
scaler = 32767

#Creates white noise for usage in algorithm
def makeNoise(numNoises):
    noises = []

    #Generate n random values between +- 1/2
    for x in range(numNoises):
        randInt = rand.uniform(-0.5, 0.5)
        noises.append(randInt)
    
    return noises

#Creates a sound file that plays the note created by the frequency arg    
def createSoundFile(frequency, numSamples):

    #The // operation is floor division, i.e. 3 / 2 = 1.5, 3 // 2 = 1
    #necessary because we can't do a fraction of a sample
    numNoises = samplingRate // frequency

     
    whiteNoise = makeNoise(numNoises)
    
    samples = []

    #do Karplus-Strong Algorithm witchcraft
    #more info at https://www.cs.princeton.edu/courses/archive/fall07/cos126/assignments/guitar.html
    for i in range(numSamples):
        #Add first element in whiteNoise to samples, do alg and append
        #gradually moving forward in array to look at next pair
        samples.append(whiteNoise[i])
        
        #.996 is the "energy decay factor" 
        averaged = 0.996 * 0.5 * (whiteNoise[i] + whiteNoise[i+1])
        whiteNoise.append(averaged)

    #Scale values in samples using our maximum value
    for j in range(len(samples)):
        #Have to cast to int for later processing, if we did not we would get floats
        samples[j] = int(samples[j] * scaler)

    #using array's tostring method to convert all the int values to string values
    #argument 'i' indicates that they should be looked at as signed ints
    note = arr.array('i', samples).tostring()

    #writeframes requires string or buffer, hence earlier conversion
    newNote.writeframes(note)

for i in range(len(notes)):
    #create new wav file with name x.wav
    noteNum = str(i+1) + '.wav'

    #second option 'wb' means write only. Probably not strictly necessary but good practice
    newNote = wave.open(noteNum, 'wb')

    #tell program what paramaters should be used for this sound file
    #(num channels, compression, rate of sampling, etc)
    newNote.setparams((1, 2, samplingRate, samplingRate * 4, 'NONE', 'noncompressed'))

    #Do the algorithmic stuff, again using floor division (cant have fractions of samples)
    createSoundFile(notes[i], 44100 // soundDuration)

    #close file, done creating the note at notes[i], iterate again
    newNote.close()

#open Tk window, set size, bind event handlers
master = Tk()
inc = 25
wt = inc * 8
w = Canvas(master, width=wt, height=100)
master.bind("<KeyPress>", press)
master.bind("<KeyRelease>", release)
w.pack()

#create keys
keys = [
  ('a', 'C'),
  ('s', 'D'),
  ('d', 'E'),
  ('f', 'F'),
  ('g', 'G'),
  ('h', 'A'),
  ('j', 'B'),
  ('k', 'high_C'),
  ('w', 'C#'),
  ('e', 'D#'),
  ('t', 'F#'),
  ('y', 'G#'),
  ('u', 'A#')
]

keyboard = []

#create white keys with normal and disabled states, with tags denoting which computer key to press
for i in range(0,8):
  keyboard.append(w.create_rectangle(i*inc,0,(i+1)*inc,100, fill="red", disabledfill="white", state="disabled", tags=keys[i][0]))

#create black keys with normal and disabled states, with tags denoting which computer key to press
ct = 0
for i in range(0,7):
  if i%7 != 2 and i%7 != 6:
    keyboard.append(w.create_rectangle(((i+1)*inc)-5,0,((i+1)*inc)+5,75, fill="red", disabledfill="black", state="disabled", tags=keys[8+ct][0]))
    ct += 1

#run main loop - required for Tk
mainloop()

#close pyaudio
p.terminate()
