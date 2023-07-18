# LPR_CE4
Workflow for data selection of GPR data from Chang'E-4 explorer 

LPR data from Cheng'e 4 mission are freely avaiable at http://moon.bao.ac.cn/searchOrder_dataSearchData.search . 

We used raw data at the 500MHz, named LPR_2B.
We structure a workflow to open pds4 format and select only the traces that are useful for the study.

The rover performs different tasks, and it stops often to acquire other data: due to an error in the positioning system -or in the reading of the binary file- velocity and position does not help in understanding when the rover moves or not. 

To avoid this we made a workflow which is able to select when the rover is moving or not. 

Data are read using pds4_tools package by python: this file can be read only with a version <= 0.71 which can be downloaded from https://pdssbn.astro.umd.edu/toolsrc/readpds_python/0.71/
You can find the zipped version in this repository

In raw data there are a lot of horizontal lines, which should be linked period in which the rover stops.

We tested different ways to select the parts of interest. After extensive tests we propose this workflow:

	0: open pds4 structure and select LPR data
	1: cut dataset [300:, :]
	2: apply a Sobel filter in x direction with a kernel size of 5.
	3: apply a median filter 
	4: sum the absolute values of the filtered traces on time axis
	5: select values in a window that are over threshold value
		
    
1: due to the presence of very high values in the first 300 timesteps, so we excluded them

2: in order to suppres signals from the flat areas (marker of the rover not moving)

3: reduce spikes and random noise in the dataset. We can see this in Fig. 1B.

4: once the dataset is filtered, most of the information should be linked to the part of interest in the dataset. 
The other values have been lowered by the filtering processes.

5: we chose to use a moving window to avoid taking into account spickes due to other factors.

Exemple of the final result:

![final1](https://user-images.githubusercontent.com/52165234/112841512-d9500800-90a0-11eb-978c-85a3b32dd6b1.png)
