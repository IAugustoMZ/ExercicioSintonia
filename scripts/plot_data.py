# script para a geração dos gráficos de análise
import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt

# ignorar warnings
warnings.filterwarnings('ignore')

# definição das constantes
# definição de constantes
equip = 'tank'                          # equipamento que será feito a análise
if equip == 'reactor':
    STEP_TIME = 300                     # tempo no qual o passo foi dado no modelo do reator
    STEP = 15                           # valor do passo dado no modelo do reator
    CONTROLLED_VAR = 'Ca'               # variável controlada no modelo do reator
    MANIP_VAR = 'F'                     # variável manipulada no modelo do reator
    MANIP_MAX = 2*0.0065                # valor máximo da variável manipulada do reator
    MAX_TIME = 50                       # tempo máximo da simulação do reator
    SET_POINT = 2                       # set point do controlador do reator
    K = 0.03185                         # ganho do método de Ziegler-Nichols do reator
    tau = 29                            # constante de tempo do método de Ziegler-Nichols do reator
    td = 3                              # tempo morto do método de Ziegler-Nichols do reator
    Kc = 364.21                         # constante proporcional do ajuste fino do reator
    tauI = 25                           # tempo de ação integral do ajuste fino do reator
    tauD = 1.5                          # tempo de ação derivativo do ajuste fino do reator
    time_unit = 's'                     # unidade do tempo
else:
    STEP_TIME = 25                      # tempo no qual o passo foi dado no modelo do tanque
    STEP = 50                           # valor do passo dado no modelo do tanque
    CONTROLLED_VAR = 'h'                # variável controlada no modelo do tanque
    MANIP_VAR = 'F'                     # variável manipulada no modelo do tanque
    MANIP_MAX = 2*20                    # valor máximo da variável manipulada do tanque
    MAX_TIME = 5                        # tempo máximo da simulação do tanque
    SET_POINT = 5                       # set point do controlador do tanque
    K = 0.3016                          # ganho do método de Ziegler-Nichols do tanque
    tau = 2.1                           # constante de tempo do método de Ziegler-Nichols do tanque
    td = 0.3                            # tempo morto do método de Ziegler-Nichols do tanque
    Kc = 50                         # constante proporcional do ajuste fino do tanque
    tauI = 2.5                           # tempo de ação integral do ajuste fino do tanque
    tauD = 0.3                          # tempo de ação derivativo do ajuste fino do tanque
    time_unit = 'h'                     # unidade do tempo

CONTROL = 'pid'                        # tipo de ação de controle (p - proporcional
                                    # pi - proporcional/integral; pid - proporcional-integral-derivativo)

# leitura dos dados de acordo com o tipo de controle
def load_data(control_type: str = None):
    """
    realiza a leitura e junção dos dados de acordo com o 
    tipo de controle aplicado

    Parameters
    ----------
    control_type : str, optional
        tipo de controle aplicado, by default None
    """
    # se nenhum tipo de controle for informado, carregar os dados
    if not control_type:
        # arquivo de valores medidos
        values = pd.read_csv(os.path.join('./data',f'zn_values_control_tunning_{equip}.csv'), header=None)
        values.columns = [CONTROLLED_VAR, 'set_point', MANIP_VAR]

        # arquivos de valores de tempo
        time = pd.read_csv(os.path.join('./data',f'zn_time_control_tunning_{equip}.csv'), header = None)
        time.columns = ['time']

        model_name = ''

    else:
        # arquivo de valores medidos
        values = pd.read_csv(os.path.join('./data',f'zn_values_control_{control_type}_{equip}.csv'), header=None)
        values.columns = [CONTROLLED_VAR, 'set_point', MANIP_VAR]

        # arquivos de valores de tempo
        time = pd.read_csv(os.path.join('./data',f'zn_time_control_{control_type}_{equip}.csv'), header = None)
        time.columns = ['time']

        # cálculo dos parâmetros de sintonia de Ziegler-Nichols para nome do modelo
        if control_type == 'p':
            Kc = (tau)/(td*K)
            model_name = r'Controlador P - $K_c$ = ' + f'{round(Kc,2)}'
        elif control_type == 'pi':
            Kc = (0.9*tau)/(td*K)
            tauI = 3.33*td
            model_name = r'Controlador PI - $K_c$ = ' + f'{round(Kc,2)} - ' + r'$\tau_I$ = ' + f'{round(tauI,2)} {time_unit}'
        else:
            Kc = (1.2*tau)/(td*K)
            tauI = 2*td
            tauD = (td/2)
            model_name = r'Controlador PID - $K_c$ = ' + f'{round(Kc,2)} - ' + r'$\tau_I$ = ' + f'{round(tauI,2)} {time_unit} - ' + \
                r'$\tau_D$ = ' + f'{round(tauD,2)} {time_unit}'

    return values.join(time), model_name

# carregando os dados
data, model_name = load_data(control_type=CONTROL)

# se o nome do modelo vier vazio, construir
if model_name == '':
    if equip == 'reactor':
        model_name = r'Controlador PID - $K_c$ = ' + f'{round(Kc,2)} - ' + r'$\tau_I$ = ' + f'{round(tauI,2)} s - ' + \
                r'$\tau_D$ = ' + f'{round(tauD,2)} s'
    else:
        model_name = r'Controlador PID - $K_c$ = ' + f'{round(Kc,2)} - ' + r'$\tau_I$ = ' + f'{round(tauI,2)} h - ' + \
                r'$\tau_D$ = ' + f'{round(tauD,2)} h'

# construindo o gráfico
fig = plt.figure(figsize = (16,8))

ax = fig.add_subplot(1,2,1)
ax.plot(data.time, data[CONTROLLED_VAR], 'k-', label = 'Dados Experimentais')
ax.plot(data.time, data.set_point, 'r--', label = 'Set Point')
if equip == 'reactor':
    ax.set_xlabel('Tempo (s)', size = 14)
    ax.set_ylabel(r'Concentração de Saída ($kmol.m^{-3}$)', size = 14)
else:
    ax.set_xlabel('Tempo (h)', size = 14)
    ax.set_ylabel(r'Altura do Nível do Tanque ($m$)', size = 14)
ax.set_title('Curva de Resposta da Variável Controlada', size = 16)
ax.legend(loc = 'best', prop = {'size': 14})
ax.set_xlim([0, MAX_TIME])
ax.set_ylim([0, 1.3*SET_POINT])

ax = fig.add_subplot(1,2,2)
ax.plot(data.time, data[MANIP_VAR], 'b-')
if equip == 'reactor':
    ax.set_xlabel('Tempo (s)', size = 14)
    ax.set_ylabel(r'Vazão de Alimentação ($m^{3}.s^{-1}$)', size = 14)
else:
    ax.set_xlabel('Tempo (h)', size = 14)
    ax.set_ylabel(r'Vazão de Alimentação ($m^{3}.h^{-1}$)', size = 14)
ax.set_title('Comportamento da Variável Manipulada', size = 16)
ax.set_xlim([0, MAX_TIME])
ax.set_ylim([0, 1.2*data[MANIP_VAR].max()])
ax.axhspan(ymin = MANIP_MAX, ymax = 100*MANIP_MAX, color = 'tomato', alpha = 0.1)

if CONTROL in ['p', 'pi', 'pid']:
    plt.suptitle('Resultados de Sintonia Ziegler-Nichols - ' + model_name, size = 20)
else:
    plt.suptitle('Resultados do Ajuste Fino dos Parâmetros de Controle - ' + model_name, size = 20)
plt.tight_layout()
plt.show()