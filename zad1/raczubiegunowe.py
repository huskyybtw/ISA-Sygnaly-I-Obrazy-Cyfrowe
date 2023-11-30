import argparse
import numpy as np
import matplotlib.pyplot as plt
import cv2
from os import mkdir
from os.path import isdir
from shutil import rmtree
from matplotlib.lines import Line2D
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter
from matplotlib.image import AxesImage
from typing import List, Tuple
from copy import deepcopy

# Setup
SENSOR = 256
M = 64

# Generating propellers in polar coordinates
def propeller_polar(blades: int, theta: np.array, m: float) -> np.array:
    r = np.sin(blades * theta + ((m * np.pi) / 10))
    return r

def get_data_polar(blades: int) -> np.array:
    theta = np.linspace(0, 2 * np.pi, SENSOR)
    ms = np.linspace(-M / 2, M / 2 ,M )

    return np.array(
        [[propeller_polar(blades, x, m) for x in theta] for m in ms])

def update_polar(frame: int, prop: Line2D, prop_data: np.array) -> Line2D:
    prop.set_data(np.linspace(0, 2 * np.pi, SENSOR), prop_data[frame])

    return prop

def get_shuttered_prop_data(video: cv2.VideoCapture, lines: int) -> Tuple[List[np.array], List[np.array]]:
    shutter_data = list()
    prop_data = list()
    is_captured, frozen_frame = video.read()
    is_captured, current_frame = video.read()
    frozen_frame, current_frame = cv2.cvtColor(frozen_frame, cv2.COLOR_BGR2RGB), \
                                  cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)

    read_frames = 1

    while is_captured and read_frames <= SENSOR:
        frozen_frame[0:SENSOR - read_frames - 1, :] = current_frame[0:SENSOR - read_frames - 1, :]
        shutter_data.append(deepcopy(frozen_frame))
        prop_data.append(deepcopy(current_frame))

        is_captured, current_frame = video.read()
        current_frame = cv2.cvtColor(current_frame, cv2.COLOR_BGR2RGB)
        read_frames += lines

    video.release()

    return prop_data, shutter_data

def main() -> None:
    parser = argparse.ArgumentParser(
        description='Arguments to configure a script')

    parser.add_argument(
        '-b',
        '--blades',
        type=int,
        required=True,
        help='specify a number of propeller blades (3 or 5)')

    parser.add_argument(
        '-l',
        '--lines',
        type=int,
        required=True,
        help='specify a number of lines that sensor can read at once')

    parser.add_argument(
        '--save',
        action='store_true',
        help='specify if generated animation should be saved')

    args = parser.parse_args()

    if args.blades not in (1,2,3, 5):
        raise ValueError('Number of propeller blades should be equal to 3 or 5!')

    prop_data = get_data_polar(args.blades)

    fig = plt.figure(figsize=(SENSOR / 100, SENSOR / 100), dpi=100)
    ax = fig.add_subplot(111, projection='polar')
    ax.set_ylim(0, SENSOR)
    ax.set_axis_off()

    prop, = ax.plot(np.linspace(0, 2 * np.pi, SENSOR), prop_data[0])

    # Propeller animation
    animation = FuncAnimation(fig, update_polar, frames=M, fargs=(prop, prop_data), interval=M)
    mkdir('./tmp') if not isdir('./tmp') else None
    animation.save('./tmp/propeller.gif', PillowWriter(fps=30))
    propeller_animation = cv2.VideoCapture('./tmp/propeller.gif')

    prop_data, shuttered_prop_data = get_shuttered_prop_data(propeller_animation, args.lines)
    rmtree('./tmp') if isdir('./tmp') else None

if __name__ == '__main__':
    main()
