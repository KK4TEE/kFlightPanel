#kFlight by KK4TEE
#Started 2014-9-24
#Cumulative time so far: around 22 hours
#Please keep in mind this is my first time using pygame
#and only my 2nd python project. That said, I hope you can
#gain some use from my work here. Cheers!
#
#ToDo list:
#   write a proper timing routine
#   code vertical speed and altitude bars
#   add more text readouts
#   internalize navball texture

import time
import os, sys
import pygame
from pygame.locals import *
from math import pi, radians, sin, cos, tan
from copy import *
import json
import urllib2

import config

if not pygame.font: 
    print ('Warning, fonts disabled')
if not pygame.mixer: 
    print ('Warning, sound disabled')


def telemetry(oldNews):
    #I need to figure out how to use error handling  properly.
    # The program will still occasionally crash with key errors
    #if an update fails partway through.

    oldNews = deepcopy(oldNews)
    try:
        tele = json.load(urllib2.urlopen(config.URL + \
            'VesselName=v.name' + '&' +\
            'BodyName=v.body' + '&' +\
            'RadarAlt=v.heightFromTerrain' + '&' +\
            'MET=v.missionTime' + '&' +\
            'Altitude=v.altitude' + '&' +\
            'ApA=o.ApA' + '&' +\
            'PeA=o.PeA' + '&' +\
            \
            'Pitch=n.pitch' + '&' +\
            'Roll=n.roll' + '&' +\
            'Heading=n.heading' + '&' +\
            \
            'LiquidFuel=r.resource[LiquidFuel]' + '&' +\
            'LiquidFuelMax=r.resourceMax[LiquidFuel]' + '&' +\
            'Oxidizer=r.resource[Oxidizer]' + '&' +\
            'OxidizerMax=r.resourceMax[Oxidizer]' + '&' +\
            'MonoPropellant=r.resource[MonoPropellant]' + '&' +\
            'MonoPropellantMax=r.resourceMax[MonoPropellant]' + '&' +\
            'ElectricCharge=r.resource[ElectricCharge]' + '&' +\
            'ElectricChargeMax=r.resourceMax[ElectricCharge]' + '&' +\
            \
            'Throttle=f.throttle' + '&' +\
            'Light=v.lightValue' + '&' +\
            'Brake=v.brakeValue' + '&' +\
            'Gear=v.gearValue' + '&' +\
            'SAS=v.sasValue' + '&' +\
            'RCS=v.rcsValue'
            ))
        #print tele
        if tele['Pitch'] > 0:
            pass
        return tele
    except:
        print ('Telemachus update failed')
        return oldNews


def clamp(num, minn, maxn):
    if num < minn:
        return minn
    elif num > maxn:
        return maxn
    else:
        return num


def rot_center(image, angle):
    """rotate an image while keeping its center and size"""
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    rot_rect.center = rot_image.get_rect().center
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image


def percentScale(lowVal, highVal, currentVal):
    scaleDiff = float(highVal-lowVal)
    spotOnScale = float(currentVal - lowVal)
    return (spotOnScale/scaleDiff)*100

def formatPercentAsString(val):
    rv = clamp(round(val,2),-10,100)
    return "{:3.2f}".format(rv)

def drawTextReadouts(screen, position, tele):
    x, y = position
    boxX, boxY = (430,700)
    color = (0,255,0)
    fontSize = 24
    yLineSpace = 10
    fontHeader = pygame.font.Font(None, 30)
    text = 'Flight Status'
    Header = fontHeader.render(text, 1, (0, 255, 0))
    tx, ty = fontHeader.size(text)
    screen.blit(Header, (x+boxX/2-tx/2, y+ty/2))

    font = pygame.font.Font(None, fontSize)
    xLine = x + 10
    yLine = y + fontSize + 5

    #Ship's Name
    text = 'Vessel:'
    tx, ty = font.size(text)
    screen.blit(font.render(text, 1, color), (xLine, yLine + ty/2))
    tx, ty = font.size(tele['VesselName'])
    xLine = x + boxX - 5 - tx
    screen.blit(font.render(tele['VesselName'], 1, color), (xLine, yLine + ty/2))
    xLine = x + 10
    yLine += ty + yLineSpace

    #Body Name
    text = 'Planatary Body:'
    tx, ty = font.size(text)
    screen.blit(font.render(text, 1, color), (xLine, yLine + ty/2))
    tx, ty = font.size(tele['BodyName'])
    xLine = x + boxX - 5 - tx
    screen.blit(font.render(tele['BodyName'], 1, color), (xLine, yLine + ty/2))
    xLine = x + 10
    yLine += ty + yLineSpace

    #Radar Altitude
    text = 'Radar Altitude:'
    tx, ty = font.size(text)
    screen.blit(font.render(text, 1, color), (xLine, yLine + ty/2))
    tx, ty = font.size(str(tele['RadarAlt']))
    xLine = x + boxX - 5 - tx
    screen.blit(font.render(str(tele['RadarAlt']), 1, color), (xLine, yLine + ty/2))
    xLine = x + 10
    yLine += ty + yLineSpace


    #Box border
    pygame.draw.rect(screen, (128, 128, 128), \
            (x,y,boxX,boxY), 4)


def drawPrimaryFlightDisplay(screen, position, tele):
    x, y = position
    boxX, boxY = (600,535)
    #boxX, boxY = (525,525)
    sidecut = 5.0 #this is a fraction
    PFDbackground = pygame.Surface((boxX,boxY))
    PFDbackground.set_colorkey((255,255,254))
    PFDbackground.fill((0, 0, 0))
    pygame.draw.circle(PFDbackground, (255,255,254), (boxX/2, boxY/2), (boxY-20)/2, 0)
    pygame.draw.rect(PFDbackground, (0,0,0), \
            (0, 0,boxX/sidecut, boxY), 0)
    pygame.draw.rect(PFDbackground, (0,0,0), \
            (boxX-boxX/sidecut, 0,boxX, boxY), 0)


    screen.blit(PFDbackground, position)

    #Ship stencel
    pygame.draw.rect(screen, (255,255,200), \
            (boxX/2-boxX/5/2,boxY/2,boxX/5,5), 2)
    pygame.draw.line(screen, (255,255,200), (boxX/2-boxX/5, boxY/2), \
            (boxX/2+boxX/5, boxY/2), 3)
    #Box border
    pygame.draw.rect(screen, (128, 128, 128), \
            (x,y,boxX,boxY), 4)
    #pygame.draw.circle(screen, (0,0,200), (x+boxX/2, y+boxY/2), (boxY-20)/2, 1)




def drawLEDBox(screen, label, position, lit, color):
    x, y = position
    boxX, boxY = (160,80)
    font = pygame.font.Font(None, 42)
    lx, ly = font.size(label)
    #print "LED font position: " + str(lx) + " - " + str(ly)
    if lit is True or lit == 'True' or (lit > 0 and lit <= 1): #Accept bool or string True
        pygame.draw.rect(screen, color, \
            (x,y,boxX,boxY), 0)
        text = font.render(label, 1, (255, 255, 255))
        screen.blit(text, (x+boxX/2-lx/2, y+boxY/2-ly/2))
    else:
        pygame.draw.rect(screen, (50, 50, 50), \
            (x,y,boxX,boxY), 0)
        text = font.render(label, 1, (1, 1, 1))
        screen.blit(text, (x+boxX/2-lx/2, y+boxY/2-ly/2))

    #Box border
    pygame.draw.rect(screen, (128, 128, 128), \
            (x,y,boxX,boxY), 4)



def drawAnalogGauge(screen, gaugeLabel, position, lowVal, highVal, currentVal):
    x, y = position #Modify this def to add ability to resize the gauges automatically
    percentOfGaugeRange = percentScale(lowVal, highVal, currentVal)
    inverseGaugeFill = ((5*pi/4) / (highVal-lowVal) * (highVal-currentVal))
    gaugeFill = ((5*pi/4) / (highVal-lowVal) * currentVal)
    fillThickness = 20
    #Outer Ring
    pygame.draw.circle(screen, (0,127,0), position, 100, 1)

    font = pygame.font.Font(None, 28)
    gtext0 = font.render(str(formatPercentAsString(percentOfGaugeRange)) + '%', 1, (20, 255, 20))
    gtext1 = font.render(gaugeLabel, 1, (20, 255, 20))
    x, y = position
    lx, ly = font.size(gaugeLabel)
    screen.blit(gtext0, (x-25, y-14))
    screen.blit(gtext1, (x-lx/2, y+ly/2))

    #arc(Surface, color, Rect, start_angle, stop_angle, width=1)
    if percentOfGaugeRange > 0 and percentOfGaugeRange < 15:
        #Red Section
        pygame.draw.arc(screen, (255, 0, 0), [x-99, y-99, 198, 198], \
             inverseGaugeFill + pi/4, \
             inverseGaugeFill + pi/4 + gaugeFill, \
             fillThickness)
    elif percentOfGaugeRange >= 15 and percentOfGaugeRange < 33:
        #Yellow Section
        pygame.draw.arc(screen, (255, 255, 0), [x-99, y-99, 198, 198], \
             inverseGaugeFill + pi/4, \
             inverseGaugeFill + pi/4 + gaugeFill, \
             fillThickness)
    elif percentOfGaugeRange >= 33 and percentOfGaugeRange <= 100:
        #Green Section
        pygame.draw.arc(screen, (0, 255, 0), [x-99, y-99, 198, 198], \
             inverseGaugeFill + pi/4, \
             inverseGaugeFill + pi/4 + gaugeFill, \
             fillThickness)
    else:
        #White Section
        pygame.draw.arc(screen, (255, 255, 255), [x-99, y-99, 198, 198], \
             inverseGaugeFill + pi/4, \
             inverseGaugeFill + pi/4 + gaugeFill, \
             fillThickness)

class PyManMain:
    """The Main PyMan Class - This class handles the main
    initialization and creating of the Game."""

    def __init__(self):
        """Initialize"""
        """Initialize PyGame"""
        pygame.init()
        """Set the window Size"""
        self.width, self.height = config.ScreenDimensions
        self.display_trace_color = (0, 255, 0)
        """Create the Screen"""
        if config.GoFullscreen is True:
            self.screen = pygame.display.set_mode((0,0), FULLSCREEN | DOUBLEBUF, 0)
            self.background = pygame.Surface(pygame.display.list_modes()[0])
            print ("Going fullscreen")
        else:
            self.screen = pygame.display.set_mode((self.width, self.height), 0, 0)
              #Note: RESIZEABLE can go as the 2nd to last option, but things get messy
            print ("Resolution set to " + str(config.ScreenDimensions))
            self.background = pygame.Surface(self.screen.get_size())
        pygame.display.set_caption('kFlight by KK4TEE')

        #self.navImg = pygame.image.load(os.path.join('data', 'navball.png'))
        nixie0 = pygame.image.load(os.path.join('data', 'nixie_tube', '0.png'))
        nixie1 = pygame.image.load(os.path.join('data', 'nixie_tube', '1.png'))
        nixie2 = pygame.image.load(os.path.join('data', 'nixie_tube', '2.png'))
        nixie3 = pygame.image.load(os.path.join('data', 'nixie_tube', '3.png'))
        nixie4 = pygame.image.load(os.path.join('data', 'nixie_tube', '4.png'))
        nixie5 = pygame.image.load(os.path.join('data', 'nixie_tube', '5.png'))
        nixie6 = pygame.image.load(os.path.join('data', 'nixie_tube', '6.png'))
        nixie7 = pygame.image.load(os.path.join('data', 'nixie_tube', '7.png'))
        nixie8 = pygame.image.load(os.path.join('data', 'nixie_tube', '8.png'))
        nixie9 = pygame.image.load(os.path.join('data', 'nixie_tube', '9.png'))
        nixiedl = pygame.image.load(os.path.join('data', 'nixie_tube', 'dl.png'))
        nixiedr = pygame.image.load(os.path.join('data', 'nixie_tube', 'dr.png'))
        self.nixieList = [nixie0, nixie1, nixie2, nixie3, nixie4, nixie5,
            nixie6, nixie7, nixie8, nixie9, nixiedl, nixiedr]
        self.navImg = pygame.Surface((1400,1400))
        pygame.draw.rect(self.navImg, (128,128,255), \
            (0, 0,1400, 700), 0)
        pygame.draw.rect(self.navImg, (128,64,0), \
            (0, 700,1400, 1400), 0)

        self.navImg.convert()
        self.navImg = pygame.transform.scale(self.navImg, (1400,1400))

        #Set up the 8-ball layer for the Primary Flight Display
        #self.navball = pygame.display.set_mode((800, 800), 0, 0)

        #Set up the PFD Layer
        #self.PFD = pygame.display.set_mode((600, 525), 0, 0)

        #Set up the black background layer
        self.background = self.background.convert()
        self.background.fill((0, 0, 0))


    def AnalogGauges(self, xOffset, yOffset, radius,tele):
        xOffset += radius/2
        yOffset += radius/2
        if tele['MonoPropellant'] is not -1:
            drawAnalogGauge(self.screen, "Mono Prop", (xOffset, yOffset), 0,\
                tele['MonoPropellantMax'], tele['MonoPropellant'])
        xOffset += radius + config.SpaceBetweenGaugesX
        if tele['LiquidFuel'] is not -1:
            drawAnalogGauge(self.screen, "Liquid Fuel", (xOffset, yOffset), 0, \
                tele['LiquidFuelMax'], tele['LiquidFuel'])
            xOffset += radius + config.SpaceBetweenGaugesX
        if tele['Oxidizer'] is not -1:
            drawAnalogGauge(self.screen, "Oxidizer", (xOffset, yOffset), 0,\
                tele['OxidizerMax'], tele['Oxidizer'])
            xOffset += radius + config.SpaceBetweenGaugesX
        if tele['ElectricCharge'] is not -1:
            drawAnalogGauge(self.screen, "Electricity", (xOffset, yOffset), 0,\
                tele['ElectricChargeMax'], tele['ElectricCharge'])
            xOffset += radius + config.SpaceBetweenGaugesX
            xOffset += radius + config.SpaceBetweenGaugesX


    def LEDBoxes(self, x, y, boxX, boxY, tele):
        xOffset, yOffset = x, y
        drawLEDBox(self.screen, 'Alarm', (xOffset,yOffset), False, (255,0,0))
        xOffset += boxX + 5
        drawLEDBox(self.screen, 'Throttle', (xOffset,yOffset), tele['Throttle'], (220,220,20))

        xOffset, yOffset = x, y + boxY + 5
        drawLEDBox(self.screen, 'SAS', (xOffset,yOffset), tele['SAS'], (40,40,245))
        xOffset += boxX+ 5
        drawLEDBox(self.screen, 'RCS', (xOffset,yOffset), tele['RCS'], (210,210,210))

        xOffset, yOffset = x, yOffset + boxY + 5
        drawLEDBox(self.screen, 'Gear', (xOffset,yOffset), tele['Gear'], (40,245,40))
        xOffset += boxX + 5
        drawLEDBox(self.screen, 'Brake', (xOffset,yOffset), tele['Brake'], (245,40,40))

        xOffset, yOffset = x, yOffset + boxY + 5
        drawLEDBox(self.screen, 'Light', (xOffset,yOffset), tele['Light'], (245,245,40))
        xOffset += boxX+ 5
        drawLEDBox(self.screen, 'G-Force', (xOffset,yOffset), False, (245,40,40))

        xOffset, yOffset = x, yOffset + boxY + 5
        drawLEDBox(self.screen, 'EVA', (xOffset,yOffset), False, (245,245,40))
        xOffset += boxX+ 5
        drawLEDBox(self.screen, 'Landed', (xOffset,yOffset), False, (245,40,40))

        xOffset, yOffset = x, yOffset + boxY + 5
        if self.tele['RadarAlt'] != -1:
            drawLEDBox(self.screen, 'SurfRadar', (xOffset,yOffset), True, (245,245,40))
        else:
            drawLEDBox(self.screen, 'SurfRadar', (xOffset,yOffset), False, (245,245,40))
        xOffset += boxX + 5
        drawLEDBox(self.screen, 'Pilot Ejected', (xOffset,yOffset), False, (245,40,40))


    def NavBallImg(self, screen, X, Y, roll, pitch, heading):
        navballSize = (520,520)
        #navballSize = (450,450)
        nsX, nsY = navballSize
        radius = nsX/2
        navball = pygame.Surface(navballSize)
        niX, niY = self.navImg.get_size()
        #print "Pitch: " + str(pitch) + " Roll: " + str(roll)
        #Roll
        navImg = pygame.Surface((niX,niY))
        text = str(int(round(heading)))
        color = (255,255,255)
        font = pygame.font.Font(None, 28)
        tx, ty = font.size(text)
        navImg.blit(self.navImg, (0, 3*pitch))
        navball.blit(navImg, ( -niX/2 + nsX/2, -niY/2 + nsY/2  ))
        navball.blit(rot_center(navball, roll), (0,0))
#        navball.blit(navImg, (-niX/2+200, -niY/2+250))
        navball.blit(font.render(text, 1, color), (nsX/2-ty/2, nsY/2- ty/2))
        screen.blit(navball, (X - nsX/2,Y - nsY/2 -2))

    def Nt(self, screen, X, Y, V):
        nixieSize = self.nixieList[V].get_size()
        niX, niY = nixieSize
        nixie = pygame.Surface(nixieSize)
        #nixie.blit(self.nixie0, (niX / 2 + nsX / 2, -niY / 2 + nsY / 2))
        nixie.blit(self.nixieList[V], (0,0))
        screen.blit(nixie, (X, Y))

    def NixieReadout(self, screen, cX, cY, Num):
        n = min(abs(int(Num)), 999999)
        deltaWidth, deltaHeight = self.nixieList[0].get_size()
        self.Nt(self.screen, cX, cY, (n / 100000) % 10)
        cX += deltaWidth
        self.Nt(self.screen, cX, cY, (n / 10000) % 10)
        cX += deltaWidth
        self.Nt(self.screen, cX, cY, (n / 1000) % 10)
        cX += deltaWidth
        self.Nt(self.screen, cX, cY, (n / 100) % 10)
        cX += deltaWidth
        self.Nt(self.screen, cX, cY, (n / 10) % 10)
        cX += deltaWidth
        self.Nt(self.screen, cX, cY, (n / 1) % 10)


    def TextTelementry(self, xOffset, yOffset):
        pass


    def DrawBorder(self):
        info =  pygame.display.Info()
        pygame.draw.rect(self.screen, (0, 128, 0), \
            (2,2,info.current_w - 5,info.current_h - 5), 2)


    def UserHandler(self):
        pygameEvents = pygame.event.get()
        keysPressedList = []
        for event in pygameEvents:
            if event.type == pygame.KEYDOWN:
                if event.key == K_ESCAPE:
                    print ("Exiting by ESC")
                    sys.exit()
                if event.key == K_q:
                    print ("q")


        ''' #Instead of using a qeue, see what is being pressed RIGHT NOW
        keysPressed = pygame.key.get_pressed()
        if (keysPressed[K_ESCAPE]):
            print "Exiting by ESC"
            sys.exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print 'pygame Quit'
                sys.exit()
        '''

    def MainLoop(self):
        print ("Resolutions detected: "+str(pygame.display.list_modes()))
        frameCount = 0
        xM, yM = self.screen.get_size()
        self.tele = {}
        lasttime = time.time()
        self.screen.blit(self.background, (0, 0))
        self.DrawBorder()
        programStartTime = time.time()

        self.tele= {u'MonoPropellant': 189.084091375693,u'ApA': 0.0, u'PeA': 0.0,u'Altitude': 2109111.7047641, u'LiquidFuelMax': 720, u'RCS': u'False', u'ElectricChargeMax': 950.159999996424, u'Oxidizer': 478.732902340961, u'Roll': 8.91797637939453, u'Gear': u'False', u'SAS': u'False', u'Throttle': 0, u'BodyName': u'Kerbin', u'MonoPropellantMax': 190, u'Light': u'True', u'RadarAlt': -1, u'LiquidFuel': 391.690572273977, u'Heading': 174.4286, u'OxidizerMax': 880, u'VesselName': u'Mark1-2Pod (Kerbal X)', u'ElectricCharge': 950.006827276331, u'MET': 3456.6799228806, u'Brake': u'True', u'Pitch': -8.6469259262085}


        while 1:
            pygame.time.Clock().tick(config.RefreshRate)
            self.UserHandler()
            self.screen.blit(self.background, (0, 0))
            #self.DrawBorder()
            self.tele = telemetry(self.tele)
            #print self.tele

            self.NavBallImg(self.screen, 250 + 50, 250 + 25,
                -self.tele['Roll'], self.tele['Pitch'],
                self.tele['Heading'])
            self.AnalogGauges(config.SpaceBetweenGaugesX + 5,
                yM - config.SpaceBetweenGaugesX - 200 - 5,
                200, self.tele)
            self.LEDBoxes(xM-0-760,0, 160, 80, self.tele)
            drawTextReadouts(self.screen, (xM-0-430, 0), self.tele)
            drawPrimaryFlightDisplay(self.screen, (0,0), self.tele)

            self.NixieReadout(self.screen, xM - 427, 150, self.tele['MET'])
            self.NixieReadout(self.screen, xM - 427, 290, self.tele['Altitude'])
            self.NixieReadout(self.screen, xM - 427, 430, self.tele['ApA'])
            self.NixieReadout(self.screen, xM - 427, 560, self.tele['PeA'])

            pygame.display.flip()
            frameCount += 1

            #####Debugging#####
            currentTime = time.time()
            looptime = currentTime - lasttime
            lasttime = currentTime
            print ("")
            print ("Frame Count: " + str(frameCount))
            print ("Loop time:   " + str(looptime) + "s")
            print ("FramesPerSec:" + str(1.0/looptime))
            print ("Avg FPS:     " + str(frameCount/(currentTime - programStartTime)) + "FPS")
            print ("Program Run:       " + str(currentTime - programStartTime))
            #print self.tele
            self.tele['Roll'] +=50*looptime

            '''
            if looptime < 1.0/config.RefreshRate:
                time.sleep(1.0/config.RefreshRate - looptime)
                print "Sleeping" + str(1.0/config.RefreshRate - looptime)'''


if __name__ == "__main__":
    MainWindow = PyManMain()
    MainWindow.MainLoop()
