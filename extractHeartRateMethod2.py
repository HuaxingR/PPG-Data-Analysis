import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import csv
from scipy.fftpack import fft, fftfreq

time = pd.read_csv("stream_raw.csv", header=1, usecols=[1])
ppg_values = pd.read_csv("stream_raw.csv", header=1, usecols=[2])
# convert the readings from Pandas result to numpy array
# also flatten the 2D array to 1D list
value_list = (ppg_values.to_numpy()).flatten()
time_list = (time.to_numpy()).flatten()
# make a time list to use when plotting the values to make the graph neatly
time_array = np.arange(0, int(float(len(time_list))))
# plt.plot(time_array, value_list, c="red", linewidth=0.5)
# plt.gcf().autofmt_xdate()
# plt.xlabel('Time')
# plt.ylabel('ppg')
# plt.legend(labels=['PPG'])
# plt.title('Time vs PPG')
# plt.show()

time = pd.read_csv("stream_raw.csv", header=1, usecols=[1])
flatten_time = (time.to_numpy()).flatten()
x_time = [datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S.%f") for d in flatten_time]
i = 0
time = []
while i < len(x_time):
    splitTemp = (time_list[i]).split('.')
    time.append(splitTemp[0])
    i += 1

ppg_values = pd.read_csv("stream_raw.csv", header=1, usecols=[2])
# convert the readings from Pandas result to numpy array
# also flatten the 2D array to 1D list
value_list = (ppg_values.to_numpy()).flatten()

# an example with samples of first 10 second
N = 640
t = np.arange(0, N - 1, 1)
fft_val = np.abs(fft(value_list[0:N]))
sample_freq = fftfreq(value_list[0:N].size, d=1 / 64)
plt.title('Frequency domain Signal')
plt.xlabel('Frequency (Hz)')
plt.ylabel('Amplitude')
plt.plot(sample_freq, fft_val)
plt.show()
n = np.size(t)
index = np.argmax(fft_val)
frequency_max = sample_freq[index]
print(frequency_max)
print(frequency_max * 60)
# plt.plot(fft_val)
# plt.title('Frequency domain Signal')
# plt.xlabel('Frequency (Hz)')
# plt.ylabel('Amplitude')
# plt.show()

HR = []
i = 0


while i < np.size(value_list) - 1792:
    fft_slice = fft(value_list[i:i + 1792])
    fft_m = abs(fft_slice)
    sample_freq = fftfreq(value_list[i:i+1792].size, d=1 / 64)
    index = np.argmax(fft_m)
    frequency_max = sample_freq[index]
    hr = frequency_max*60
    temp = []
    temp.append(time[i])
    temp.append(hr)
    HR.append(temp)
    i += 64

freqfileName = "task2_outputHR.csv"
with open(freqfileName, 'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Time','HR'])
    csvwriter.writerows(HR)


manualComputation = pd.read_csv("HR_stream.csv", header=1, usecols=[1])
result = pd.read_csv("task2_outputHR.csv", header=1, usecols=[1])
manual_time = pd.read_csv("HR_stream.csv", header=1, usecols=[0])
result_time = pd.read_csv("task2_outputHR.csv", header=1, usecols=[0])
flatten_manual_time = (manual_time.to_numpy()).flatten()
flatten_result_time = (result_time.to_numpy()).flatten()
x_manual = [datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in flatten_manual_time]
x_result = [datetime.datetime.strptime(a, "%Y-%m-%d %H:%M:%S") for a in flatten_result_time]
win_len = 58
result_rolling = result.rolling(win_len).mean()
flatten_result_rolling = (result_rolling.to_numpy()).flatten()
plt.figure()
time_array = np.arange(0, int(float(len(flatten_result_rolling))))

result_list = (result.to_numpy()).flatten()
computation_list = (manualComputation.to_numpy()).flatten()
diff_time = (int(float(len(computation_list))))-(int(float(len(flatten_result_rolling))))
time_array = np.arange(0, int(float(len(computation_list))))
time_array_1 = np.arange(0, int(float(len(flatten_result_rolling))))
plt.plot(time_array_1+(diff_time/2), flatten_result_rolling, c='green')
plt.plot(time_array, computation_list, c='red')
z = np.polyfit(time_array_1, result_list, 1)
p = np.poly1d(z)
plt.plot(time_array, p(time_array), "b--")
plt.ylabel('HR')
plt.xlabel('Time in second')
plt.legend(labels=['HR', 'estimated HR','Trendline'])
plt.suptitle('Task 2: Compare the HR with the estimated HR')
plt.title("y=%.6fx+%.6f"%(z[0], z[1]))
plt.show()
