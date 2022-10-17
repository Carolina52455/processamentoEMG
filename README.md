# processamentoEMG

O código presente é constituído por dois ficheiros: a main.py e EMGfunctions.py. O primeiro tem a função de correr o programa, ou seja:

1º Lê os ficheiros, presentes numa pasta, correspondentes aos sinais EMG e converte-os para mV através da função de transferência, tendo em conta o sistema de aquisição, o BITalino; De modo de explemplo, colocou-se a pasta Convencionais_2022-06-03 para o utilizador conseguir correr o programa. Para ler outra pasta, o utilizador apenas tem de alterar o nome (correspondente à pasta pretendida) no seguinte comando: path = 'Convencionais_2022-06-03/' e modificar a diretoria onde se encontram os ficheiros .py e a pasta correspondente aos sinais EMG, no seguinte comando: save_path = r'C:\Users\35196\Desktop\emg'.

2º Chama as funções presentes no ficheiro EMGfunctions.py de modo a processar o sinal EMG e tirar as características pretendidas: Ruído rms, Amplitude RMS do sinal, SNR, amplitude original, PSD média e envelope RMS médio.

3º Cria ficheiros .csv com as características acima mencionadas. Os ficheiros .cvs contêm valores para cada intervalo do sinal. Por exemplo, a pasta Convencionais_2022-06-03  corresponde a um exemplo de aquisições de sinais EMG que contém 11 medições. Cada medição é constituída por 5 contrações de 5 segundos espaçadas de um repouso de 10 segundos. Assim, cada intervalo foi definido pelos 5 segundos de cada contração ± 2 segundos do repouso. Deste modo, os ficheiros .cvs contêm 55 (5 x 11) valores para cada característica.
