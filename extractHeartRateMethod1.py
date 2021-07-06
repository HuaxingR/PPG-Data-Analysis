import csv
from scipy.signal import find_peaks
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime

time = pd.read_csv("stream_raw.csv", header=1, usecols=[1])
ppg_values = pd.read_csv("stream_raw.csv", header=1, usecols=[2])
# convert the readings from Pandas result to numpy array
# also flatten the 2D array to 1D list
value_list = (ppg_values.to_numpy()).flatten()
time_list = (time.to_numpy()).flatten()
peaks, _ = find_peaks(value_list, prominence=25)
# make a time list to use when plotting the values to make the graph neatly
time_array = np.arange(0, int(float(len(time_list))))
plt.scatter(time_array[peaks], value_list[peaks], c='green', s=1)
plt.plot(time_array, value_list, c="red", linewidth=0.5)
plt.gcf().autofmt_xdate()
plt.xlabel('Time')
plt.ylabel('ppg')
plt.legend(labels=['PPG', 'Peak'])
plt.title('Time vs PPG with peak values')
plt.show()

# make a list of time with a peak value
i = 0
timeWithPeak = []
while i < len(peaks):
    timeWithPeak.append(time_list[(peaks[i])])
    i += 1

# create a list of time to make the output clear
i = 0
time_output_file = []
while i < len(peaks):
    tempList = []
    splitTemp = (time_list[(peaks[i])]).split('.')
    tempList.append(splitTemp[0])
    time_output_file.append(tempList)
    i += 1


# output a csv file for the number of peaks for manually computing HR
i = 0
collect_count = []
while i < len(peaks)-1:
    count = 1
    while time_output_file[i][0] == time_output_file[i+count][0]:
        count += 1
    tempList = []
    tempList.append(count)
    collect_count.append(tempList)
    i += count


# Compute HR
second_counted = 0
line_count = 0
hr_num = 0
HR = []
u = 0
sum = 0
datetimeFormat = '%Y-%m-%d %H:%M:%S.%f'
# peak = peak[:100]
while u < (len(peaks)-line_count):
    hr_count = 0
    second_counted = 1
    line_count = 0
    second_duplicate = 0
    while second_counted <= 15:
        line_count += 1
        date_list = (timeWithPeak[u + line_count - 1]).split('.')
        first_second = date_list[0]
        if (u + line_count) == len(peaks):
            date_list = (timeWithPeak[u + line_count - 1]).split('.')
            second_second = date_list[0]
            break
        date_list = (timeWithPeak[u + line_count]).split('.')
        second_second = date_list[0]
        if first_second != second_second:
            if second_counted == 1:  # if the first second is a duplicate
                second_duplicate = line_count
            second_counted += 1
        if second_counted == 16:
            second_counted -= 1
            break
    output_time = (timeWithPeak[u + line_count - 1]).split('.')
    u += second_duplicate
    hr_count = line_count * 4
    sum += hr_count
    line_list = []
    line_list.append(output_time[0])
    line_list.append(hr_count)
    HR.append(line_list)
print("summmmmmmmmm", (sum/(len(HR)-1)))
print("Outputting into output_HR.csv...")
peakFile = "PeakFile.csv"
with open(peakFile, 'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(time_output_file)

HRfileName = "output_HR.csv"
with open(HRfileName, 'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Time','HR'])
    csvwriter.writerows(HR)

collect_count_file = "ForManuallyComputePeak.csv"
with open(collect_count_file, 'w',newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerows(collect_count)

# use small windows to optimize the graph
manualComputation = pd.read_csv("HR_stream.csv", header=1, usecols=[1])
result = pd.read_csv("output_HR.csv", header=1, usecols=[1])
manual_time = pd.read_csv("HR_stream.csv", header=1, usecols=[0])
result_time = pd.read_csv("output_HR.csv", header=1, usecols=[0])
flatten_manual_time = (manual_time.to_numpy()).flatten()
flatten_result_time = (result_time.to_numpy()).flatten()
x_manual = [datetime.datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in flatten_manual_time]
x_result = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") for i in flatten_result_time]
win_len = 58
result_rolling = result.rolling(win_len).mean()
flatten_result_rolling = (result_rolling.to_numpy()).flatten()
plt.figure()
plt.plot(x_manual, manualComputation, color='red')
plt.plot(x_result, result_rolling, color='blue')
plt.gcf().autofmt_xdate()
time_array = np.arange(0, int(float(len(flatten_result_rolling))))
print(flatten_result_rolling)
z = np.polyfit(time_array, flatten_result_rolling, 1)
p = np.poly1d(z)
plt.plot(time_array, p(time_array), "y--")
plt.ylabel('HR')
plt.xlabel('Time in second')
plt.legend(labels=['HR', 'estimated HR'])
plt.suptitle('Compare the HR with the estimated HR')
plt.show()

# plot the HR with a trend line and without the datetime as x-axis
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
plt.suptitle('Compare the HR with the estimated HR')
plt.title("y=%.6fx+%.6f"%(z[0], z[1]))
plt.show()

exit()
