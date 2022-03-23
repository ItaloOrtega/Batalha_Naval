import numpy as np  # Essa biblioteca é dedicada para o trabalho com matrizes evetores, trabalhando apenas com números
from tkinter import *
import random  # Biblioteca que disponibiliza funções de randomizaçam

valor = 0 #Valor do barco atual
qtd_barcos = [2,1,1,1] #Qtd de cada barco a ser alocado
orientacao = True #Orientação do barco a ser alocado
btt_tabu = {} #Botões do tabuleiro
btt_barcos = [] #Botões dos tipos de barcos
posicoes = [] #Posições dos barcos alocados

class Usuario:
  def __init__(self, resp, tela):
    self.board = np.zeros([8, 8])
    self.consulta = np.zeros([8, 8])
    self.acertos = 0
    if resp == False: #Caso resp for falsa, logo o usuario quer aleatorizar as posições dos barcos
      self.aleatorizar(self.board)
    else: #Senão o proprio usuario coloca os seus barcos
      self.alocar(tela, self.board)
  
  def alocar(self, tela, board):
    global btt_tabu, btt_barcos
    #Lbls para melhorar disposição dos botões
    lbl_aux0 = Label(tela, text="    ", bg= "#CCCCCC",font= "Calibri 10")
    lbl_aux0.grid(row=0, column=0, columnspan=20)
    lbl_aux1 = Label(tela, text="    ", bg= "#CCCCCC",font= "Calibri 10")
    lbl_aux1.grid(row=1, column=0)
    lbl_aux2 = Label(tela, text="    ", bg= "#CCCCCC",font= "Calibri 10")
    lbl_aux2.grid(row=2, column=10)
    lbl_aux3 = Label(tela, text="         ", bg= "#CCCCCC",font= "Calibri 10")
    lbl_aux3.grid(row=10, column=12)
  
    lbl_txt = Label(tela, text="Coloque seus barcos no tabuleiro",padx=20, bg= "#6666FF", fg="#FFFFFF" ,font= "Calibri 20")
    lbl_txt.grid(row=1, column=0, columnspan=20)

    lbl_erro = Label(tela, text="    ", bg= "#CCCCCC",fg="#FFFFFF", font= "Calibri 10 bold")
    lbl_erro.grid(row=2, column=0, columnspan=20)
    
    #Criação dos botões da matriz dos barcos e a legenda horizontal e vertical da matriz
    lbls_tabu = {}
    for x in range(0,8):
      for y in range(0,8):
        btt_tabu["btt"+str(x+1)+str(y+1)] = botao(tela, board, x, y,lbl_erro)
        btt_tabu["btt"+str(x+1)+str(y+1)].grid(row=4+x, column=y+2)
      lbls_tabu["lbl_x"+str(x+1)] = Label(tela, text=str(x+1), bg= "#CCCCCC",font= "Calibri 10 bold")
      lbls_tabu["lbl_x"+str(x+1)].grid(row=3, column=2+x)
      lbls_tabu["lbl_y"+str(x+1)] = Label(tela, text=str(x+1)+" ", bg= "#CCCCCC",font= "Calibri 10 bold")
      lbls_tabu["lbl_y"+str(x+1)].grid(row=4+x, column=1)

    #Criação dos botões do tipo de barcos
    btt_b1 = Button(tela, text="Submarino", padx=42, pady=10, command=lambda:trocavalor(2), bg= "#666666", fg="#FFFFFF",font= "Calibri 15")
    btt_b1.grid(row=4, column=11, columnspan=20)
    btt_barcos.append(btt_b1) #Adiciona na lista o botão desse barco
    btt_b2 = Button(tela, text="Navio Tanque", padx=27, pady=10, command=lambda:trocavalor(3), bg= "#CC99FF", fg="#FFFFFF",font= "Calibri 15")
    btt_b2.grid(row=5, column=11, columnspan=20)
    btt_barcos.append(btt_b2)
    btt_b3 = Button(tela, text="Contratorpedeiro", pady=10, command=lambda:trocavalor(4), fg="#FFFFFF", bg="#003399",font= "Calibri 15")
    btt_b3.grid(row=6, column=11, columnspan=20)
    btt_barcos.append(btt_b3)
    btt_b4 = Button(tela, text="Porta-aviões", padx=35, pady=10, command=lambda:trocavalor(5), fg="#FFFFFF", bg= "#663399",font= "Calibri 15")
    btt_b4.grid(row=7, column=11, columnspan=20)
    btt_barcos.append(btt_b4)
    
    #Orientação atual do barco que será alocado
    lbl_orientacao = Label(tela, text="Orientação do Barco", bg= "#6666FF", fg="#FFFFFF",font= "Calibri 12 bold")
    lbl_orientacao.grid(row=8, column=11, columnspan=3)
    lbl_ori = Label(tela, text="■■■", bg= "#CCCCCC",font= "Calibri 8")
    lbl_ori.grid(row=9, column=11, columnspan=3)

    #Criação dos botões desfazer, girar e salvar
    lbl_des = Label(tela, text="Desfazer", bg= "#CCCCCC",font= "Calibri 15")
    lbl_des.grid(row=10, column=11)
    btt_des = Button(tela, text="↩", padx=20,pady=10, command= lambda:desfazer(board), bg= "#CCCCCC",font= "Calibri 15")
    btt_des.grid(row=11, column=11)
    lbl_girar = Label(tela, text="Girar", bg= "#CCCCCC",font= "Calibri 15")
    lbl_girar.grid(row=10, column=13)
    btt_girar = Button(tela, text="↺", padx=20,pady=10, command=lambda:girar(lbl_ori), bg= "#CCCCCC",font= "Calibri 15")
    btt_girar.grid(row=11, column=13)
    btt_salvar = Button(tela, text="Salvar", padx=20,pady=10, command=lambda:salvar(tela, lbl_erro), bg= "#33CC00",font= "Calibri 15")
    btt_salvar.grid(row=12, column=11, columnspan=3)

    tela.mainloop()

  
  def aleatorizar(self, board):
    flag = True  # Flag de erro de coordenadas
    z = int(0)  # Variavel para contar a qtd de barcos
    while z < 5:  # While para alocar os 5 barcos
      while flag is True:  # While que é executado até a coordenada seja valida
        flag = False  # Desativa a flag
        tam_b = int(z)  # Variavel que é a diferença entre o começo e o final das coordenadas do barco
        if z == 0:  # Caso seja z == 0, o tam_b é igual a 1
          tam_b = int(1)
        # Gera aleatoriamente valores para o X e o Y, podendo ir de 0 até 7
        posxi = random.randint(0, 7)
        posyi = random.randint(0, 7)
        # Cria um vetor que recebera as possisões possiveis para o final do barco
        vetor = []
        i = 0
        while i < 2:  # while para criar as coordenadas possíveis de final do barco, para ele ser posta na vertical
          if 0 <= (posxi + tam_b) <= 7:  # Caso seja possivel movimentar para o x para uma posição + tam_b ...
          # que deve ser entre 0 e 7, pois tam_b, dependendo da itereção, pode valer positivo ou negativo...
          # Isso porque o x pode ir tanto para a cima quanto para baixo
            posxf = posxi + tam_b  # posição final de x é igual posição inical + tam_b
            posyf = posyi  # y se mantem igual
            linha = str(posxf) + " " + str(posyf)  # Ambos os valores são colocados em uma string, separada por espaço
            vetor.append(linha)  # A string é adicionada no vetor de valores possiveis de final
          tam_b = tam_b * -1  # tam_b é multiplicado por -1, para que se for negativo, indo para cima, vire positivo, para baixo. E vice-versa.
          i += 1  # i é incrementado

        i = 0
        # é feita a mesma coisa, mas so que se mantendo na mesma linha e movimentando entre as colunas.
        while i < 2:
          if 0 <= (posyi + tam_b) <= 7:
            posyf = posyi + tam_b
            posxf = posxi
            linha = str(posxf) + " " + str(posyf)
            vetor.append(linha)
          tam_b = tam_b * -1
          i += 1
        # Apos ter todos os valores possiveis que o final possa estar no vetor, é escolhido aleatoriamente uma posição do vetor
        i = random.randint(0, (len(vetor) - 1))
        # Logo depois do final ser escolhido, a linha é dividada para os valores finais de x e y
        posxf, posyf = vetor[i].split(" ", 2)
        # X e Y finais são alocados como inteiros
        posxf = int(posxf)
        posyf = int(posyf)

        # Caso o X ou o Y inicial sejam maiores que os finais, eles são trocados de lugar
        if posxi > posxf:
          posxi, posxf = troca(posxi, posxf)

        if posyi > posyf:
          posyi, posyf = troca(posyi, posyf)

        # É verificado se o valor é válido, caso não for, a flag é acionada
        flag = verifica(board, posxf, posyf, posxi, posyi, tam_b+1)
      # Tendo coordenadas validas, o barco é alocado nessa posição do board
      board = colocar(board, posxi, posxf, posyi, posyf, tam_b+1)
      flag = True  # Flag é acionada para que seja possível a proxíma iteração
      z += 1
    # O board com os todos os navios alocados é retornado, agora completo
    return board


class Adversario(Usuario): #Classe filha de usuario, que tem agora o ultimo acerto feito
  def __init__(self, resp, tela):
    super().__init__(resp, tela)
    self.last_hit = " "


def salvar(tela, lbl):#Função para salvar os dados, se todos os barcos ja terem sido alocados
  flag = False
  for x in qtd_barcos: #Caso ainda exista algum barco nao alocado
     if x > 0:
       flag = True
  if flag == False: #Caso totos os barcos ja terem sido alocados
    tela.destroy() #Fecha a tela
  else: #Senão, é mostrado um erro
    lbl.config(text="Erro!",bg="#CC3333",fg="#FFFFFF")


def desfazer(board): #Função que desfaz o ultimo barco colocado pelo usuario
  global posicoes, btt_barcos, qtd_barcos
  dist = 0
  if len(posicoes) > 0: #Caso ja tenha tido algum barco alocado
    xi,yi,xf,yf = posicoes[int(len(posicoes))-1].split(",") #Pega as posições que estão alocadas na lista
    if int(xi) == int(xf): #Caso a posições de X forem iguais o barco está na horizontal
      dist = int(yf) - int(yi) #Distancia calculada para ativar novamente os botões
    else:
      dist = int(xf) - int(xi) #Distancia calculada para ativar novamente os botões
    board = colocar(board,int(xi),int(xf),int(yi),int(yf),0) #Coloca nesses botões o valor 0, ou seja, deixando as posições limpas
    if qtd_barcos[dist-1] == 0: #Caso a qtd desse barco estiver zerada
      btt_barcos[dist-1].config(state="normal") #Ativa denovo o botão do barco para ele ser colocado
    qtd_barcos[dist-1] += 1 #Aumenta em 1 a qtd desse barco
    posicoes.pop() #Tira da lista o barco
    pintar(board) #Pinta o board com os dados atualizados
  else:
    pass

def botao(tela,board,x,y,lbl): #Função para alocar corretamente os botões e seus valores no board
  aux = Button(tela,text="  ", command=lambda:alloc(board,x,y,lbl), padx=15, pady=15, bg="#3399FF", fg="#000000")
  return aux

def alloc(board,x,y,lbl): #Função de alocação dos barcos pelo botão clicado
  global qtd_barcos, posicoes, valor, btt_barcos
  if valor > 1: #Caso o valor for maior que 1, ou seja, um barco tenha sido selecionado
    #Verifica qual é a orientação do barco e calcula quais são as posições finais
    if orientacao == True:
      xi = xf = x
      yi = y
      yf = y+valor-1
    else:
      yi = yf = y
      xi = x
      xf = x+valor-1
    #Verifica se é possivel fazer essa alocação
    flag = verifica(board,xf,yf,xi,yi,valor)
    if flag == False: #Caso ela for possivel o barco é colocado no tabuleiro
      board = colocar(board,xi,xf,yi,yf,valor)
      lbl.config(text="  ",bg="#CCCCCC",fg="#FFFFFF")
      qtd_barcos[valor-2] -= 1 #Subtrai em 1 a qtd desse barco a ser alocada
      if qtd_barcos[valor-2] == 0: #Caso a qtd for igual a 0, o botão desse barco é desabilitado
        btt_barcos[valor-2].config(state='disabled')
      linha = str(xi)+","+str(yi)+","+str(xf)+","+str(yf) #Aloca na lista posições do barco que foi alocado
      posicoes.append(linha)
      valor = 0 #Zera o valor, ja que o barco ja foi alocado
      pintar(board) #Atualiza o tabuleiro
    else: #Caso a posição para colocar o barco não seja possivel
      lbl.config(text="Posição não valida!",bg="#CC3333",fg="#FFFFFF")


def pintar(board): #Função que pinta o tabuleiro da maneira correta
  global btt_tabu
  #Cores Representam: Agua, Acerto, Submarino, Navio Tanque, Contraporpedeiro, Porta Avioes 
  cores = ("#3399FF","#CC3333","#666666","#CC99FF","#003399","#663399")
  for x in range(0,8):
    for y in range(0,8):
      btt_tabu["btt"+str(x+1)+str(y+1)].config(bg=cores[int(board[x,y])])


def trocavalor(num): #Função que troca o valor da qtd de espaços que o barco ocupa
  global valor
  valor = num


def girar(lbl): #Função que gira a orientação do barco de horizontal para vertical e vice-versa
  global orientacao, lbl_ori
  if orientacao == True: #Caso o barco esteja na horizontal
    orientacao = False
    lbl.config(text="■\n■\n■")
  else: #Caso ele esteja na vertical
    lbl.config(text="■■■")
    orientacao = True


def verifica(board, posxf, posyf, posxi, posyi, tamb):  # Função para verificar se existe alguma posição já ocupada entre a posição inicial e final do barco
  flag = False  # Variavel flag para dizer se possui ou não erro
  if posxf > 7 or posyf > 7:
    flag = True
    return flag
  if posxi == posxf:  # caso posxi == posxf, significa que o barco está sendo colocado na horizontal
    if ((posyf - posyi) + 1) != tamb:  # Caso o barco esteja ocupando espaços a mais ou menos do que o devido
      flag = True
    i = posyi  # i = a posição inical de y do barco
    while i <= posyf:  # while para percorrer até a coluna de posição final de y
      if board[posxf, i] != 0:  # caso em algum momento o valor atual da matriz não seja igual a 0...
          flag = True  # Significa que já existe um barco lá. Ativando assim a flag de erro
      i += 1
  else:  # barco esta sendo posto na vertical
    if ((posxf - posxi) + 1) != tamb:  # Caso o barco esteja ocupando espaços a mais ou menos do que o devido
      flag = True
    i = posxi  # i = a posição inical de x do barco
    while i <= posxf:  # while para percorrer até a linha de posição final de x
      if board[i, posyi] != 0:  # caso em algum momento o valor atual da matriz não seja igual a 0...
          flag = True  # Significa que já existe um barco lá. Ativando assim a flag de erro
      i += 1
  return flag  # Retorna o estado atual da flag


def colocar(board, posxi, posxf, posyi, posyf, tam_b):  # Função que coloca na matriz os barcos pelo seu tamanho
  # Exemplo: O Porta-aviões será o valor 5 na matriz, pois ocupa 5 espaços. O submarino é o valor 2, pois ocupa 2 espaços.
  if posxi == posxf:  # sendo iguais significa que o barco sera posto na horizontal
    i = posyi  # i = a posição inical de y do barco
    while i <= posyf:  # while para percorrer até a coluna de posição final de y
      board[posxf, i] = int(tam_b)  # Aloca na posição um pedaço do barco, com o valor do total de espaços que ele ocupa
      i += 1
  else:  # caso contrario ele é posto na vertical
    i = posxi  # i = a posição inical de x do barco
    while i <= posxf:  # while para percorrer até a linha de posição final de x
      board[i, posyi] = int(tam_b)  # Aloca na posição um pedaço do barco, com o valor do total de espaços que ele ocupa
      i += 1
  return board  # Retorna o board com o barco já colocado


def troca(x, y):  # Função de troca de valores ente duas variaveis
  aux = x
  x = y
  y = aux
  return x, y  # Retorna as variaveis com valores trocados
