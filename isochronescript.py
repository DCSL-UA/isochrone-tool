#!/usr/bin/python3

"""
This script _____

Last modified: Myles Mcleroy, 2/4/2019
"""


# Function to create an array that is the amount to increment or decrement by based on lat/long
# returns the array itself, 0 -> 180 (0->90 and -90->-1 = 91 + )
# Do the math we have been, store that value in each index through 180
# python dist.py try1.txt -off AIzaSyBlGF0c9WDFymECTZ15thY0WFOROdlUC5Q 0 0 0 0 1 0 0 0 0
# Users/user/anaconda/bin/python /Users/user/Google_DirectionsAPI_PointPicker/isochronescript.py uploads_isochrone/testing1.txt output_isochrone/crontab1new.txt -off AIzaSyCvtVQxMV9pSnQsgjKxvqdlj929X3BPncM 0 0 0 0 0 0 on 0 0 0 0 0 on 900 32 "33.217617, -87.558822" 0 bicycling

from __future___ import print_function

import datetime
import googlemaps
import json
import math
import os
import urllib
import simplekml
import sys
import time

from area import area
from cStringIO import StringIO
from datetime import datetime as dt
from geographiclib.geodesic import Geodesic
from math import sin, cos, sqrt, atan2, radians
from multiprocessing import Lock
from Polygon import *
from xml.dom.minidom import parseString
from zipfile import ZipFile

start_time = dt.now()
kmlstr = \
'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>
<name>Polygon: %s</name>
  <open>1</open>
  %s
</Document>
</kml>'''
polystr = \
'''     <Placemark>
         <name>%i</name>
         <Polygon>
           <altitudeMode>clampedToGround</altitudeMode>
           <outerBoundaryIs>
           <LinearRing>
             <coordinates>
             %s
             </coordinates>
           </LinearRing>
           </outerBoundaryIs>
         </Polygon>
       </Placemark>'''

""""""
def openKMZ(filename):
    zip = ZipFile(filename)
    for z in zip.filelist:
        if z.filename[-4:] == '.kml':
            fstring = zip.read(z)
            break
        else:
            raise Exception("Could not find kml file in %s" % filename)
    
    return fstring

""""""
def openKML(filename):
    try:
        fstring = openKMZ(filename)
    except Exception:
        fstring=open(filename,'r').read()
        return parseString(fstring)

""""""
def readPoly(filename):
    """"""
    def parseData(d):
        poly = []
        dlines = d.split()
        for l in dlines:
            l = l.strip()
            if l:
                point = []
                for x in l.split(','):
                    point.append(float(x))
                poly.append(point[:2])
        return poly

    desc = {}
    xml = openKML(filename)
    nodes = xml.getElementsByTagName('Placemark')
    for n in nodes:
        names = n.getElementsByTagName('name')
        try:
            desc['name'] = names[0].childNodes[0].data.strip()
        except Exception:
            pass
          
    descriptions = n.getElementsByTagName('description')
    try:
        desc['description']=names[0].childNodes[0].data.strip()
    except Exception:
        pass

    times = n.getElementsByTagName('TimeSpan')
    try:
        desc['beginTime']=times[0].getElementsByTagName('begin')[0].childNodes[0].data.strip()
        desc['endTime'  ]=times[0].getElementsByTagName('end'  )[0].childNodes[0].data.strip()
    except Exception:
        pass

    times = n.getElementsByTagName('TimeStamp')
    try:
        desc['timeStamp']=times[0].getElementsByTagName('when')[0].childNodes[0].data.strip()
    except Exception:
        pass

    polys = n.getElementsByTagName('Polygon')
    for poly in polys:
        invalid = False
        c = n.getElementsByTagName('coordinates')
        if len(c) != 1:
            continue
        if not invalid:
          c = c[0]
          d = c.childNodes[0].data.strip()
          data = parseData(d)
          yield (data,desc)

""""""
def latlon2meters(p):
    pi2 = 2. * math.pi
    reradius = 1. / 6370000
    alat = 0
    alon = 0
    for i in p:
        alon = alon + i[0]
        alat = alat + i[1]

    lon_ctr= alon / len(p)
    lat_ctr= alat / len(p)
    unit_fxlat=pi2/(360. * reradius)
    unit_fxlon=math.cos(lat_ctr*pi2/360.) * unit_fxlat
      
    q=[]
    olon=p[0][0]
    olat=p[0][1]
    for i in p:
        q.append(((i[0] - olon) * unit_fxlon,
                  (i[1] - olat) * unit_fxlat))
    return q

""""""
def polyStats(p):
    pm = Polygon(latlon2meters(p))
    area = pm.area()
    numpts = len(p)
    pl = Polygon(p)
    bbox = pl.boundingBox()
    center = pl.center()
    stat = { \
        'vertices':'%i' % numpts,
        'bounding box':'(%f , %f) - (%f , %f)' % (bbox[0],bbox[2],bbox[1],bbox[3]),
        'center':'(%f , %f)' % (center[0],center[1]),
        'area':'%f m^2' % (area) }
    return stat

""""""
def makepoly(p):
    return Polygon(p)

""""""
def intersect(p1, p2):
    q1 = makepoly(p1)
    q2 = makepoly(p2)
    q = q1 & q2
    return q

""""""
def get_area(p):
    q = makepoly(p)
    return p.area()

""""""
def write_poly(p,fname):
    f = open(fname,'w') if isinstance(fname,basestring) else fname

    for i in p:
        f.write('%19.16f,%19.16f,0.\n' % (i[0],i[1]))
    f.flush()

""""""
def read_poly(fname):
    if isinstance(fname,basestring):
        f = open(fname,'r')
    else:
        f = fname
        s = f.readlines()
        p = []

    for i in s:
        i = i.strip()
        j = i.split(',')
        p.append((float(j[0]),float(j[1])))
    
    return p

""""""
def poly2kmz(pp, fname):
    strs = []
    i = 0
    for p in pp:
        i += 1
        f = StringIO()
        write_poly(p,f)
        strs.append(polystr % (i,f.getvalue()))
        s = '\n'.join(strs)
        s = kmlstr % (fname,s)
        open(fname, 'w').write(s)

def gmaps_traveltimeordist(directions11, last, timeordist):
    if len(directions11) > 0 and timeordist == 1:
        return directions11[0]["legs"][0]["duration"]["value"]   # Extract json from Google
    if len(directions11) > 0 and timeordist == 0:
        return directions11[0]["legs"][0]["distance"]["value"]   # Comes back in meters
    else:   # Time not available
      return last

""""""
def pointfits(pointa, pointadone, goaltimeplus, goaltimeminus):
    return pointa if pointadone >= goaltimeminus \
                 and pointadone <= goaltimeplus else False

""""""
def closestpoint(InitialPoint, timelist, latlist, goaltime, additionalkeys, finallist): 
    thepair = 0
    thekey = 0
    thetime = 0
    thepair = 0
    lastclosest = 1000
    for key in additionalkeys:
        #print "KEY is  " + str(key)
        for combo in additionalkeys[key]:
            combo = combo.split("/") 
        if abs(int(combo[0]) - goaltime) < lastclosest:
            lastclosest = abs(int(combo[0]) - goaltime) 
            thetime = combo[0]
            thepair = combo[1]
            thekey = key

    finallist[thekey] = str(thetime) + "/" + str(thepair)
    return finallist

""""""
def isunevenbearing(keys, count):
    return True if abs(keys[count + 1] - keys[count]) \
                != abs(keys[count] - keys[count - 1]) else False

""""""
def matchup(testedlist, testedtimeslist, lister):
    for x, y in zip(testedlist, testedtimeslist):
        lister.append(str(y) + "/" + str(x))
    return lister

""""""
def my_algorithm(outputfile, d, distance, Initial_increment, goaltime, InitialPoint, mode, modes_to_run, \
  output, KEYS, degreeincrements,timeordist,Order_list,linenumber):
    global gmaps
    originaldist = distance
    finallist = {}
    finallist["0"] = {}
    finallist["1"] = {}
    additionalkeys = {}
    negative = False
    goaltimeplus = goaltime + (goaltime * .05) #seconds
    goaltimeminus = goaltime -  (goaltime * .05) #seconds
    testedlist = []
    testedtimeslist = []
    keys = [key for key, value in sorted(d.iteritems())]
    count = 0
    attemptcounter = 0
    attempted = []
    lastbeginning = InitialPoint
    previoustestlists = {}
    bearingproblem = ""
    x33 = 2
    lasttime = 0
    numberofmoves = abs(keys[count] - degreeincrements) // 4  # Count of degree increments by 2 that we are allowing up or down

    if numberofmoves > 3:
        numberofmoves = 3
    originalnumberofmoves = numberofmoves

    while count <= len(keys) - 1:       # While we have bearings to get answers for
        x = 0                           # closest, the exact distance away
        pointa = d[keys[count]][0]
        lastbeginning = InitialPoint
        testedlist.append(pointa)
        attempted.append(pointa)
        distance3 = float(get_distance( \
          float(lastbeginning[0]), float(lastbeginning[1]), float(pointa.split(",")[0]), float(pointa.split(",")[1])))

        try_except(outputfile, gmaps, InitialPoint, pointa, mode, modes_to_run, output, KEYS, x, Order_list, linenumber)

        attemptcounter += 1
        pointadone = gmaps_traveltimeordist(directions11, lasttime, timeordist)
        lasttime = pointadone
        testedtimeslist.append(pointadone)

        if keys[count] in finallist["1"]:
            finallist["1"][keys[count]].append(str(pointa) + "/" + str(pointadone) + "/" + str(distance3))
        else:
            finallist["1"][keys[count]] = []
            finallist["1"][keys[count]].append(str(pointa) + "/" + str(pointadone) + "/" + str(distance3))

        if len(testedlist) >= 6 and not pointfits(pointa, pointadone, goaltimeplus, goaltimeminus): # If we just maxed out and the point we checked doesn't fit
            if numberofmoves == originalnumberofmoves and not negative: # If we still have moves to be made going down from original bearing, and no more going up
                bearingproblem = keys[count]

            if numberofmoves >= 1 and not negative and keys[count] + 2 > 0:  # Need to have a positive bearing, can't go into - (start bearing = 0 example)
                keys.insert(count, keys[count] + 2)   # Insert this key again but with + 2 degrees
                d.pop(keys[count] - 2, None)          # Pop off the old key
                additionalkeys[keys[count] - 2] = matchup(testedlist, testedtimeslist, [])
                keys.remove(keys[count] - 2)          # Remove the old key from main list
                d[keys[count]] = []                   # Create new lat long point, empty list and below is where we create
                d = singlebearingupdate(InitialPoint, 1, 1, distance * 0.621371, d, 0, keys[count]) # hard coded to same distance away as starting point was
                testedlist = []
                testedtimeslist = []
                numberofmoves = numberofmoves - 1 # Remove 1 move, if we don't have more moves left then set negative to true because next time around we may have to go negative
                if numberofmoves < 1:
                    negative = True
            else: 
                if numberofmoves < 1:   # No moves can be made  
                    moveby = abs(keys[count] - bearingproblem)
                    #print "CALLING AGAIN 33with " + str(x33)
                    keys.insert(count, keys[count] - moveby - 2)
                    d.pop(keys[count] + 2 + moveby, None)
                    additionalkeys[keys[count] + 2 + moveby] = matchup(testedlist, testedtimeslist, [])
                    keys.remove(keys[count] + 2 + moveby)
                    testedlist = []
                    testedtimeslist = []
                    d[keys[count]] = []
                    d = singlebearingupdate(InitialPoint, 1, 1, distance * 0.621371, d, 0, keys[count])
                    numberofmoves += 1  
                else:   # There is more than 1 move available to be made
                    d.pop(keys[count-1], None)
                    keys.remove(keys[count-1])
                    additionalkeys[keys[count-1]] = matchup(testedlist,testedtimeslist,[])
                    finallist["0"].pop(bearingproblem,None)
                    testedtimeslist = []
                    testedlist = []
                    lastbeginning = InitialPoint
                    lastend = "000"
                    numberofmoves = originalnumberofmoves
                    negative = False
                    count += 1
                    distance = originaldist
                    additionalkeys = {}
        elif pointfits(pointa, pointadone, goaltimeplus, goaltimeminus):
            distance = originaldist
            finallist["0"][keys[count]] = (str(pointa) + "/" + str(pointadone) + "/" + str(distance3))
            testedlist = []
            numberofmoves = originalnumberofmoves
            negative = False
            additionalkeys = {}
            testedtimeslist = []
            distance2 = float(get_distance( \
              float(lastbeginning[0]), float(lastbeginning[1]), float(pointa.split(",")[0]), float(pointa.split(",")[1])))
            lastbeginning = InitialPoint
            lastend = "000"
            count += 1
            if count < len(keys) - 1:
                d[keys[count]] = []   # Create new lat long point, empty list and below is where we create
                d = singlebearingupdate(InitialPoint, 1, 1, distance2 * 0.621371, d, 0, keys[count])
        elif pointadone >= goaltimeminus:   # Must be in range 0 to a
            ratio = float(float(goaltime) / float(pointadone))
            distance2 = float(get_distance(float(lastbeginning[0]),
                                           float(lastbeginning[1]),
                                           float(pointa.split(",")[0]), 
                                           float(pointa.split(",")[1])))
            d = singlebearingupdate(InitialPoint, 1, 1, float((float(distance2)) * float(ratio)) * 0.621371, d, 0, keys[count])
            lastend = tuple(pointa.split(","))
        else:
            ratio = float(float(goaltime) / float(pointadone))
            distance2 = float(get_distance( \
              float(lastbeginning[0]), float(lastbeginning[1]), float(pointa.split(",")[0]), float(pointa.split(",")[1])))
            d = singlebearingupdate(lastbeginning, 1, 1, float(float(distance2) * float(ratio)) * 0.621371, d, 0, keys[count])
            lastbeginning = tuple(pointa.split(","))
    return finallist

""""""
def format_orderlist(list):
    message = ""
    for item in list:
        if item.lower() == "rail":
            message += "train|tram|subway"
        else:
            if item != "0":
                message += item.lower()
        if list.index(item) != len(list) - 1:
            if list[list.index(item)+1] != "0":
                message += "|"
    return message

""""""
def leaving(time_to_leave):
    return time.time() + int(time_to_leave) * 60

""""""
def google_leaving(time_to_leave):
  return "now" if time_to_leave == "0" else leaving(time_to_leave)

def client(API_KEY_INPUT):
    global x
    try:
        global gmaps
        gmaps = googlemaps.Client(key=str(API_KEY_INPUT))
    except:
        x += 1
        if got_more_keys(KEYS, x) != False:      
          client(got_more_keys(KEYS,x))
        else:
          exit()

""""""
def finish_line(outputfile, address, destination, mode, output, linenumber):
    outfile = open(sys.argv[2], "r")
    contents = outfile.readlines()
    while int(linenumber) != int(len(contents)):
        time.sleep(1)
        outfile.seek(0)
        contents = outfile.readlines()

    output.write(str(address[0]) + "," + str(address[1]) + ",")
    output.write(time.strftime('%H:%M:%S', time.localtime(time.time()))+ ",")
    output.write(str(mode) + ",FAILED,\n")

""""""
def format_orderlist(list):
    message = ""
    for item in list:
        if item.lower() == "rail":
            message += "train|tram|subway"
        else:
            if item != "0":
                message += item.lower()
        if list.index(item) != len(list) - 1:
            if list[list.index(item)+1] != "0":
                message += "|"
    return message

def try_except(outputfile, gmaps12, address, destination, mode, modes_to_run, output, KEYS, a, Order_list, linenumber):
    global gmaps
    global x
    try:
        global directions11
        if mode == "transit":
            directions11 = gmaps.directions(address, destination, mode=mode,
                                            units="metric", departure_time="now",
                                            transit_mode=Order_list, alternatives="true")
        else:
          directions11 = gmaps.directions(address, destination, mode=mode,
                                          units="metric", departure_time="now",
                                          alternatives="true")
    except googlemaps.exceptions.ApiError as e:
        print(e)
        x += 1
        if got_more_keys(KEYS, x):
            client(got_more_keys(KEYS, x))
            try_except(outputfile, gmaps, address, destination, mode, modes_to_run, output, KEYS, a, Order_list)
        else:
            finish_line(outputfile,address,destination,mode,output,linenumber)
            exit()
    except Exception as e:
        print(e)
        x += 1
        if got_more_keys(KEYS, x):
            client(got_more_keys(KEYS, x))
            try_except(outputfile,gmaps,address,destination,mode,modes_to_run,output,KEYS,a,Order_list)
        else:
            finish_line(outputfile,address,destination,mode,output,linenumber)
            exit()

""""""
def get_mode(count):
    if count == 0:
        return "driving"
    if count == 1:
        return "walking"
    if count == 2:
        return "bicycling"
    if count == 3:
        return "transit"
    return "invalid"

""""""
def file_len(fname):
    i = 0
    with open(str(os.getcwd()) + "/" + fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1

""""""
def get_seconds(t1, t2, Entry_count, mode_count):
    h1, m1, s1 = t1.hour, t1.minute, t1.second
    h2, m2, s2 = t2.hour, t2.minute, t2.second
    t1_secs = s1 + 60 * (m1 + 60 * h1)
    t2_secs = s2 + 60 * (m2 + 60 * h2)

    return (t2_secs / Entry_count) / mode_count

""""""
def got_more_keys(KEYS, count):
    global x
    if KEYS[count - 1] == str("0") or x > len(KEYS) - 1:
        return False
    return KEYS[count - 1]

""""""
def check_timetoleave(line):
    return line[3] if len(line) > 2 else "0"

""""""
def getEarthRadius(PointA):
    return getEarthRadiusAtLatitude(PointA[0])

""""""
def getEarthRadiusAtLatitude(latitude):
    earthRadius = 6367
    equatorRadius = 6378.137
    polarRadius = 6356.7523142

    lat = radians(latitude)
    part1 = equatorRadius * sqrt(pow(polarRadius, 4) / \
            pow(equatorRadius, 4) * pow((sin(lat)), 2) + pow(cos(lat), 2))
    part2 = sqrt(1 - (1 - (polarRadius * polarRadius) / \
            (equatorRadius * equatorRadius)) * pow(sin(lat), 2))
    
    return part1 / part2

""""""
def get_distance(a, b, c, d):
    R = 6373.0            # Approximate radius of earth in km
    lat1 = radians(a)     # Optimized for locations around 39 degrees from the equator (roughly the Latitude of Washington, DC, USA).
    lon1 = radians(b)
    lat2 = radians(c)
    lon2 = radians(d)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    arc = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(arc), sqrt(1 - arc))

    distance = getEarthRadiusAtLatitude(lat1) * c

    return distance

""""""
def get_departuretime(directions):
    if "departure_time" in directions.keys():
        if "value" in directions['departure_time'].keys():
            return directions['departure_time']['value']
    
    return int(time.time())

""""""
def check_dest_space(line):
    if line.strip().split(',')[2][0] == ' ':
        return line.strip().split(",")[2][1:] + "," + line.strip().split(",")[3]
    else:
        return line.strip().split(",")[2] + "," + line.strip().split(",")[3]

        """
        if type(pointA) != tuple or type(pointB) != tuple:
            raise TypeError("Only tuples are supported as arguments")

        lat1 = math.radians(int(pointA[0]))
        lat2 = math.radians(int(pointB[0]))

        diffLong = math.radians(int(pointB[1]) - int(pointA[1]))

        x = math.sin(diffLong) * math.cos(lat2)
        y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))
        initial_bearing = math.atan2(x, y)
        initial_bearing = math.degrees(initial_bearing)
        compass_bearing = initial_bearing

        return compass_bearing
        """

""""""
def go_to_corner(PointA, radius, numberofpairs, btwnmarks, currentdict, Dictkey, degreeincrements):
    global square_count
    square_count += 1
    PointB = [0,0]
    PointB[0] = PointA[0]
    PointB[1] = PointA[1]
    circular(PointB[0], PointB[1], numberofpairs, btwnmarks, currentdict, Dictkey, degreeincrements)

""""""
def singlebearingupdate(PointA, radius, numberofpairs, btwnmarks, currentdict, Dictkey, bearing):
    global square_count
    square_count += 1
    PointB = [0,0]
    PointB[0] = PointA[0]
    PointB[1] = PointA[1]

    currentdict[bearing] = circularsingle(PointB[0], PointB[1], numberofpairs,
                                          btwnmarks, currentdict, Dictkey,bearing)
    if len(currentdict[bearing]) >= 2:
        currentdict[bearing] = currentdict[bearing][numberofpairs:]
    return currentdict

""""""
def distlat(lat1):
    if (lat1 < 0):
        return LAT_NUMBERS[int(str(lat1[1:]).split('.')[0])]
    return LAT_NUMBERS[int(str(lat1).split('.')[0])]

""""""
def incrementlat(currentbearing, a, lat1, distance):
    x = .1
    while float(distance / x) > a + .01 or float(distance / x) < a - .01:
        x += .001

    return float(float(lat1) + float(float(1.000 / float(x)) * cos(radians(currentbearing))))

""""""
def incrementlon(currentbearing, a, lon1, distance):
    x = .1
    while float(distance / x) > a + .01 or float(distance / x) <  a - .01:
        x += .001

    return float(float(lon1) + float(float(1.000 / float(x)) * sin(radians(currentbearing))))

""""""
def decrementlat(currentbearing, a, lat1, distance):
    x = .1
    while float(distance / x) > a + .01 or float(distance / x) <  a - .01:
        x += .001

    return float(float(lat1) - float(float(1.000 / float(x)) * cos(radians(currentbearing))))

""""""
def decrementlon(currentbearing, a, lon1, distance):
    x = .1
    while float(distance / x) > a + .01 or float(distance / x) <  a - .01:
        x += .001

    return float(float(lon1) - float(float(1.000 / float(x)) * sin(radians(currentbearing))))

""""""
def distanceindegree(lon1, latitude):
    if lat1 < 0:
        return LONG_NUMBERS[int(str(latitude[1:]).split('.')[0])]
  
    return LONG_NUMBERS[int(str(latitude).split('.')[0])]

""""""
def circular(lat1, lon1, numberofpairs, btwnmarks, currentdict, Dictkey, degreeincrements):
    y = 1
    x = 0
    originallong = lon1
    originallat = lat1
    global square_count
    firstlat = lat1
    firstlon = lon1
    degrees = 0

    while 0 <= degrees <= 90:   # Go .05 miles to the right and query
        lat1 = incrementlat(degrees, float(btwnmarks), lat1,
                            distlat(lat1))
        lon1 = incrementlon(degrees, float(btwnmarks), lon1, 
                            distanceindegree(lon1, lat1))
        x += 1
        currentdict[degrees].append(str(round(lat1, 6)) +
                                        "," + str(round(lon1, 6)))
        print(str(lat1) + "," + str(lon1))
        if x == numberofpairs:
            degrees += degreeincrements
            x = 0
            lat1 = firstlat
            lon1 = firstlon

    while 90 <= degrees < 180:    # Go .05 miles to the right and query
        lat1 = decrementlat(degrees, float(btwnmarks),lat1,
                            distlat(lat1))
        lon1 = decrementlon(degrees, float(btwnmarks), lon1,
                            distanceindegree(lon1, lat1))
        x += 1
        currentdict[degrees].append(str(round(lat1, 6)) +
                                        "," + str(round(lon1, 6)))
        print(str(lat1) + "," + str(lon1))
        if x == numberofpairs:
            degrees += degreeincrements
            lat1 = firstlat
            lon1 = firstlon
            x = 0

    while 180 <= degrees <= 270:   # Go .05 miles to the right and query
        lat1 = incrementlat(degrees, float(btwnmarks), lat1,
                            distlat(lat1))
        lon1 = incrementlon(degrees, float(btwnmarks), lon1,
                            distanceindegree(lon1, lat1))
        x += 1
        currentdict[degrees].append(str(round(lat1, 6)) +
                                        "," + str(round(lon1, 6)))
        print(str(lat1) + "," + str(lon1))
        if x == numberofpairs:
            degrees += degreeincrements
            x = 0
            lat1 = firstlat
            lon1 = firstlon

    while 270 <= degrees <= 360:   # Go .05 miles to the right and query
        lat1 = decrementlat(degrees, float(btwnmarks), lat1,
                            distlat(lat1))
        lon1 = decrementlon(degrees, float(btwnmarks), lon1,
                            distanceindegree(lon1, lat1))
        x += 1
        currentdict[degrees].append(str(round(lat1, 6)) +
                                        "," + str(round(lon1, 6)))
        print(str(lat1) + "," + str(lon1))
        if x == numberofpairs:
            degrees += degreeincrements
            x = 0        
            lat1 = firstlat
            lon1 = firstlon

    lastlat = lat1
    lastlon = lon1
    distance = get_distance(firstlat, firstlon, lastlat, lastlon) * 0.621371

""""""  
def circularsingle(lat1, lon1, count, btwnmarks, currentdict, Dictkey, degrees):
    originallong = lon1
    originallat = lat1
    y = 1
    x = 0
    global square_count
    
    firstlat = lat1
    firstlon = lon1
    fixeddegrees = degrees if degrees > 360 else degrees - 360

    while 0 <= fixeddegrees <= 90:   # Go .05 miles to the right and query
        lat1 = incrementlat(fixeddegrees, float(btwnmarks), lat1,
                            distlat(lat1))
        lon1 = incrementlon(fixeddegrees, float(btwnmarks), lon1,
                            distanceindegree(lon1, lat1))
        x += 1
        currentdict[degrees].append(str(round(lat1, 6)) +
                                        "," + str(round(lon1, 6)))
        if x == count:
            return currentdict[degrees]

    while 90 <= fixeddegrees < 180:   # Go .05 miles to the right and query
        lat1 = decrementlat(fixeddegrees, float(btwnmarks), lat1,
                            distlat(lat1))
        lon1 = decrementlon(fixeddegrees, float(btwnmarks), lon1,
                            distanceindegree(lon1, lat1))
        x += 1
        currentdict[degrees].append(str(round(lat1, 6)) +
                                        "," + str(round(lon1, 6)))
        if x == count:
            return currentdict[degrees]

    while 180 <= fixeddegrees <= 270:   # Go .05 miles to the right and query
        lat1 = incrementlat(fixeddegrees, float(btwnmarks), lat1,
                            distlat(lat1))
        lon1 = incrementlon(fixeddegrees, float(btwnmarks), lon1,
                            distanceindegree(lon1, lat1))
        x += 1
        currentdict[degrees].append(str(round(lat1, 6)) +
                                        "," + str(round(lon1, 6)))
        if x == count:
            return currentdict[degrees]

    while 270 <= fixeddegrees <= 360:   # Go .05 miles to the right and query
        lat1 = decrementlat(fixeddegrees, float(btwnmarks), lat1,
                            distlat(lat1))
        lon1 = decrementlon(fixeddegrees, float(btwnmarks), lon1,
                            distanceindegree(lon1, lat1))
        x += 1
        currentdict[fixeddegrees].append(str(round(lat1, 6)) +
                                             "," + str(round(lon1, 6)))
        if x == count:
            return currentdict[degrees]

    lastlat = lat1
    lastlon = lon1
    distance = get_distance(firstlat, firstlon, lastlat, lastlon) * 0.621371

    return currentdict[degrees]

""""""
def tomyratio(numofmeters):
    numofkm = float(numofmeters) * 4.38888888889 * .001
    return numofkm

""""""
def get_dist(lat1, lon1, lat2, lon2): 
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

""""""
def remove_newlines(fname):
    flist = open(fname).readlines()
    return [s.rstrip('\n') for s in flist]

""""""
def makekeys(storage, increment):
    for k in degreelist(increment):
        storage[k] = []
    return storage

""""""
def degreelist(number):
    mylist = []
    counter = 0
    while counter < 360:
        mylist.append(counter)
        counter += number
    return mylist

""""""
def checknumbers(thedict, thepair, thetime):
    pairtime = ""
    for key in thedict:
        pairtime = thedict[key].split("/")

""""""
def cleanprint(thedict, goaltime, output):
    counter = 0
    for key in thedict:
        pairtime = key
        counter += 1
        output.write('"' + str(pairtime[0]) + "," + str(pairtime[1]) + '",')

""""""
def printoffbypercents(thedict, goaltime):
    pairtime = ""
    for key in thedict:
        pairtime = thedict[key].split("/")

""""""
def find_key(partial, partial2, thedict):
    for key in thedict:
        if partial in thedict[key]:
            if partial2 in thedict[key]:
                return str(key)

""""""
def kmlmerged(mypoints, filename, greenpoints, allpoints, goaltime):
    kml = simplekml.Kml()
    finallist =  {}
    cnt = 0
    style = simplekml.Style()
    style.labelstyle.color = simplekml.Color.red  # Make the text red
    style.labelstyle.scale = 2  # Make the text twice as big
    style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
    for key in allpoints:
        for pont in allpoints[key]:
            point,time,distance = pont.split("/")
            point = point.split(",")
            pnt = kml.newpoint(name='Travel Time: {} Point: {},{}'.format(time,point[1], point[0]))
            style = simplekml.Style()
            style.iconstyle.icon.href = get_pointcolor(goaltime, int(time))
            pnt.coords = [(point[1], point[0])] 
            pnt.style = style
    
    finallist =  []
    for pont in mypoints:
        finallist.append((pont[1],pont[0]))
    pol = kml.newpolygon(name=filename, outerboundaryis=finallist)
    os.chdir("merged_kml")
    kml.save("merged_" + filename + ".kml")
    os.chdir("..")

""""""
def kmlcolor(mypoints, filename, thedict, goaltime):
    kml = simplekml.Kml()
    finallist =  {}
    cnt = 0
    style = simplekml.Style()
    style.labelstyle.color = simplekml.Color.red  # Make the text red
    style.labelstyle.scale = 2  # Make the text twice as big
    style.iconstyle.icon.href = 'http://maps.google.com/mapfiles/kml/shapes/placemark_circle.png'
    for key in thedict:
        for pont in thedict[key]:
            point,time,distance = pont.split("/")
            point = point.split(",")
            pnt = kml.newpoint(name='Travel Time: {} Point: {},{}'.format(time,point[1], point[0]))
            style = simplekml.Style()
            style.iconstyle.icon.href = get_pointcolor(goaltime, int(time))
            pnt.coords = [(point[1], point[0])] 
            pnt.style = style

    os.chdir("color_points_kml")
    kml.save("color_" + filename + ".kml")
    os.chdir("..")

"""
def get_pointcolor(goaltime,time):
    percentoff = float(float(time) / float(goaltime))
    if percentoff > 1:  # Time was greater, aka farther
        percentoff = float(percentoff - 1) * 100   # Absolute percent off by, can only be green or red at this point
        if (percentoff < .5): # perfect green
            return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 1.5 and percentoff > .5): # removed shades of green, just perfect because it doesn't really matter
            return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 1.5 and percentoff > .5): # removed shades of green, just perfect because it doesn't really matter
            return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 2.5 and percentoff > 1.5): # removed shades of green, just perfect because it doesn't really matter
            return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 3.5 and percentoff > 2.5): # removed shades of green, just perfect because it doesn't really matter
          return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 4.5 and percentoff > 3.5): # removed shades of green, just perfect because it doesn't really matter
          return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 5.5 and percentoff > 4.5): # 5 shades off red
          return "http://mkkeffeler.azurewebsites.net/icons/red5.png"
        elif (percentoff < 6.5 and percentoff > 5.5): #4 shades off red
          return "http://mkkeffeler.azurewebsites.net/icons/red5.png"
        elif (percentoff < 7.5 and percentoff > 6.5): #3 shades off red
          return "http://mkkeffeler.azurewebsites.net/icons/red4.png"
        elif (percentoff < 8.5 and percentoff > 7.5): #2 shades off red
          return "http://mkkeffeler.azurewebsites.net/icons/red3.png"
        elif (percentoff < 9.5 and percentoff > 8.5): # 1 shade off red
          return "http://mkkeffeler.azurewebsites.net/icons/red2.png"
        else: #perfect red
          return "http://mkkeffeler.azurewebsites.net/icons/red1.png"
      else: #time was shorter, aka closer
        percentoff = float(1 - percentoff) * 100  #Absolute percent off by, can only be blue or green at this point
        if (percentoff < .5): #perfect green
          return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 1.5 and percentoff > .5): # removed shades of green, just perfect because it doesn't really matter
          return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 1.5 and percentoff > .5): # removed shades of green, just perfect because it doesn't really matter
          return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 2.5 and percentoff > 1.5):# removed shades of green, just perfect because it doesn't really matter
          return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 3.5 and percentoff > 2.5): # removed shades of green, just perfect because it doesn't really matter
          return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 4.5 and percentoff > 3.5): # removed shades of green, just perfect because it doesn't really matter
          return "http://mkkeffeler.azurewebsites.net/icons/green1.png"
        elif (percentoff < 5.5 and percentoff > 4.5): # 5 shades off blue
          return "http://mkkeffeler.azurewebsites.net/icons/blue5.png"
        elif (percentoff < 6.5 and percentoff > 5.5): #4 shades off blue
          return "http://mkkeffeler.azurewebsites.net/icons/blue5.png"
        elif (percentoff < 7.5 and percentoff > 6.5): #3 shades off blue
          return "http://mkkeffeler.azurewebsites.net/icons/blue4.png"
        elif (percentoff < 8.5 and percentoff > 7.5): #2 shades off blue
          return "http://mkkeffeler.azurewebsites.net/icons/blue3.png"
        elif (percentoff < 9.5 and percentoff > 8.5): #1 shade off blue
          return "http://mkkeffeler.azurewebsites.net/icons/blue2.png"
        else: #perfect blue
          return "http://mkkeffeler.azurewebsites.net/icons/blue1.png"
"""

""""""
def kmlunedited(mypoints, mydirectory, filename, thedict):
    kml = simplekml.Kml()
    os.chdir(mydirectory)
    finallist =  []
    for pont in mypoints:
        try:
            finallist.append((pont[1],pont[0]))
        except:
            mypoints.remove(pont)
            pass
    pol = kml.newpolygon(name=filename,outerboundaryis=finallist)
    kml.save(str(filename + ".kml"))

""""""
def polyarea(mydirectory, filename):
  fname=filename
  os.chdir(mydirectory)
  i = 0
  for p in readPoly(fname):
      p,desc=p
      i += 1
      stats=polyStats(p)
      desc.update(stats)
      for d, v in desc.iteritems():
          if d == "area":
              return v[1:-4]

""""""
def getclosest(origin, thelist, goaltimeplus, goaltimeminus):
    prevpoint = ""
    prevdistance = ""
    prevtime = ""
    curpoint = ""
    for pnt in thelist:
        point,time,distance = pnt.split("/")
        if int(time) < goaltimeplus and prevpoint == "": # This point fits the bill and we don't currently have a solution
            prevpoint = point
            prevdistance = distance
            prevtime = time
        elif int(time) < goaltimeplus:  # This point is valid
            if distance > prevdistance: # and it is further than the current point
                prevpoint = point
                prevdistance = distance
                prevtime = time
    if prevpoint == "":
        for pnt in thelist:
            point, time, distance = pnt.split("/")
            if int(time) > goaltimeplus and prevpoint == "": # This point fits the bill and we don't currently have a solution
                prevpoint = point
                prevdistance = distance
                prevtime = time
            elif int(time) > goaltimeplus:  # This point is valid
                if distance < prevdistance: # and it is closer than the current point
                    prevpoint = point
                    prevdistance = distance
                    prevtime = time
        return "0","0","0" if prevpoint == "" else origin,0,0
    else:
        "RETURNING A BLUE or GREEN"
        return prevpoint,prevtime,prevdistance

""""""
def converter(thelist, goaltimeminus, goaltimeplus):
    totallist = []
    first = []
    second = []
    third = []
    fourth = []
    for key in (sorted(thelist)):
        if int(key) <= 90:
            point,time,distance = thelist[key].split("/")
            if int(time) > goaltimeminus and int(time) < goaltimeplus:
                first.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
        if 180 >= int(key) >= 91:
            point,time,distance = thelist[key].split("/")
            if int(time) > goaltimeminus and int(time) < goaltimeplus:
                second.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
        if 270 >= int(key) >= 181:
            point,time,distance = thelist[key].split("/")
            if int(time) > goaltimeminus and int(time) < goaltimeplus:
                third.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
        if 359 >= int(key) >= 271:
            point,time,distance = thelist[key].split("/")
            if int(time) > goaltimeminus and int(time) < goaltimeplus:
                fourth.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))

    if len(second) == 0 and len(third) >= 2:
        first.insert(0, third[len(third) - 2])
        totallist = first + fourth + third[:-1] + second
    elif len(second) == 0 and len(third) == 0 and len(fourth) >= 2:
        first.insert(0, fourth[len(fourth) - 2])
        totallist = first + fourth[:-1] + third + second
    elif len(second) == 0 and len(third) == 0 and len(fourth) == 1:
        first.insert(0, fourth[len(fourth) - 1])
        totallist = first + fourth[:-1] + third + second
    elif len(second) == 1:
        first.insert(0, second[len(second) - 1])
        totallist = first + fourth + third + second[:-1]
    else:
        first.insert(0,second[len(second)-2])
        totallist = first + fourth + third + second[:-1]

    return totallist

""""""
def converteralt(origin, thelist, goaltimeminus, goaltimeplus):
    totallist = []
    first = []
    second = []
    third = []
    fourth = []
    for key in (sorted(thelist)):
        if int(key) <= 90:
            point,time,distance = getclosest(origin, thelist[key], goaltimeplus, goaltimeminus)
            if point != "0":
                first.append(tuple(point.split(","))) if type(point) != tuple else first.append(point)

        if 180 >= int(key) >= 91:
            point,time,distance = getclosest(origin, thelist[key], goaltimeplus, goaltimeminus)
            if point != "0":
                second.append(tuple(point.split(","))) if type(point) != tuple else second.append(point)

        if 270 >= int(key) >= 181:
            point,time,distance = getclosest(origin, thelist[key], goaltimeplus, goaltimeminus)
            if point != "0":
                third.append(tuple(point.split(","))) if type(point) != tuple else third.append(point)

        if 359 >= int(key) >= 271:
            point,time,distance = getclosest(origin, thelist[key], goaltimeplus, goaltimeminus)
            if point != "0":
                fourth.append(tuple(point.split(","))) if type(point) != tuple else fourth.append(point)

    if len(second) == 0 and len(third) >= 2:
        first.insert(0, third[len(third) - 2])
        totallist = first + fourth + third[:-1] + second
    elif len(second) == 0 and len(third) == 0 and len(fourth) >= 2:
        first.insert(0, fourth[len(fourth) - 2])
        totallist = first + fourth[:-1] + third + second
    elif len(second) == 0 and len(third) == 0 and len(fourth) == 1:
        first.insert(0, fourth[len(fourth) - 1])
        totallist = first + fourth[:-1] + third + second
    elif len(second) == 1:
        first.insert(0, second[len(second) - 1])
        totallist = first + fourth + third + second[:-1]
    else:
        first.insert(0, second[len(second) - 2])
        totallist = first + fourth + third + second[:-1]

    return totallist

""""""
def polypoints(mydirectory, filename):
    fname = filename
    os.chdir(mydirectory)
    i = 0
    for p in readPoly(fname):
        p, desc = p
        i += 1
        stats = polyStats(p)
        desc.update(stats)
        for d, v in desc.iteritems():
            if d == "vertices":
                return v[1:]

""""""
def find_pointa(pointadist, d, a, b):
    count = 0
    for x in d['45']:
        lat = x.split(',')[0]
        lon = x.split(',')[1]
        if get_distance(a, b, lat, lon) >= pointadist:
            return count
        else:
            count += 1
        if len(d['45']) == count - 1:
          exit(1)

""""""
def find_pointb(pointbdist, d, a, b):
    count = 0
    for x in d['45']:
        lat = x.split(',')[0]
        lon = x.split(',')[1]
        if get_distance(a, b, lat, lon) >= pointbdist:
            return count
        else:
            count += 1
        if len(d['45']) == count - 1:
            exit(1)

LAT_NUMBERS = [68.703, 68.7108222222, 68.7186444444, 68.7264666667, 68.7342888889, 68.7421111111,
               68.7499333333, 68.7577555555, 68.7655777778, 68.7734, 68.7812222222, 68.7890444444,
               68.7968666666, 68.8046888889, 68.8125111111, 68.8203333333, 68.8281555555,  
               68.8359777777, 68.8438, 68.8516222222, 68.8594444444, 68.8672666666, 68.8750888888,
               68.8829111111, 68.8907333333, 68.8985555555, 68.9063777777, 68.9141999999,
               68.9220222222, 68.9298444444, 68.9376666666, 68.9454888888, 68.953311111,
               68.9611333333, 68.9689555555, 68.9767777777, 68.9845999999, 68.9924222221,
               69.0002444444, 69.0080666666, 69.0158888888, 69.023711111, 69.0315333332,
               69.0393555555, 69.0471777777, 69.0549999999, 69.0628222221, 69.0706444443,
               69.0784666666, 69.0862888888, 69.094111111, 69.1019333332, 69.1097555554,
               69.1175777777, 69.1253999999, 69.1332222221,69.1410444443, 69.1488666665,
               69.1566888888, 69.164511111, 69.1723333332, 69.1801555554, 69.1879777776,
               69.1957999999, 69.2036222221, 69.2114444443, 69.2192666665, 69.2270888887,
               69.234911111, 69.2427333332, 69.2505555554, 69.2583777776, 69.2661999998,
               69.2740222221, 69.2818444443, 69.2896666665, 69.2974888887, 69.3053111109,
               69.3131333332, 69.3209555554, 69.3287777776, 69.3365999998, 69.344422222,
               69.3522444443, 69.3600666665, 69.3678888887, 69.3757111109, 69.3835333331,
               69.3913555554, 69.3991777776]

LONG_NUMBERS = [69.172, 69.1614647694, 69.1298622866, 69.077202178, 69.0035004846, 68.9087796564,
                68.7930685464, 68.6564024013, 68.498822851, 68.3203778956, 68.1211218914,
                67.9011155334, 67.660425838, 67.3991261213, 67.117295978, 66.8150212561,
                66.4923940314, 66.1495125795, 65.7864813452, 65.4034109114, 65.000417965,
                64.5776252617, 64.1351615881, 63.673161723, 63.1917663961, 62.6911222449,
                62.1713817706, 61.6327032912, 61.0752508932, 60.4991943822, 59.9047092306,
                59.2919765242, 58.6611829073, 58.0125205259, 57.3461869688, 56.6623852076,
                55.9613235349, 55.243215501, 54.5082798485, 53.7567404459, 52.9888262194,
                52.2047710832, 51.4048138679, 50.5891982484, 49.758172669, 48.9119902682,
                48.0509088014, 47.1751905622, 46.2851023031, 45.3809151533, 44.4629045372,
                43.5313500897, 42.5865355712, 41.6287487815, 40.6582814716, 39.6754292553,
                38.6804915189, 37.6737713301, 36.6555753455, 35.6262137177, 34.586, 33.5352510517,
                32.474286941, 31.403430848, 30.3230089657, 29.2333504011, 28.1347870748,
                27.0276536199, 25.9122872798, 24.7890278059, 23.6582173541, 22.5202003801,
                21.3753235349, 20.2239355591, 19.0663871766, 17.9030309878, 16.7342213624,
                15.5603143311, 14.3816674772, 13.1986398282, 12.0115917456, 10.8208848158,
                9.62688173961, 8.42994622202, 7.23044286115, 6.02873703734, 4.82519480183,
                3.62018276524, 2.41406798591, 1.20721785808]

def kickofffunc(inputfile, outputfile, traffictoggle, apikeys, key2, key3, key4, key5,
    drive, walk, bike, transit, orderparam1, orderparam2, orderparam3, orderparam4, timevar,
    goaltimeordistvar, numofpoints, line, linenumber, mode):
    x = 1
    gmaps = ""
    global directions11
    directions11 = ""
    
    # Compile all modes to see which are to be run (ORDER: Driving,Walking,Biking,Transit)
    Types_of_Bus = ["BUS","INTERCITY_BUS","TROLLEYBUS"]
    Types_of_Rail = ["RAIL","METRO_RAIL","MONORAIL","COMMUTER_TRAIN","HEAVY_RAIL","HIGH_SPEED_TRAIN"]
    Types_of_Tram = ["TRAM"]
    Types_of_Subway = ["SUBWAY"]
    
    # Approximate radius of earth in km
    R = 6373.0
    lat1 = radians(40.834288)
    lon1 = radians(-73.851028)
    lat2 = radians(40.693797)
    lon2 = radians(-73.990696)
    global square_count
    square_count = 0

    os.chdir("output_isochrone")
    output = open(str(outputfile), "a")
    os.chdir("..")
    os.chdir("uploads_isochrone")
    inputfile = open(str(inputfile), "r")
    os.chdir("..")
    
    # Path to output file created
    modes_to_run = []
    
    # -off and -on
    Toggle_traffic_models = traffictoggle
    
    # API KEY STORAGE
    API_KEY_INPUT = apikeys
    KEY2 = key2
    KEY3 = key3
    KEY4 = key4
    KEY5 = key5
    
    modes_to_run = []
    all_modes = [drive, walk, bike, transit]
    Order_list = [orderparam1, orderparam2, orderparam3, orderparam4]
    istime = timevar
    goaltimedist = goaltimeordistvar
    numberofpoints = numofpoints
    formated_list = format_orderlist(Order_list)

    istime = 1 if istime == "on" else 0

    # Get Count of how many modes we are running
    mode_count = 0
    for entry in all_modes:
        if entry == "on":
            mode = get_mode(mode_count)
            modes_to_run.append(mode)
        mode_count += 1

    key_count = 0
    KEYS = [API_KEY_INPUT, KEY2, KEY3, KEY4, KEY5]
    for key in KEYS:
        if key != "0":
            key_count += 1

    address = ""
    traffic_models_list = []
    destination = ""

    counter = 0
    y = 0
    client(API_KEY_INPUT)
    currentindex = 0
    i = 0
    counter += 1
    modes_to_run = [mode]
    if counter >= 2490:
        #print "Key #" + str(y) + " reached its limit.<br>"
        counter = 0
        y += 1
        if KEYS[x] == '0':
            exit()
        API_KEY_INPUT = KEYS[x]
        x += 1

    time_to_leave = check_timetoleave(line.strip().split(","))
    PointA = (float(line.strip().split(",")[0]), float(line.strip().split(",")[1]))
    currentname = {}
    currentname = makekeys(currentname, int(360 / int(numberofpoints)))
    go_to_corner(PointA, 1, 1, .5, currentname, 0, int(360 / int(numberofpoints)))   # This gets 3 pairs that are 10, 20,and 30 miles from origin on bearing
    iterate_counter=0
    thelist = my_algorithm(outputfile, currentname, .5, 1, int(goaltimedist), PointA,
                           mode, modes_to_run, output, KEYS, int(360 / int(numberofpoints)),
                           int(istime), formated_list, linenumber)  # Last parameter is 1 = time, 0 = distance

    numofnewlines = 0
    mypointsalt = converteralt(PointA, thelist["1"], int(goaltimedist) - (int(goaltimedist) * .05),
                               int(goaltimedist) +  (int(goaltimedist) * .05))
    mypoints = converter(thelist["0"], int(goaltimedist) - (int(goaltimedist) * .05),
                         int(goaltimedist) + (int(goaltimedist) * .05))
    lock = Lock()
    lock.acquire()
    filename = str(os.path.basename(outputfile).split(".")[0]) # These need to be changed based on either windows or mac (windows = \\, mac = /)
    kmlcolor(mypoints,str(filename),thelist["1"], int(goaltimedist))
    kmlunedited(mypoints, "original_kml", "original_" + str(filename), thelist["0"])
    os.chdir("..")
    kmlunedited(mypointsalt,"edited_kml", "edited_" + str(filename), thelist["0"])
    os.chdir("..")
    kmlmerged(mypointsalt, str(filename), thelist["0"], thelist["1"], int(goaltimedist))
    area = polyarea("original_kml", "original_" + str(filename) + ".kml") # These need to be changed based on either windows or mac (windows = \\, mac = /)
    os.chdir("..")
    areaalt = polyarea("edited_kml", "edited_" + str(filename)+ ".kml")   # These need to be changed based on either windows or mac (windows = \\, mac = /)
    os.chdir("..")
    points = polypoints("edited_kml", "edited_" + str(filename) + ".kml") # These need to be changed based on either windows or mac (windows = \\, mac = /)
    os.chdir("..")
    os.chdir("output_isochrone")
    output = open(outputfile, "a")
    outfile = open(outputfile, "r")
    contents = outfile.readlines()
    output.write(str(PointA[0]) + "," + str(PointA[1]) + ",")
    output.write(time.strftime('%H:%M:%S', time.localtime(time.time())) + ",")
    output.write(mode+ ",")
    output.write(numberofpoints + ",")

    output.write(str(len(mypoints)) + ",")
    output.write("T|" + str(goaltimedist) + ",") if int(istime) == 1 else output.write("D|" + str(goaltimedist) + ",")

    output.write(area + ",")
    cleanprint(mypoints, int(goaltimedist), output)
    output.write("\n")
    output.write(str(PointA[0]) + "," + str(PointA[1]) + ",")
    output.write(time.strftime('%H:%M:%S', time.localtime(time.time()))+ ",")
    output.write(mode + ",")
    output.write(numberofpoints + ",")
    output.write(str(len(mypointsalt)) + ",")
    output.write("T|" + str(goaltimedist) + ",") if int(istime) == 1 else output.write("D|" + str(goaltimedist) + ",")
    output.write(areaalt + ",")
    cleanprint(mypointsalt, int(goaltimedist), output)
    output.write("\n")
    output.close()
    currentindex += 1
    lock.release()
    end_time = dt.now()
    
    #print("Duration: {}".format(end_time-start_time))
    #  for pnt in mypoints:
    #   p.AddPoint(pnt[0], pnt[1])
    #num, perim, area = p.Compute()
    ###print "Perimeter/area of Antarctica are {:.3f} m / {:.1f} m^2".format(perim, area)
    #10 miles out with 1 mile increments finding times that are at x seconds
