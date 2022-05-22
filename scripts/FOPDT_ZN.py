import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

# ignorar warnings
warnings.filterwarnings('ignore')

# definição de constantes
equip = 'tank'                          # equipamento que será feito a análise
if equip == 'reactor':
    STEP_TIME = 300                     # tempo no qual o passo foi dado no modelo do reator
    STEP = 15                           # valor do passo dado no modelo do reator
    CONTROLLED_VAR = 'Ca'               # variável controlada no modelo do reator
    MANIP_VAR = 'F'                     # variável manipulada no modelo do reator
else:
    STEP_TIME = 25                      # tempo no qual o passo foi dado no modelo do tanque
    STEP = 50                           # valor do passo dado no modelo do tanque
    CONTROLLED_VAR = 'h'                # variável controlada no modelo do tanque
    MANIP_VAR = 'F'                     # variável manipulada no modelo do tanque
time_range = 30                         # amplitude dos dados a serem coletados para cálculo da variável desvio

# carregar os dados
values = pd.read_csv(os.path.join('./data',f'zn_data_{equip}.csv'), header=None)
values.columns = [CONTROLLED_VAR, MANIP_VAR]
time = pd.read_csv(os.path.join('./data',f'zn_data_time_{equip}.csv'), header=None)
time.columns = ['time']

# unindo os dados
data = values.join(time)

# cálculo do intervalo de amostragem
SAMPLE_PERIOD = data['time'][1] - data['time'][0]

# subgrupo de amostras para primeiro estado estacionário
time_sample = [STEP_TIME-(SAMPLE_PERIOD*t) for t in range(time_range)]

# valor do primeiro estado estacionário
SS1_VALUE = data.loc[data.time.isin(time_sample),CONTROLLED_VAR].mean()

# calculando as variáveis-desvio
data[f'{CONTROLLED_VAR}_vd'] = data[CONTROLLED_VAR] - SS1_VALUE
data['time_vd'] = data['time'] - STEP_TIME

# amostrando apenas a parte da curva de reação
data_zn = data.loc[data.time_vd >= 0,:]

# construindo a função do modelo do FOPDT
def fopdt_model(t, A, B):
    return A*(1-(1+(t/B))*np.exp(-(t/B)))

# ajustando parâmetros do modelo do FOPDT
popt, pov = curve_fit(
    f = fopdt_model,
    xdata = data_zn.time_vd,
    ydata = data_zn[f'{CONTROLLED_VAR}_vd']
)

# calculando o modelo com os parâmetros ajustados
data_zn['model'] = data_zn['time_vd'].apply(fopdt_model, A = popt[0], B = popt[1])

# subgrupo de amostras para segundo estado estacionário
time_sample = [data_zn.time_vd.tail(1).values[0]-(SAMPLE_PERIOD*t) for t in range(time_range)]

# valor do segundo estado estacionário
SS2_VALUE = data_zn.loc[data_zn.time_vd.isin(time_sample),'model'].mean()

# cálculo do ganho proporcional
K = SS2_VALUE / STEP

# cálculo da derivada
data_zn['d_model'] = data_zn['model'].diff()/SAMPLE_PERIOD

# determinação do ponto de inflexão
inflex = data_zn.loc[data_zn.d_model==data_zn.d_model.max(),['time_vd', 'model', 'd_model']]

# cálculo da reta tangente ao ponto de inflexão
def tang_inflex(t, a, b, m):
    return b + ((t - a)*m)

data_zn['tang'] = data_zn.time_vd.apply(tang_inflex, 
                                     a = inflex.time_vd.values[0], 
                                     b = inflex.model.values[0], 
                                     m = inflex.d_model.values[0])

# cálculo do tempo que a gente tangente cruza o eixo x - tempo morto (s)
t_d = data_zn.loc[data_zn.tang >= 0, 'time_vd'].head(1).values[0]

# cálculo da constante de tempo + tempo morto
tau_td = data_zn.loc[data_zn.tang >= SS2_VALUE, 'time_vd'].head(1).values[0]

# cálculo da constante de tempo
tau = tau_td - t_d

# criando nome com os parâmetros de sintonia
if equip == 'reactor':
    param_names = r'$K$' + f' = {round(K,2)} - ' + r'$\tau$ = ' + \
        f'{round(tau,2)} s - ' + r'$t_d$' + f' = {round(t_d,2)} s'
else:
    param_names = r'$K$' + f' = {round(K,2)} - ' + r'$\tau$ = ' + \
        f'{round(tau,2)} h - ' + r'$t_d$' + f' = {round(t_d,2)} h'

print(popt)
print(K, tau, t_d)

# construir gráfico
fig = plt.figure(figsize=(16,8))
ax = fig.add_subplot(1,2,1)
ax.plot(data_zn['time_vd'], data_zn[f'{CONTROLLED_VAR}_vd'], 'k.', label = 'Dados Originais')
ax.plot(data_zn['time_vd'], data_zn['model'], 'r-', label = 'Modelo FOPDT')
if equip == 'reactor':
    ax.set_xlabel('Tempo (s) - Variável Desvio', size = 14)
    ax.set_ylabel(r'Concentração de Saída ($kmol/m^3$) - Variável Desvio', size = 14)
    ax.set_title(f'Curva de Reação do Reator CSTR - Degrau de {STEP} %\n{param_names}', size = 18)
    ax.set_xlim([0, 100])
else:
    ax.set_xlabel('Tempo (h) - Variável Desvio', size = 14)
    ax.set_ylabel(r'Altura do Nível do Tanque ($m$) - Variável Desvio', size = 14)
    ax.set_title(f'Curva de Reação do Tanque de Armazenamento - Degrau de {STEP} %\n{param_names}', size = 18)
    ax.set_xlim([0, 10])
ax.set_ylim([0, 1.05*SS2_VALUE])
ax.legend(loc = 'best', prop = {'size': 14})


ax = fig.add_subplot(1,2,2)
ax.plot(data_zn['time_vd'], data_zn[f'{CONTROLLED_VAR}_vd'], 'k.', label = 'Dados Originais')
ax.plot(data_zn['time_vd'], data_zn['model'], 'r-', label = 'Modelo FOPDT')
ax.plot(data_zn['time_vd'], data_zn['tang'], 'b--', label = 'Reta Tangente')
if equip == 'reactor':
    ax.set_xlabel('Tempo (s) - Variável Desvio', size = 14)
    ax.set_ylabel(r'Concentração de Saída ($kmol/m^3$) - Variável Desvio', size = 14)
    ax.set_xlim([0, 100])
    ax.text(x = tau_td+2, y = .2, s = r'$\tau$ + $t_d$'f' = {round(tau_td,2)} s')
    ax.text(x = t_d+1, y = .4, s = r'$t_d$' + f' = {round(t_d,2)} s')
else:
    ax.set_xlabel('Tempo (h) - Variável Desvio', size = 14)
    ax.set_ylabel(r'Altura do Nível do Tanque ($m$) - Variável Desvio', size = 14)
    ax.set_xlim([0, 10])
    ax.text(x = tau_td+0.1, y = 5, s = r'$\tau$ + $t_d$'f' = {round(tau_td,2)} h')
    ax.text(x = t_d+0.1, y = 13, s = r'$t_d$' + f' = {round(t_d,2)} h')
ax.set_title('Método FOPDT', size = 18)
ax.axvline(t_d, color = 'gray', ls = '--')
ax.axvline(tau_td, color = 'gray', ls = '--')
ax.axhline(SS2_VALUE, color = 'orange', ls = '-.')

ax.legend(loc = 'best', prop = {'size': 14})
ax.set_ylim([0, 1.05*SS2_VALUE])

plt.show()