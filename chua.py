
#x˙=−α(x−y)−αf(x),
#y˙=z−(y−x),
#z˙=−βy−γz,

from collections import namedtuple
import array, wave

v3d = namedtuple('v3d', 'x y z')

def diode(m0, m1, x):
	return m1 * x + .5 * (m0 - m1) * (abs(x + 1.) - abs(x - 1.))

def chua_rk(prev, alfa, beta, gamma, m0, m1, h):
	x = prev.x - alfa * h * (prev.x - prev.y + diode(m0, m1, prev.x))
	y = prev.y + h * (prev.z - prev.y + prev.x)
	z = prev.z - h * (beta * prev.y + gamma * prev.z)
	return v3d._make((x, y, z))

p = v3d._make((-.1, .2, -.1))
h = 0.02
alfa = 8.41
beta = 11.23
gamma = 0.0435
m0 = -1.366
m1 = -0.17

v = []
for it in range(44100 * 10):
	p = chua_rk(p, alfa, beta, gamma, m0, m1, h)
	v.append(p.z)

v_max = max(v)
v_min = min(v)
normalize = lambda s : 2. * (s - v_min) / (v_max - v_min) - 1.
v_norm = [int(32767 * normalize(s)) for s in v]
samples = array.array('h', v_norm)

f = open('chua.wav', 'wb')
wav = wave.Wave_write(f)
wav.setframerate(44100)
wav.setnchannels(1)
wav.setsampwidth(2)
wav.writeframes(samples)
wav.close()
