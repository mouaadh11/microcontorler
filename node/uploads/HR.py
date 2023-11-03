# #First let's import
# import heartpy as hp
# import matplotlib.pyplot as plt

# data= hp.get_data("node/uploads/youcef.csv", column_name='hr')
# time = hp.get_data("node/uploads/youcef.csv", column_name='datetime')
# # (2023, 10, 24, 2, 27, 28, 1, 297)
# # sample_rate = hp.get_samplerate_datetime(time, timeformat='(%Y, %m, %d, %H, %M, %S)')
# # sample_rate = hp.get_samplerate_datetime(time, timeformat='%Y-%m-%d %H:%M:%S')
# print (data)
# # print (time)
# # print (sample_rate)
# # print('sample rate is: %f Hz' %sample_rate)
# wd, m = hp.process(data, sample_rate = 47.0)

# #plot
# # plt.figure(figsize=(12,4))
# # hp.plotter(wd, m)
import heartpy as hp

data = hp.get_data('node/uploads/1.csv', column_name='hr')
# print(data)
working_data, measures = hp.process(data, 46.0)
# print(working_data)
print(measures)
# hp.plotter(working_data, measures)