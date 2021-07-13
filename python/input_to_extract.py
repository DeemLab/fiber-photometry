from tdt import read_block
import numpy as np
import matplotlib.pyplot as plt
import os
import math
import statistics


def extract_name_streams(blockname, tankdir, filename1, filename2, trimstart, trimend):
	for block in blockname:
		idx = blockname.index(block)
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
		process(idx, GCAMP, ISOS, num, filename1, filename2, data, trimstart, trimend)


def process(idx, GCAMP, ISOS, num, filename1, filename2, data, trimstart, trimend):
	file1 = filename1[idx]

	if num > 1:
		file2 = filename2[idx]
		files = [file1, file2]
	else:
		files = [file1]

	for i in range(0, num):
		file = files[i]

		# trim
		fs = data.streams[GCAMP.title()].fs
		start = int(math.floor(trimstart * fs))
		stop = int(math.ceil(trimend * fs))
		time = np.arange(start=1, stop=len(data.streams[GCAMP.title()].data)+1, step=1)/data.streams[GCAMP.title()].fs
		data_GCAMP = np.array(data.streams[GCAMP.title()].data)
		data_ISOS = np.array(data.streams[ISOS.title()].data)
		Signal465 = data_GCAMP[start:-stop]
		Signal405 = data_ISOS[start:-stop]
		trimtime = time[start:-stop]

		# downsample
		N = fs
		arr_GCAMP = (np.arange(start = 1, stop = len(Signal465)-N+2, step = N)).astype(int)
		down_GCAMP = [statistics.mean(Signal465[i:round(i+N-1)]) for i in arr_GCAMP]
		arr_ISOS = (np.arange(start=1, stop=len(Signal405) - N + 2, step=N)).astype(int)
		down_ISOS = [statistics.mean(Signal405[i:round(i + N - 1)]) for i in arr_ISOS]

		downtime = trimtime[0::round(N)]
		downt = downtime[0:len(down_GCAMP)]

		# smooth
		smooth_win = 10
		smooth_GCAMP = moving_average(down_GCAMP, smooth_win)
		smooth_ISOS = moving_average(down_ISOS, smooth_win)

		# fit and calculate dff
		fit_data = np.polyfit(smooth_ISOS, smooth_GCAMP, 1)
		fit_ISOS = np.multiply(fit_data[0], smooth_ISOS) + fit_data[1]
		dF = smooth_GCAMP-fit_ISOS
		dFF = 100*dF/fit_ISOS

		# plot
		fig = plt.figure(figsize=(20, 12))
		ax = fig.add_subplot(411)
		p1, = ax.plot(time, data.streams[GCAMP.title()].data, linewidth=2,
					   color='green', label='GCaMP')
		p2, = ax.plot(time, data.streams[ISOS.title()].data, linewidth=2,
					  color='dodgerblue', label='Isosbestic')
		ax.set_xlabel('Time (s)')
		ax.set_ylabel('mV')
		ax.set_title('Raw Signals ' + str(file))
		ax.legend(handles=[p1, p2], loc='upper right')
		ax.set_xlim([time[0], time[len(time)-1]])

		ax2 = fig.add_subplot(412)
		p3, = ax2.plot(downt, smooth_GCAMP, linewidth=2,
					  color='green', label='Processed GCaMP')
		p4, = ax2.plot(downt, smooth_ISOS, linewidth=2,
					  color='dodgerblue', label='Processed Isosbestic')
		p5, = ax2.plot(downt, fit_ISOS, linewidth=2,
					   color='dodgerblue', label='Fit Isosbestic')
		ax2.set_xlabel('Time (s)')
		ax2.set_ylabel('mV')
		ax2.set_title('Smoothed, Fit and Aligned Signals ' + str(file))
		ax2.legend(handles=[p3, p4, p5], loc='upper right')
		ax2.set_xlim([downt[0], len(downt)])

		ax3 = fig.add_subplot(413)
		p6, = ax3.plot(downt, dF, linewidth=2,
					   color='black', label='Baseline Corrected GCaMP')
		ax3.set_xlabel('Time (s)')
		ax3.set_ylabel(r'$\Delta$mV')
		ax3.set_title('Subtracted Signal ' + str(file))
		ax3.legend(handles=[p6], loc='upper right')
		ax3.set_xlim([downt[0], len(downt)])

		ax4 = fig.add_subplot(414)
		ax4.plot(downt, dFF, linewidth=2,
					   color='green')
		ax4.set_xlabel('Time (s)')
		ax4.set_ylabel(r'$\Delta$F/F (%)')
		ax4.set_title(r'$\Delta$F/F, ' + str(file))
		ax4.set_xlim([downt[0], len(downt)])

		fig.suptitle('Data Processing ' + str(file), fontsize=16)
		fig.tight_layout()
		plt.savefig(str(file) + '.png')

		# plot just dFF
		fig2 = plt.figure(figsize=(20, 12))
		ax = fig2.add_subplot(211)
		ax.plot(downt, dFF, linewidth=2,
					   color='green')
		ax.set_xlabel('Time (s)')
		ax.set_ylabel(r'$\Delta$F/F (%)')
		ax.set_title(r'$\Delta$F/F, ' + str(file))
		ax.set_xlim([downt[0], len(downt)])

		fig2.tight_layout()
		plt.savefig('dFF_' + str(file) + '.png')


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same') / w


def main():
	tankdir = "/Volumes/GoogleDrive/Shared drives/Schwartz/Data/Fiber Photometry Experiments/Faber DMH Project/Circadian HFHS Presentation"
	trimstart = 30
	trimend = 30
	blockname = ['DMH-3-201108-123527', 'DMH-4-201108-132008', 'DMH-6-201108-140804', 'DMH-7-201108-153449',
				  'DMH-3-201110-201611', 'DMH-4-201110-210026', 'DMH-6-201110-214402', 'DMH-7-201110-222751']
	filename1 = ['ZT7-DMH3', 'ZT7-DMH4', 'ZT7-DMH6', 'ZT7-DMH7', 'ZT14-DMH3', 'ZT14-DMH4', 'ZT14-DMH6', 'ZT14-DMH7']
	filename2 = []
	extract_name_streams(blockname, tankdir, filename1, filename2, trimstart, trimend)


if __name__ == "__main__":
	main()
