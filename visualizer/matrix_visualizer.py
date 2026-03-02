import random
import time
import array
import math

import board
import displayio
import framebufferio
import rgbmatrix
import analogio
import digitalio
import vectorio
import adafruit_lis3dh
import busio

from ulab import zeros as u_zeros
from ulab import concatenate as u_concat
from ulab import array as u_array
from ulab import float as u_float
from ulab import vector as u_vector


from constants import WIDTH, HEIGHT, TOTAL_HEIGHT, TOTAL_WIDTH, ORIGIN_WIDTH, ORIGIN_HEIGHT
from constants import CHAIN_ACROSS, TILE_DOWN, SERPENTINE
from constants import PALETTES,PALETTE_LENGTH
from constants import CHUNK, MIN_SENSITIVITY

import helper as helper
import visualizer as visualizer

displayio.release_displays()
print(dir(board))



scale = 1

matrix = rgbmatrix.RGBMatrix(
    width=TOTAL_WIDTH, height=TOTAL_HEIGHT, bit_depth=3,
    rgb_pins=[
        board.MTX_R1,
        board.MTX_G1,
        board.MTX_B1,
        board.MTX_R2,
        board.MTX_G2,
        board.MTX_B2
    ],
    addr_pins=[
        board.MTX_ADDRA,
        board.MTX_ADDRB,
        board.MTX_ADDRC,
        board.MTX_ADDRD
    ],
    clock_pin=board.MTX_CLK,
    latch_pin=board.MTX_LAT,
    output_enable_pin=board.MTX_OE,
    tile=TILE_DOWN, serpentine=SERPENTINE,
)

initialPalette = PALETTES[0]
initialPaletteLength = len(initialPalette)

# accelerometer for auto rotation
i2c = board.I2C()
lis3dh = adafruit_lis3dh.LIS3DH_I2C(i2c, address=0x19)
lis3dh.range = adafruit_lis3dh.RANGE_16_G

display = framebufferio.FramebufferDisplay(matrix, auto_refresh=True, rotation=0)
palette = displayio.Palette(initialPaletteLength)
for i, pi in enumerate(initialPalette):
    palette[initialPaletteLength-1-i] = pi

bitmap = displayio.Bitmap(display.width // scale, display.height // scale, initialPaletteLength)

tg = displayio.TileGrid(bitmap, pixel_shader=palette)

g = displayio.Group(max_size=3, scale=scale)
g.append(tg)
display.show(g)


def changePalette(givenPalette):
    for i, pi in enumerate(givenPalette):
        palette[PALETTE_LENGTH-1-i] = pi

# calculates orientation around z axis
def calculate_angle(x,y,z, angle):
    xy = 0
    yx = 0
    if x != 0 or y != 0:
        xy = math.asin(y/math.sqrt(x**2 + y**2))
        yx = math.acos(x/math.sqrt(x**2 + y**2))
    mn = yx - xy
    mx = yx + xy
    if xy != 0 and yx != 0:
        if mn > 3 and mx > 3 and angle != 90:
            return 90
        if mn < 0.2 and mx > 3 and angle != 180:
            return 180
        if mn > 3 and mx < 0.2 and angle != 0:
            return 0
        if mn < 0.2 and mx < 0.2 and angle != 270:
            return 270
    #print("xy = %0.3f, yx = %0.3f" % (xy, yx))
    return angle

def run():
    vis = visualizer.Visualizer(bitmap)


    chunkClock = 0
    micBuff = u_array([0] * CHUNK, dtype=u_float)

    tempHistory = u_array([0] * CHUNK, dtype=u_float)
    ampHistory = u_array([0] * CHUNK, dtype=u_float)

    adc = analogio.AnalogIn(board.A1)
    pot = analogio.AnalogIn(board.A2)
    rotation = 0
    angle = 0

    switchProfiles = False
    profile = 0
    numProfiles = 6


    switchColors = False
    color = 0

    buttonUp = digitalio.DigitalInOut(board.BUTTON_UP)
    buttonUp.direction = digitalio.Direction.INPUT
    buttonUp.pull = digitalio.Pull.UP

    buttonDown = digitalio.DigitalInOut(board.BUTTON_DOWN)
    buttonDown.direction = digitalio.Direction.INPUT
    buttonDown.pull = digitalio.Pull.UP

    totalMax = 25000
    sensitivity = 0
    historyMax = 10
    offset = 0
    while True:
        micBuff[chunkClock] = adc.value

        if not buttonUp.value:
            time.sleep(0.3)
            switchProfiles = True

        if not buttonDown.value:
            time.sleep(0.3)
            switchColors = True

        if switchProfiles:
            profile = (profile + 1) % numProfiles
            bitmap.fill(0)
            switchProfiles = False
            vis.reset_rotation()
            offset = 0

        chunkClock += 1
        #TODO: check if chunkClock fills the whole buffer
        if chunkClock >= CHUNK:
            #spectro = helper.calculate_fft(micBuff)
            #print("%0.3f, %0.3f" % (spectro[3], spectro[CHUNK//2-4]))
            sensitivity = math.pow(65536- pot.value, 14/15)
            scaled, totalMax = helper.scale_data(micBuff, totalMax, sensitivity)
            #print("%0.3f, %0.3f, %0.3f" % (sensitivity, totalMax, pot.value))
            amp = math.ceil(helper.normalized_rms(scaled))
            #print(amp, totalMax)

            ampHistory = u_concat((u_array([amp]), ampHistory[:-1]))

            display.auto_refresh = False

            if switchColors:
                color = (color + 1) % (len(PALETTES))
                switchColors = False
                print(color, len(PALETTES))
                changePalette(PALETTES[color])

            bitmap.fill(0)
            if profile == 0:
                vis.visualize_dna(ampHistory)
            elif profile == 1:
                vis.visualize_knot(ampHistory)
            elif profile == 2:
                vis.visualize_wave(ampHistory)
            elif profile == 3:
                vis.visualize_tornado_2(ampHistory)
            elif profile == 4:
                vis.visualize_shape(ampHistory, 3)
            elif profile == 5:
                vis.visualize_shape(ampHistory, 4)

            display.auto_refresh = True

            chunkClock = 0


            x,y,z = [value/adafruit_lis3dh.STANDARD_GRAVITY for value in lis3dh.acceleration]
            newAngle = calculate_angle(x,y,z, angle)
            if newAngle != angle:
                display.rotation = newAngle
                angle = newAngle
            #print("x = %0.3f G, y = %0.3f G, z = %0.3f G" % (x, y, z))
            #print(microcontroller.cpu.temperature)


run()


