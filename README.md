# Sintonia de Controladores PID usando Método de Ziegler-Nichols

Esse projeto apresenta uma implementação em Python do primeiro método de Ziegler-Nichols para sintonia dos controladores PID para dois processos industriais, sendo um reator CSTR e um tanque de armazenamento com efeito não linear. Esse projeto foi desenvolvido como parte da última tarefa do módulo FEQ1012 - Controle e Instrumentação de Processos do curso de Especialização em Engenharia de Processos Químicos da Faculdade de Engenharia Química da Unicamp.

## :hammer: Funcionalidades do projeto

- `Simulação do Comportamento Dinâmico`: utilizando diagramas Xcos (Scilab) e scripts, o projeto permite simular o comportamento dinâmico dos dois processos mencionados
- `Método de Ziegler-Nichols`: um dos scripts implementados aplica a estimativa dos parâmetros de sintonia do controlador proposto por Ziegler-Nichols com base na curva de reação de forma automática
- `Visualização da resposta ao controlador`: outros scripts implementados apresentam a construção de visualizações que apresentam a resposta dos sistemas frente às ações dos controladores P, PI, PID e PID com sintonia fina


## 🖥 Acesso ao projeto

Para utilizar os arquivos, você precisa ter instalado o Scilab no seu computador. Além disso, é importante ter um interpretador Python (tipo Anaconda) e um editor de texto para executar os scripts Python.

## 🎮 Execução

- para executar as simulações, abra os arquivos da pasta `simulations` no Scilab e execute os diagramas Xcos. Os scripts já podem ser executados diretamente, pois eles executam a simulação do diagrama Xcos
- para aplicar o método de Ziegler-Nichols, abra o arquivo `FOPDT_ZN.py` da pasta `scripts` num editor de texto com interpretador Python e modifique o equipamento desejado (`equip = reactor` ou `equip = tank`) para aplicar o método à curva de reação desejada
- para construir as visualizações das respostas às ações de controle, abra o arquivo `plot_data.py` da pasta `scripts` num editor de texto com intepretador Python e modifique o equipamento desejado (`equip = reactor` ou `equip = tank`) e também informe qual a ação de controle desejada (`CONTROL`) - sendo `p` para controle proporcional, `pi` para controle proporcional-integral, `pid` para controle proporcional-integral-derivativo. Se o campo for deixado vazio, o script compreende que se trata de um ajuste fino e vai usar os valores dos parâmetros de sintonia definidos no próprio script

## ✔ Tecnologias utilizadas

- Scripts Python
- Simulações Xcos
- Scripts Scilab

## 👨‍🔧 Contribuidores

O projeto foi possível graças aos ensinamentos do prof. Flávio Vasconcelos da Silva, do módulo FEQ1012 - Controle e Instrumentação em Processos Químicos

## 👨‍🎓 Autores

| [<img src="https://avatars.githubusercontent.com/u/42342168?s=400&u=6aa00c4fdc744dca529170a61a19c38d2bed1689&v=4" width=115><br><sub>Ícaro Augusto Maccari Zelioli</sub>](https://github.com/IAugustoMZ)
