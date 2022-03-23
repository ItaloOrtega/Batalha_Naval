from tkinter import *
from usuario import *

#Criação dos obejtos cpu e usuario vazios
user = " "
cpu = " "
#Dicionarios vazios dos botões e lbls
btt_tabu = {}
lbls_tabu = {}
#Lbl atual que é onde mostra se é o tabuleiro do usario ou de ataque
lbl_atual = " "

def sair(): #Função sai da aplicação toda
  quit()


def dados(modo): #Função que atualiza/mostra o board de consulta ou de ataque 
  global btt_tabu, lbl_atual
  if modo is True: #Caso for true, significa que o usario quer trocar o board que esta sendo mostrado
    if lbl_atual['text'] == "Tabuleiro Usuário":
      lbl_atual.config(text="Tabuleiro de Ataque")
      board = user.consulta
    elif lbl_atual['text'] == "Tabuleiro de Ataque":
      lbl_atual.config(text="Tabuleiro Usuário")
      board = user.board
  else: #Senão é so para atualizar os locais atacados pelo usuario/CPU
    if lbl_atual['text'] == "Tabuleiro Usuário":
      board = user.board
    elif lbl_atual['text'] == "Tabuleiro de Ataque":
      board = user.consulta
  '''
  Significado de cada cor:
  Agua = #3399FF
  Acerto = #CC3333
  Submario = #666666
  Navio tanque = #CC99FF
  Contratorpedeiro = #003399
  Porta-Aviões = #663399
  Erro = #000066
  '''
  cores = ("#3399FF","#CC3333","#666666","#CC99FF","#003399","#663399","#000066")
  #Fors para atualizar cada botão do tabuleiro
  for x in range(0,8):
    for y in range(0,8):
      btt_tabu["btt"+str(x+1)+str(y+1)].config(bg=cores[int(board[x,y])])
      if int(board[x,y]) != 0 or lbl_atual['text'] == "Tabuleiro Usuário":
        #Se for o tabuleiro do usario ele não pode cliar em nenhum botão
        btt_tabu["btt"+str(x+1)+str(y+1)].config(state='disabled')
      elif lbl_atual['text'] == "Tabuleiro de Ataque" and int(board[x,y]) == 0:
        #Se for o tabuleiro de ataque ele pode
        btt_tabu["btt"+str(x+1)+str(y+1)].config(state='normal')


def placar():
  pop_up = Toplevel()
  pop_up.title("Placar Atual do Jogo")
  larg_s = pop_up.winfo_screenwidth() # largura da tela do usuario
  alt_s = pop_up.winfo_screenheight() # altura da tela do usuario
  #calcaula as coordenadas para mostrar a tela da aplicação no meio do monitor
  a = (larg_s/2) - (310/2)
  b = (alt_s/2) - (175/2)
  pop_up.geometry('%dx%d+%d+%d' % (310, 175, a, b-50)) #Aloca a nova tela, para que mostre o resultado do usuario
  pop_up.geometry("310x175") #Coloca o tamanho da tela como 310x175 pixels
  pop_up.resizable(False, False) #Desabilita a redimensão da janela
  pop_up.configure(bg= "#CCCCCC")
  lbl_pop = Label(pop_up, text="Placar", bg= "#3399FF", fg="#FFFFFF", font= "Calibri 15 bold")
  lbl_pop.grid(row=0, column=0, columnspan=20)
  #Labels para melhor visualização dos botões
  lbl_aux1 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux1.grid(row=1, column=0, columnspan=20)
  lbl_aux2 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux2.grid(row=2, column=0)
  lbl_aux3 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux3.grid(row=2, column=2)
  lbl_aux4 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux4.grid(row=2, column=4)
  #Botões de resposta do usuário
  btt_sim = Label(pop_up, text=f'Jogador:\n{user.acertos}', padx= 10,pady=25, bg="#66CC33", fg="#000000",font= "Calibri 15 bold")
  btt_nao = Label(pop_up, text=f'CPU:\n{cpu.acertos}', padx= 35, pady=25, bg="#3333FF", fg="#000000",font= "Calibri 15 bold")
  btt_sim.grid(row=2, column= 1)
  btt_nao.grid(row=2, column= 3)

def botao(tela,x,y): #Função para criação de um botão corretamente
  btt = Button(tela,text="  ", padx=15, pady=15, bg="#3399FF", fg="#000000", command=lambda:seleciona(tela,x,y))
  return btt

def seleciona(tela,x,y): #Função onde um botão é selecionado para atacar o CPU
  turno = True
  # While feito até o usuário ou o CPU conseguir 16 pontos, ou seja, derrubar todos os barcos do adversário
  if user.acertos < 16 and cpu.acertos < 16:
    hit = True  # Varivael de acerto em um barco pela coordenada
    if hit is True and turno is True:  # Enquanto ocorrer erros de coordenada ou caso de acertos, ocorre esse while   
      # Board do usuário, Board do usuário de consulta, variaveis flag e hit recebem o resultado da função AcertoErro
      # Um acerto ou um erro é feito em cima do board do CPU.
      cpu.board, user.consulta, hit, user.acertos = AcertoErro(cpu.board, user.consulta, hit, x, y, user.acertos)
      btt_tabu["btt"+str(x+1)+str(y+1)].config(state='disabled')
      if hit is False: #Caso não tenha sido um acerto, turno vira false e vai para a vez do CPU
        turno = False
    # Só vai para a vez do CPU, se o usuário ainda não tenha ganhado e ja tenha passado o turno
    if user.acertos < 16 and turno is False:
      flag = True  # Variavel de erro de coordenada
      hit = True  # Varivael de acerto em um barco pela coordenada
      while flag is True or hit is True:  # Enquanto ocorrer erros de coordenada ou caso de acertos, ocorre esse while
        hit = False  # Desativa a variável hit
        while flag is True:  # while que ocorre até ter uma coordenada valida de bombardeamento
          flag = False  # Desativa a variavel de erro
          escolha1 = "z"
          if cpu.last_hit != " ":
            escolha1 = random.choice(["x", "y","z"])  # Gera uma escolha entre x,y e z, onde ...
            # x simboliza que a próxima coordenada vai se manter na linha do ultimo acerto
            # y simboliza que a proxima coordenada vai se manter na coluna do ultimo acerto
            # z simboliza que a proxima coordenada vai ser aleatoria

          # Caso tenha ocorrido um acerto anteriormente pelo CPU, e ter sido escolhido manter-se naquela coordenada
          if (escolha1 == "x" or escolha1 == "y") and cpu.last_hit != " ":
            x,y = cpu.last_hit.split(",") #Recebe o valor do ultimo acerto
            x = int(x)
            y = int(y)
            # Este if é para o caso do CPU manter na linha
            if escolha1 == "x" and (x+1 <= 7 or x-1 >= 0):
              #Para ser possivel se manter na coluna,para cima ou para baixo deve ser possivel se movimentar
              escolha2 = random.choice(["+", "-"])  # É feita uma escolha para ir para cima, -, ou para baixo, +
              # Sendo possivel ir para cima, x+1 <= 7, e a coordenada não tendo sido escolhida anteriormente
              if escolha2 == "+" and x+1 <= 7 and cpu.consulta[x+1, y] == 0:
                x += 1  # O X é incrementado em 1
              # Ocorre o mesmo logo abaixo, so que é o caso de se movimentar para cima, subtraindo 1 de X
              elif cpu.consulta[x-1, y] == 0:
                if x - 1 >= 0:
                  x -= 1
            # Ocorre o mesmo que no caso anterior, mas ligado o CPU se mantendo na mesma linha ...
            # E se movimentando somente para esquerda ou  pelas colunas, Y
            elif escolha1 == "y" and (y+1 <= 7 or y-1 >= 0):
              escolha2 = random.choice(["+", "-"])
              if escolha2 == "+" and y+1 <= 7 and cpu.consulta[x, y+1] == 0:
                y += 1
              elif cpu.consulta[x, y-1] == 0:
                if y-1 >= 0:
                  y -= 1
          else:
            # Gera aleatoriamente valores para o X e o Y, podendo ir de 0 até 7
            x = random.randint(0, 7)
            y = random.randint(0, 7)

          if cpu.consulta[x, y] != 0:  # If que verifica se o CPU já utilizou ou não está coordenada
            flag = True  # Coordenada já sendo utilizada, a flag é ativada para que outra coordenada seja gerada
        # Board do CPU, Board do CPU de consulta, hit recebem o resultado da função AcertoErro
        # Um acerto ou um erro é feito em cima do board do usuário.
        user.board, cpu.consulta, hit, cpu.acertos = AcertoErro(user.board, cpu.consulta, hit, x, y, cpu.acertos)

        if hit is True:  # Caso tenha um acerto pelo CPU, flag é ativada e é copiado esse ultimo acerto
          cpu.last_hit = str(x)+","+str(y)
          flag = True
        else:
          turno = True
  dados(False) #Atualiza as posições que foram bombardeadas
  if user.acertos == 16 or cpu.acertos == 16: #Caso alguem tenha vencido
    placar() #Mostra o placar final
    final(tela) #E chama a função final


def criar(pop_up, resp): #Função para criar os objetos usuario e adversario para o jogo
  global user, cpu
  cpu = Adversario(False, "")
  aloc = False
  if resp == True:#Caso resp for true significa que o usuario deseja alocar os seus proprios barcos
    #Então criamos a tela para a alocação deles
    aloc = Tk()
    aloc.configure(bg= "#CCCCCC")
    aloc.title("Batalha Naval")
    aloc.protocol("WM_DELETE_WINDOW", quit) #Coloca o X da janela para sair da aplicação toda
    #Largura e altura da tela
    larg = 650
    alt = 590
    #Calcula as dimensões da tela que esta sendo usado pelo usuario
    larg_s = aloc.winfo_screenwidth() # largura da tela do usuario
    alt_s = aloc.winfo_screenheight() # altura da tela do usuario
    #calcaula as coordenadas para mostrar a tela da aplicação no meio do monitor
    a = (larg_s/2) - (larg/2)
    b = (alt_s/2) - (alt/2)
    aloc.geometry('%dx%d+%d+%d' % (larg, alt, a, b-50))
    aloc.resizable(False, False) #Desabilita a redimensão da janela
  pop_up.destroy() #Fecha essa tela
  user = Usuario(resp, aloc) #Cria o usuario
  jogar() #Chama a função jogar e o jogo é iniciado

# Função que verifica se teve um acerto ou um erro durante o jogo
def AcertoErro(board_inimigo, board_consulta, hit, x, y, contador):
  # Caso o board inimigo tenha um barco lá e a posição não ter sido ainda escolhida
  if board_inimigo[x, y] != 0 and board_consulta[x, y] == 0:
    contador += 1  # Incrementa no contator de pontos 1 ponto
    if contador < 16:  # Caso o contador seja menor que 16, que é o valor máximo possível...
      hit = True
    board_consulta[x, y] = 1  # Mostra no board de consulta que teve um acerto naquela posição
    board_inimigo[x, y] = 1  # Coloca no board inimigo 6 na posição que o barco foi atacada

  else:  # Caso não tenha acertado nenhum barco, somente na água
    board_consulta[x, y] = 6  # Mostra no board de consulta que teve um erro naquela posição
    board_inimigo[x, y] = 6
    hit = False
  # Retorna os boards atualizadas, variaveis acionadas ou não e o contador
  return board_inimigo, board_consulta, hit, contador 


def jogar(): #Função que cria a tela onde ocorrera as jogadas de ataque, o jogo em si
  global lbl_atual
  tela = Tk() #Tela principal
  tela.configure(bg= "#CCCCCC")
  tela.title("Batalha Naval")
  #Largura e altura da tela
  larg = 440
  alt = 600
  #Calcula as dimensões da tela que esta sendo usado pelo usuario
  larg_s = tela.winfo_screenwidth() # largura da tela do usuario
  alt_s = tela.winfo_screenheight() # altura da tela do usuario
  #calcaula as coordenadas para mostrar a tela da aplicação no meio do monitor
  a = (larg_s/2) - (larg/2)
  b = (alt_s/2) - (alt/2)
  tela.geometry('%dx%d+%d+%d' % (larg, alt, a, b-50))
  tela.resizable(False, False) #Desabilita a redimensão da janela
  for i in range(0,8): #Cria todos os botões que seram possiveis selecionar
    for j in range(0,8):
      btt_tabu["btt"+str(i+1)+str(j+1)] = botao(tela,i,j) #Cria o botão 
      btt_tabu["btt"+str(i+1)+str(j+1)].grid(row=6+i, column=j+2) #Aloca ele no grid
    #Legenda horizontal e vertical para os valores
    lbls_tabu["lbl_x"+str(i+1)] = Label(tela, text=str(i+1), bg= "#CCCCCC",font= "Calibri 10 bold")
    lbls_tabu["lbl_x"+str(i+1)].grid(row=5, column=2+i)
    lbls_tabu["lbl_y"+str(i+1)] = Label(tela, text=str(i+1)+" ", bg= "#CCCCCC",font= "Calibri 10 bold")
    lbls_tabu["lbl_y"+str(i+1)].grid(row=6+i, column=1)
  #Labels para melhor visualização dos botões
  lbl_aux1 = Label(tela, text="    ", bg= "#CCCCCC",font= "Calibri 10")
  lbl_aux1.grid(row=0, column=0, columnspan=20)
  lbl_aux2 = Label(tela, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux2.grid(row=2, column=0)
  lbl_aux3 = Label(tela, text="    ", bg= "#CCCCCC",font= "Calibri 5")
  lbl_aux3.grid(row=4, column=0)
  
  #Bões de trocar os tabuleiros e vizualizar o placar
  btt_troca = Button(tela, text="↺", padx=5,pady=5, command=lambda:dados(True), bg= "#CCCCCC",font= "Calibri 15")
  btt_troca.config()
  btt_troca.grid(row=1, column=5)
  btt_placar = Button(tela, text="P", padx=5,pady=5, command=placar, bg= "#CCCCCC",font= "Calibri 15")
  btt_placar.grid(row=1, column=6)

  #Label que diz qual é o tabuleiro que está sendo visualizado no momento
  lbl_atual = Label(tela, text="Tabuleiro Usuário", bg= "#CCCCCC",font= "Calibri 16")
  lbl_atual.grid(row=3, column=1, columnspan=20)

  tela.bind('<Escape>', lambda event:sair()) #Aloca a tecla Esc para sair do pop up de ajuda
  dados(False) #Atualiza cada botão
  tela.mainloop()


def final(tela): #Função de quando o jogo é finalizado, para jogar novamente ou não
  tela.destroy()
  pop_up = Tk()
  pop_up.title("Jogar Novamente?")
  larg_s = pop_up.winfo_screenwidth() # largura da tela do usuario
  alt_s = pop_up.winfo_screenheight() # altura da tela do usuario
  #calcaula as coordenadas para mostrar a tela da aplicação no meio do monitor
  a = (larg_s/2) - (310/2)
  b = (alt_s/2) - (290/2)
  pop_up.geometry('%dx%d+%d+%d' % (310, 290, a, b-50)) #Aloca a nova tela, para que mostre o resultado do usuario
  pop_up.geometry("310x290") #Coloca o tamanho da tela como 310x175 pixels
  pop_up.resizable(False, False) #Desabilita a redimensão da janela
  pop_up.configure(bg= "#CCCCCC")
  pop_up.protocol("WM_DELETE_WINDOW", quit) #Coloca o X da janela para sair da aplicação toda
  lbl_vencedor = Label(pop_up, text="", bg= "#3399FF", fg="#FFFFFF", font= "Calibri 15")
  if user.acertos == 16: #Caso o usuario tenha 16 pontos
    lbl_vencedor.config(text="Parabéns! Você ganhou!")
  else: #Senão
    lbl_vencedor.config(text="Que pena! Você perdeu!")
  lbl_vencedor.grid(row=0, column=0, columnspan=20)
  lbl_pop = Label(pop_up, text="Deseja Jogar Novamente?", bg= "#3399FF", fg="#FFFFFF", font= "Calibri 15")
  lbl_pop.grid(row=1, column=0, columnspan=20)
  #Labels para melhor visualização dos botões
  lbl_aux1 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux1.grid(row=2, column=0, columnspan=20)
  lbl_aux2 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux2.grid(row=3, column=0)
  lbl_aux3 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux3.grid(row=3, column=2)
  lbl_aux4 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux4.grid(row=3, column=4)
  lbl_aux5 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux5.grid(row=4, column=0, columnspan=20)
  #Botões de resposta do usuário
  btt_sim = Button(pop_up, text='↺', padx=35, pady=25, bg="#66CC33", fg="#000000",command=lambda:again(pop_up), font= "Calibri 35")
  btt_nao = Button(pop_up, text='✖',padx=35, pady=25, bg="#CC0000", fg="#000000", command=sair, font= "Calibri 35")
  btt_sim.grid(row=3, column= 1)
  btt_nao.grid(row=3, column= 3)
  lbl_placarf = Label(pop_up, text=f"Placar Final\nVocê = {user.acertos} | CPU = {cpu.acertos}", bg= "#333366", fg="#FFFFFF", font= "Calibri 15")
  lbl_placarf.grid(row=5, column=0, columnspan=20)
  pop_up.bind('<Escape>',lambda event:sair()) #Aloca a tecla Esc para sair do pop up de ajuda
  pop_up.mainloop()


def again(aux): #Função que fecha o pop up de jogar novamente e cria denovo o tabuleiro, jogador e cpu
  aux.destroy()
  inicio()


def inicio(): #Função do inicio da aplicação, onde o usario escolhe se quer alocar seus barcos ou não
  pop_up = Tk()
  pop_up.attributes("-topmost", True)
  pop_up.title("Inicio de Jogo")
  larg_s = pop_up.winfo_screenwidth() # largura da tela do usuario
  alt_s = pop_up.winfo_screenheight() # altura da tela do usuario
  #calcaula as coordenadas para mostrar a tela da aplicação no meio do monitor
  a = (larg_s/2) - (550/2)
  b = (alt_s/2) - (240/2)
  pop_up.geometry('%dx%d+%d+%d' % (550, 240, a, b-50))
  pop_up.geometry("550x240")
  pop_up.resizable(False, False) #Desabilita a redimensão da janela
  pop_up.configure(bg= "#CCCCCC")
  pop_up.protocol("WM_DELETE_WINDOW", quit) #Coloca o X da janela para sair da aplicação toda
  lbl_aux0 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux0.grid(row=0, column=0, columnspan=20)
  lbl_pop = Label(pop_up, text="Deseja alocar suas embarcações\nOU\nQue sejam alocadas para você aleatoriamente?", fg="#000000", font= "Calibri 15")
  lbl_pop.grid(row=1, column=0, columnspan=20)

  #Labels para melhor visualização dos botões
  lbl_aux1 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux1.grid(row=2, column=0, columnspan=20)
  lbl_aux2 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux2.grid(row=3, column=0)
  lbl_aux3 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux3.grid(row=3, column=2)
  lbl_aux4 = Label(pop_up, text="    ", bg= "#CCCCCC",font= "Calibri 15")
  lbl_aux4.grid(row=3, column=4)

  #Botões de resposta do usuário
  btt_sim = Button(pop_up, text='✓Alocalar', padx=50, pady=20, bg="#9999FF", fg="#000000",command= lambda: criar(pop_up, True), font= "Calibri 20")
  btt_nao = Button(pop_up, text='➲Aleatoriezar', padx=20, pady=20, bg="#993399", fg="#000000", command= lambda: criar(pop_up, False), font= "Calibri 20")
  btt_sim.grid(row=3, column= 1)
  btt_nao.grid(row=3, column= 3)

  pop_up.bind('<Escape>', lambda event:sair()) #Aloca a tecla Esc para sair do pop up de ajuda
  pop_up.mainloop()

inicio() #chama função inicio, para começar a aplicação