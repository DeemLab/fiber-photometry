from tdt import read_block
import numpy as np
import os


def extract_name_streams(blockname, tankdir, filename1, filename2, trimstart, trimend):
	for block in blockname:
		full_path = os.path.join(tankdir, block)
		data = read_block(full_path)
		fields = list(data.streams.keys())
		if len(fields) < 4 or (len(fields) == 4 and (filename1 is None and filename2 is not None)):
			GCAMP = fields[0]
			ISOS = fields[1]
			num = 1;
		elif len(fields) == 4 and (filename1 is not None and filename2 is not None):
			GCAMP = fields[2]
			ISOS = fields[3]
			num = 2;
		elif len(fields) == 4 and (filename1 is not None and filename2 is None):
			GCAMP = fields[2]
			ISOS = fields[3]
			num = 1;
		pre_process(GCAMP, ISOS, num, filename1, filename2, data, trimstart, trimend)


def pre_process(GCAMP, ISOS, num, filename1, filename2, data, trimstart, trimend):
	files = [filename1, filename2]
	for i in range(0, num):
		file = files[i]
		fs = data.streams[GCAMP.title()].fs
		start = trimstart * fs
		print(start)
		stop = trimend * fs
		time = np.arange(start=1, stop=len(data.streams[GCAMP.title()].data), step=1)/data.streams[GCAMP.title()].fs
		data_GCAMP = np.array(data.streams[GCAMP.title()].data)
		data_ISOS = np.array(data.streams[GCAMP.title()].data)
		#Signal470 = data_GCAMP[find_nearest(data_GCAMP, start):-stop]
		#Signal405 = data.streams[ISOS.title()].data[start:-stop]
		#trimtime = time[start:-stop]
		idf = find_nearest(data_GCAMP, data_GCAMP[len(data_GCAMP) - 1] - stop)
		array_length = len(data_GCAMP)
		last_element = data_GCAMP[array_length - 1]
		print(last_element)
		print(idf)

def find_nearest(array, value):
    ''' Find nearest value is an array '''
    idx = (np.abs(array-value)).argmin()
    return idx

def main():
	tankdir = "/Volumes/GoogleDrive/Shared drives/Schwartz/Data/Fiber Photometry Experiments/Faber DMH Project/Circadian HFHS Presentation"
	n = 16
	savedata = "/Volumes/GoogleDrive/Shared drives/Schwartz/Data/Fiber Photometry Experiments/Faber DMH Project/Circadian HFHS Presentation/Data/test2"
	savefigs = "/Volumes/GoogleDrive/Shared drives/Schwartz/Data/Fiber Photometry Experiments/Faber DMH Project/Circadian HFHS Presentation/Figures/test2"
	trimstart = 20
	trimend = 20
	blockname = ['DMH-3-201108-123527']
	blockname1 = ['DMH-3-201108-123527', 'DMH-4-201108-132008', 'DMH-6-201108-140804', 'DMH-7-201108-153449',
				  'DMH-3-201110-201611', 'DMH-4-201110-210026', 'DMH-6-201110-214402', 'DMH-7-201110-222751']
	filename1 = ['ZT7-DMH3', 'ZT7-DMH4', 'ZT7-DMH6', 'ZT7-DMH7', 'ZT14-DMH3', 'ZT14-DMH4', 'ZT14-DMH6', 'ZT14-DMH7']
	filename2 = None
	extract_name_streams(blockname, tankdir, filename1, filename2, trimstart, trimend)


if __name__ == "__main__":
	main()