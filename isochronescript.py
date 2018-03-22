#Function to create an array that is the amount to increment or decrement by based on lat/long
    #returns the array itself, 0 -> 180 (0->90 and -90->-1 = 91 +  )
    #Do the math we have been, store that value in each index through 180
# python dist.py try1.txt -off AIzaSyBlGF0c9WDFymECTZ15thY0WFOROdlUC5Q 0 0 0 0 1 0 0 0 0
from math import sin, cos, sqrt, atan2, radians
import json, urllib
import googlemaps
import time
from datetime import datetime
import sys
import datetime
import math
from area import area
from geographiclib.geodesic import Geodesic
import math
import simplekml
from multiprocessing import Lock
from cStringIO import StringIO
from xml.dom.minidom import parseString
from zipfile import ZipFile
from Polygon import *
kmlstr=\
'''<?xml version="1.0" encoding="UTF-8"?>
<kml xmlns="http://earth.google.com/kml/2.0">
<Document>
<name>Polygon: %s</name>
  <open>1</open>
  %s
</Document>
</kml>'''

polystr=\
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

def openKMZ(filename):
    zip=ZipFile(filename)
    for z in zip.filelist:
        if z.filename[-4:] == '.kml':
            fstring=zip.read(z)
            break
    else:
        raise Exception("Could not find kml file in %s" % filename)
    return fstring

def openKML(filename):
    try:
        fstring=openKMZ(filename)
    except Exception:
        fstring=open(filename,'r').read()
    return parseString(fstring)


def readPoly(filename):
    def parseData(d):
        dlines=d.split()
        poly=[]
        for l in dlines:
            l=l.strip()
            if l:
                point=[]
                for x in l.split(','):
                    point.append(float(x))
                poly.append(point[:2])
        return poly

    xml=openKML(filename)
    nodes=xml.getElementsByTagName('Placemark')
    desc={}
    for n in nodes:
        names=n.getElementsByTagName('name')
        try:
            desc['name']=names[0].childNodes[0].data.strip()
        except Exception:
            pass
        
        descriptions=n.getElementsByTagName('description')
        try:
            desc['description']=names[0].childNodes[0].data.strip()
        except Exception:
            pass

        times=n.getElementsByTagName('TimeSpan')
        try:
            desc['beginTime']=times[0].getElementsByTagName('begin')[0].childNodes[0].data.strip()
            desc['endTime'  ]=times[0].getElementsByTagName('end'  )[0].childNodes[0].data.strip()
        except Exception:
            pass

        times=n.getElementsByTagName('TimeStamp')
        try:
            desc['timeStamp']=times[0].getElementsByTagName('when')[0].childNodes[0].data.strip()
        except Exception:
            pass

            
        polys=n.getElementsByTagName('Polygon')
        for poly in polys:
            invalid=False
            c=n.getElementsByTagName('coordinates')
            if len(c) != 1:
                print ('invalid polygon found')
                continue
            if not invalid:
                c=c[0]
                d=c.childNodes[0].data.strip()
                data=parseData(d)
                yield (data,desc)

def latlon2meters(p):
    pi2=2.*math.pi
    reradius=1./6370000
    alat=0
    alon=0
    for i in p:
        alon=alon+i[0]
        alat=alat+i[1]
    lon_ctr=alon/len(p)
    lat_ctr=alat/len(p)
    unit_fxlat=pi2/(360. * reradius)
    unit_fxlon=math.cos(lat_ctr*pi2/360.) * unit_fxlat

    q=[]
    olon=p[0][0]
    olat=p[0][1]
    for i in p:
        q.append( ( (i[0] - olon) * unit_fxlon , \
                    (i[1] - olat) * unit_fxlat ) )
    return q

def polyStats(p):
    pm=Polygon(latlon2meters(p))
    area=pm.area()
    numpts=len(p)
    pl=Polygon(p)
    bbox=pl.boundingBox()
    center=pl.center()

    stat=\
            {'vertices':'%i' % numpts,
             'bounding box':'(%f , %f) - (%f , %f)' % (bbox[0],bbox[2],bbox[1],bbox[3]),
             'center':'(%f , %f)' % (center[0],center[1]),
             'area':'%f m^2' % (area) }
    return stat

def makepoly(p):
    return Polygon(p)

def intersect(p1,p2):
    q1=makepoly(p1)
    q2=makepoly(p2)

    q=q1 & q2

    return q

def get_area(p):
    q=makepoly(p)
    return p.area()

def write_poly(p,fname):
    if isinstance(fname,basestring):
        f=open(fname,'w')
    else:
        f=fname
    for i in p:
        f.write('%19.16f,%19.16f,0.\n' % (i[0],i[1]))
    f.flush()

def read_poly(fname):
    if isinstance(fname,basestring):
        f=open(fname,'r')
    else:
        f=fname
    s=f.readlines()
    p=[]
    for i in s:
        i=i.strip()
        j=i.split(',')
        p.append((float(j[0]),float(j[1])))
    return p

def poly2kmz(pp,fname):
    strs=[]
    i=0
    for p in pp:
        i=i+1
        f=StringIO()
        write_poly(p,f)
        strs.append(polystr % (i,f.getvalue()))
    s='\n'.join(strs)
    s=kmlstr % (fname,s)
    open(fname,'w').write(s)

def gmaps_traveltimeordist(directions11,last,timeordist):

  if len(directions11) > 0 and timeordist == 1:
   # print "TIME : " + str(directions11[0]["legs"][0]["duration"]["value"])
    return directions11[0]["legs"][0]["duration"]["value"]   #Extracts json value from google
  if len(directions11) > 0 and timeordist == 0:
   # print "DIST : " + str(directions11[0]["legs"][0]["distance"]["value"])
    return directions11[0]["legs"][0]["distance"]["value"]   #comes back in meters
  else:
    #print "TIME NOT AVAILABLE"
    return last
def pointfits(pointa,pointadone,goaltimeplus,goaltimeminus):
  if (pointadone >= goaltimeminus and pointadone <= goaltimeplus):
    return pointa
  else:
    return False
def closestpoint(InitialPoint,timelist,latlist,goaltime,additionalkeys,finallist): 
  #print "START CLOSEST"
  #print "THE LIST\n\n"
  #print cleanlist(latlist)
  #print "\n\n"
  lastclosest = 1000
  thepair = 0
  thekey = 0
  thetime = 0
  thepair = 0
  for key in additionalkeys:
      #print "KEY is  " + str(key)
      for combo in additionalkeys[key]:
        combo = combo.split("/") 
      if abs(int(combo[0])-goaltime) < lastclosest:
        lastclosest = abs(int(combo[0])-goaltime) 
        #print combo[1]
        #print "New Closest is " + str(lastclosest)
        thetime = combo[0]
        thepair = combo[1]
        thekey = key
  finallist[thekey] = str(thetime) + "/" + str(thepair)
  #print "END CLOSEST"
  return finallist
def isunevenbearing(keys,count):
  if (abs(keys[count+1] - keys[count]) != abs(keys[count] - keys[count-1])):
    return True
  else:
    return False
def matchup(testedlist,testedtimeslist,lister):
    for x,y in zip(testedlist,testedtimeslist):
        lister.append(str(y) + "/" + str(x))
    return lister

def my_algorithm(d,distance,Initial_increment,goaltime,InitialPoint,mode,modes_to_run,output,KEYS,degreeincrements,timeordist,Order_list,linenumber):
  originaldist = distance
  finallist = {}
  additionalkeys = {}
  negative = False
  goaltimeplus = goaltime + (goaltime * .05) #seconds
  goaltimeminus = goaltime -  (goaltime * .05) #seconds
  global directions11
  global gmaps
#  print "My Algorithm"
  printinglist = ""
  testedlist = []
  testedtimeslist = []
  keys = [key for key, value in sorted(d.iteritems())]
 # #print "KEYS = " + str(keys)
  count = 0
  attemptcounter = 0
  lastbeginning = InitialPoint
  previoustestlists = {}
  bearingproblem = ""
  x33 = 2
  lasttime = 0
  numberofmoves = abs(keys[count] - degreeincrements)/4
  if (numberofmoves >3):
    numberofmoves = 3
  originalnumberofmoves = numberofmoves
  while count <= len(keys)-1:
   # if (distance < .75):
    #  #print "DISTANCE WAS TOO SMALL"
     # distance = .25
    for item in testedlist:
      printinglist += item + "\n"
   # #print "TESTED IS " + str(printinglist)
    printlist = ""
  #  #print "COUNT IS " + str(count)
   # print "BEARING IS " + str(keys[count])
    for item in d[keys[count]]:
      printlist += item + "\n"
 #   #print "LIST IS " + str(printlist
    pointa = d[keys[count]][0]    #Closest, the exact distance away
    #print "Pointa distance = " + str(get_distance(float(InitialPoint[0]),float(InitialPoint[1]),float(pointa.split(",")[0]),float(pointa.split(",")[1])))
    #print "Distance between points: " + str(distance)
    lastbeginning = InitialPoint
    testedlist.append(pointa)
    x=0
    try_except(gmaps,InitialPoint,pointa,mode,modes_to_run,output,KEYS,x,Order_list,linenumber)
    attemptcounter += 1
    pointadone = gmaps_traveltimeordist(directions11,lasttime,timeordist)
    lasttime = pointadone
  #  checknumbers(lastrun,pointa,pointadone)
    testedtimeslist.append(pointadone)
    if (len(testedlist) >= 6 and not(pointfits(pointa,pointadone,goaltimeplus,goaltimeminus)) ):
      if (numberofmoves == originalnumberofmoves and not(negative)):
        bearingproblem = keys[count]
      if (numberofmoves >= 1 and not(negative) and keys[count]+ 2 > 0):  
        #print "CALLING AGAIN 11with " + str(x33)
     #   additionalkeys[keys[count]] = []
        keys.insert(count,keys[count]+ 2)
        #print "TAKE OUT: " + str(keys[count]-2)
        d.pop(keys[count]- 2, None)
        additionalkeys[keys[count]-2] = matchup(testedlist,testedtimeslist,[])
        keys.remove(keys[count]- 2)
        d[keys[count]] = []
        d = singlebearingupdate(InitialPoint,1,1,distance,d,0,keys[count])
        testedlist = []
        testedtimeslist = []
        #print "Just added: " + str(d[keys[count]])
        #print "BREAK"
     #   testedlist = []
      #  x33 = x33 + 2
        
        numberofmoves = numberofmoves - 1
        if (numberofmoves < 1):
            negative = True
      else:
        if (numberofmoves < 1):
            moveby = abs(keys[count] - bearingproblem)
            #print "CALLING AGAIN 33with " + str(x33)
            keys.insert(count,keys[count] - moveby - 2)
            d.pop(keys[count]+ 2+moveby, None)
            additionalkeys[keys[count]+ 2 + moveby] = matchup(testedlist,testedtimeslist,[])
            keys.remove(keys[count]+ 2+moveby)

            d[keys[count]] = []
            d = singlebearingupdate(InitialPoint,1,1,distance,d,0,keys[count])
            numberofmoves = numberofmoves + 1
            testedlist = []
            testedtimeslist = []
        else: 
            if (numberofmoves < originalnumberofmoves):
                #print "CALLING AGAIN44 with " + str(x33)
     #   additionalkeys[keys[count]] = []
                keys.insert(count,keys[count] - 2)
                d.pop(keys[count]+ 2, None)
                additionalkeys[keys[count]+ 2] = matchup(testedlist,testedtimeslist,[])
                keys.remove(keys[count]+ 2)
                d[keys[count]] = []
                d = singlebearingupdate(InitialPoint,1,1,distance,d,0,keys[count])
                numberofmoves = numberofmoves + 1
                testedlist = []
                testedtimeslist = []
            else:

                d.pop(keys[count-1], None)
                keys.remove(keys[count-1])
                additionalkeys[keys[count-1]] = matchup(testedlist,testedtimeslist,[])
                #finallist = closestpoint(InitialPoint,testedtimeslist,testedlist,goaltime,additionalkeys,finallist)
                #closestpoint(InitialPoint,testedtimeslist,testedlist,goaltime,additionalkeys,finallist)
                finallist.pop(bearingproblem,None)
                testedtimeslist = []
                testedlist = []
                lastbeginning = InitialPoint
                lastend = "000"
                numberofmoves = originalnumberofmoves
                negative = False
                count += 1
                distance = originaldist
                additionalkeys = {}


    elif (pointfits(pointa,pointadone,goaltimeplus,goaltimeminus)):
        #print "POINT FITS"
        distance = originaldist
        finallist[keys[count]] = str(pointa) + "/" + str(pointadone)
        testedlist = []
        numberofmoves = originalnumberofmoves
        negative = False
        additionalkeys = {}
        testedtimeslist = []
        lastbeginning = InitialPoint
        lastend = "000"
        count += 1

    elif(pointadone >= goaltimeminus):   #Must be in range 0 to a
        #print "0 to a"
        ratio = float(float(goaltime) / float(pointadone))
        ##print "RATIO is " + str(ratio)
    #    #print "List was: " + str(d[keys[count]])
        distance = float(get_distance(float(lastbeginning[0]),float(lastbeginning[1]),float(pointa.split(",")[0]),float(pointa.split(",")[1])))
        d = singlebearingupdate(InitialPoint,1,1,float((float(distance)) * float(ratio)) * 0.621371,d,0,keys[count])
      #  #print "DISTANCE: " + str(distance)
    #    #print "Ration: " + str(float((float(distance)) * float(ratio)) * 0.621371)
    #    #print "List is: " + str(d[keys[count]])
        lastend = tuple(pointa.split(","))
   #     d[keys[count]] = d[keys[count]][1:]
    else:
      #print "A TO B"
    #  #print "List was: " + str(d[keys[count]])
      ratio = float(float(goaltime) / float(pointadone))
      distance = float(get_distance(float(lastbeginning[0]),float(lastbeginning[1]),float(pointa.split(",")[0]),float(pointa.split(",")[1])))
      d = singlebearingupdate(lastbeginning,1,1,float((float(distance)) * float(ratio)) * 0.621371,d,0,keys[count])
      #  #print "DISTANCE: " + str(distance)
   #   #print "Ration: " + str( float(ratio))
   #   #print "List is: " + str(d[keys[count]])
      lastbeginning = tuple(pointa.split(","))
   #     d[keys[count]] = d[keys[count]][1:]
   #     d[keys[count]].append(pointb)
  
  for item in testedlist:
    printinglist += item + "\n"
  #  #print "TESTED IS " + str(printinglist)
  print ("ATTEMPTS: " + str(attemptcounter))

  return finallist
def format_orderlist(list):
  message = ""
  for item in list:
    if item.lower() == "rail":
      message += "train|tram|subway"
    else:
      if item != "0":
        message += item.lower()
    if list.index(item) != len(list)-1:
      if list[list.index(item)+1] != "0":
        message += "|"
  return message

def leaving(time_to_leave):
  return (time.time()+ (int(time_to_leave)*60))
def google_leaving(time_to_leave):
    if (time_to_leave == "0"):
      return "now"
    else:
      return (int(time.time())+ (int(time_to_leave)*60))

def print_breakdown_types(total_time,total_dist,bus,sub,train,tram,walk,wait,output):
  output.write(",")
  output.write(str(bus[0]))
  output.write(",")
  output.write(str(float(100* (float(bus[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(sub[0]))
  output.write(",")
  output.write(str(float(100* (float(sub[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(train[0]))
  output.write(",")
  output.write(str(float(100* (float(train[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(tram[0]))
  output.write(",")
  output.write(str(float(100* (float(tram[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(walk[0]))
  output.write(",")
  output.write(str(float(100* (float(walk[0])/float(total_time[0])))))
  output.write(",")
  output.write(str(wait[0]))
  output.write(",")
  output.write(str(float(100* (float(wait[0])/float(total_time[0])))))


def client(API_KEY_INPUT):
  global x
  try:
    global gmaps
    #print "CLIENT KEY" + str(API_KEY_INPUT)
    gmaps = googlemaps.Client(key = str(API_KEY_INPUT))
  except:
    #print "API Key " + str(x-1) + " Was Full or invalid.<br>"
    x += 1
    if (got_more_keys(KEYS,x) != False):      
      client(got_more_keys(KEYS,x))
    else:
      #print "No More keys to run on. None of the keys provided worked."
      exit()
def finish_line(address,destination,mode,output,linenumber):
  outfile = open(sys.argv[2],"r")
  contents = outfile.readlines()
  while ((int(linenumber)) != int(len(contents))):
    time.sleep(1)
    outfile.seek(0)
    contents = outfile.readlines()
  output.write(str(address[0]) + "," + str(address[1]) + ",")
  output.write(time.strftime('%H:%M:%S', time.localtime(time.time()))+ ",")
  output.write(str(mode) + ",FAILED,\n")
def format_orderlist(list):
  message = ""
  for item in list:
    if item.lower() == "rail":
      message += "train|tram|subway"
    else:
      if item != "0":
        message += item.lower()
    if list.index(item) != len(list)-1:
      if list[list.index(item)+1] != "0":
        message += "|"
  return message

def try_except(gmaps12,address,destination,mode,modes_to_run,output,KEYS,a,Order_list,linenumber):
  #print "MY MODE: " + str(mode)
  global gmaps
  global x
  try:
    global directions11
    if mode == "transit":
      directions11 = gmaps.directions(address,destination,mode=mode,units="metric",departure_time="now",transit_mode=Order_list,alternatives="true")
    else:
      directions11 = gmaps.directions(address,destination,mode=mode,units="metric",departure_time="now",alternatives="true")

  #  with open(destination + ".json","w") as file:
     # json.dump(directions11,file)
  except googlemaps.exceptions.ApiError as e:
    x += 1
    #print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,mode,modes_to_run,output,KEYS,a,Order_list)
    else:
      #print "Key Has filled up or another error has occured. Any partial data from google can be downloaded below.<br>\n"
      finish_line(address,destination,mode,output,linenumber)
      exit()
  except Exception as e:
    x += 1
    #print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,mode,modes_to_run,output,KEYS,a,Order_list)
    else:
      #print "Key " + str(x-1) + " Has filled up or another error has occured. Any partial data from google can be downloaded below.<br>\n"
      finish_line(address,destination,mode,output,linenumber)
      exit()

def get_mode(count):
  if(count == 0):
    return "driving"
  if(count == 1):
    return "walking"
  if(count == 2):
    return "bicycling"
  if(count == 3):
    return "transit"

def file_len(fname):
    with open(fname) as f:
        for i, l in enumerate(f):
            pass
    return i + 1
def get_seconds(t1,t2,Entry_count,mode_count):
  h1, m1, s1 = t1.hour, t1.minute, t1.second
  h2, m2, s2 = t2.hour, t2.minute, t2.second
  t1_secs = s1 + 60 * (m1 + 60*h1)
  t2_secs = s2 + 60 * (m2 + 60*h2)
  return((t2_secs/Entry_count)/mode_count)

def got_more_keys(KEYS,count):
  global x
  if(KEYS[count-1] == str("0") or x > len(KEYS)-1):
    return False
  return KEYS[count-1]
def check_timetoleave(line):
  if(len(line) > 2):
    return line[3]
  else:
    #print "ELSE"
    return "0"

def getEarthRadius(PointA):
  return getEarthRadiusAtLatitude(PointA[0])
  
def getEarthRadiusAtLatitude(latitude):
  earthRadius = 6367
  equatorRadius = 6378.137
  polarRadius = 6356.7523142

  lat = radians(latitude)
  part1 = equatorRadius * sqrt(pow(polarRadius,4)/pow(equatorRadius,4)*pow((sin(lat)),2)+pow(cos(lat),2))
  part2 = sqrt(1-(1-(polarRadius*polarRadius)/(equatorRadius*equatorRadius)) * pow(sin(lat),2))
  return part1/part2
def get_distance(a,b,c,d):
# approximate radius of earth in km
    R = 6373.0

# optimized for locations around 39 degrees from the equator (roughly the Latitude of Washington, DC, USA).
    lat1 = radians(a)
    lon1 = radians(b)
    lat2 = radians(c)
    lon2 = radians(d)

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    arc = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(arc), sqrt(1 - arc))

    distance = getEarthRadiusAtLatitude(lat1) * c
    return distance
def get_departuretime(directions):
  if "departure_time" in directions.keys():
    if "value" in directions['departure_time'].keys():
      return directions['departure_time']['value']
  else:
    return int(time.time())
def check_dest_space(line):
  if(line.strip().split(',')[2][0] == ' '):
    return line.strip().split(",")[2][1:] + "," +line.strip().split(",")[3]
  else:
    return line.strip().split(",")[2] + "," +line.strip().split(",")[3]

def calculate_initial_compass_bearing(pointA, pointB):
    if (type(pointA) != tuple) or (type(pointB) != tuple):
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

def numofiterations(square_count): 
    return 3
def go_to_corner(PointA,radius,numberofpairs,btwnmarks,currentdict,Dictkey,degreeincrements):
    global square_count
    square_count += 1
    PointB = [0,0]
   # PointB[0] = incrementlat(0,distance,PointA[0],distlat(PointA[0]))
   # PointB[1] = decrementlon(0,distance,PointA[1],distanceindegree(PointA[1],PointA[0]))
    PointB[0] = PointA[0]
    PointB[1] = PointA[1]
  #  lat1 = incrementlat(-180,.125/4,lat1,distlat(lat1)) 
    circular(PointB[0],PointB[1],numberofpairs,btwnmarks,currentdict,Dictkey,degreeincrements)
def singlebearingupdate(PointA,radius,numberofpairs,btwnmarks,currentdict,Dictkey,bearing):
    global square_count
    square_count += 1
    PointB = [0,0]
   # PointB[0] = incrementlat(0,distance,PointA[0],distlat(PointA[0]))
   # PointB[1] = decrementlon(0,distance,PointA[1],distanceindegree(PointA[1],PointA[0]))
    PointB[0] = PointA[0]
    PointB[1] = PointA[1]
    #print "BEARING: " + str(bearing)
  #  lat1 = incrementlat(-180,.125/4,lat1,distlat(lat1)) 
    currentdict[bearing] = circularsingle(PointB[0],PointB[1],numberofpairs,btwnmarks,currentdict,Dictkey,bearing)
    if (len(currentdict[bearing]) >= 2):
      currentdict[bearing] = currentdict[bearing][numberofpairs:]
    #print "PAIRS:" + str(numberofpairs)

    return currentdict
def distlat(lat1):
  if (lat1 < 0):
    return latnumbers[int(str(lat1[1:]).split('.')[0])]
  else:
    return latnumbers[int(str(lat1).split('.')[0])]
def incrementlat(currentbearing,a,lat1,distance):
    ##print "DIST: " + str(distance)
    x = .1
    while(float(distance/x) > a + .01 or float(distance/x) < a - .01):
    #   #print float(distance/x)
        x += .001
    ##print "X : " + str(x)
    ##print "LAT INC: " + str(float(float(lat1) + float( float(1.000/float(x)) * math.cos(math.radians(currentbearing)))))
    return float(float(lat1) + float( float(1.000/float(x)) * math.cos(math.radians(currentbearing))))

def incrementlon(currentbearing,a,lon1,distance):
#   #print "DIST: " + str(distance)
    x = .1
    while(float(distance/x) > a + .01 or float(distance/x) <  a - .01 ):
    #   #print float(distance/x)
        x += .001
    ##print "X : " + str(x)
    ##print "LONG INC: " + str(float(float(lon1) + float( float(1.000/float(x)) * math.sin(math.radians(currentbearing)))))
    return float(float(lon1) + float(float(1.000/float(x)) * math.sin(math.radians(currentbearing))))

def decrementlat(currentbearing,a,lat1,distance):
    ##print "DIST: " + str(distance)
    x = .1
    while(float(distance/x) > a + .01 or float(distance/x) <  a - .01):
    #   #print float(distance/x)
        x += .001
    return float(float(lat1) - float( float(1.000/float(x)) * math.cos(math.radians(currentbearing))))

def decrementlon(currentbearing,a,lon1,distance):
    ##print "DIST: " + str(distance)
    x = .1
    while(float(distance/x) > a + .01 or float(distance/x) <  a - .01 ):
    #   #print float(distance/x)
        x += .001
    return float(float(lon1) - float(float(1.000/float(x)) * math.sin(math.radians(currentbearing))))


def distanceindegree(lon1,latitude):
  if (lat1 < 0):
    return longnumbers[int(str(latitude[1:]).split('.')[0])]
  else:
    return longnumbers[int(str(latitude).split('.')[0])]

def circular(lat1,lon1,numberofpairs,btwnmarks,currentdict,Dictkey,degreeincrements):
    originallong = lon1
    originallat = lat1
    y = 1
    x = 0
    global square_count
    
    firstlat = lat1
    firstlon = lon1
    degrees = 0
    #print str(degrees) + " " + str(lat1) + "," + str(lon1)

    while (degrees <= 90):
      lat1 = incrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
      #print str(degrees) + " " + str(lat1) + "," + str(lon1)
      if (x == numberofpairs):
        degrees += degreeincrements
        x = 0
        lat1 = firstlat
        lon1 = firstlon
 #   degrees = degrees - 15
    while (degrees >= 90 and degrees < 180 ):
      lat1 = decrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
      #print str(degrees) + " " + str(lat1) + "," + str(lon1)
      if (x == numberofpairs):
        degrees += degreeincrements
        lat1 = firstlat
        lon1 = firstlon
        x = 0
   # degrees = degrees - 15
   # #print "DONE"
    while (degrees >= 180 and degrees <= 270):
      lat1 = incrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
      #print str(degrees) + " " + str(lat1) + "," + str(lon1)
      if (x == numberofpairs):
        degrees += degreeincrements
        x = 0
        lat1 = firstlat
        lon1 = firstlon
  #  degrees = degrees - 15
    while (degrees >= 270 and degrees < 360):
      lat1 = decrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
      #print str(degrees) + " " + str(lat1) + "," + str(lon1)
      if (x == numberofpairs):
        degrees += degreeincrements
        x = 0        
        lat1 = firstlat
        lon1 = firstlon
    lastlat = lat1
    lastlon = lon1
    distance = get_distance(firstlat,firstlon,lastlat,lastlon) * 0.621371
      #print key,value    
def circularsingle(lat1,lon1,count,btwnmarks,currentdict,Dictkey,degrees):
    originallong = lon1
    originallat = lat1
    y = 1
    x = 0
    global square_count
    
    firstlat = lat1
    firstlon = lon1
   # #print str(lat1) + "," + str(lon1)
    fixeddegrees = degrees
    if (degrees > 360):
      fixeddegrees = degrees - 360
    while (fixeddegrees <= 90):
      lat1 = incrementlat(fixeddegrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(fixeddegrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
   #   #print str(lat1) + "," + str(lon1)
      if (x == count):
        return currentdict[degrees]
    while (fixeddegrees >= 90 and fixeddegrees < 180 ):
      lat1 = decrementlat(fixeddegrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(fixeddegrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
  #    #print str(lat1) + "," + str(lon1)
      if (x == count):
        return currentdict[degrees]
   # degrees = degrees - 15
   # #print "DONE"
    while (fixeddegrees >= 180 and fixeddegrees <= 270):
      lat1 = incrementlat(fixeddegrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(fixeddegrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
   #   #print str(lat1) + "," + str(lon1)
      if (x == count):
        return currentdict[degrees]
  #  degrees = degrees - 15
    while (fixeddegrees >= 270 and fixeddegrees <= 360):
      lat1 = decrementlat(fixeddegrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(fixeddegrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[fixeddegrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
    #  #print str(lat1) + "," + str(lon1)
      if (x == count):
        return currentdict[degrees]
    lastlat = lat1
    lastlon = lon1
    distance = get_distance(firstlat,firstlon,lastlat,lastlon) * 0.621371
   # for key, value in currentdict.iteritems() :
      #print key,value    
    return currentdict[degrees]

def tomyratio(numofmeters):
    numofkm = float(numofmeters) * 4.38888888889 * .001
    ##print "NUM: " + str(numofkm)
    return numofkm

def get_dist(lat1,lon1,lat2,lon2): 
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def remove_newlines(fname):
    flist = open(fname).readlines()
    return [s.rstrip('\n') for s in flist]

def makekeys(storage,increment):
  for k in degreelist(increment):
    storage[k] = []
  return storage
def degreelist(number):
  mylist = []
  counter = 0
  while counter < 360:
    mylist.append(counter)
    counter += number
  return mylist
def checknumbers(thedict,thepair,thetime):
  pairtime = ""
  for key in thedict:
    pairtime = thedict[key].split("/")

def cleanprint(thedict,goaltime,output):
  counter = 0
  pairtime = ""
  for key in thedict:
    pairtime = thedict[key].split("/")
    if len(pairtime[0]) < 5:
      counter += 1
      output.write('"' + pairtime[1]+'",')
    else:
       output.write('"' + pairtime[0]+'",')
#$  print str(counter) + " Were off by more than +- 5%"
#  printoffbypercents(thedict,goaltime)
def printoffbypercents(thedict,goaltime):
  pairtime = ""
  for key in thedict:
    pairtime = thedict[key].split("/")

def find_key(partial,partial2,thedict):
  for key in thedict:
    if partial in thedict[key]:
      if (partial2 in thedict[key]):
        return str(key)
def kmlmaker(mypoints,filename,thedict):    
  kml = simplekml.Kml()
  finallist =  []
  for pont in mypoints:
    finallist.append((pont[1],pont[0]))
  pol = kml.newpolygon(name=filename,outerboundaryis=finallist)
  kml.save("kml\\" + filename + ".kml")
def polyarea(filename):
  fname=filename
  i=0
  for p in readPoly(fname):
      p,desc=p
      i=i+1
      stats=polyStats(p)
      desc.update(stats)
    #  print 'Polygon #%i' % i
      for d,v in desc.iteritems():
        if (d == "area"):
          return v[1:-4]
def polypoints(filename):
  fname=filename
  i=0
  for p in readPoly(fname):
      p,desc=p
      i=i+1
      stats=polyStats(p)
      desc.update(stats)
  #    print 'Polygon #%i' % i
      for d,v in desc.iteritems():
        if (d == "vertices"):
          return v[1:]
def converter(thelist):
  totallist = []
  first = []
  second = []
  third = []
  fourth = []
#  thedict = {}
 # thedict["type"] = "Polygon"
  #thedict["coordinates"] = []
  for key in (sorted(thelist)):
  #  print "KEY : " + str(key) + " PNT: " + str(thelist[key].split("/")[0])
    if int(key) <= 90:
 #     print "1"
      first.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
    if 180 >= int(key) >= 91:
 #     print "2"
      second.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
    if 270 >= int(key) >= 181:
 #     print "3"
      third.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
    if 359 >= int(key) >= 271:
  #    print "4"
      fourth.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
  if (len(second) == 0 and len(third)>=2):
    first.insert(0,third[len(third)-2])
    totallist = first + fourth + third[:-1] + second
  elif (len(second) == 0 and len(third) == 0 and len(fourth) >= 2):
    first.insert(0,fourth[len(fourth)-2])
    totallist = first + fourth[:-1] + third + second
  elif (len(second) == 0 and len(third) == 0 and len(fourth) == 1):
    first.insert(0,fourth[len(fourth)-1])
    totallist = first + fourth[:-1] + third + second

  elif (len(second) == 1):
      first.insert(0,second[len(second)-1])
      totallist = first + fourth + third + second[:-1]

  else:
    first.insert(0,second[len(second)-2])
    totallist = first + fourth + third + second[:-1]
 # thedict["coordinates"].append(totallist)
  return totallist

def polypoints(filename):
  fname=filename
  i=0
  for p in readPoly(fname):
      p,desc=p
      i=i+1
      stats=polyStats(p)
      desc.update(stats)
    #  print 'Polygon #%i' % i
      for d,v in desc.iteritems():
        if (d == "area"):
          return v[1:-4]
def polypoints(filename):
  fname=filename
  i=0
  for p in readPoly(fname):
      p,desc=p
      i=i+1
      stats=polyStats(p)
      desc.update(stats)
  #    print 'Polygon #%i' % i
      for d,v in desc.iteritems():
        if (d == "vertices"):
          return v[1:]
def converter(thelist):
  totallist = []
  first = []
  second = []
  third = []
  fourth = []
#  thedict = {}
 # thedict["type"] = "Polygon"
  #thedict["coordinates"] = []
  for key in (sorted(thelist)):
  #  print "KEY : " + str(key) + " PNT: " + str(thelist[key].split("/")[0])
    if int(key) <= 90:
 #     print "1"
      first.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
    if 180 >= int(key) >= 91:
 #     print "2"
      second.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
    if 270 >= int(key) >= 181:
 #     print "3"
      third.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
    if 359 >= int(key) >= 271:
  #    print "4"
      fourth.append(tuple(str(str(thelist[key]).split("/")[0]).split(",")))
  if (len(second) == 0 and len(third)>=2):
    first.insert(0,third[len(third)-2])
    totallist = first + fourth + third[:-1] + second
  elif (len(second) == 0 and len(third) == 0 and len(fourth) >= 2):
    first.insert(0,fourth[len(fourth)-2])
    totallist = first + fourth[:-1] + third + second
  elif (len(second) == 0 and len(third) == 0 and len(fourth) == 1):
    first.insert(0,fourth[len(fourth)-1])
    totallist = first + fourth[:-1] + third + second

  elif (len(second) == 1):
      first.insert(0,second[len(second)-1])
      totallist = first + fourth + third + second[:-1]

  else:
    first.insert(0,second[len(second)-2])
    totallist = first + fourth + third + second[:-1]
 # thedict["coordinates"].append(totallist)
  return totallist
def find_pointa(pointadist,d,a,b):
  count = 0
  for x in d['45']:
    lat = x.split(',')[0]
    lon = x.split(',')[1]
    if (get_distance(a,b,lat,lon) >= pointadist):
      return count
    else:
      count += 1
    if (len(d['45']) == count-1):
      exit(1)

def find_pointb(pointbdist,d,a,b):
  count = 0
  for x in d['45']:
    lat = x.split(',')[0]
    lon = x.split(',')[1]
    if (get_distance(a,b,lat,lon) >= pointbdist):
      return count
    else:
      count += 1
    if (len(d['45']) == count-1):
      exit(1)
latnumbers = [68.703,
68.7108222222,
68.7186444444,
68.7264666667,
68.7342888889,
68.7421111111,
68.7499333333,
68.7577555555,
68.7655777778,
68.7734,
68.7812222222,
68.7890444444,
68.7968666666,
68.8046888889,
68.8125111111,
68.8203333333,
68.8281555555,
68.8359777777,
68.8438,
68.8516222222,
68.8594444444,
68.8672666666,
68.8750888888,
68.8829111111,
68.8907333333,
68.8985555555,
68.9063777777,
68.9141999999,
68.9220222222,
68.9298444444,
68.9376666666,
68.9454888888,
68.953311111,
68.9611333333,
68.9689555555,
68.9767777777,
68.9845999999,
68.9924222221,
69.0002444444,
69.0080666666,
69.0158888888,
69.023711111,
69.0315333332,
69.0393555555,
69.0471777777,
69.0549999999,
69.0628222221,
69.0706444443,
69.0784666666,
69.0862888888,
69.094111111,
69.1019333332,
69.1097555554,
69.1175777777,
69.1253999999,
69.1332222221,
69.1410444443,
69.1488666665,
69.1566888888,
69.164511111,
69.1723333332,
69.1801555554,
69.1879777776,
69.1957999999,
69.2036222221,
69.2114444443,
69.2192666665,
69.2270888887,
69.234911111,
69.2427333332,
69.2505555554,
69.2583777776,
69.2661999998,
69.2740222221,
69.2818444443,
69.2896666665,
69.2974888887,
69.3053111109,
69.3131333332,
69.3209555554,
69.3287777776,
69.3365999998,
69.344422222,
69.3522444443,
69.3600666665,
69.3678888887,
69.3757111109,
69.3835333331,
69.3913555554,
69.3991777776]
longnumbers = [69.172,
69.1614647694,
69.1298622866,
69.077202178,
69.0035004846,
68.9087796564,
68.7930685464,
68.6564024013,
68.498822851,
68.3203778956,
68.1211218914,
67.9011155334,
67.660425838,
67.3991261213,
67.117295978,
66.8150212561,
66.4923940314,
66.1495125795,
65.7864813452,
65.4034109114,
65.000417965,
64.5776252617,
64.1351615881,
63.673161723,
63.1917663961,
62.6911222449,
62.1713817706,
61.6327032912,
61.0752508932,
60.4991943822,
59.9047092306,
59.2919765242,
58.6611829073,
58.0125205259,
57.3461869688,
56.6623852076,
55.9613235349,
55.243215501,
54.5082798485,
53.7567404459,
52.9888262194,
52.2047710832,
51.4048138679,
50.5891982484,
49.758172669,
48.9119902682,
48.0509088014,
47.1751905622,
46.2851023031,
45.3809151533,
44.4629045372,
43.5313500897,
42.5865355712,
41.6287487815,
40.6582814716,
39.6754292553,
38.6804915189,
37.6737713301,
36.6555753455,
35.6262137177,
34.586,
33.5352510517,
32.474286941,
31.403430848,
30.3230089657,
29.2333504011,
28.1347870748,
27.0276536199,
25.9122872798,
24.7890278059,
23.6582173541,
22.5202003801,
21.3753235349,
20.2239355591,
19.0663871766,
17.9030309878,
16.7342213624,
15.5603143311,
14.3816674772,
13.1986398282,
12.0115917456,
10.8208848158,
9.62688173961,
8.42994622202,
7.23044286115,
6.02873703734,
4.82519480183,
3.62018276524,
2.41406798591,
1.20721785808]

if __name__ == '__main__':
  print ("WE IN HERE")
  x=1
  gmaps = ""
  global directions11
  directions11 = ""
  #Compile all modes to see which are to be run (ORDER: Driving,Walking,Biking,Transit)
  Types_of_Bus = ["BUS","INTERCITY_BUS","TROLLEYBUS"]
  Types_of_Rail = ["RAIL","METRO_RAIL","MONORAIL","COMMUTER_TRAIN","HEAVY_RAIL","HIGH_SPEED_TRAIN"]
  Types_of_Tram = ["TRAM"]
  Types_of_Subway = ["SUBWAY"]
  # approximate radius of earth in km
  R = 6373.0
  lat1 = radians(40.834288)
  lon1 = radians(-73.851028)
  lat2 = radians(40.693797)
  lon2 = radians(-73.990696)
  global square_count
  square_count = 0


  output = open(sys.argv[2],"a")
  inputfile = open(sys.argv[1],"r")
  testiter = open(sys.argv[1],"r")
  #Path to output file created
  modes_to_run = []
  #-off and -on
  Toggle_traffic_models = sys.argv[3]
  #API KEY STORAGE
  API_KEY_INPUT = sys.argv[4]
  KEY2 = sys.argv[5]
  KEY3 = sys.argv[6]
  KEY4 = sys.argv[7]
  KEY5 = sys.argv[8]
  modes_to_run = []
  all_modes = [sys.argv[9],sys.argv[10],sys.argv[11],sys.argv[12]]
  Order_list = [sys.argv[13],sys.argv[14],sys.argv[15],sys.argv[16]]
  istime = sys.argv[17]
  goaltimedist = sys.argv[18]
  numberofpoints = sys.argv[19]
  formated_list = format_orderlist(Order_list)
  if (istime == "on"):
    istime = 1
  else:
    istime = 0


  mode_count = 0
  #Get Count of how many modes we are running
  for entry in all_modes:
    if(entry == "on"):
      mode = get_mode(mode_count)
      modes_to_run.append(mode)
    mode_count += 1

  key_count = 0
  KEYS=[API_KEY_INPUT,KEY2,KEY3,KEY4,KEY5]
  for key in KEYS:
    if(key != "0"):
      key_count += 1
  #Compile all modes to see which are to be run (ORDER: Driving,Walking,Biking,Transit)

  address = ""
  traffic_models_list = []
  destination = ""
  print ("<br>LINE COUNT: " + str(file_len(str(sys.argv[1]))))

  counter=0
  y=0
  #client(API_KEY_INPUT)
  #print str(API_KEY_INPUT)
  client(API_KEY_INPUT)
  linenumber = sys.argv[21]
  line = sys.argv[20]
  currentindex = 0
  i=0
  counter += 1
  mode = sys.argv[22]
  modes_to_run = [mode]
  if(counter>=2490):
      #print "Key #" + str(y) + " Reached its limit.<br>"
      counter=0
      y += 1
      if(KEYS[x] == '0'):
        #print "END of Keys. Partial data download is available below.\n"
        exit()
      API_KEY_INPUT = KEYS[x]
      x+=1
  time_to_leave = check_timetoleave(line.strip().split(","))
  PointA = (float(line.strip().split(",")[0]),float(line.strip().split(",")[1]))
  currentname = {}
  currentname = makekeys(currentname,int(360/int(numberofpoints)))
  go_to_corner(PointA,1,1,.5,currentname,0,int(360/int(numberofpoints)))   #This gets 3 pairs that are 10,20, and 30 miles from origin on bearing
  iterate_counter=0
  thelist = my_algorithm(currentname,.5,1,int(goaltimedist),PointA,mode,modes_to_run,output,KEYS,int(360/int(numberofpoints)),int(istime),formated_list,linenumber)   #Last parameter is 1 = time, 0 = distance
  #print thelist
  numofnewlines = 0
  mypoints = converter(thelist)
  #print mypoints
  lock = Lock()
  lock.acquire()
  filename = str(str(sys.argv[2]).split('/')[1]).split(".")[0]#These need to be changed based on either windows or mac (windows = \\, mac = /)
  kmlmaker(mypoints,str(filename)+ "line" + str(linenumber),thelist)
  area = polyarea("kml\\" + str(filename)+ "line" + str(linenumber) + ".kml")#These need to be changed based on either windows or mac (windows = \\, mac = /)
  points = polypoints("kml\\" + str(filename)+ "line" + str(linenumber) + ".kml") #These need to be changed based on either windows or mac (windows = \\, mac = /)
  output = open(sys.argv[2],"a")
  outfile = open(sys.argv[2],"r")
  contents = outfile.readlines()
  while ((int(linenumber)) != int(len(contents))):
    time.sleep(1)
    outfile.seek(0)
    contents = outfile.readlines()
  output.write(str(PointA[0]) + "," + str(PointA[1]) + ",")
  #print str(PointA[0]) + "," + str(PointA[1]) + ","
  output.write(time.strftime('%H:%M:%S', time.localtime(time.time()))+ ",")
  output.write(mode+ ",")
  output.write(numberofpoints + ",")

  output.write(str(len(thelist)) + ",")
  if (int(istime) == 1):
    output.write("T|" + str(goaltimedist) + ",")
  else:
    output.write("D|" + str(goaltimedist) + ",")

  output.write(area + ",")
  cleanprint(thelist,int(goaltimedist),output)
  output.write("\n")
  output.close()
  currentindex += 1
  lock.release()
  #  for pnt in mypoints:
  #   p.AddPoint(pnt[0], pnt[1])
  #num, perim, area = p.Compute()
  ##print "Perimeter/area of Antarctica are {:.3f} m / {:.1f} m^2".format(perim, area)
  #10 miles out with 1 mile increments finding times that are at x seconds
