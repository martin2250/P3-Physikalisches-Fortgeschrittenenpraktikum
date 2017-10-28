#!/usr/bin/python
from __future__ import division, print_function
import sys
import os
import os.path
import struct
import numpy as np

# Martin Pittermann, October 2017
# searches for negative peaks in two (two channels) wavedump files
# finds peak of each channel in every waveform
# stores
# - power for both channels
# - time difference between the peak in channel0 and channel1
# - timestamp of trigger condition (optional, not enabled by default)


# check arguments
if len(sys.argv) < 2:
	print('usage: %s <folder> [options]'%sys.argv[0])
	print("""
folder structure:
<folder>
 |- wave0.dat
 |- wave1.dat

options:
trim_time <int>        | maximum number of seconds to save (default 400)
trim_samples <int>     | maximum number of samples to save (default 1e7)
box_car_size <int>     | number of samples to average for peak detection (default 10)
save_timestamp         | flag, include 'C' timestamp array
""")
	exit(1)

box_car_size = 10
trim_samples = int(1e7)	# limit maximum number of events to copy
trim_time = 400
save_timestamp = False

# read options
i = 2
while i < len(sys.argv):
	optn = sys.argv[i]
	val = None
	if (i + 1) < len(sys.argv):
		val = sys.argv[i + 1]

	if optn == 'trim_time':
		trim_time = float(val)
		i += 1
	elif optn == 'trim_samples':
		trim_samples = int(val)
		i += 1
	elif optn == 'box_car_size':
		box_car_size = int(val)
		i += 1
	elif optn == 'save_timestamp':
		save_timestamp = True

	i += 1
del i

# helper functions
def checkFile(filename, should_exist=True):
	if should_exist != os.path.isfile(filename):
		if should_exist:
			print('error: file %s does not exist'%filename)
		else:
			print('error: file %s exists'%filename)
		exit(1)

def readHeader(f):
	s = f.read(24)
	if len(s) != 24:
		return False, 0, 0
	event_size, boardID, pattern, channel, event_num, trigger_time = struct.unpack("<LLLLLL", s)

	return (
		int((event_size - 24)/2),	# number of 16-bit samples
		event_num,
		trigger_time)

# set up box-car-averaging filter for waveforms
filtermatrix = np.ones((box_car_size,))/box_car_size

def readData(f, sample_count):
	sample_count = int(sample_count)
	s = f.read(sample_count * 2)	# two bytes per sample
	if len(s) != (sample_count * 2):
		return False, 0, 0
	data = np.array(struct.unpack("<"+str(sample_count)+"H", s))	# read x uint16 values
	return np.convolve(data, filtermatrix, mode='valid')	# apply box-car-averaging

# prepare file paths
folder = sys.argv[1].rstrip('/')
wave0 = folder + '/wave0.dat'
wave1 = folder + '/wave1.dat'
outputfile = folder + '.npz'

# check input and output files
checkFile(outputfile, should_exist=False)
checkFile(wave0)
checkFile(wave1)

# prepare arrays
T = np.array([0], dtype=np.int16)	# time difference of peaks between channels (inside sample window) (in clock cycles (8ns ea.))
E = np.array([[0, 0]], dtype=np.uint16)	# energy of event (relative to first 10 samples)
C = np.array([0], dtype=np.uint64)	# timestamp of trigger condition

# set up
expandlength = int(1e5)	# new entries added to arrays when arrays are full, improves performance compared to adding entries individually

# open files
filesize = os.stat(wave0).st_size
if filesize != os.stat(wave1).st_size:
	print('error: file sizes don\'t match')
	exit(1)

f1 = open(wave0, "rb")
f2 = open(wave1, "rb")

# step through files
index = -1	# waveform count
time_offset = 0	# compensate for trigger time rollover
while index < trim_samples:
	index += 1

	# report progress only every X samples
	if (index % 1000) == 0:
		progress = 100 * f1.tell()/filesize
		sys.stdout.write("\r Progress: %0.1f%%"%progress)

	# read headers
	scount, evntnum, trigger_time = readHeader(f1)
	scount2, evntnum2, trigger_time2 = readHeader(f2)

	# check for EOF
	if not scount or not scount2:
		break

	# compare headers
	if (scount, evntnum, trigger_time) != (scount2, evntnum2, trigger_time2):
		print('error: waveforms #%d: headers don\'t match'%index)
		exit(1)

	# read data: record = Byte length of the waveform event (16 bit per sample) + 24 (6*4Byte) header length
	data1 = readData(f1, scount)
	data2 = readData(f2, scount)

	# check for EOF
	if data1 is int or data2 is int:
		print('error: waveforms #%d: unexpected end of file')
		exit(1)

	# get average of fist X samplse to compare peak against
	baseline1 = np.mean(data1[0:10])
	baseline2 = np.mean(data2[0:10])

	# find index of (negative) peak
	amin1 = np.argmin(data1)
	amin2 = np.argmin(data2)

	# expand arrays if necessary
	if (index % expandlength) == 0:
		T = np.append(T, np.zeros(expandlength, dtype=np.uint16))
		E = np.append(E, np.zeros((expandlength, 2), dtype=np.uint16), axis=0)
		C = np.append(C, np.zeros(expandlength, dtype=np.uint64))

	# compensate for trigger time rollover
	if index > 0 and (trigger_time + time_offset) < C[index - 1]:
		time_offset += int(2**31)

	# store data
	T[index] = amin2 - amin1
	E[index][0] = baseline1 - data1[amin1]
	E[index][1] = baseline2 - data2[amin2]
	C[index] = trigger_time + time_offset

f1.close()
f2.close()


# convert C from clock ticks (8ns) to microseconds
C = C * 0.008
print('\nread %d waveforms in %0.2f seconds'%(index, C[index - 1]*1e-6))

# trim after [trim_time] seconds
endindex = 0
while endindex < index and C[endindex] < (trim_time * 1e6):
	endindex += 1

print('%d waveforms recorded in first %d seconds'%(endindex, trim_time))

if endindex == index:
	print('------------------------------------------------')
	print('| WARNING: recording is shorter than trim_time |')
	print('|', folder, '|')
	print('------------------------------------------------')

# trim excess entries
E = E[0:endindex]
T = T[0:endindex]
C = C[0:endindex]

print('writing output to %s'%outputfile)

if save_timestamp:
	np.savez_compressed(outputfile, power = E, time_delta = T, capture_time = C)
else:
	np.savez_compressed(outputfile, power = E, time_delta = T)
