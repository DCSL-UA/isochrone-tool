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
from getlat import latnumbers,longnumbers,makekeys,checknumbers,cleanprint
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

def gmaps_traveltime(directions11):
  if len(directions11) > 0:
    print "TIME : " + str(directions11[0]["legs"][0]["duration"]["value"])
    return directions11[0]["legs"][0]["duration"]["value"]   #Extracts json value from google
  else:
    print "TIME NOT AVAILABLE"
    return 0
def pointfits(pointa,pointadone,goaltimeplus,goaltimeminus):
  if (pointadone >= goaltimeminus and pointadone <= goaltimeplus):
    return pointa
  else:
    return False
def closestpoint(InitialPoint,timelist,latlist,goaltime): 
  print "START CLOSEST"
  print "THE LIST\n\n"
  print "\n\n"
  lastclosest = 1000
  thepair = 0
  for time in timelist:
    thetime = time
    for pair in latlist:
      thepair = pair
      if abs(int(time)-goaltime) < lastclosest:
        lastclosest = abs(int(time)-goaltime) 
        print pair
        print InitialPoint
        print "New Closest is " + str(lastclosest)
        thetime = time
        thepair = pair
  print "END CLOSEST"
  return str(thetime) + "/" + str(thepair)
def my_algorithm(d,distance,Initial_increment,goaltime,InitialPoint,mode,modes_to_run,output,KEYS):
  originaldist = distance
  finallist = {}
  goaltimeplus = goaltime + (goaltime * .05) #seconds
  goaltimeminus = goaltime -  (goaltime * .05) #seconds
  global directions11
  global gmaps
#  print "My Algorithm"
  printinglist = ""
  testedlist = []
  testedtimeslist = []
  keys = [key for key, value in d.iteritems()]
 # print "KEYS = " + str(keys)
  count = 0
  attemptcounter = 0
  lastbeginning = InitialPoint
  while count <= len(keys)-1:
   # if (distance < .75):
    #  print "DISTANCE WAS TOO SMALL"
     # distance = .25
    for item in testedlist:
      printinglist += item + "\n"
   # print "TESTED IS " + str(printinglist)
    printlist = ""
  #  print "COUNT IS " + str(count)
  #  print "BEARING IS " + str(keys[count])
    for item in d[keys[count]]:
      printlist += item + "\n"
 #   print "LIST IS " + str(printlist
    pointa = d[keys[count]][0]    #Closest, the exact distance away
    print "Pointa distance = " + str(get_distance(float(InitialPoint[0]),float(InitialPoint[1]),float(pointa.split(",")[0]),float(pointa.split(",")[1])))
    print "Distance between points: " + str(distance)
    lastbeginning = InitialPoint
    testedlist.append(pointa)
    try_except(gmaps,InitialPoint,pointa,mode,modes_to_run,output,KEYS,x)
    attemptcounter += 1
    pointadone = gmaps_traveltime(directions11)
   # checknumbers(lastrun,pointa,pointadone)
    testedtimeslist.append(pointadone)
    if (len(testedlist) >= 10):
      distance = originaldist
      finallist[keys[count]] = closestpoint(InitialPoint,testedtimeslist,testedlist,goaltime)
      testedtimeslist = []
      testedlist = []
      lastbeginning = InitialPoint
      lastend = "000"
      count += 1

    if (pointfits(pointa,pointadone,goaltimeplus,goaltimeminus)):
      print "POINT FITS"
      distance = originaldist
      finallist[keys[count]] = str(pointa) + "/" + str(pointadone)
      testedlist = []
      testedtimeslist = []
      lastbeginning = InitialPoint
      lastend = "000"
      count += 1

    elif(pointadone >= goaltimeminus):   #Must be in range 0 to a
        print "0 to a"      
        ratio = float(float(goaltime) / float(pointadone))
        #print "RATIO is " + str(ratio)
        print "List was: " + str(d[keys[count]])
        distance = float(get_distance(float(lastbeginning[0]),float(lastbeginning[1]),float(pointa.split(",")[0]),float(pointa.split(",")[1])))
        d = singlebearingupdate(InitialPoint,1,1,float((float(distance)) * float(ratio)) * 0.621371,d,0,keys[count])
      #  print "DISTANCE: " + str(distance)
        print "Ration: " + str(float((float(distance)) * float(ratio)) * 0.621371)
        print "List is: " + str(d[keys[count]])
        lastend = tuple(pointa.split(","))
   #     d[keys[count]] = d[keys[count]][1:]
    else:
      print "A TO B"
      print "List was: " + str(d[keys[count]])
      ratio = float(float(goaltime) / float(pointadone))
      distance = float(get_distance(float(lastbeginning[0]),float(lastbeginning[1]),float(pointa.split(",")[0]),float(pointa.split(",")[1])))
      d = singlebearingupdate(lastbeginning,1,1,float((float(distance)) * float(ratio)) * 0.621371,d,0,keys[count])
      #  print "DISTANCE: " + str(distance)
      print "Ration: " + str( float(ratio))
      print "List is: " + str(d[keys[count]])
      lastbeginning = tuple(pointa.split(","))
   #     d[keys[count]] = d[keys[count]][1:]
   #     d[keys[count]].append(pointb)
  
  for item in testedlist:
    printinglist += item + "\n"
  #  print "TESTED IS " + str(printinglist)
  print "ATTEMPTS: " + str(attemptcounter)
  return finallist

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


def adjust_totals(total_time,total_dist,bus,sub,train,tram,walk,step):
    if (step['transit_details']['line']['vehicle']['type'] in Types_of_Bus):
      bus[0] += step['duration']['value']
      bus[1] += step['distance']['value']
      total_dist[0] += step['distance']['value']
      total_time[0] += step['duration']['value']

    if (step['transit_details']['line']['vehicle']['type'] in Types_of_Subway):
      sub[0] += step['duration']['value'] 
      sub[1] += step['distance']['value']
      total_dist[0] += step['distance']['value']
      total_time[0] += step['duration']['value']
    if (step['transit_details']['line']['vehicle']['type'] in Types_of_Rail):
      train[0] += step['duration']['value']
      train[1] += step['distance']['value']
      total_dist[0] += step['distance']['value']
      total_time[0] += step['duration']['value']
    if (step['transit_details']['line']['vehicle']['type'] in Types_of_Tram):
      tram[0] += step['duration']['value']
      tram[1] += step['distance']['value']
      total_dist[0] += step['distance']['value']
      total_time[0] += step['duration']['value']
    return step['distance']['value']




def leaving_adjust(time_to_leave):
    return (int(time.time())+ (int(time_to_leave)*60))
def correct_leave_time(duration,departure_epoch,leavetime):
  time1 = departure_epoch - leavetime
  time2 = duration + time1
  return time2
def client(API_KEY_INPUT):
  global x
  try:
    global gmaps
    print "CLIENT KEY" + str(API_KEY_INPUT)
    gmaps = googlemaps.Client(key = str(API_KEY_INPUT))
  except:
    print "API Key " + str(x-1) + " Was Full or invalid.<br>"
    x += 1
    if (got_more_keys(KEYS,x) != False):      
      client(got_more_keys(KEYS,x))
    else:
      print "No More keys to run on. None of the keys provided worked."
      exit()
def finish_line(array_size,array_index,output):
  while(array_index != array_size):
    output.write(",transit,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL,NULL")
    array_index += 1
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
def try_except(gmaps12,address,destination,mode,modes_to_run,output,KEYS,a):
  print "MY MODE: " + str(mode)
  global gmaps
  global x
  try:
    global directions11
    directions11 = gmaps.directions(address,destination,mode=mode,units="metric",departure_time="now",alternatives="true")
    with open(destination + ".json","w") as file:
      json.dump(directions11,file)
  except googlemaps.exceptions.ApiError as e:
    x += 1
    print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,mode,modes_to_run,output,KEYS,a)
    else:
      print "Key Has filled up or another error has occured. Any partial data from google can be downloaded below.<br>\n"
      finish_line(len(modes_to_run),modes_to_run.index(mode),modes_to_run,output)
      exit()
  except Exception as e:
    x += 1
    print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,mode,modes_to_run,output,KEYS,a)
    else:
      print "Key " + str(x-1) + " Has filled up or another error has occured. Any partial data from google can be downloaded below.<br>\n"
      finish_line(len(modes_to_run),modes_to_run.index(mode),modes_to_run,output)
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
    print "ELSE"
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
def go_to_corner(PointA,radius,numberofpairs,btwnmarks,currentdict,Dictkey):
    global square_count
    square_count += 1
    PointB = [0,0]
   # PointB[0] = incrementlat(0,distance,PointA[0],distlat(PointA[0]))
   # PointB[1] = decrementlon(0,distance,PointA[1],distanceindegree(PointA[1],PointA[0]))
    PointB[0] = PointA[0]
    PointB[1] = PointA[1]
  #  lat1 = incrementlat(-180,.125/4,lat1,distlat(lat1)) 
    circular(PointB[0],PointB[1],numberofpairs,btwnmarks,currentdict,Dictkey)
def singlebearingupdate(PointA,radius,numberofpairs,btwnmarks,currentdict,Dictkey,bearing):
    global square_count
    square_count += 1
    PointB = [0,0]
   # PointB[0] = incrementlat(0,distance,PointA[0],distlat(PointA[0]))
   # PointB[1] = decrementlon(0,distance,PointA[1],distanceindegree(PointA[1],PointA[0]))
    PointB[0] = PointA[0]
    PointB[1] = PointA[1]
  #  lat1 = incrementlat(-180,.125/4,lat1,distlat(lat1)) 
    currentdict[bearing] = circularsingle(PointB[0],PointB[1],numberofpairs,btwnmarks,currentdict,Dictkey,bearing)
    currentdict[bearing] = currentdict[bearing][numberofpairs:]
    print "PAIRS:" + str(numberofpairs)

    return currentdict
def distlat(lat1):
  if (lat1 < 0):
    return latnumbers[int(str(lat1[1:]).split('.')[0])]
  else:
    return latnumbers[int(str(lat1).split('.')[0])]
def incrementlat(currentbearing,a,lat1,distance):
    #print "DIST: " + str(distance)
    x = .1
    while(float(distance/x) > a + .01 or float(distance/x) < a - .01):
    #   print float(distance/x)
        x += .001
    #print "X : " + str(x)
    #print "LAT INC: " + str(float(float(lat1) + float( float(1.000/float(x)) * math.cos(math.radians(currentbearing)))))
    return float(float(lat1) + float( float(1.000/float(x)) * math.cos(math.radians(currentbearing))))

def incrementlon(currentbearing,a,lon1,distance):
#   print "DIST: " + str(distance)
    x = .1
    while(float(distance/x) > a + .01 or float(distance/x) <  a - .01 ):
    #   print float(distance/x)
        x += .001
    #print "X : " + str(x)
    #print "LONG INC: " + str(float(float(lon1) + float( float(1.000/float(x)) * math.sin(math.radians(currentbearing)))))
    return float(float(lon1) + float(float(1.000/float(x)) * math.sin(math.radians(currentbearing))))

def decrementlat(currentbearing,a,lat1,distance):
    #print "DIST: " + str(distance)
    x = .1
    while(float(distance/x) > a + .01 or float(distance/x) <  a - .01):
    #   print float(distance/x)
        x += .001
    return float(float(lat1) - float( float(1.000/float(x)) * math.cos(math.radians(currentbearing))))

def decrementlon(currentbearing,a,lon1,distance):
    #print "DIST: " + str(distance)
    x = .1
    while(float(distance/x) > a + .01 or float(distance/x) <  a - .01 ):
    #   print float(distance/x)
        x += .001
    return float(float(lon1) - float(float(1.000/float(x)) * math.sin(math.radians(currentbearing))))


def distanceindegree(lon1,latitude):
  if (lat1 < 0):
    return longnumbers[int(str(latitude[1:]).split('.')[0])]
  else:
    return longnumbers[int(str(latitude).split('.')[0])]

def circular(lat1,lon1,numberofpairs,btwnmarks,currentdict,Dictkey):
    originallong = lon1
    originallat = lat1
    y = 1
    x = 0
    global square_count
    
    firstlat = lat1
    firstlon = lon1
    degrees = 0
    print str(lat1) + "," + str(lon1)

    while (degrees <= 90):
      lat1 = incrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
      print str(lat1) + "," + str(lon1)
      if (x == numberofpairs):
        degrees += 11.25
        x = 0
        lat1 = firstlat
        lon1 = firstlon
 #   degrees = degrees - 15
    while (degrees >= 90 and degrees < 180 ):
      lat1 = decrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
      print str(lat1) + "," + str(lon1)
      if (x == numberofpairs):
        degrees += 11.25
        lat1 = firstlat
        lon1 = firstlon
        x = 0
   # degrees = degrees - 15
   # print "DONE"
    while (degrees >= 180 and degrees <= 270):
      lat1 = incrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
      print str(lat1) + "," + str(lon1)
      if (x == numberofpairs):
        degrees += 11.25
        x = 0
        lat1 = firstlat
        lon1 = firstlon
  #  degrees = degrees - 15
    while (degrees >= 270 and degrees <= 360):
      lat1 = decrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
      print str(lat1) + "," + str(lon1)
      if (x == numberofpairs):
        degrees += 11.25
        x = 0        
        lat1 = firstlat
        lon1 = firstlon
    lastlat = lat1
    lastlon = lon1
    distance = get_distance(firstlat,firstlon,lastlat,lastlon) * 0.621371
    for key, value in currentdict.iteritems():
      print key,value    
def circularsingle(lat1,lon1,count,btwnmarks,currentdict,Dictkey,degrees):
    originallong = lon1
    originallat = lat1
    y = 1
    x = 0
    global square_count
    
    firstlat = lat1
    firstlon = lon1
   # print str(lat1) + "," + str(lon1)

    while (degrees <= 90):
      lat1 = incrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
   #   print str(lat1) + "," + str(lon1)
      if (x == count):
        return currentdict[degrees]
    while (degrees >= 90 and degrees < 180 ):
      lat1 = decrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
  #    print str(lat1) + "," + str(lon1)
      if (x == count):
        return currentdict[degrees]
   # degrees = degrees - 15
   # print "DONE"
    while (degrees >= 180 and degrees <= 270):
      lat1 = incrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
   #   print str(lat1) + "," + str(lon1)
      if (x == count):
        return currentdict[degrees]
  #  degrees = degrees - 15
    while (degrees >= 270 and degrees <= 360):
      lat1 = decrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      currentdict[degrees].append(str(round(lat1,6)) + "," + str(round(lon1,6)))
    #  print str(lat1) + "," + str(lon1)
      if (x == count):
        return currentdict[degrees]
    lastlat = lat1
    lastlon = lon1
    distance = get_distance(firstlat,firstlon,lastlat,lastlon) * 0.621371
    for key, value in currentdict.iteritems() :
      print key,value    
    return currentdict[bearing]

def tomyratio(numofmeters):
    numofkm = float(numofmeters) * 4.38888888889 * .001
    #print "NUM: " + str(numofkm)
    return numofkm

def get_dist(lat1,lon1,lat2,lon2): 
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance

def make_header(fname,output):
    for line in fname:
        output.write("inputlat,inputlong,time,")
    output.write("\n")

output = open(sys.argv[2],"w")
#print sys.argv[1]
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
modes_to_run = [sys.argv[9],sys.argv[10],sys.argv[11],sys.argv[12]]

key_count = 0
KEYS=[API_KEY_INPUT,KEY2,KEY3,KEY4,KEY5]
for key in KEYS:
  if(key != "0"):
    key_count += 1
#Compile all modes to see which are to be run (ORDER: Driving,Walking,Biking,Transit)

address = ""
traffic_models_list = []
destination = ""
#print "<br>LINE COUNT: " + str(file_len(str(sys.argv[1])))

counter=0
y=0
#client(API_KEY_INPUT)
make_header(testiter,output)
print str(API_KEY_INPUT)
client(API_KEY_INPUT)

for line in inputfile:
  i=0
  counter += 1
  if(counter>=2490):
      print "Key #" + str(y) + " Reached its limit.<br>"
      counter=0
      y += 1
      if(KEYS[x] == '0'):
        print "END of Keys. Partial data download is available below.\n"
        exit()
      API_KEY_INPUT = KEYS[x]
      x+=1

  time_to_leave = check_timetoleave(line.strip().split(","))
  PointA = (float(line.strip().split(",")[0]),float(line.strip().split(",")[1]))
  currentname = {}
  currentname = makekeys(currentname,11.25)
  go_to_corner(PointA,1,1,.5,currentname,0)   #This gets 3 pairs that are 10,20, and 30 miles from origin on bearing
  iterate_counter=0
  thelist = my_algorithm(currentname,.5,1,500,PointA,"driving",["driving"],output,KEYS)   #Now we can start to analyze
  print "FINAL LIST WAS: " + str(cleanprint(thelist,600))
 #10 miles out with 1 mile increments finding times that are at x seconds
