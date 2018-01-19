import math
import LatLon
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
def adjustdistance(a,b,c,d):
    x = 0 
    while (get_distance(a,b,c,d) > firstdistance + .5 or get_distance(a,b,c,d) < firstdistance - .5):
        if (get_distance(a,b,c,d) > firstdistance + .5):
            c = decrementlat(c,tomyratio(64000),distlat(c))
            x += 1
            if (x > 20):
                c = adjustbearing(x,c,d,a,b)
                x = 0
#           d = decrementlon(d,distanceindegree(d,c),tomyratio(64000))
#       else:
#           print "ELSE"
            c = incrementlat(c,tomyratio(1000),distlat(c))
#           d = incrementlon(d,distanceindegree(d,c),tomyratio(1000))
        distance = get_distance(a,b,c,d)
        print "Result:" + str(distance)
        print "Bearing: " + str(calculate_initial_compass_bearing((a,b),(c,d)))

def adjustbearing(x,c,d,a,b):
    while (calculate_initial_compass_bearing((a,b),(c,d)) < -0.5 or calculate_initial_compass_bearing((a,b),(c,d)) > 0.5):
        if (calculate_initial_compass_bearing((a,b),(c,d)) < 89.5):
            c = decrementlat(c,tomyratio(1000),distlat(c))
            d = incrementlon(d,distanceindegree(d,c),tomyratio(1000))
        else:
            c = incrementlat(c,tomyratio(1000),distlat(c))
            d = incrementlon(d,distanceindegree(d,c),tomyratio(1000))
        print " final Bearing: " + str(calculate_initial_compass_bearing((a,b),(c,d)))
        return (c,d)
#print str(calculate_initial_compass_bearing((40.757461,-73.990548),(40.757461, -73.990548)))
x = 46.765
#print str(calculate_initial_compass_bearing((40.757461,-73.990548),(40.757461, (-73 + x))))
x = 46.765 * 2
#print str(calculate_initial_compass_bearing((40.757461,-73.990548),(40.757461, (-73 + x))))
x = 46.765 * 3
#print str(calculate_initial_compass_bearing((40.757461,-73.990548),(40.757461, (-73 + x))))
x = 90
#print str(calculate_initial_compass_bearing((40.757461,-73.990548),(40.757461, (-73 + x))))
x = 30
##print str(calculate_initial_compass_bearing((40,-70),(40,-30)))
print str(calculate_initial_compass_bearing((0,0),(40,-50)))
print str(calculate_initial_compass_bearing((0,0),(40,-70)))
print str(calculate_initial_compass_bearing((0,0),(40,-90)))
print str(calculate_initial_compass_bearing((0,0),(40,-110)))

#palmyra = LatLon(Latitude(5.8833), Longitude(-162.0833))
#while(x < 46.8):
 #   print str(calculate_initial_compass_bearing((40.757461,-73.990548),(40.757461, (-73 + x))))
  #  x += .235
