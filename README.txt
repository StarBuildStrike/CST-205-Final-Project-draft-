Our project, perhaps not so-elegantly named "Guitariano," is the offshoot of our initial plan to create
a guitar-hero type game that would be played using the keyboard.  The name comes from the fact that we
use the Karplus-Strong Algorithm in order to synthesize string sounds, which sound quite guitar-like, yet
use a piano display.  The motivation for a piano display is that it is a very simple interface that 
makes sense to the viewer naturally, and more easily demonstrates visually which note is being played.
Additionally, we have little to no musical experience (or talent), so representing notes in a meaningful
way on a guitar neck is a bit out of our wheelhouse.

The Karplus-Strong Algorithm is used to create the notes for the "piano," generating a scale of 
CDEFGABC as well as C#, D#, F#, G#, A#.  It does this by generating random "white noise" samples that are
then averaged in pairs and scaled by an energy decay factor to model the excitation of the string for each
given frequency.  Our implementation simply creates a sound file for each note at run time in the local
directory so as to avoid having to repeat calculations each time a note is pressed; however, it would be
possible to run the Algorithm and calculate in real-time, if you were so inclined.  Then a piano interface
created using Tkinter, which runs a main loop that handles events in the manner defined by the code, playing
the corresponding sound to a given keypress event.

A lot of our work was done in segments divided amongst team members on local machines, and only finalized 
recently.  We got together several times outside of class in order to make up for our incompatible 
schedules and bounce ideas off each other.  As such, our github is somewhat sparse with commits- once 
we were each given our tasks, we ground away at them on our own.  Normally this could cause issues with
combining the separate chunks at the end of the day, but our project was set up in such a way that each
task was a module that could function independently of the other (more or less).

Github here: https://github.com/StarBuildStrike/CST-205-Final-Project-draft-

The GuitarHero.py and GuitarHeroWeb.py were examples that we built on top of, and not relevant to the final
submission, so they have been removed from the repo.
