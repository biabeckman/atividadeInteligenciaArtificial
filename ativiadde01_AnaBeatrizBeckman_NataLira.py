import os
import random
import time

class Environment:
    def __init__(self, width, height, num_clouds):
        self.width = width
        self.height = height
        self.clouds = set()
        self.goal_position = (width // 2, height - 1)
        self.agent_position = (width // 2, 0)

        # Garante que nuvens não sejam criadas na posição inicial do agente ou no objetivo
        while len(self.clouds) < num_clouds:
            cloud_x = random.randint(0, width - 1)
            cloud_y = random.randint(0, height - 1)
            if (cloud_x, cloud_y) != self.agent_position and (cloud_x, cloud_y) != self.goal_position:
                self.clouds.add((cloud_x, cloud_y))

    def display(self):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.clouds:
                    print('☁️', end=' ')
                elif (x, y) == self.agent_position:
                    print('🚀', end=' ')
                elif (x, y) == self.goal_position:
                    print('🌚', end=' ')
                else:
                    print(' ', end=' ')
            print()

    def get_perception(self):
        return self.agent_position, self.goal_position, self.clouds

class Agent:
    def __init__(self, environment):
        self.environment = environment
        self.position = (environment.width // 2, 0)
        self.history = set()
        self.history.add(self.position)

    def select_action(self, perception):
        agent_x, agent_y = self.position
        goal_x, goal_y = self.environment.goal_position
        clouds = self.environment.clouds

        # Define a prioridade dos movimentos: cima, direita, baixo, esquerda
        possible_moves = [
            (agent_x, agent_y + 1),  # Cima
            (agent_x + 1, agent_y),  # Direita
            (agent_x, agent_y - 1),  # Baixo
            (agent_x - 1, agent_y)   # Esquerda
        ]

        # Filtra movimentos válidos: dentro do grid, não em nuvens, e não repetidos
        valid_moves = [
            move for move in possible_moves
            if 0 <= move[0] < self.environment.width and
               0 <= move[1] < self.environment.height and
               move not in clouds and
               move not in self.history
        ]

        if valid_moves:
            # Seleciona a posição mais próxima do objetivo usando a distância Manhattan
            return min(valid_moves, key=lambda pos: abs(pos[0] - goal_x) + abs(pos[1] - goal_y))
        else:
            return self.position  # Fica na mesma posição se não houver movimentos válidos

    def update_state(self, new_position):
        self.history.add(self.position)
        self.position = new_position

def simulate(environment, agent, max_steps=150):
    steps = 0
    while steps < max_steps:
        os.system('cls' if os.name == 'nt' else 'clear')
        perception = environment.get_perception()
        new_position = agent.select_action(perception)
        agent.update_state(new_position)
        environment.agent_position = new_position
        environment.display()

        if new_position == environment.goal_position:
            print("Foi usado ", steps, "passos para chegar a LUA!")
            break

        steps += 1
        time.sleep(0.1)

    if steps == max_steps:
        print("Rocket did not reach the goal in the maximum number of steps.")

# Cria o ambiente e o agente
environment = Environment(50, 30, 150)
agent = Agent(environment)

# Exibe o ambiente inicial
environment.display()

# Executa a simulação
simulate(environment, agent, max_steps=150)
