// definir constantes do reator
F = 0.0065;                             // vazão de entrada [m3/min]
V = 0.24;                               // volume do conteúdo do reator [m3]
k = 0.017;                              // constante cinética da reação [1/min]
K = 0.03185;                            // constante proporcional
tau = 29;                               // tempo da ação integral [min]
td = 3;                                 // tempo da ação derivativa [min]
Cain = 8;                               // concentração inicial de A [kmol/m3]
tempo = 50;                             // tempo da simulação [min]
period = 0.1;                           // período de amostragem [min-1]
initial_cond = 4.7248;                  // concentração de regime permanente da concentração [kmol/m3]

// importar o diagrama XCos
importXcosDiagram("controleCSTR.zcos");

// calcular os parâmetros de controle via Ziegler-Nichols

// ganho proporcional
//Kc = tau/(td*K)                         // controle P
//Kc = (0.9*tau)/(td*K)                   // controle PI
Kc = (1.2*tau)/(td*K)                   // controle PID

// tempo de ação integral
//Ti = 1e32                               // controle P
//Ti = 3.33*td                            // controle PI
//Ti = 2*td                               // controle PID
Ti = 25                                   // controle PID - ajuste fino

// tempo de ação derivativa
//Td = 0                                  // controle P e PI
Td = (td/2)                             // controle PID

// realizar a simulação
xcos_simulate(scs_m, 4);

// salvar os dados como arquivo csv

// arquivos de tempo
//write_csv(PC3.time, 'zn_time_control_p.csv')            // controle P
//write_csv(PC3.time, 'zn_time_control_pi.csv')            // controle PI
//write_csv(PC3.time, 'zn_time_control_pid.csv')            // controle PID
write_csv(PC3.time, 'zn_time_control_tunning.csv')        // controle PID - ajuste fino

// arquivos de medições de variáveis
//write_csv(PC3.values, 'zn_values_control_p.csv')            // controle P
//write_csv(PC3.values, 'zn_values_control_pi.csv')            // controle PI
//write_csv(PC3.values, 'zn_values_control_pid.csv')            // controle PID
write_csv(PC3.values, 'zn_values_control_tunning.csv')        // controle PID - ajuste fino
