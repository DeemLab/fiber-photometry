from tdt import read_block
import numpy as np
import matplotlib.pyplot as plt
import os
import statistics


def extract_name_streams(blocknames, tankdir, filenames, trimstart, trimend):
	for block in blocknames:
		full_path = os.path.join(tankdir, block)
		data = read_block(full_path)
		fields = list(data.streams.keys())
		files = filenames.get(block)
		chars = []
		GCAMP_list = []
		ISOS_list = []
		# identify signal names
		for field in fields:
			last_char = field[-1]
			if last_char not in chars and (last_char == "A" or last_char == "C" or last_char == "E" or last_char == "G"):
				if ("_470A" in fields):
					GCAMP = "_470A"
					ISOS = "_405A"
					GCAMP_list.append(GCAMP)
					ISOS_list.append(ISOS)
				else:
					chars.append(last_char)
					GCAMP = "_465" + last_char
					GCAMP_list.append(GCAMP)
					ISOS = "_405" + last_char
					ISOS_list.append(ISOS)
		process(GCAMP_list, ISOS_list, files, data, trimstart, trimend)


def process(GCAMP_list, ISOS_list, files, data, trimstart, trimend):
	for i in range (0, len(GCAMP_list)):
		file = files[i]
		# trim
		GCAMP = GCAMP_list[i]
		ISOS = ISOS_list[i]
		fs = data.streams[GCAMP.title()].fs
		start = trimstart
		stop = trimend
		time = np.arange(start=1, stop=len(data.streams[GCAMP.title()].data)+1, step=1)/data.streams[GCAMP.title()].fs

		data_GCAMP = np.array(data.streams[GCAMP.title()].data)
		data_ISOS = np.array(data.streams[ISOS.title()].data)
		Signal_GCAMP = data_GCAMP[start:-stop]
		Signal_ISOS = data_ISOS[start:-stop]
		trimtime = time[start:-stop]

		# downsample
		N = fs
		arr_GCAMP = (np.arange(start = 1, stop = len(Signal_GCAMP) - N + 1, step = N)).astype(int)
		down_GCAMP = [statistics.mean(Signal_GCAMP[i:round(i+N-1)]) for i in arr_GCAMP]
		arr_ISOS = (np.arange(start=1, stop=len(Signal_ISOS) - N + 1, step=N)).astype(int)
		down_ISOS = [statistics.mean(Signal_ISOS[i:round(i + N - 1)]) for i in arr_ISOS]
		downtime = trimtime[::round(N)]
		downt = downtime[:len(down_GCAMP)]

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
		fig = plt.figure(figsize=(6,8))
		ax = fig.add_subplot(411)
		p1, = ax.plot(time, data.streams[GCAMP.title()].data, linewidth=2,
					  color='green', label='GCaMP')
		p2, = ax.plot(time, data.streams[ISOS.title()].data, linewidth=2,
					  color='blueviolet', label='Isosbestic')
		ax.set_xlabel('Time (s)')
		ax.set_ylabel('mV')
		ax.set_title('Raw Signals ' + str(file))
		ax.legend(handles=[p1, p2], loc='upper right')
		ax.set_xlim([start, time[len(time)-1]-stop])

		ax2 = fig.add_subplot(412)
		p3, = ax2.plot(downt, smooth_GCAMP, linewidth=2, color='green', label='Processed GCaMP')
		p4, = ax2.plot(downt, smooth_ISOS, linewidth=2, color='blueviolet', label='Processed Isosbestic')
		p5, = ax2.plot(downt, fit_ISOS, linewidth=2, color='dodgerblue', label='Fit Isosbestic')
		ax2.set_xlabel('Time (s)')
		ax2.set_ylabel('mV')
		ax2.set_title('Smoothed, Fit, and Aligned Signals ' + str(file))
		ax2.legend(handles=[p3, p4, p5], loc='upper right')
		ax2.set_xlim([start, len(downt)-stop])

		ax3 = fig.add_subplot(413)
		p6, = ax3.plot(downt, dF, linewidth=2, color='black', label='Baseline Corrected GCaMP')
		ax3.set_xlabel('Time (s)')
		ax3.set_ylabel(r'$\Delta$mV')
		ax3.set_title('Subtracted Signal ' + str(file))
		ax3.legend(handles=[p6], loc='upper right')
		ax3.set_xlim([start, len(downt)-stop])

		ax4 = fig.add_subplot(414)
		ax4.plot(downt, dFF, linewidth=2, color='green')
		ax4.set_xlabel('Time (s)')
		ax4.set_ylabel(r'$\Delta$F/F (%)')
		ax4.set_title(r'$\Delta$F/F, ' + str(file))
		ax4.set_xlim([start, len(downt)-stop])

		fig.suptitle('Data Processing ' + str(file), fontsize=16)
		fig.tight_layout()
		plt.savefig(str(file) + '.png')

		# plot just dff
		fig2 = plt.figure()
		ax = fig2.add_subplot(211)
		ax.plot(downt, dFF, linewidth=2, color='green')
		ax.set_xlabel('Time (s)')
		ax.set_ylabel(r'$\Delta$F/F (%)')
		ax.set_title(r'$\Delta$F/F, ' + str(file))
		ax.set_xlim([start, len(downt)-stop])

		fig2.tight_layout()
		plt.savefig('dFF_' + str(file) + '.png')


def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'same') / w


def main():
	tankdir = "/Volumes/GoogleDrive/Shared drives/Schwartz/Data/Fiber Photometry Experiments/Practice"
	trimstart = 20
	trimend = 20
	blocknames = ['VMH_Pacap4_67-210716-120928', 'VMH_Pacap4_1345-210716-115350']
	filenames = {
		'VMH_Pacap4_67-210716-120928': ['VMH_Pacap4_67_1', 'VMH_Pacap4_67_2', 'VMH_Pacap4_67_3', 'VMH_Pacap4_67_4'],
		'VMH_Pacap4_1345-210716-115350': ['VMH_Pacap4_1345_1', 'VMH_Pacap4_1345_2', 'VMH_Pacap4_1345_3', 'VMH_Pacap4_1345_4']}
	extract_name_streams(blocknames, tankdir, filenames, trimstart, trimend)


if __name__ == "__main__":
	main()
