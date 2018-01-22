import threading
import sys
import os
import multiprocessing

class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)
arr = ["t1","t2","t3"]
storage = []
# Example usage
def someOtherFunc(data,linenumber):
  print "DATA IS " + str(data)
  print "PROCESS ID: " + str(os.getpid())
  storage.append(os.system('python isochronescript.py ' + data + " " + str(linenumber)))
def tostring(args):
   message = ""
   for item in args:
      message += str(item) + " "
   return message
output = open(sys.argv[2],"w")
##print sys.argv[1]
output.write("Slat,Slong,time,mode,#requested points,#calculated points,timeordist,area (m^2),points (lat,long)\n")
output.close()
inputfile = open((sys.argv[1]),"r")
print "ARGS ARE: " + str(sys.argv)
linenumber = 0
thevals = sys.argv[1:]
for line in inputfile:
  linenumber += 1
  print "START THREAD"
  arr[linenumber] = multiprocessing.Process(target=someOtherFunc,args=(tostring(thevals)+'"' + str(line.rstrip()) + '"',str(linenumber),))
  arr[linenumber].start()

jobcount = linenumber
line = 0
