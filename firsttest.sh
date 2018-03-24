#!/bin/bash

#
# This script calls the extract_apk.sh script many times in parallel
# for each of the sorted applications to unpack apk files and parse
# their contents.
#

python multithreaded.py "uploads_isochrone/testing1.txt" "output_isochrone/output1.txt" -off AIzaSyC3M-I5OJpzf5xFUWYH69IB_BZ2xU5t3rs 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32 > output1.txt
python multithreaded.py "uploads_isochrone/testing1.txt" "output_isochrone/output2.txt" -off AIzaSyCyn3sWd6YOVe9T7PiYeIWzP3l9aMcrhwA 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32 > output2.txt
python multithreaded.py "uploads_isochrone/testing1.txt" "output_isochrone/output3.txt" -off AIzaSyBHAZNH56BkFjQn0DeSd5NcAfdxxF4BhVU 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32 > output3.txt
python multithreaded.py "uploads_isochrone/testing1.txt" "output_isochrone/output4.txt" -off AIzaSyBlGF0c9WDFymECTZ15thY0WFOROdlUC5Q 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32 > output4.txt
python multithreaded.py "uploads_isochrone/testing1.txt" "output_isochrone/output5.txt" -off AIzaSyD_BC3mh_SBcCL2rk-Kg-L_8YJO9BKtfUE 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32 > output5.txt
python multithreaded.py "uploads_isochrone/testing1.txt" "output_isochrone/output6.txt" -off AIzaSyCHH3lA-fLaVulJvNvev_ZD7GAVOb76znM 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32 > output6.txt
python multithreaded.py "uploads_isochrone/testing1.txt" "output_isochrone/output7.txt" -off AIzaSyBKp0ojJsl_RpWHNoOHgbDI0K5QNKF_r1w 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32 > output7.txt
python multithreaded.py "uploads_isochrone/testing1.txt" "output_isochrone/output8.txt" -off AIzaSyBIXalcvqeaUmLK9J3Jx_6HFHb2BAlXKl8 0 0 0 0 on 0 0 0 0 0 0 0 on 500 32 > output8.txt