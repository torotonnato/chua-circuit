import random
import math
import sounddevice as sd

lastFrame = 0

def callback(outdata, frames, time, status):
	global lastFrame
	if status:
		print(status)
	print(time.outputBufferDacTime)
	f = 1440
	t = 0.
	for it in range(frames):
		v = math.sin((it + lastFrame) * 2. * math.pi * f / 44100)
		v = (.6 * v + .4 * random.random()) * 32767
		t = .1 * t + .9 * v
		outdata[it][0] = int(t)
		outdata[it][1] = int(t)
	lastFrame += frames

with sd.OutputStream(channels=2, dtype='int16', callback=callback):
	sd.sleep(30000)
