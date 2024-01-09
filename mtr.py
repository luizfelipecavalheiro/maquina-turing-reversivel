class MTR:
    # Construtor da classe MTR
    def __init__(self):
        self.estados = []
        self.entradaAlfabeto = []
        self.saidaAlfabeto = []

        self.estadoAtual = None
        self.estadoInicial = None
        self.estadoFinal = None
        self.funcoesTransicao = []
        self.branco = 'B'

        self.fitas = {
            'input': [],
            'history': [],
            'output': []
        }
        self.cabecalhos = {
            'input': 0,
            'history': 0
        }      
 
    class Transicao:
        #Construtor da classe Transicao
        def __init__(self, estadoAnterior, simboloEntrada, estadoSeguinte, simboloSaida, direcao):
            self.estadoAnterior = estadoAnterior
            self.simboloEntrada = simboloEntrada
            self.estadoSeguinte = estadoSeguinte
            self.simboloSaida = simboloSaida
            self.direcao = direcao

            # Quadruplas para representar a Máquina de Turing Reversível
            self.setLeEscreveQuadrupla()
            self.setDeslocamentoQuadrupla()

        def setLeEscreveQuadrupla(self):
            self.quadrupla = {
                'estadoAnterior': self.estadoAnterior, 
                'simboloEntrada': self.simboloEntrada,
                'simboloSaida': self.simboloSaida,
                'estadoTemporario': self.estadoAnterior + "_"
            }
        
        def setDeslocamentoQuadrupla(self):
            self.deslocamentoQuadrupla = {
                'estadoTmp': self.estadoAnterior + "_",
                'espacoEmBranco': '/',
                'direcao': self.direcao,
                'estadoSeguinte': self.estadoSeguinte
            }
          
        # Retorna uma representacao de string do objeto
        def __str__(self):
            return "(" + self.estadoAnterior + "," + self.simboloEntrada + ")=(" + self.estadoSeguinte + "," + self.simboloSaida + "," + self.direcao + ")"

    # Retorna a transicao e o indice dela
    def getTransicao(self, estado, simbolo):
        i = 0
        # Para cada um das transicoes, caso o simbolo do parametro seja igual ao simbolo de entrada e o estado seja igual ao estado anterior (primeira parte da funcao de transicao), retorna a transicao e seu indice, caso não encontre, encerra
        for transicao in self.funcoesTransicao:
            if transicao.estadoAnterior == estado and transicao.simboloEntrada == simbolo:
                return transicao, i
            i += 1
        exit()        
    
    # Adiciona estado
    def addEstado(self, label):
        label = label.strip()
        # Se não tiver estado atual, o estado atual, é o inicial
        if self.estadoAtual is None:
            self.estadoInicial = label
            self.estadoAtual = label  
        # Estado "label" é adicionada a lista de estados
        self.estados.append(label)
        # Atualiza o estado final
        self.estadoFinal = label
      
    # Adiciona transicao
    def addTransicao(self, estadoAnterior, simboloEntrada, estadoSeguinte, simboloSaida, direcao):
        if estadoAnterior in self.estados:
            if estadoSeguinte in self.estados:
                transicao = self.Transicao(estadoAnterior, simboloEntrada, estadoSeguinte, simboloSaida, direcao)
                self.funcoesTransicao.append(transicao)
            else:
                exit("estado ", estadoSeguinte, " inexistente")
        else:
            exit("estado ", estadoAnterior, " inexistente")

    # Cada simbolo que faz parte do alfabeto de entrada descrito no arquivo, é adicionado ao alfabeto de entrada da máquina, o caractere branco é adicionado ao fim
    def setInputAlfabeto(self, entradaAlfabeto):
        for simbolo in entradaAlfabeto:
            self.entradaAlfabeto.append(simbolo)
        self.entradaAlfabeto.append(self.branco)
    
    # Cada simbolo que faz parte do alfabeto de saida descrito no arquivo, é adicionado ao alfabeto de saida da máquina
    def setOutputAlfabeto(self, saidaAlfabeto):
        for simbolo in saidaAlfabeto:
            self.saidaAlfabeto.append(simbolo)
    
    # Adiciona caracteres na fita
    def setInputFita(self, fita):
        # Para cada simbolo da fita verifica se faz parte do alfabeto de entrada da Máquina de Turing.
        for simbolo in fita:
            if simbolo not in self.entradaAlfabeto:
                exit("O símbolo ", simbolo, " não pertence ao alfabeto de entrada.")
        # Caso todos os simbolos sejam parte do alfabeto de entrada, a fita da máquina recebe a fita verificada adicionando o caractere branco no final
        self.fitas['input'] = fita
        self.fitas['input'].append(self.branco)

    # Se for reverso, avança a cabeça da fita e a fita de entrada recebe a fota de saida, caso não seja reverso, escreve a saida na fita de  entrada e avança para o próximo estado, avançando a cabeça da fita
    
    def executaIda(self):
        while True:
            # Se o estado atual for o final e a pos do cabecalho da fita de entrada, for maior que a propria fita, atualiza o cabecalho de history pra pos final da fita history, já não há mais nada para ler
            if self.estadoAtual == self.estadoFinal and self.cabecalhos['input'] >= len(self.fitas['input']):
                self.cabecalhos['history'] = len(self.fitas['history']) - 1
                return             
            # simbolo atual é aquele sobre o qual esta a cabeca da fita entrada
            simboloAtual = self.fitas['input'][self.cabecalhos['input']]
            # Retorna a transicao e seu indice
            transicao, indiceTransicao = self.getTransicao(self.estadoAtual, simboloAtual)
            # Adiciona o indice de transicao na fita historico
            self.fitas['history'].append(indiceTransicao)

            print("Fita de Entrada\t", self.fitas['input'], "\nHistory\t", self.fitas['history'])

            
            # Escreve o simbolo de saida na fita de entrada
            self.fitas['input'][self.cabecalhos['input']] = transicao.quadrupla['simboloSaida']
          
            # Avança para o próximo estado
            self.estadoAtual = transicao.deslocamentoQuadrupla['estadoSeguinte']
            # Avança a cabeça da fita de entrada
            if transicao.deslocamentoQuadrupla['direcao'] == 'R':
                self.cabecalhos['input'] += 1
            elif transicao.deslocamentoQuadrupla['direcao'] == 'L':
                self.cabecalhos['input'] -= 1
            

    def executaVolta(self):
        while True:
            # Se chegou no estado inicial e a pos. cabecalho de entrada for 0 para a maquina, já chegou ao fim
            if self.estadoAtual == self.estadoInicial and self.cabecalhos['input'] == 0:
                return
              
            # Indice da transicao será o indice da cabeca de history
            indiceTransicao = self.fitas['history'][self.cabecalhos['history']]
            transicao = self.funcoesTransicao[indiceTransicao]

            # Avança a cabeça da fita
            if transicao.deslocamentoQuadrupla['direcao'] == 'L':
                self.cabecalhos['input'] += 1
            elif transicao.deslocamentoQuadrupla['direcao'] == 'R':
                self.cabecalhos['input'] -= 1
            
            # Fita de entrada recebe o simbolo de entrada da funcao de transicao, pois está voltando, lê a primeira parte da transicao
            self.fitas['input'][self.cabecalhos['input']] = transicao.quadrupla['simboloEntrada']

            # estadoAtual é o estado anterior, da primeira parte da transicao
            self.estadoAtual = transicao.quadrupla['estadoAnterior']
          
            print("Fita de Entrada\t", self.fitas['input'], "\nHistory\t", self.fitas['history'])

            # exclui o ultimo elemento da fita history e atualiza o cabeçalho
            self.fitas['history'].pop()
            self.cabecalhos['history'] -= 1
         
    # Salva a entrada na fita de saida
    def copiaDaEntradaParaSaida(self):
        self.fitas['output'] = self.fitas['input'].copy()

    def rodar(self):
        # Fase 1 da Máquina de Turing Reversivel:
        print("FASE 1 -> COMPUTA DA ESQUERDA PARA A DIREITA:")
        self.executaIda()

        # Fase 2 da Máquina de Turing Reversivel:
        print("\nFASE 2 -> COPIA DA ENTRADA PARA A SAIDA")
        self.copiaDaEntradaParaSaida()

        # Fase 3 da Máquina de Turing Reversivel:
        print("\nFASE 3 -> REVERTE (DIREITA PARA A ESQUERDA):")
        self.executaVolta()

        print("\nConcluido!!!\n")
        print('Fita de Entrada:', self.fitas['input'])
        print('Fita de Saída:  ', self.fitas['output'])
        print('Histórico funcoes de transicao: ', self.fitas['history'])
        