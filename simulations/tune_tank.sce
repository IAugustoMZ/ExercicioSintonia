// constantes para o modelo do tanque
clear;
A = 2; // área da seção transversal (m2)
Fin = 20; // vazão volumétrica primária (m3/h)
Fd = 12; // vazão volumétrica secundária (m3/h)
beta = 10.5; // constante Cv da válvula (m3/h)^0,5
K = 0.3016;                            // constante proporcional
tau = 2.10;                               // tempo da ação integral [h]
td = 0.30;                                 // tempo da ação derivativa [h]
Kc = 0; // constante proporcional
Ti = 1e32; // tempo de ação integral (h)
Td = 0; // tempo de ação derivativa (h)
time = 5; // tempo de simulação (h)
period = 0.01; // período de amostragem (1/h)
ss_ref= 9.2944; // nível de referência do estado estacionário

// importar o diagrama XCos
importXcosDiagram("./simulations/controleTANK.zcos");

// calcular os parâmetros de controle via Ziegler-Nichols

// ganho proporcional
//Kc = tau/(td*K)                         // controle P
//Kc = (0.9*tau)/(td*K)                   // controle PI
//Kc = (1.2*tau)/(td*K)                   // controle PID
Kc = 50

// tempo de ação integral
//Ti = 1e32                               // controle P
//Ti = 3.33*td                            // controle PI
//Ti = 2*td                               // controle PID
Ti = 2.5                                   // controle PID - ajuste fino

// tempo de ação derivativa
//Td = 0                                  // controle P e PI
//Td = (td/2)                             // controle PID
Td = 0.3

// realizar a simulação
xcos_simulate(scs_m, 4);

// salvar os dados como arquivo csv

// arquivos de tempo
//write_csv(tank.time, './data/zn_time_control_p_tank.csv')            // controle P
//write_csv(tank.time, './data/zn_time_control_pi_tank.csv')            // controle PI
//write_csv(tank.time, './data/zn_time_control_pid_tank.csv')            // controle PID
write_csv(tank.time, './data/zn_time_control_tunning_tank.csv')        // controle PID - ajuste fino

// arquivos de medições de variáveis
//write_csv(tank.values, './data/zn_values_control_p_tank.csv')            // controle P
//write_csv(tank.values, './data/zn_values_control_pi_tank.csv')            // controle PI
//write_csv(tank.values, './data/zn_values_control_pid_tank.csv')            // controle PID
write_csv(tank.values, './data/zn_values_control_tunning_tank.csv')        // controle PID - ajuste fino
