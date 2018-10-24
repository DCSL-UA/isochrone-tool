# Google_DirectionsAPI_PointPicker
Given a single lat,long, this will generate radius of lat,long points a specified distance away and will then create a list of lat,longs that satisfies time or distance conditions (Directions API used to determine what distance and time to travel are) to be used in the creation of contour maps and more.


On a Mac, I can run python multithreaded.py "uploads_isochrone/try1.txt" "output_isochrone/output3.txt" -off AIzaSyA9VrtjosIim9RzG2fR5-1oy6_QfvipGDc 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32


and it will work. Issue is that the filesystem on Windows uses backslashes (which must be escaped) and Linux uses forward. Thus, I have to have these 2 separate branches. 
