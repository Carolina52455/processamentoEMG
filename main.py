# -*- coding: utf-8 -*-
"""
Created on Mon Apr 25 16:43:02 2022

@author: 35196
"""
from numpy import array, linspace
from numpy import loadtxt
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import EMGfunctions as emgf
from scipy import signal
import csv
import os
from tqdm import tqdm
import tsfel
import pandas as pd


# ficheiro para guardar os valores de SNR
path = '3mm_seco_2022-06-27/'
file_name = path[:-1]
save_path = r'C:\Users\35196\Desktop\emg' #diretoria da pasta
path_id = next(os.walk(path))[2]
file_name_path = os.path.join(save_path, file_name + '.csv')
csv_file = open(file_name_path, 'w')
dados_writer = csv.writer(csv_file)
dados_writer.writerow(['R_rms_1','A_rms_1','SNR_1', 'A1',
                       'R_rms_2','A_rms_2','SNR_2', 'A2',
                       'R_rms_3','A_rms_3','SNR_3', 'A3' ,
                       'R_rms_4','A_rms_4','SNR_4', 'A4',
                       'R_rms_5','A_rms_5','SNR_5', 'A5', 'PSD_media', 'RMS_media'])
# coluna 5 tem os valores ADC
channel_column = 5
# taxa de amostragem
sr = 1000
# resolução do Bitalino
resolution = 10
# Ganho do sensor
G_emg = 1009
# tensão operacional
Vcc = 3.3
window_size = 1000
t_start = 7*sr
t_end = 18*sr
sinais = []
nomes = []
tempo = []
envelope_RMS = []
média_amplitudes = []
#percorrer os vários sinais presentas na pasta
for n, id_ in tqdm(enumerate(path_id), total=len(path_id)):
    # abrir o ficheiro emg a analisar
    line = np.array([])
    data = loadtxt(path + id_)
    emg = data[:, channel_column]
    # função de transferência para passar valores ADC para mV
    emg_mv = ((((emg/2**resolution)-(1/2)) * Vcc)/G_emg)*1000
    emg_correctmean = emg_mv-np.mean(emg_mv)
    print(np.max(emg_correctmean))
    # vetor tempo com taxa de amostragem de 1000 Hz
    time = np.array([i/sr for i in range(0, len(emg_correctmean), 1)])
    # módulo do sinal
    emg_rectified = emgf.emg_rectified(emg_correctmean, time)
# aplicação de filtro passa baicxo para fazer envelope do sinal
    emg_envelope = emgf.envelope(emg_rectified, time)
# tempo rmsenvelope
    start = int(window_size/2)
    end = int(len(time) - window_size/2 + 1)
    time2 = time[start:end]
# envelope rms
    rmsenvelope = emgf.envelope_rms(emg_correctmean, time, time2)
# criação de janelas com as diferentes contrações de 5 segundos e 3 segundos antes e depois da contração
# referentes ao momento de repouso
    contraction_segments = list()
    contraction_segments = emgf.janelas(rmsenvelope, time, sr)
    contraction_segments_1 = emgf.janelas(emg_rectified, time, sr)
    snr = np.array([])
    amplitudes = np.array([])
    ruido= np.array([])
    amplitudes_max = np.array([])
    
# cáluclo do valor SNR para cada intervalo
    for i in range(5):
        snr_i = 20 * \
            np.log10(
                np.max(contraction_segments[i])/np.mean(contraction_segments[i][0:2*sr]))
        ruido_i= np.mean(contraction_segments[i][0:2*sr])  
        ruido= np.append(ruido, ruido_i)
        line = np.append(line, ruido_i)
        amplitudes_i = np.mean(contraction_segments[i][4*sr:7*sr])
        amplitudes = np.append(amplitudes, amplitudes_i)
        line = np.append(line, amplitudes_i)
        snr = np.append(snr, snr_i)
        line = np.append(line, snr_i)
        amplitudes_max_i = np.max(contraction_segments_1[i])
        amplitudes_max = np.append(amplitudes_max, amplitudes_max_i)
        line = np.append(line, amplitudes_max_i)

   # média_amplitudes = np.mean(amplitudes)
   # line = np.append(line, média_amplitudes)
    dados_writer.writerow(line)
    
    # estudo das frequências
    emg_fft = emgf.frequencia(emg_correctmean, "FFT"+id_, sr, time, f_ratio=0.5)
    # emg_welch =  emgf.welch(emg_correctmean, sr)
    sinais.append(emg_correctmean)
    envelope_RMS.append(rmsenvelope)
    tempo.append(time2)
    nomes.append(id_[:-8])
    emgf.welch(emg_correctmean, sr)
    
#média da PDS das 11 medições
media = emgf.welch_total(sinais, nomes, sr)
line = np.append(line, media)
dados_writer.writerow(line)
#média do envelope RMS das 11 medições
media_envelope, des_padrao_envelope = emgf.envelope_rms_total(envelope_RMS, nomes, tempo, sr)
#line = np.append(line, media_envelope)
# dados_writer.writerow(line)
df=pd.DataFrame({'media': media_envelope, 'desvio_padrao': des_padrao_envelope})
df.to_csv(os.path.join(save_path, file_name + '_m.csv'), index=False)
csv_file.flush()
print("Ficheiro Terminado")
csv_file.close()



  
