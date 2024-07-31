import os
import random
import time
import heapq

class Ambiente:
    def __init__(self, largura, altura, num_nuvens):
        self.largura = largura
        self.altura = altura
        self.nuvens = set()
        self.posicao_objetivo = (largura // 2, altura - 1)
        self.posicao_agente = (largura // 2, 0)

        # Garante que nuvens não sejam criadas na posição inicial do agente ou no objetivo
        while len(self.nuvens) < num_nuvens:
            nuvem_x = random.randint(0, largura - 1)
            nuvem_y = random.randint(0, altura - 1)
            if (nuvem_x, nuvem_y) != self.posicao_agente and (nuvem_x, nuvem_y) != self.posicao_objetivo:
                self.nuvens.add((nuvem_x, nuvem_y))

    def exibir(self):
        for y in range(self.altura):
            for x in range(self.largura):
                if (x, y) in self.nuvens:
                    print('☁️', end=' ')
                elif (x, y) == self.posicao_agente:
                    print('🚀', end=' ')
                elif (x, y) == self.posicao_objetivo:
                    print('🌚', end=' ')
                else:
                    print(' ', end=' ')
            print()

    def obter_percepcao(self):
        return self.posicao_agente, self.posicao_objetivo, self.nuvens

class Agente:
    def __init__(self, ambiente):
        self.ambiente = ambiente
        self.posicao = (ambiente.largura // 2, 0)
        self.historico = set()
        self.historico.add(self.posicao)

    def selecionar_acao(self, percepcao):
        agente_x, agente_y = self.posicao
        objetivo_x, objetivo_y = self.ambiente.posicao_objetivo
        nuvens = self.ambiente.nuvens

        # Função heurística para o A* (distância de Manhattan)
        def heuristica(x, y):
            return abs(x - objetivo_x) + abs(y - objetivo_y)

        # Fila de prioridade para o A*
        fronteira = []
        heapq.heappush(fronteira, (0, self.posicao))

        # Dicionários para armazenar custos e caminhos
        custo = {self.posicao: 0}
        caminho = {self.posicao: None}

        while fronteira:
            _, atual = heapq.heappop(fronteira)

            if atual == self.ambiente.posicao_objetivo:
                # Reconstruir o caminho
                caminho_ate_objetivo = []
                while atual is not None:
                    caminho_ate_objetivo.append(atual)
                    atual = caminho[atual]
                return caminho_ate_objetivo[-2]  # Retorna a posição antes da atual

            for movimento in [
                (atual[0], atual[1] + 1),  # Cima
                (atual[0] + 1, atual[1]),  # Direita
                (atual[0], atual[1] - 1),  # Baixo
                (atual[0] - 1, atual[1])   # Esquerda
            ]:
                if 0 <= movimento[0] < self.ambiente.largura and \
                0 <= movimento[1] < self.ambiente.altura and \
                movimento not in nuvens:

                    novo_custo = custo[atual] + 1
                    if movimento not in custo or novo_custo < custo[movimento]:
                        custo[movimento] = novo_custo
                        prioridade = novo_custo + heuristica(movimento[0], movimento[1])
                        heapq.heappush(fronteira, (prioridade, movimento))
                        caminho[movimento] = atual

        return self.posicao

    def atualizar_estado(self, nova_posicao):
        self.historico.add(self.posicao)
        self.posicao = nova_posicao

def simular(ambiente, agente, max_passos=150):
    passos = 0
    while passos < max_passos:
        os.system('cls' if os.name == 'nt' else 'clear')
        percepcao = ambiente.obter_percepcao()
        nova_posicao = agente.selecionar_acao(percepcao)
        agente.atualizar_estado(nova_posicao)
        ambiente.posicao_agente = nova_posicao
        ambiente.exibir()

        if nova_posicao == ambiente.posicao_objetivo:
            print("Foi usado ", passos, "passos para chegar a LUA!")
            break

        passos += 1
        time.sleep(0.1)

    if passos == max_passos:
        print("O foguete não alcançou o objetivo no número máximo de passos.")

# Cria o ambiente e o agente
ambiente = Ambiente(30, 25, 100)
agente = Agente(ambiente)

# Exibe o ambiente inicial
ambiente.exibir()

# Executa a simulação
simular(ambiente, agente, max_passos=150)
