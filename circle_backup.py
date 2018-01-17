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
def calculate_hypotenuse(a,b):
  return sqrt(a**2 + b**2)
def short_or_full(directions):
  if "short_name" in directions.keys():
    return directions['short_name']
  else:
    return directions['name']
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
def try_except(gmaps12,address,destination,time_to_leave,output,KEYS,a,Order_list):
  global gmaps
  global x
  try:
    global directions11
    directions11 = gmaps.directions(address,destination,departure_time=leaving(time_to_leave),mode='transit',units="metric",transit_mode=Order_list,alternatives="true")
  except googlemaps.exceptions.ApiError as e:
    print e
    x += 1
    print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,time_to_leave,output,KEYS,a,Order_list)
    else:
      print "Key Has filled up or another error has occured. Any partial data from google can be downloaded below.<br>\n"
      finish_line(1,0,output)
      exit()
  except Exception as e:
    print e
    x += 1
    print "Key " + str(x-2) + " Has filled up or another error has occured.<br>\n"
    if(got_more_keys(KEYS,x) != False):
      client(got_more_keys(KEYS,x))
      try_except(gmaps,address,destination,time_to_leave,output,KEYS,a,Order_list)
    else:
      print "Key " + str(x-1) + " Has filled up or another error has occured. Any partial data from google can be downloaded below.<br>\n"
      finish_line(1,0,output)
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

    distance = R * c
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

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1) * math.cos(lat2) * math.cos(diffLong))
    initial_bearing = math.atan2(x, y)
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = initial_bearing
    return compass_bearing

def numofiterations(square_count): #Actually +1, for square 1 we have 3 points inside the square tested
    return 2 + (3 * (square_count-1)) 
def go_to_corner(PointA,radius,squares,distance):
    global square_count
    square_count += 1
    PointB = [0,0]
   # PointB[0] = incrementlat(0,distance,PointA[0],distlat(PointA[0]))
   # PointB[1] = decrementlon(0,distance,PointA[1],distanceindegree(PointA[1],PointA[0]))
    PointB[0] = PointA[0]
    PointB[1] = PointA[1]
  #  lat1 = incrementlat(-180,.125/4,lat1,distlat(lat1)) 
    circular(PointB[0],PointB[1],squares,distance)
def distlat(lat1):
    return float(68.703  + (float(lat1) * 0.00782222222))
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
    #print "Long Dist: " + str(abs(float(math.cos(math.radians(float(latitude))) * 69.172)))
    return abs(float(math.cos(float(math.radians(float(latitude)))) * 69.172))

def circular(lat1,lon1,count,btwnmarks):
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
       # print "WE AT here " + str(degrees)
      lat1 = incrementlat(degrees,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(degrees,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      print str(lat1) + "," + str(lon1)
      if (x == count):
        degrees += 15
        x = 0
        lat1 = firstlat
        lon1 = firstlon
 #   print "NEW LOOP " + str(degrees)
    degrees = degrees - 15
    while (degrees >= 90 and degrees <= 180):
      lat1 = decrementlat(degrees-90,float(btwnmarks),lat1,distlat(lat1))
      lon1 = decrementlon(degrees-90,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      print str(lat1) + "," + str(lon1)
      if (x == count):
        degrees += 15
        lat1 = firstlat
        lon1 = firstlon
        x = 0
#    print "new loop2"
    degrees = degrees - 15
   # print "DONE"
    while (degrees >= 180 and degrees <= 270):
      lat1 = decrementlat(degrees-90,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(degrees-90,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      print str(lat1) + "," + str(lon1)
      if (x == count):
        degrees += 15
        x = 0
        lat1 = firstlat
        lon1 = firstlon
    degrees = degrees - 15
 #   print 'BLAH ' + str(degrees)
    while (degrees >= 270 and degrees <= 360):
      lat1 = incrementlat(degrees+180,float(btwnmarks),lat1,distlat(lat1))
      lon1 = incrementlon(degrees+180,float(btwnmarks),lon1,distanceindegree(lon1,lat1)) #Go directly .05 miles to the right and query
      x += 1
      print str(lat1) + "," + str(lon1)
      if (x == count):
        degrees += 15
        x = 0        
        lat1 = firstlat
        lon1 = firstlon
    lastlat = lat1
    lastlon = lon1
    distance = get_distance(firstlat,firstlon,lastlat,lastlon) * 0.621371
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

for line in inputfile:
  print line
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
  print "HERE"
  output.write(address+","+destination+",")
  output.write(time.strftime('%H:%M:%S', time.localtime(leaving(time_to_leave))))
  iterate_counter=0
  PointA = go_to_corner(PointA,1,5,.125)
