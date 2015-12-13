from tkinter import *
import pyaudio
import wave

def press(event):
  if not w.playing:
    w.playing = True
    key = event.char
    w.itemconfig(key,state="normal")
    sound = w.find_withtag(key);
    playsound(sound)

def release(event):
  key = event.char
  w.itemconfig(key,state="disabled")
  w.playing = False

def playsound(sound):
    chunk = 1024
    f = wave.open(r"%s.wav" % sound, "rb")
    p = pyaudio.PyAudio()
    stream = p.open(format = p.get_format_from_width(f.getsampwidth()),  
                channels = f.getnchannels(),  
                rate = f.getframerate(),  
                output = True) 
    data = f.readframes(chunk)
    while data != '':  
	    stream.write(data)  
	    data = f.readframes(chunk)
    stream.stop_stream()
    stream.close()

master = Tk()
wt = 300
w = Canvas(master, width=wt, height=100)
master.bind("<KeyPress>", press)
master.bind("<KeyRelease>", release)
w.playing = False
w.pack()

keys = [
  ('a', 'C'), #1
  ('s', 'D'), #2
  ('d', 'E'), #...
  ('f', 'F'),
  ('g', 'G'),
  ('h', 'A'),
  ('j', 'B'),
  ('k', 'high_C'), #8
  ('w', 'C#'), #9
  ('e', 'D#'), #...
  ('t', 'F#'),
  ('y', 'G#'),
  ('u', 'A#') #13
]

keyboard = []
inc = 25
for i in range(0,8):
  keyboard.append(w.create_rectangle(i*inc,0,(i+1)*inc,100, fill="red", disabledfill="white", state="disabled", tags=keys[i]))

ct = 0
for i in range(0,7):
  if i%7 != 2 and i%7 != 6:
    keyboard.append(w.create_rectangle(((i+1)*inc)-5,0,((i+1)*inc)+5,75, fill="red", disabledfill="black", state="disabled", tags=keys[8+ct]))
    ct += 1

mainloop()

#TODO: fix sound playing before animation changes
#      make keys clickable (if time)
