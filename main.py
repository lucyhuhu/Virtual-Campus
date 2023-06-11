from os import path
import pandas as pd
from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as request
from cmu_112_graphics import *
from map import *
import random
# This is the main file that runs the app and includes most drawing functions.

# images:
# https://www.cmu.edu/cdfd/master-plan/2022-master-plan-introduction-and-planning-process.pdf
# https://www.redbubble.com/i/sticker/cmk-by-clairekeanna/29859239.EJUG5
# https://www.redbubble.com/i/sticker/cmu-by-clairekeanna/29859200.EJUG5
# https://www.cmu.edu/hub/contact/
# https://www.moorerubleyudell.com/projects/tepper-quad-carnegie-mellon-university
# https://ikminc.com/projects/carnegie-mellon-university-gates-hillman-center-classrooms/
# https://www.cmu.edu/computing/services/teach-learn/tes/classrooms/locations/doherty.html
# https://www.cmu.edu/cohon-university-center/center-facilities/Kirr-Commons/index.html
# http://gigapan.com/gigapans/33308
# https://ikminc.com/projects/carnegie-mellon-university-wean-hall-lobby/cmu-wean-hall-interior-03/
# https://www.flickr.com/photos/32215181@N08/5521124726
# https://commons.wikimedia.org/wiki/File:Carnegie_Mellon_University_College_of_Fine_Arts_building_-_hallway.jpg
# https://www.cmu.edu/computing/services/teach-learn/tes/computer-labs/locations/cyert-labs.html
# http://www.libraryofthefuture.org/blog/2015/4/24/when-your-students-are-nascent-architects
# https://stock.photoshelter.com/image/I00005W9cp5V7kw0
# https://www.cmu.edu/computing/services/teach-learn/tes/classrooms/locations/posner.html
# I took the pictures for ph, hbh, warner, and the cut

# https://www.cs.cmu.edu/~112/notes/notes-animations-part4.html#imageMethods
# https://www.wikipython.com/tkinter-ttk-tix/summary-information/colors/


class User():
    def __init__(self):
        self.cx, self.cy, self.r = 810, 498, 8  # user location
        self.dx, self.dy = 0, 0


# after running webscraping.py to create the excel:
# read the excel
df1 = pd.read_excel('students.xlsx')


def appStarted(app):
    app.user = User()
    app.g = g
    app.start, app.destination = cut, None
    app.path = dict()
    app.inside = False
    app.df = df1
    app.studentsInfo = dict()  # {building:2d list of student info}
    app.studentsLocation = dict()  # {building:(x, y, dx, dy, isPaused)}
    app.infoToDisplay = list()
    app.studentClicked = list()

    app.image1 = app.loadImage('campus map.png')
    app.studentImage = app.loadImage('student.png')
    app.userImage1 = app.loadImage('user.png')

    app.userImage = app.scaleImage(app.userImage1, 1/10)
    tepImage = app.loadImage('tep.png')

    app.tepImage = app.scaleImage(tepImage, 2)
    ghcImage = app.loadImage('ghc.png')

    app.ghcImage = app.scaleImage(ghcImage, 2)
    dhImage = app.loadImage('dh.png')

    app.dhImage = app.scaleImage(dhImage, 2)
    cucImage = app.loadImage('cuc.png')

    app.cucImage = app.scaleImage(cucImage, 2)
    nshImage = app.loadImage('nsh.png')

    app.nshImage = app.scaleImage(nshImage, 2.5)
    wehImage = app.loadImage('weh.png')

    app.wehImage = app.scaleImage(wehImage, 1.5)

    bhImage = app.loadImage('bh.png')
    app.bhImage = app.scaleImage(bhImage, 1.5)

    app.cfaImage = app.loadImage('cfa.png')

    cyhImage = app.loadImage('cyh.png')
    app.cyhImage = app.scaleImage(cyhImage, 2)

    app.hbhImage = app.loadImage('hbh.png')

    hlImage = app.loadImage('hl.png')
    app.hlImage = app.scaleImage(hlImage, 2)

    miImage = app.loadImage('mi.png')
    app.miImage = app.scaleImage(miImage, 2.5)

    phImage = app.loadImage('ph.png')
    app.phImage = app.scaleImage(phImage, 1.2)

    posImage = app.loadImage('pos.png')
    app.posImage = app.scaleImage(posImage, 2)

    app.whImage = app.loadImage('wh.png')

    app.cutImage = app.loadImage('cut.png')

    getStudents(app)


def timerFired(app):
    # to move the user:
    if app.destination != None:
        x1, y1 = app.destination.cx, app.destination.cy
        # update the user location to the closest building:
        for name, vertex in app.g.vertices.items():
            x, y = vertex.cx, vertex.cy
            d = ((app.user.cx-x)**2+(app.user.cy-y)**2)**0.5
            if (d <= vertex.r):
                app.start = vertex
                app.user.cx, app.user.cy = vertex.cx, vertex.cy
                # move the user based on the x and y distance:
                if ((x1-app.user.cx > 0) == ((x1-app.start.cx) > 0) and
                        (y1-app.user.cy > 0) == ((y1-app.start.cy) > 0)):
                    app.user.dx = (x1-app.user.cx)/1000000
                    app.user.dy = (x1-app.user.cy)/1000000
                    app.user.cx = app.user.cx + app.user.dx
                    app.user.cy = app.user.cy + app.user.dy
                app.user.dx, app.user.dy = 0, 0
    # to move the students:
    for building, locations in app.studentsLocation.items():
        for i in range(len(locations)):
            (x, y, dx, dy, isPaused) = locations[i]
            if isPaused == True:
                dx, dy = 0, 0

            x += dx
            y += dy
            locations[i] = (x, y, dx, dy, isPaused)  # update locations
            if x < 0 or x > app.width or y < 0 or y > app.height:
                locations.remove((x, y, dx, dy, isPaused))
                x, y = random.randrange(
                    100, app.width-100), random.randrange(677, app.height-20)
                dx, dy = random.randint(-3, 3), random.randint(-3, 3)
                locations.append((x, y, dx, dy, isPaused))


def mousePressed(app, event):
    if not app.inside:
        # get current location:
        for name, vertex in app.g.vertices.items():
            x0, y0 = vertex.cx, vertex.cy
            x1, y1 = app.user.cx, app.user.cy  # current location
            d = ((x1-x0)**2+(y1-y0)**2)**0.5
            if (d <= vertex.r):
                app.start = vertex

        # get destination:
        for name, vertex in app.g.vertices.items():
            x0, y0 = vertex.cx, vertex.cy
            x1, y1 = event.x, event.y
            d = ((x1-x0)**2+(y1-y0)**2)**0.5
            # if click inside a circle (that is not the current location):
            if d <= vertex.r and vertex != app.start:
                app.destination = vertex  # save as destination
                app.path = app.g.findPath(app.start, app.destination)
                # update user location:
                app.user.cx, app.user.cy = app.destination.cx, app.destination.cy
            # if click at the user location (to enter the building):
            elif d <= vertex.r and vertex == app.start:
                app.inside = True
    if app.inside:
        # empty the lists every time you enter a new building:
        app.infoToDisplay = list()
        app.studentClicked = list()
        width, height = app.studentImage.size
        width, height = width/5, height/5

        for i in range(len(app.studentsLocation[app.start.name])):
            (x, y, dx, dy, isPaused) = app.studentsLocation[app.start.name][i]

            # if click on a student:
            if (x-width/2 < event.x < x+width/2 and
                    y-height/2 < event.y < y+height/2):
                isPaused = not isPaused
                app.studentsLocation[app.start.name][i] = (
                    x, y, dx, dy, isPaused)
                if isPaused == False:
                    dx, dy = random.randint(-3, 3), random.randint(-3, 3)
                    app.studentsLocation[app.start.name][i] = (
                        x, y, dx, dy, isPaused)
                info = app.studentsInfo[app.start.name][i]
                location = (x, y)
                if ((info not in app.infoToDisplay) and
                        (location not in app.studentClicked)):
                    app.infoToDisplay.append(
                        app.studentsInfo[app.start.name][i])
                    app.studentClicked.append((x, y, isPaused))

    # click on home button:
    if 1300 < event.x < 1350 and 700 < event.y < 730:
        app.inside = False


def drawInside(app, canvas):
    # get the image inside the buidling:
    if abs(app.user.cx - tep.cx) <= app.user.r and abs(app.user.cy - tep.cy) <= app.user.r:
        imageWidth, imageHeight = app.tepImage.size
        canvas.create_image(imageWidth/2, imageHeight/2,
                            image=ImageTk.PhotoImage(app.tepImage))
        # draw students inside the buidling:
        for location in app.studentsLocation['TEP']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))

    elif abs(app.user.cx - ghc.cx) <= app.user.r and abs(app.user.cy - ghc.cy) <= app.user.r:
        imageWidth, imageHeight = app.ghcImage.size
        canvas.create_image(imageWidth/3, imageHeight/3,
                            image=ImageTk.PhotoImage(app.ghcImage))
        for location in app.studentsLocation['GHC']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))

    elif abs(app.user.cx - dh.cx) <= app.user.r and abs(app.user.cy - dh.cy) <= app.user.r:
        imageWidth, imageHeight = app.dhImage.size
        canvas.create_image(imageWidth/2, imageHeight/2,
                            image=ImageTk.PhotoImage(app.dhImage))
        for location in app.studentsLocation['DH']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - cuc.cx) <= app.user.r and abs(app.user.cy - cuc.cy) <= app.user.r:
        imageWidth, imageHeight = app.cucImage.size
        canvas.create_image(imageWidth/3, imageHeight/3,
                            image=ImageTk.PhotoImage(app.cucImage))
        for location in app.studentsLocation['CUC']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - nsh.cx) <= app.user.r and abs(app.user.cy - nsh.cy) <= app.user.r:
        imageWidth, imageHeight = app.nshImage.size
        canvas.create_image(imageWidth/2, imageHeight/2.5,
                            image=ImageTk.PhotoImage(app.nshImage))
        for location in app.studentsLocation['NSH']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - weh.cx) <= app.user.r and abs(app.user.cy - weh.cy) <= app.user.r:
        imageWidth, imageHeight = app.wehImage.size
        canvas.create_image(imageWidth/2, imageHeight/2.5,
                            image=ImageTk.PhotoImage(app.wehImage))
        for location in app.studentsLocation['WEH']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - bh.cx) <= app.user.r and abs(app.user.cy - bh.cy) <= app.user.r:
        imageWidth, imageHeight = app.bhImage.size
        canvas.create_image(imageWidth/2, imageHeight/2,
                            image=ImageTk.PhotoImage(app.bhImage))
        for location in app.studentsLocation['BH']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - cfa.cx) <= app.user.r and abs(app.user.cy - cfa.cy) <= app.user.r:
        imageWidth, imageHeight = app.cfaImage.size
        canvas.create_image(70+imageWidth/3, imageHeight/3,
                            image=ImageTk.PhotoImage(app.cfaImage))
        for location in app.studentsLocation['CFA']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - cyh.cx) <= app.user.r and abs(app.user.cy - cyh.cy) <= app.user.r:
        imageWidth, imageHeight = app.cyhImage.size
        canvas.create_image(imageWidth/3, imageHeight/3,
                            image=ImageTk.PhotoImage(app.cyhImage))
        for location in app.studentsLocation['CYH']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - hbh.cx) <= app.user.r and abs(app.user.cy - hbh.cy) <= app.user.r:
        imageWidth, imageHeight = app.hbhImage.size
        canvas.create_image(imageWidth/2, imageHeight/2,
                            image=ImageTk.PhotoImage(app.hbhImage))
        for location in app.studentsLocation['HBH']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - hl.cx) <= app.user.r and abs(app.user.cy - hl.cy) <= app.user.r:
        imageWidth, imageHeight = app.hlImage.size
        canvas.create_image(imageWidth/2.5+50, imageHeight/2.5+50,
                            image=ImageTk.PhotoImage(app.hlImage))
        for location in app.studentsLocation['HL']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - mi.cx) <= app.user.r and abs(app.user.cy - mi.cy) <= app.user.r:
        imageWidth, imageHeight = app.miImage.size
        canvas.create_image(imageWidth/2.5+50, imageHeight/2.5+50,
                            image=ImageTk.PhotoImage(app.miImage))
        for location in app.studentsLocation['MI']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - ph.cx) <= app.user.r and abs(app.user.cy - ph.cy) <= app.user.r:
        imageWidth, imageHeight = app.phImage.size
        canvas.create_image(imageWidth/2, imageHeight/2,
                            image=ImageTk.PhotoImage(app.phImage))
        for location in app.studentsLocation['PH']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - pos.cx) <= app.user.r and abs(app.user.cy - pos.cy) <= app.user.r:
        imageWidth, imageHeight = app.posImage.size
        canvas.create_image(imageWidth/2, imageHeight/2,
                            image=ImageTk.PhotoImage(app.posImage))
        for location in app.studentsLocation['POS']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - wh.cx) <= app.user.r and abs(app.user.cy - wh.cy) <= app.user.r:
        imageWidth, imageHeight = app.whImage.size
        canvas.create_image(700, 500,
                            image=ImageTk.PhotoImage(app.whImage))
        for location in app.studentsLocation['WH']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))
    elif abs(app.user.cx - cut.cx) <= app.user.r and abs(app.user.cy - cut.cy) <= app.user.r:
        imageWidth, imageHeight = app.cutImage.size
        canvas.create_image(700, 300,
                            image=ImageTk.PhotoImage(app.cutImage))
        for location in app.studentsLocation['Cut']:
            x, y, dx, dy, isPaused = location
            studentImage = app.scaleImage(app.studentImage, 1/5)
            canvas.create_image(x, y, image=ImageTk.PhotoImage(studentImage))


def drawStudentInfo(app, canvas):
    if app.infoToDisplay != list():
        width, height = app.studentImage.size
        for location in app.studentClicked:
            x, y, isPaused = location[0], location[1], location[2]
            if isPaused:
                x0, y0 = x, y-90
                x1, y1 = x+width, y0+70
                if x1 > app.width:
                    x1, y1 = app.width-20, y+30
                    x0, y0 = x1-width, y1-70
                for info in app.infoToDisplay:
                    i, year, college, major = info[0], info[1], info[2], info[3]
                    classes, building, doing = info[4], info[5], info[6]
                    midx = (x1+x0)/2
                    canvas.create_rectangle(x0, y0, x1, y1, fill='light cyan')
                    canvas.create_text(midx, y0+20, text=f'Year:{year}',
                                       font='Arial 8 bold')
                    canvas.create_text(midx, y0+30, text=f'College:{college}',
                                       font='Arial 8 bold')
                    canvas.create_text(midx, y0+40, text=f'Major:{major}',
                                       font='Arial 8 bold')
                    canvas.create_text(midx, y0+50, text=f'Class:{classes}',
                                       font='Arial 8 bold')
                    canvas.create_text(midx-100, y0+10, text=doing,
                                       font='Arial 8 bold')


def redrawAll(app, canvas):
    if not app.inside:  # on the map
        canvas.create_image(700, 300, image=ImageTk.PhotoImage(app.image1))
        app.g.drawGraph(canvas)
        if app.path != dict():
            app.g.drawPath(canvas, app.path)
        canvas.create_image(app.user.cx, app.user.cy,
                            image=ImageTk.PhotoImage(app.userImage))  # user
        canvas.create_rectangle(20, 700, 300, 760, fill='MistyRose2')
        canvas.create_text(
            160, 720, text='Click on buildings/red circles to find path')
        canvas.create_text(
            160, 740, text='Click on user/black scottie to enter building')

    else:  # inside a building
        drawInside(app, canvas)
        drawStudentInfo(app, canvas)

    canvas.create_rectangle(1300, 700, 1350, 730, fill='Plum4')
    canvas.create_text(1325, 715, text='HOME', font='Arial 14 bold')


def getStudents(app):
    # update app.studentsInfo {building:2d list of student info}and
    # app.studentsLocation {building: student locations}
    width, height = app.studentImage.size
    # list of students just for this building:
    tepL = df1.loc[df1['Building'] == 'TEP'].values.tolist()
    app.studentsInfo['TEP'] = tepL
    locationList = list()
    for i in range(len(tepL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['TEP'] = locationList

    ghcL = df1.loc[df1['Building'] == 'GHC'].values.tolist()
    app.studentsInfo['GHC'] = ghcL
    locationList = list()
    for i in range(len(ghcL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(600, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['GHC'] = locationList

    dhL = df1.loc[df1['Building'] == 'DH'].values.tolist()
    app.studentsInfo['DH'] = dhL
    locationList = list()
    for i in range(len(dhL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(500, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['DH'] = locationList

    cucL = df1.loc[df1['Building'] == 'CUC'].values.tolist()
    app.studentsInfo['CUC'] = cucL
    locationList = list()
    for i in range(len(cucL)):
        x, y = random.randrange(
            width+50, app.width-width), random.randrange(500, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['CUC'] = locationList

    nshL = df1.loc[df1['Building'] == 'NSH'].values.tolist()
    app.studentsInfo['NSH'] = nshL
    locationList = list()
    for i in range(len(nshL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(650, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['NSH'] = locationList

    wehL = df1.loc[df1['Building'] == 'WEH'].values.tolist()
    app.studentsInfo['WEH'] = wehL
    locationList = list()
    for i in range(len(wehL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(500, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['WEH'] = locationList

    bhL = df1.loc[df1['Building'] == 'BH'].values.tolist()
    app.studentsInfo['BH'] = bhL
    locationList = list()
    for i in range(len(bhL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['BH'] = locationList

    cfaL = df1.loc[df1['Building'] == 'CFA'].values.tolist()
    app.studentsInfo['CFA'] = cfaL
    locationList = list()
    for i in range(len(cfaL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['CFA'] = locationList

    cyhL = df1.loc[df1['Building'] == 'CYH'].values.tolist()
    app.studentsInfo['CYH'] = cyhL
    locationList = list()
    for i in range(len(cyhL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['CYH'] = locationList

    hbhL = df1.loc[df1['Building'] == 'HBH'].values.tolist()
    app.studentsInfo['HBH'] = hbhL
    locationList = list()
    for i in range(len(hbhL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['HBH'] = locationList

    hlL = df1.loc[df1['Building'] == 'HL'].values.tolist()
    app.studentsInfo['HL'] = hlL
    locationList = list()
    for i in range(len(hlL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(600, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['HL'] = locationList

    miL = df1.loc[df1['Building'] == 'MI'].values.tolist()
    app.studentsInfo['MI'] = miL
    locationList = list()
    for i in range(len(miL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['MI'] = locationList

    phL = df1.loc[df1['Building'] == 'PH'].values.tolist()
    app.studentsInfo['PH'] = phL
    locationList = list()
    for i in range(len(phL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['PH'] = locationList

    posL = df1.loc[df1['Building'] == 'POS'].values.tolist()
    app.studentsInfo['POS'] = posL
    locationList = list()
    for i in range(len(posL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['POS'] = locationList

    whL = df1.loc[df1['Building'] == 'WH'].values.tolist()
    app.studentsInfo['WH'] = whL
    locationList = list()
    for i in range(len(whL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['WH'] = locationList

    cutL = df1.loc[df1['Building'] == 'Cut'].values.tolist()
    app.studentsInfo['Cut'] = cutL
    locationList = list()
    for i in range(len(cutL)):
        x, y = random.randrange(
            width, app.width-width), random.randrange(677, app.height-20)
        dx, dy = random.randint(-3, 3), random.randint(-3, 3)
        isPaused = False
        locationList.append((x, y, dx, dy, isPaused))
    app.studentsLocation['Cut'] = locationList


runApp(width=1400, height=777)
