#!/usr/bin/python3

"""
This script sets up a multithreaded process based on 
executing system's operating system.

Last modified: Myles Mcleroy, 2/3/2019
"""

from __future__ import print_function

import multiprocessing
import os
import sys
import threading

from isochronescript import kickofffunc

class FuncThread(threading.Thread):
    """Function thread object"""
    def __init__(self, target, *args):
        self._target = target
        self._args = args
        threading.Thread.__init__(self)

    def run(self):
        self._target(*self._args)

def open_process(data, line_number, mode_count, trans_mode):
    """Opens a new process and records it"""
    args = []
    openprocesses = []
    for arg in sys.argv[1:]:
        args.append(arg)
        print(arg)
    args.append(data)

    openprocesses.append(os.getpid())
    kickofffunc(args[0], args[1], args[2], args[3], args[4], args[5],
                args[6], args[7], args[8], args[9], args[10], args[11],
                args[12], args[13], args[14], args[15], args[16], args[17],
                args[18], args[19], str(line_number), str(trans_mode))

def get_mode(count):
    """Returns transportation mode as a string literal"""
    if count == 0:
        return "driving"
    if count == 1:
        return "walking"
    if count == 2:
        return "bicycling"
    if count == 3:
        return "transit"
    return "invalid"

def tostring(args):
    """Converts command line arguments into a string literal"""
    message = ""
    for item in args:
        message += str(item) + " "
    return message

if __name__ == '__main__':
    processes = []

    os.chdir("output_isochrone")
    output = open(sys.argv[2], "w")
    all_modes = [sys.argv[9], sys.argv[10], sys.argv[11], sys.argv[12]]
    output.write("Slat,Slong,time,mode,#requested points,#calculated points,\
                  timeordist,area (m^2),points (lat,long)\n")
    output.close()

    os.chdir("../uploads_isochrone")
    inputfile = open(sys.argv[1], "r")
    os.chdir("..")

    mode_count = 0
    modes_to_run = []
    for entry in all_modes:
        if entry == "on":
            mode = get_mode(mode_count)
            modes_to_run.append(mode)
        mode_count += 1

    index = 0
    linenumber = 0
    thevals = sys.argv[1:]
    for line in inputfile:
        for mode in modes_to_run:
            p = multiprocessing.Process(
                target=open_process, args=(str(line.rstrip()), str(linenumber + 1),
                                           str(mode_count), str(mode)))
            p.start()
            processes.append(p)
            linenumber += 1
            index += 1

    inputfile.close()
