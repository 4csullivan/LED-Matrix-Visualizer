import ulab
import math
from constants import AVG_RATE, TOTAL_HEIGHT, TOTAL_WIDTH, ORIGIN_HEIGHT, ORIGIN_WIDTH

class Visualizer:
    def __init__(self, bitmap):
        self.bitmap = bitmap
        self.rotation = 0

    def update_rotation(self, multiple):
        self.rotation = (self.rotation + multiple) % 360

    def reset_rotation(self):
        self.rotation = 0

    def visualize_dna(self, data):
        f = 1/64
        w = 2 * math.pi * f
        v = 64
        k = (2 * math.pi) / v

        rot = self.rotation * math.pi/180
        p = rot + math.pi/2

        amp = int(ulab.numerical.mean(data[0:0+AVG_RATE]))
        for y in range(TOTAL_HEIGHT):
            if y % 4 == 0:
                yHalf = y//4
                amp = int(ulab.numerical.mean(data[yHalf:yHalf+AVG_RATE]))

            sn = math.floor((amp) * math.sin(k + w * y + p) + ORIGIN_HEIGHT)
            cs = math.floor((amp) * math.cos(k + w * y + p) + ORIGIN_HEIGHT)

            if sn >= 0 and sn < TOTAL_WIDTH-1 and cs >= 0 and cs < TOTAL_WIDTH-1:
                self.bitmap[sn + y * TOTAL_WIDTH] = int(amp)
                self.bitmap[cs + y * TOTAL_WIDTH] = int(amp)
        self.update_rotation(3)

    def draw_pipe_line(self, yPos, width, center, color):
        for x in range(center - width//2, center + width//2):
                if x % 2 == 0:
                    self.bitmap[x + yPos * TOTAL_WIDTH] = int(color)

    def visualize_tornado(self, data):
        f = 1/64
        w = 2 * math.pi * f
        v = 16
        k = (2 * math.pi) / v

        rot = self.rotation * math.pi/180
        pipeWidth = 12

        amp = int(ulab.numerical.mean(data[0:0+AVG_RATE]))
        for y in range(TOTAL_HEIGHT):
            if y %  2 == 0:
                self.draw_pipe_line(y, pipeWidth, ORIGIN_WIDTH, 40)
            if y % 2 == 0:
                yHalf = y//2
                avgAmp = int(ulab.numerical.mean(data[yHalf:yHalf+AVG_RATE]))
                p = rot + avgAmp * math.pi/2
            sn = math.floor(avgAmp * math.sin(k * rot + w * y - p) + ORIGIN_HEIGHT)
            cs = math.floor(avgAmp * math.cos(k * rot + w * y - p) + ORIGIN_HEIGHT)


            if sn >= 0 and cs >= 0 and sn < TOTAL_WIDTH and cs < TOTAL_WIDTH and avgAmp > (pipeWidth//2+1):
                #print(cs - sn, pipeWidth)
                if (cs - sn) > (pipeWidth - avgAmp):
                    self.bitmap[sn + y*TOTAL_WIDTH] = avgAmp
                if (sn - cs)  < (pipeWidth - avgAmp):
                    self.bitmap[cs + y * TOTAL_WIDTH] = avgAmp
        self.update_rotation(1)

    def visualize_knot(self, data):
        f = 1/64
        w = 2 * math.pi * f
        v = 16
        k = (2 * math.pi) / v

        rot = self.rotation# * math.pi/180
        p =  math.pi/2

        avgAmp = int(ulab.numerical.mean(data[0:0+AVG_RATE]))
        pipeWidth = 12

        for y in range(TOTAL_HEIGHT):
            if y % 4 == 0:
                yHalf = y//4
                avgAmp = int(ulab.numerical.mean(data[yHalf:yHalf+AVG_RATE]))
                #avgAmp = max(avgAmp, 5)

            sn = math.floor(avgAmp * math.sin(k * rot + w * y + p) + ORIGIN_HEIGHT)
            sn2 = math.floor(avgAmp * math.sin(k * rot + w * y) + ORIGIN_HEIGHT)
            cs = math.floor(avgAmp * math.cos(k * rot + w * y + p) + ORIGIN_HEIGHT)
            cs2 = math.floor(avgAmp * math.cos(k * rot + w * y + p*2) + ORIGIN_HEIGHT)

            if sn >= 0 and cs >= 0 and sn < (TOTAL_WIDTH-2) and cs < (TOTAL_WIDTH-2):
                #print(sn, cs)
                #if (cs - sn) >= -pipeWidth * math.pi/180:
                self.bitmap[sn + y * TOTAL_WIDTH] = int(avgAmp)
                self.bitmap[sn2 + y * TOTAL_WIDTH] = int(avgAmp)
                self.bitmap[cs + y * TOTAL_WIDTH] = int(avgAmp)
                self.bitmap[cs2 + y * TOTAL_WIDTH] = int(avgAmp)
        self.update_rotation(0.1)

    def visualize_tornado_2(self, data):
        f = 1/128
        w = 2 * math.pi * f
        v = 16
        k = (2 * math.pi) / v

        rot = self.rotation
        p =  math.pi/2

        amp = int(data[0])
        avgAmp = int(ulab.numerical.mean(data[0:0+AVG_RATE]))

        for y in range(TOTAL_HEIGHT):
            if y % 2 == 0:
                yHalf = y//2
                avgAmp = int(ulab.numerical.mean(data[yHalf:yHalf+AVG_RATE]))
                #avgAmp = max(avgAmp, 5)

            sn = math.floor(avgAmp * math.sin(k * rot + w * y + p) + ORIGIN_HEIGHT)
            sn2 = math.floor(avgAmp * math.sin(k * rot + w * y) + ORIGIN_HEIGHT)
            cs = math.floor(avgAmp * math.cos(k * rot + w * y + p) + ORIGIN_HEIGHT)
            #cs2 = math.floor(avgAmp * 0.75 * math.cos(k * rotation + w * y + p*2) + ORIGIN_HEIGHT)

            if sn >= 0 and cs >= 0 and sn < (TOTAL_WIDTH-2) and cs < (TOTAL_WIDTH-2):
                #print(sn, cs)
                #if (cs - sn) >= -pipeWidth * math.pi/180:
                self.bitmap[sn + y * TOTAL_WIDTH] = int(avgAmp)
                self.bitmap[sn2 + y * TOTAL_WIDTH] = int(avgAmp)
                self.bitmap[cs + y * TOTAL_WIDTH] = int(avgAmp)
                #bitmap[cs2 + y * TOTAL_WIDTH] = int(avgAmp)
        self.update_rotation(0.1)


    def visualize_wave(self, data):
        f = 1/128
        w = 2 * math.pi * f
        v = 16
        k = (2 * math.pi) / v

        rot = self.rotation * math.pi/180
        p = self.rotation + math.pi/2

        avgAmp = ulab.numerical.mean(data[0:0+AVG_RATE])

        amp = int(data[0])

        for y in range(TOTAL_HEIGHT):
            #if y % 2 == 0:
               # yHalf = y//2
            #avgAmp = int(ulab.numerical.mean(data[y:y+4]))

            tn = math.floor((avgAmp) * math.tan(k + w * y + p) + ORIGIN_HEIGHT)


            if tn >= 0 and tn < TOTAL_WIDTH:
                self.bitmap[tn + y * TOTAL_WIDTH] = int(avgAmp)
        self.update_rotation(avgAmp*math.pi/360)

    #############################################
    # >> draw_bresenham_line() <<
    # Draw a line between two points using
    # Bresenham's line algorithm, as seen here:
    # {https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm}
    # ---------------------------------
    # NOTE: Bitmap drawing requires integer inputs.
    # I supplied int formatting, but pay attention
    # if you need a round-up or round-down beforehand.
    # ---------------------------------
    # TODO:
    #############################################
    def draw_bresenham_line(self, x0, y0, x1, y1, color):
        x0 = math.floor(x0)
        y0 = math.floor(y0)
        x1 = math.floor(x1)
        y1 = math.floor(y1)
        dx = abs(x1-x0)
        sx = 1 if x0<x1 else -1
        dy = -abs(y1-y0)
        sy = 1 if y0 < y1 else -1
        err = dx+dy
        while True:
            if (x0 < TOTAL_WIDTH) and (x0 >= 0) and (y0 < TOTAL_HEIGHT) and (y0 >= 0):
                self.bitmap[int(x0),int(y0)] = int(color)
            if (x0 == x1) and (y0 == y1):
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def draw_point(self, x, y, color):
        if (x < TOTAL_WIDTH) and (x >= 0) and (y < TOTAL_HEIGHT) and (y >= 0):
            self.bitmap[math.floor(x) + math.floor(y) * TOTAL_WIDTH] = math.floor(color)

    #############################################
    # >> rotate_point() <<
    # Takes x & y coords and rotates them
    # around inputted origin coords.
    # ---------------------------------
    # NOTE: Supply angle when calling.
    # ---------------------------------
    # TODO:
    #############################################
    def rotate_point(self, pX, pY, oX, oY, angle):
        angle = angle * math.pi / 180.0
        x = math.cos(angle)*(pX-oX) - math.sin(angle)*(pY-oY) + oX
        y = math.sin(angle)*(pX-oX) + math.cos(angle)*(pY-oY) + oX
        return math.ceil(x),math.ceil(y)

    #############################################
    # Draws a shape based off of points
    # and Bresenham's line algorithm.
    # ---------------------------------
    # NOTE:
    # ---------------------------------
    # TODO:
    # * Generate shapes programmatically
    #   based off of user input
    # * Design smoother auditory reactions
    #############################################
    def visualize_shape(self, data, sides):
        widthHeight = min(TOTAL_HEIGHT-1, TOTAL_WIDTH-1)
        spacing = widthHeight//3
        avgAmp = ulab.numerical.mean(data[0:0+AVG_RATE])

        secondaryPosX = ulab.linspace(spacing, TOTAL_WIDTH-1 - spacing, 2)
        secondaryPosY = ulab.linspace(spacing, (TOTAL_HEIGHT)-1 - spacing, 2)

        f = 1/16
        w = 2 * math.pi * f
        v = 32
        k = (2 * math.pi) / v
        rot = self.rotation
        #p = rotation * math.pi / 180
        sn = avgAmp * 0.05 * math.sin(k + w * rot)
        cs = avgAmp * 0.05 * math.cos(k + w * rot)
        offsetX = sn if avgAmp > 10 else 0
        offsetY = cs if avgAmp > 10 else 0
        origShiftX = offsetX + ORIGIN_WIDTH
        origShiftY = offsetY + ORIGIN_HEIGHT

        radius = avgAmp + 4
        segment = math.pi * 2 / sides
        points = []
        secondaryPoints = []

        for i in range(sides):
            x = radius * math.sin(i * segment) + origShiftX
            y = radius * math.cos(i * segment) + origShiftY

            xPlus = (radius + 3) * math.sin(i * segment) + origShiftX
            yPlus = (radius + 3) * math.cos(i * segment) + origShiftY

            rotX, rotY = self.rotate_point(x,y, origShiftX, origShiftY, rot)
            xRotPlus, yRotPlus = self.rotate_point(xPlus, yPlus, origShiftX, origShiftY, -rot)

            points.append((rotX,rotY))
            secondaryPoints.append((xRotPlus,yRotPlus))


        for j in range(len(points)):
            p = points[j]
            pPlus = secondaryPoints[j]
            nxt = (j + 1) % sides
            self.draw_bresenham_line(p[0], p[1], points[nxt][0], points[nxt][1], int(avgAmp))
            self.draw_point(pPlus[0], pPlus[1], int(avgAmp))


        self.update_rotation(5)
