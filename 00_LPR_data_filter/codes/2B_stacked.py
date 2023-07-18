import matplotlib.pyplot as plt
from scipy import ndimage
from os import listdir
from tqdm import tqdm
import numpy as np
import pds4_tools
import cv2
import sys
import os

# deactivate warning
import warnings
warnings.filterwarnings("ignore")
####
##### works only if pds4_tools.__version__=='0.71'
####
	
# run the program in the folder before folder data. Need to mkdir img in that folder
try:
    os.stat('img/')
except:
    os.mkdir('img/')  

#init data_2B for data and medf for interest extrapolation
# 2048 is read by the header .2BL and it is fixed for all LPR_2B files [time dims]
data_2B = np.zeros((0, 2048))
medf = np.zeros(0)
time = np.zeros((1, 0))



def rec_time(times):
	time_res = np.reshape(times, (times.shape[0]//6, 6))
	time_bs = time_res[:, :4].astype(np.float32)
	time_bms = time_res[:, 4:].astype(np.float32)
	time_s = np.sum([time_bs[:,i]*255**(3-i) for i in range(4)], axis=0)
	time_ms =np.sum([time_bms[:,i]*255**(1-i) for i in range(2)], axis=0)
	return time_s + time_ms/1000



#Define a function which takes a nparray of data [n traces, time dims] and a string with file name for save img -only if plot_var = True-
def id_inter(data, j, plot_var):
	# do not consider first 300 lines (too high values and transpose data 
	img = data.T[300:, :]
	# compute the derivative of the data in x direction with Sobel with a kernel size of 5
	# this should eliminate the horizonatal lines
	sobelx = cv2.Sobel(img, cv2.CV_64F, 1, 0, ksize=5)
	# denoise the sobelx with a median filter of size 5 
	# we need to reduce random noise for the next step
	med_denoised = ndimage.median_filter(sobelx, 5)
	# sum the absolute values of the denoised traces on time dims
	# we should have cancelled signals on death traces --> highest value on the real traces
	med = np.sum(np.abs(med_denoised), axis = 0)
	## define a moving window to avoid taking into account small portions with high values.
	## we want to take the signals only when it has a value highest than thres for window consecutive traces
	window = 25
	thres = 20000
	## init output vector as 0s
	medf = np.zeros(med.shape)
	## for each trace
	for i in range(med.shape[0] - window):
		## if all values are > thres
		if np.all(med[i : i + window] > thres):
			## replace 0 with 1 in the output vector
			medf[i : i + window] = 1
	# if plot == True plot Data and interest points and save to /img/
	if plot_var == True:
		plt.figure(figsize=[15, 10])
		plt.title('2B data_' + j)
		plt.subplot(211)
		plt.title('Data')
		plt.imshow(data.T, cmap = 'gray', vmin = -1, vmax = 1, aspect = 'auto')
		plt.subplot(212)
		plt.title('Interest extrapolation')
		plt.xlim(0, sobelx.shape[1])
		plt.xlabel('trace number')
		plt.ylabel('interest [0-1]')
		plt.plot(medf, 'r')
		plt.savefig('img/interest_' + j, dpi=300)
		plt.close()
	return medf

# define variable for plot save
plot_var = False
# check if pds4_tools.__version__=='0.71'
if pds4_tools.__version__== '0.71':
	print('Correct pds4_tools version: it should work!')
	# find all the files in current folder with 'L' at the end --> only files with header infos
	onlyfiles = ['data/' + f for f in listdir('data/') if f[-4: ] == '.2BL']
	# init a for append
	a = []
	# append to a the correct number of file [e.g. 0001] just once
	[a.append(onlyfiles[i][-10:-6]) for i in range(len(onlyfiles)) if onlyfiles[i][-10:-6] not in a]
	# sort a in order to get the correct order
	a.sort()
	print('Found: ' + np.str(len(a)) + ' files.') 
	if plot_var == True:
		print('Plot are saved in img/\nStart conversion...')
	else: 
		print('No plot saved!\nStart conversion...')
	# for each a [tqdm is just for progress bar]
	for j in tqdm(a): 
		# for each file with .2BL in the folder
		for name in onlyfiles:
			# if filename has the correct number and is the LPR-2B version of the data
			if name[-10:-6] == j and name[14:20] == 'LPR-2B':
					# read data structure with pds4_tools [no print]
					struct_2B = pds4_tools.pds4_read(name, quiet = True)
					# copy LPR data [in [0][27]] to a temp 
					data_2keep = struct_2B.structures[0][27]
					time_keep = rec_time(struct_2B.structures[0][1])
					# append to medf vector the new values computed with id_inter on the temp
					medf_keep =  id_inter(data_2keep, j, plot_var)
					medf = np.append(medf, medf_keep, axis=0)
					# append temp to file matrix
					data_2B = np.append(data_2B, data_2keep[np.where(medf_keep==1)[0], :], axis=0)
					time = np.append(time, time_keep[np.where(medf_keep==1)[0]])
else:
	sys.exit('Wrong pds4_tools version installed!\nExpected: 0.71, but found: ' + pds4_tools.__version__)
					

print(data_2B.shape)
print(time.shape)

np.save('time_cut', time)

# fileter data according to medf
data_filtered = data_2B
# print infos
print('Data coverted!\n-------------------------\nx dims of: ' + np.str(data_filtered.shape[0]), ' samples \nt dims of: ' + np.str(data_filtered.shape[1])+' samples \nSampling rate = 0.3125ns\n-------------------------\n')
# plot and save filtered matrix
plt.figure(figsize=[20,15])
plt.title('filtered matrix')
plt.imshow(data_filtered.T, cmap = 'gray', vmin = -10, vmax = 10, aspect = 'auto')
plt.savefig('final_stacked', dpi=300)
plt.clf()

# name of the final plot
name = 'stacked_int32'
print('Saving data as ' + name)
# transpose data and save to stacked_int16 as int16 binary file
keep = data_filtered
keep.astype('int32').tofile(name)



