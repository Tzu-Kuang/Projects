import pandas as pd
import numpy as np
import glob
# File folder path
data_path = r'C:\Users\3503\Desktop\interpolation\ray'
# Save file name
file_ = r'C:\Users\3503\Desktop\interpolation\result'
# Get all files for specific folder
raw_data = glob.glob('{}/*.csv'.format(data_path))
# Data Prepocessing
for data_file_path in raw_data:
    print("Strating processing {} file!!".format(data_file_path.split('\\')[-1]))
    # Read data and fill zero with NaN
    data = pd.read_csv(data_file_path,encoding= 'utf-8', skiprows=4)
    df = pd.DataFrame(data)
    df = df.fillna(0)
    # Get time values for each probe
    interval = 0.001                                    # Interpolation resolution
    header = list(df)                                   # Data title
    time = df[header[0]]                                # Get new time for each features
    time = [round(i, 3) for i in time]
    # Get new time series for set interval
    initial_time = 0
    new_time_series = []
    last_time = max(time)
    while round(initial_time, 3) <= last_time:
        new_time_series.append(round(initial_time, 3))
        initial_time += 0.001
    new_time_series = np.array(new_time_series)
    probe_val = new_time_series   
    columns = ['Time(sec)']
    for i in range(1, len(header), 2):
        time = df[header[i - 1]]                        # Get time for each features
        time = [round(i, 3) for i in time]
        # Get new time series for set interval
        initial_time = 0
        new_time_series = []
        last_time = max(time)
        while round(initial_time, 3) <= last_time:
            new_time_series.append(round(initial_time, 3))
            initial_time += 0.001
        new_time_series = np.array(new_time_series)
        print(header[i])
        columns.append(header[i])
        probe = df[header[i]].tolist()                 # Get values for each features
        # Interpolation algorithm
        result_time = []
        result_probe = []
        for i in new_time_series:
            # If time is smaller than initial time, add probe value as zero
            # Or if time is bigger than the initial time but not in the raw time series
            # First we add zero to the result probe values to make two result lists have the same size
            if round(i, 3) < time[0] or (round(i, 3) >= time[0] and round(i, 3) not in time):
                result_time.append(round(i, 3))
                result_probe.append(0)
            # If time in new_time_series is in raw time series, get index of the raw time series and get
            # The corresponding probe values
            elif round(i, 3) >= time[0] and round(i, 3) in time:
                index = time.index(i)
                result_time.append(round(i, 3))
                result_probe.append(probe[index])
        # Do interpolation algorithm
        # Get the last non zero values of probe values
        for i in range(len(result_probe) - 1, 0, -1):
            if result_probe[i] != 0:
                index_num = i
                break
        '''
        Interpolation Alogrithm:
        -------------|(t_1)-----------|(t_i)----------------|(t_2)-----------------
                        A     (m)    probe_val    (n)          B
        1). Get two interval values (m、n)
        2). Get two of the probe values from t_1 and t_2
        3). Probe_val = (n * A) + (m * B)/ (m + n)   
        '''
        for i in new_time_series:    
            if round(i, 3) >= time[0] and round(i, 3) not in time:
                index = result_time.index(i)
                m = interval
                a = result_probe[index - 1]
                j = 0
                probe_index = index
                while probe_index <= index_num and result_probe[probe_index] == 0:
                    probe_index += 1
                    j += 1
                b = result_probe[probe_index]
                n = interval* j
                new_probe_val = round((n*a + m*b)/(m+n), 4)
                result_probe[index] = new_probe_val
        result_probe = np.array(result_probe)
        probe_val = np.vstack([probe_val,result_probe])
    # Save interpolation result to csv file     
    probe_val = np.transpose(probe_val)
    result = pd.DataFrame(probe_val, columns = columns)
    file_name = data_file_path.split('\\')[-1]
    result.to_csv('{}/{}_interpolated.csv'.format(file_, file_name), index = False)
    print('Done!!')
