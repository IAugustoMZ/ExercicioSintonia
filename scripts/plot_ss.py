import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt

# ignorar warnings
warnings.filterwarnings('ignore')

# definição de constantes
equip = 'tank'                      # equipamento que será feita a análise
CONTROLLED_VAR = 'h'                # variável controlada
MANIP_VAR = 'F'                     # variável manipulada
time_range = 30                     # amplitude dos dados a serem coletados para cálculo da variável desvio


# carregamento dos dados
# arquivo de valores medidos
values = pd.read_csv(os.path.join('./data',f'ss_values_{equip}.csv'), header=None)
try:
    values.columns = [CONTROLLED_VAR, 'set_point', MANIP_VAR]
except:
    values.columns = [CONTROLLED_VAR, MANIP_VAR]
    
# arquivos de valores de tempo
time = pd.read_csv(os.path.join('./data',f'ss_time_{equip}.csv'), header = None)
time.columns = ['time']

data = values.join(time)

# construção do gráfico
plt.figure(figsize=(10,8))
plt.plot(data.time, data[CONTROLLED_VAR], 'k-')
if equip == 'reactor':
    plt.xlabel('Tempo (s)', size = 14)
    plt.ylabel(r'Concentração na Saída ($kmol.m^{-3}$)', size = 14)
    plt.title('Determinação do Estado Estacionário de Referência\n' + r'$SS_{ref}$ = ' + \
    f'{round(data[CONTROLLED_VAR].tail(time_range).mean(),4)}' + r' $kmol.m^{-3}$', size = 16)
else:
    plt.xlabel('Tempo (h)', size = 14)
    plt.ylabel(r'Altura do Nível do Tanque ($m$)', size = 14)
    plt.title('Determinação do Estado Estacionário de Referência\n' + r'$SS_{ref}$ = ' + \
    f'{round(data[CONTROLLED_VAR].tail(time_range).mean(),4)}' + r' $m$', size = 16)

plt.xlim([0, data.time.max()])
plt.ylim([0, 1.05*data[CONTROLLED_VAR].max()])
plt.show()