"""CST 205 Final Project: Guitar Hero with the use of Karplus-Strong algorithm"""

"""

Tasks:

Ulysses and Matt: Figure out the Karplus-Strong algorithm in code form
and complete the functions one by one according to the procedures.

Clay: Continuing from the previous project, implement a wavelength function
that will respond to the key event pressed in real time.
"""

"""
Libaries needed: random
matplotlib
and numpy (if necessary)
""" 

import random

def make_noise(n):
    """Create a list of n random values between -0.5 and 0.5 representing
    initial string excitation (white noise).
    """
"""
Procedure: In guitar_heroine.py, fill in the function create_noise.
This function takes in an argument n and returns a list of n random values between -0.5 and 0.5.
Our Objective is to figure out how we cab obtain such numbers using the function 'random'.
"""
    # BEGIN SOLUTION

    n = random.random()
    for n in range(-0.5, 0.5):
        
    return [random.random()-0.5 for _ in range(n)]
    # END SOLUTION


def algorithm__ks(s, n):
    """Apply n Karplus-Strong updates to the list s and return the result,
    using the initial length of s as the frequency.

    >>> s = [0.2, 0.4, 0.5]
    >>> apply_ks(s, 4)
    [0.2, 0.4, 0.5, 0.29880000000000007, 0.4482, 0.39780240000000006, 0.37200600000000006]
    """
"""
Procedure: Next, complete the function definition of algorithm_ks, which takes in an intial sequence of noise (called s)
and applies the Karplus-Strong update to this sequence n times,
appending a new sample each time. The frequency p is the initial length of s.
Then run 'python3 server.py' from the terminal. I suggest we save our codes first before running this.
Then we have to use firefox (I don't know why but that's what the guidelines said)
and we type "localhost:8000". Once it works we should see letters on the screen followed by musical notes names.
Press any letter that's listed on our keyboard to play the corresponding note.


NOTE: This py file is in conjunction with another py file named guitar hero web.py.
We don't need to modify it, but we need that file in order to get our project working.
"""
    # BEGIN SOLUTION
    frequency = len(s)
    for t in range(n):
        s.append(0.996 * (s[t] + s[t+1])/2)
    return s
    # END SOLUTION


def create_song(notes):
    """Given a list of notes (represented as strings), return a list of each
    note's samples, which themselves are lists. To get a particular note's
    samples, call guitar_string(note).
    """

"""
Procedure: Our objective in this function is to make some songs.
Therefore we need to figure out the codes that we need to fill this function.
This function takes in a list of notes (each represented as strings),
and should return a list of each note's samples, which itself is a list.
"""
    # BEGIN SOLUTION
    song = []
    for note in notes:
        song.append(guitar_string(note))
    return song
    # END SOLUTION


def make_chord(note1, note2, note3):
    """Return the samples for the chord defined by the three given notes. A
    chord's samples can be constructed from the superposition of the samples of
    its component notes.
    """

"""
Procedure: Next, we have to implement this function,
which takes in 3 notes and returns the samples of the chord defined by these notes.
In order to obtain the samples of a particular note x,
we can simply call 'guitar_string(x)' function.

"""
    # BEGIN SOLUTION
    samples1 = guitar_string(note1)
    samples2 = guitar_string(note2)
    samples3 = guitar_string(note3)
    return [a+b+c for (a,b,c) in zip(samples1, samples2, samples3)]
    # END SOLUTION


def make_song():

"""
Procedure: After filling the 'create_song' function, we will fill this function,
and we have to modify the list of the notes according to what song we want.
The list that we are filling in represents the notes that will be played in our song sequentially.
Since I was following the guidelines, they have provided Twinkle, Twinkle as the sample song.
We can either use this or any song that we can agree on.

NOTE (alternative choice): We can also use chords in our song by calling simply make_chord function!
"""
    # Fill in notes for a song below.  This example starts "Twinkle, Twinkle."
    notes = ['C', make_chord('C', 'E', 'G'), 'G', 'G', 'A', 'A', 'G']
    return songify(notes)


# Utility functions and initialization

"""

NOTE: We don't need to modify the two functions below,
as stated in the guidelines.
"""

def make_strings(quant=256):
    """Return a (key, note, samples) tuple for each key.

    key and note are strings;  samples is a list of ints in [-quant, quant].
    """
    strings = []
    for (key, note) in keys:
        string = guitar_string(note)
        strings.append([key, note, string])
    return strings


def guitar_string(note, num_samples=30000, sample_rate=44100, quant=256):
    """Return a list of num_samples samples synthesizing a guitar string."""

    # Deal with chords
    if type(note) == list:
        return note

    key = notes[note]
    frequency = frequencies[key]
    delay = int(sample_rate / frequency)
    noise = make_noise(delay)
    samples = algorithm_ks(noise, num_samples - delay)
    samples = [int(s*quant) for s in samples]
    return samples

keys = [
  ('a', 'C'),
  ('w', 'C#'),
  ('s', 'D'),
  ('e', 'D#'),
  ('d', 'E'),
  ('f', 'F'),
  ('t', 'F#'),
  ('g', 'G'),
  ('y', 'G#'),
  ('h', 'A'),
  ('u', 'A#'),
  ('j', 'B'),
  ('k', 'high_C')
]

A = 440
C = A * 2 ** (3/12)
frequencies, notes = {}, {}

for i, (key, note) in enumerate(keys):
    frequencies[key] = C * 2 ** (i/12)
    notes[note] = key
