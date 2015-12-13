import random as rand
import array as arr
import wave
 
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
    
