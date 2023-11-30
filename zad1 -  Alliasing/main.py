import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from PIL import Image

#NOTION

n = 5 # ĹmigĹa
L = 8  # linie
j = 0
res = (256 / 96) * 2  # rozdzielczoĹÄ

x = np.arange(0, 2 * np.pi, 0.02)
y = np.sin(n * x + np.pi)

fig1, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(res, res))

line, = ax.plot(x, y)

ax.set_rmin(-1)
ax.set_rmax(1)
ax.set_rticks([])

shutter = Image.new('RGB', (512, 512), color='blue')


def shutterfunc():
    global j
    print(j)
    plt.savefig('tempIMG.png')
    temp_img = Image.open('tempIMG.png')
    temp_crop = temp_img.crop((0, j * L, 512, j * L + L))
    shutter.paste(temp_crop, (0, j * L))
    j += 1
    if round(j > 512 / L):
        shutter.show()
        exit()


def animate(i):
    line.set_ydata(np.sin(n * x + (i * np.pi / 10)))
    shutterfunc()
    return line,


ani = animation.FuncAnimation(
    fig1, animate, 129, blit=False, save_count=10)

plt.show()