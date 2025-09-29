# Campo Minado em Python(Terminal)</h1>

Um projeto acadêmico que recria o clássico jogo Campo Minado para ser jogado diretamente no terminal, utilizando a biblioteca `curses` do Python para a interface gráfica.

## Autoras

Desenvolvido por **Gabriela Ramalho da Silva** e **Lara Giovanna de Moura Soares**, alunas do curso de **Ciência da Computação** da **Universidade Federal de Campina Grande (UFCG)**, do período **2025.1**. O jogo se trata de um projeto das disciplicas Laboratório de Programação 1 e Programação 1.

## Funcionalidades

- Interface gráfica no terminal: utiliza a biblioteca `curses` para criar janelas, bordas e controlar cores.

- Níveis de dificuldade: três opções de dificuldade (Fácil, Médio, Difícil) que alteram o tamanho do campo e a quantidade de bombas.

- Navegação por teclado: controle total do cursor utilizando as setas do teclado.

- Jogabilidade clássica: cavar um local para revelar o que há por baixo, marcar e desmarcar possíveis locais de bomba.

- Cronômetro e contador de bombas: acompanhe seu tempo e a quantidade de bombas restantes.

- Telas de vitória e derrota: telas personalizadas com arte em ASCII e animações para feedback de fim de jogo.

- Animação de Início: Uma tela de abertura com o nome do jogo em arte ASCII.

## Tecnologias Utilizadas

- Python 3: linguagem principal do projeto.

- Biblioteca `curses`: para toda a manipulação da interface no terminal (janelas, cores, entrada de teclado).

- Biblioteca threading: utilizada no arquivo **cronometro.py** para que o tempo passe em segundo plano sem travar o jogo.

## Pré-requisitos

Para rodar este projeto, você precisará de:

- Um ambiente Linux ou um subsistema como o WSL no Windows.

- Python 3 instalado.

- A biblioteca ncurses (geralmente já vem instalada na maioria das distribuições Linux, como o Ubuntu).

Você pode baixar o programa na sua maquina por meio dessa versão no github:
https://github.com/lgiovannadms/campo-minado-terminal

## Estrutura do Projeto

O projeto é dividido em quatro arquivos principais:

- **campo_minado.py**: o arquivo principal que **inicializa o jogo**, contém o loop principal (main) e a função jogar, que gerencia a lógica da partida.

- **interface.py**: contém a classe Interface, responsável por todo o desenho na tela. Funções de menu, janelas, telas de vitória/derrota e a atualização visual do campo estão aqui.

- **campo.py**: contém a classe Campo, que gerencia a lógica interna do tabuleiro: onde as bombas estão, os números de cada casa, e as regras de cavar e marcar.

- **cronometro.py**: uma classe simples para controlar o tempo de jogo usando uma thread separada.
