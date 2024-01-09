from mtr import MTR

# Cria instância da classe MTR
mt = MTR()

# strip() => retorna string após remocao de caracteres brancos no inicio e no final
# split() => separa strings em substrings e retorna listas, recebe como parametro o separador das strings, no caso o caractere branco: ' '

# A seguir, as variaveis da primeira linha do arquivo
numEstados, inTamAlfabeto, outTamAlfabeto, numTransicoes = [int(i.strip()) for i in input().strip().split(' ')]

# Variavel que recebe os estados, segunda linha do arquivo
estados = input().strip().split(' ')

# Alfabeto da entrada, terceira linha
inputAlfabeto = input().strip().split(' ')
mt.setInputAlfabeto(inputAlfabeto)

# Alfabeto de saída, quarta linha
outputAlfabeto = input().strip().split(' ')
mt.setOutputAlfabeto(outputAlfabeto)

# Adiciona os estados na Maquina de Turing Reversível
for i in range(numEstados):
    mt.addEstado(estados[i])

# Adiciona as transicoes na Máquina de Turing Reversível
for i in range(0, numTransicoes):
    _in, _out = input().strip().split('=')
    _in = _in.strip('()').split(',')
    _out = _out.strip('()').split(',')
    mt.addTransicao(_in[0], _in[1], _out[0], _out[1], _out[2])

# Variavel que recebe a ultima linha do arquivo, a fita de entrada
inputFita = list(input().strip())

# Adiciona caracteres na fita, verificando se o alfabeto da fita faz parte do alfabeto de entrada da Máquina de Turing.
mt.setInputFita(inputFita)

# Chama a funcao que roda a Máquina de Turing
mt.rodar()


