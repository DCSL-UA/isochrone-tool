# Google_DirectionsAPI_PointPicker
Given a single lat,long, this will generate radius of lat,long points a specified distance away and will then create a list of lat,longs that satisfies time or distance conditions (Directions API used to determine what distance and time to travel are) to be used in the creation of contour maps and more.

Issue was that the filesystem on Windows uses backslashes (which must be escaped) and Linux uses forward. Thus, I have to have these 2 separate branches. This has been resolved in this commit. It works when running the following command:

python multithreaded.py "try1.txt" "myruntodayfresh2.txt" -off AIzaSyA9VrtjosIim9RzG2fR5-1oy6_QfvipGDc 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32

try1.txt contains the input, myruntodayfresh2.txt is the output file name. 

Note, the PHP scripts that accompany this app will be appending uploads_isochrone and output_isochrone to try1.txt and myruntodayfresh2.txt, respectively. This functionality had to be changed so as to make these scripts agnostic of the OS. 
