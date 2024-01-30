import cv2
from cv2 import imread, cvtColor, COLOR_BGR2RGB as RGB, COLOR_BGR2GRAY as BW
from matplotlib.pyplot import subplots, subplots_adjust, axes, show
from matplotlib.widgets import Slider, RadioButtons,Button
## https://matplotlib.org/3.2.1/gallery/widgets/slider_demo.html
from numpy.random import poisson
from auxiliary import displayImages as DI
from numpy import clip
from random import choice

''' Warning: Never ignore warnings... ;) '''
import warnings; warnings.filterwarnings('ignore')

# A handy shortcut...
DIH = lambda img, ttl = '', cmp = 'gray', shw = False: DI(img, ttl, cmp, shw)

# Globalna zmienna do przechowywania przetworzonego obrazu
processed_img = None

# GUI event handlers
# GUI event handlers
def poissonimg(val):
    global fig, img, lambda_display, processed_img
    λ = 2 ** (val - 8.0)
    processed_img = clip(poisson(img * λ) / λ, 0, 0xff).astype('uint8')
    DIH(processed_img, f'{val}EV')
    lambda_display.set_text(f'λ = {λ:.2f}')

    # Zmiana nazwy pliku przy zapisie, aby zawierała wartość λ
    filename = f'lambda_{λ:.2f}.png'
    cv2.imwrite(filename, cv2.cvtColor(processed_img, cv2.COLOR_RGB2BGR))

    fig.canvas.draw_idle()

def scotophotopic(label):
    global img, mb, slEV
    img = cvtColor(imread(mb), RGB if label == 'RGB' else BW)
    poissonimg(slEV.val)

# GUI elements
fig, _ = subplots(num="Nihil novi sub stella..."); subplots_adjust(left=.25, bottom=.35)

axEV, axc = axes([.25, .1, .65, .03]), axes([.025, .5, .15, .15])
slEV = Slider(axEV, 'EV', 0.0, 16.0, valinit=8.0, valstep=1.0)
radio = RadioButtons(axc, ('RGB', 'B&W'), active=0)

# Tworzenie dodatkowego obszaru dla wyświetlania wartości λ
ax_lambda = fig.add_axes([.9, .1, .1, .03])
ax_lambda.set_xticks([])
ax_lambda.set_yticks([])
ax_lambda.set_navigate(False)

# Inicjalizacja tekstu dla wyświetlania wartości λ
lambda_display = ax_lambda.text(0.5, 0.5, '', horizontalalignment='center', verticalalignment='center')

slEV.on_changed(poissonimg); radio.on_clicked(scotophotopic)

# Image re/de-generation
mb = 'drugi.png'
img = cvtColor(imread(mb), RGB)

poissonimg(8)
show()