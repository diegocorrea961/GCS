# TRABALHO FINAL - GERENCIAMENTO DE CONFIGURAÇÃO DE SOFTWARE
 **Nomes:** Diego Corrêa, Gabriel Depaoli e Mickael Castro

**Professor: Filipo Mór**


Funções Definidas
-
Diego > Gerente de Cofiguração e Analista 

Gabriel > Desenvolvedor e Analista 

Mickael > Desenvolvedor

Funcionalidades Selecionadas:
-
1. Criar uma tela de introdução ao estilo Insert Coin
2. Criar uma tela de encerramento(para vitória e para derrota)
3. Criar ao menos 3 fases distintas, com diferentes dinâmicas, efeitos sonoros e de tela, músicas de fundo e dificuldades de jogo.
4. Definir condições de vitória, por exemplo: jogo contra o tempo, ou até atingir uma pontuação específica.
5. Permitir o uso do mouse para controlar a nave
6. Permitir o salvamento dos High Scores, mostrado os na tela de início/introdução
7. Fazer com que a imagem de fundo mude conforme a dificuldade do jogo seja alterada
8. animar o sprite do meteoro
9. permitir que a nave tenha armas que podem destruir os meteoros atingidos por seus 
10. alterar musica de fundo de acordo com as fases do jogo
11. fazer com que os meteoros caiam em velocidades diferentes

Projeto de Jogo
-
- tela inicial: musica de fundo, fundo de um espaço pixelizado, aparece os 3 níveis diponíveis para jogar mostrando o high score de cada nivel separadamente abaixo do botão de iniciar cada nível; abaixo, a escrita "insert coin" pulsando
    - nível fácil: fundo estrelado preto, música 1, baixa quantidade de meteoros que aumenta com o tempo, eles possuem sempre a mesma velocidade(não muito rapida), ganham 1 ponto a cada meteoro destruido
    - nível médio: fundo estrelado azul escuro, música 2, quantidade um pouco maior de meteoros que aumentam com o tempo, alguns meteoros podem ser mais rapidos que outros, ganha 2 pontos a cada meteoro destruido
    - nivel dificil: fundo estrelado vermelho escuro, música 3, grande quantidade de meteoros gerada que amenta com o tempo, todos meteoros vem numa velocidade mais rapida, ganha 3 pontos a cada meteoro destruido
- tela de game over: caso a nave seja atingida por 1 meteoro, tela de game over aparece e salva a pontuação atingida como high score do nível jogado
- tela de vitória: aparece ao completar uma quantidade x de pontos
  - nível fácil: 300 pontos
  - nível médio: 250 pontos
  - nível dificil: 200 pontos