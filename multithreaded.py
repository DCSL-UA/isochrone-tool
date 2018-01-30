import threading
import sys
import os
import multiprocessing
import time
class FuncThread(threading.Thread):
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)
 
    def run(self):
        self._target(*self._args)
arr = []
storage = []
# Example usage
def someOtherFunc(data,linenumber,mode_count,mode):
 # print "DATA IS " + str(data)
#  print "PROCESS ID: " + str(os.getpid())
  if (str(linenumber) == "1"):
    os.system('python isochronescript.py ' + data + " " + str(linenumber)+ " " + str(mode))
  else:
    os.system('python isochronescript.py ' + data + " " + str(int(linenumber)) + " " + str(mode))
  
def get_mode(count):
  if(count == 0):
    return "driving"
  if(count == 1):
    return "walking"
  if(count == 2):
    return "bicycling"
  if(count == 3):
    return "transit"
def tostring(args):
   message = ""
   for item in args:
      message += str(item) + " "
   return message
if __name__ == '__main__':    
  output = open(sys.argv[2],"w")
  ##print sys.argv[1]
  output.write("Slat,Slong,time,mode,#requested points,#calculated points,timeordist,area (m^2),points (lat,long)\n")
  output.close()
  all_modes = [sys.argv[9],sys.argv[10],sys.argv[11],sys.argv[12]]
  inputfile = open((sys.argv[1]),"r")
  mode_count = 0
  modes_to_run = []
  for entry in all_modes:
    if(entry == "on"):
      mode = get_mode(mode_count)
      modes_to_run.append(mode)
    mode_count += 1
  linenumber = 0
  index = 0 
 # myzip = ZipFile('spam.zip', 'w+')
 # filename = str(str(sys.argv[2]).split("\\")[1]).split(".")[0]#These need to be changed based on either windows or mac (windows = \\, mac = /)

  thevals = sys.argv[1:]
  for line in inputfile:
    for mode in modes_to_run:
   #   print "START THREAD"
    #  while (len(arr) > 8):
    #    time.sleep(1)
    
      arr.append(multiprocessing.Process(target=someOtherFunc,args=(tostring(thevals)+'"' + str(line.rstrip()) + '"',str(linenumber+1),str(mode_count),str(mode))))
      arr[index].start()
      linenumber += 1
      index += 1

  inputfile.close()



