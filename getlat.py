# -*- coding: utf-8 -*-
# @Author: Miclain Keffeler
# @Date:   2017-12-19 09:32:43
# @Last Modified by:   Miclain Keffeler
# @Last Modified time: 2018-01-18 18:37:28
import math
import simplekml
from polystuff import readPoly,polyStats

def makekeys(storage,increment):
	for k in degreelist(increment):
		storage[k] = []
	return storage
def degreelist(number):
	mylist = []
	counter = 0
	while counter <= 360:
		mylist.append(counter)
		counter += number
	return mylist
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

def checknumbers(thedict,thepair,thetime):
	pairtime = ""
	for key in thedict:
		pairtime = thedict[key].split("/")
		if len(pairtime[0]) < 5:
			if (str(pairtime[1]) == str(thepair)):	
				if (str(thetime) != str(pairtime[0])):
					print "bearing: " + str(key) + " pair: " + str(pairtime[1]) + " time was: " + str(pairtime[0]) + " now is " + str(thetime)
		else:
			if (str(pairtime[0]) == str(thepair)):	
				if (str(thetime) != str(pairtime[1])):
					print "bearing: " + str(key) + " pair: " + str(pairtime[0]) + " time was: " + str(pairtime[1]) + " now is " + str(thetime)

lastrun = {0: '41.047526,-73.990548/2212', 135: '40.962568,-74.257683/2187', 270: '40.757461,-74.279822/2129', 15: '41.013693,-73.900913/2123', 150: '40.987156,-74.16327/2223', 285: '40.709271,-73.75631/2296', 30: '40.987156,-73.817826/2321', 165: '40.972997,-74.065767/2112', 300: '40.684945,-73.826962/2201', 45: '40.860015,-73.85698/2250', 180: '40.659492,-74.039437/2216', 315: '40.680415,-73.958151/2217', 60: '40.850584,-73.780476/2196', 195: '40.61737,-74.039437/2290', 330: '40.719506,-73.743892/2213', 75: '40.799701,-73.785231/2263', 210: '40.691625,-73.873301/2128', 345: '40.659485,-73.82111/2250', 90: '40.757461,-73.701274/2194', 225: '40.674512,-73.909691/2306', 360: '40.683313,-73.871979/2273', 105: '40.832535,-74.355461/2263', 240: '40.64623,-74.24147/2134', 120: '40.902494,-74.31772/2215', 255: '40.682387,-74.355461/2272'}
def cleanprint(thedict,goaltime,output):
  counter = 0
  pairtime = ""
  for key in thedict:
    pairtime = thedict[key].split("/")
    if len(pairtime[0]) < 5:
      counter += 1
      print "OFFFFFF: " + str(pairtime[1]) + " || " + str(pairtime[0])
      output.write('"' + pairtime[1]+'",')
    else:
       output.write('"' + pairtime[0]+'",')
 # print str(counter) + " Were off by more than +- 5%"
 # printoffbypercents(thedict,goaltime)
def printoffbypercents(thedict,goaltime):
  print "PERCENT OFF BY"
  pairtime = ""
  for key in thedict:
    pairtime = thedict[key].split("/")
    if len(pairtime[0]) < 5:
      print str(float(float(float(pairtime[0])/goaltime) * 100))  + "/" + str(pairtime[0]) + "/" + str(key)
    else:
      print str(float(float(float(pairtime[1])/goaltime) * 100)) + "/" + str(pairtime[1]) + "/" + str(key)
def cleanlist(thelist):
  for item in thelist:
    print item

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
          return v[1:]
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
   #   print "1"
      first.append(list(str(str(thelist[key]).split("/")[0]).split(",")))
    if 180 >= int(key) >= 91:
  #    print "2"
      second.append(list(str(str(thelist[key]).split("/")[0]).split(",")))
    if 270 >= int(key) >= 181:
  #    print "3"
      third.append(list(str(str(thelist[key]).split("/")[0]).split(",")))
    if 359 >= int(key) >= 271:
  #    print "4"
      fourth.append(list(str(str(thelist[key]).split("/")[0]).split(",")))
  if (len(second) == 0):
    first.insert(0,third[len(third)-2])
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
      print "No Item was far enough. Exiting."
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
      print "No Item was far enough. Exiting."
      exit(1)
