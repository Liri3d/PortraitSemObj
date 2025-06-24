import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Any
import networkx as nx
import matplotlib.pyplot as plt

def find_keys_not_in_values(input_dict: Dict[str, List[Any]]) -> List[str]:

    # Собираем все значения, разворачивая списки в одно множество
    values_set = set(value for values in input_dict.values() for value in values)
    
    # Находим ключи, которых нет в значениях
    keys_not_in_values = [key for key in input_dict.keys() if key not in values_set]

    for key in keys_not_in_values:
        print(key)

    return keys_not_in_values[0]

def build_transitions(graph, start_edges, last_elements):
    transitions = {}
    state_counter = 0

    # Функция для создания нового состояния
    def get_new_state_name():
        nonlocal state_counter
        state_name = f'S{state_counter}'
        state_counter += 1
        return state_name

    # Получаем начальное состояние
    initial_state = get_new_state_name()
    transitions[initial_state] = {}  # Создаем начальное состояние

    # Создание завершающего состояния
    final_state = 'Z'
    transitions[final_state] = {}  # Создаем завершающее состояние

    # Вспомогательная структура для отслеживания переходов
    edge_to_state = {}

    # Начинаем обработку переходов
    def process_edge(edge, current_state):
        # Получаем все возможные переходы для данного ребра
        next_states = graph.get(edge, [])
        new_state = get_new_state_name()  # Получаем новое имя состояния
        transitions[current_state][edge] = new_state  # Создаем переход в словаре

        # Создаем новое состояние в transitions
        transitions[new_state] = {}

        # Запоминаем, что это ребро ведет к новому состоянию
        edge_to_state[edge] = new_state

        # Рекурсивно обрабатываем следующие переходы
        for next_edge in next_states:
            if next_edge in last_elements:
                transitions[new_state][next_edge] = final_state  # Переход к завершающему состоянию
            else:
                process_edge(next_edge, new_state)  # Обрабатываем рекурсивно

    # Сначала обрабатываем начальное состояние
    process_edge(start_edges, initial_state)

    # Теперь добавим переходы в завершенное состояние по last_elements
    for edge in last_elements:
        can_add_to_Z = True
        
        # Проверяем все состояния для наличия перехода к Z
        for state in transitions:
            if state != final_state and edge in transitions[state]:
                can_add_to_Z = False
                break
        if can_add_to_Z:
            transitions[final_state][edge] = ''  # Переход из Z в Z

    stack = [transitions]
        
    while stack:
        current_dict = stack.pop()
            
        for key, value in current_dict.items():
            if isinstance(value, dict):
                stack.append(value)
            elif value == '':
                current_dict[key] = 'Z'  # Заменяем пустое значение на 'Z'
                
    return transitions

def plot_graph(transitions):
    G = nx.DiGraph()
    
    for state, edges in transitions.items():
        for symbol, next_state in edges.items():
            G.add_edge(state, next_state, label=symbol)

    pos = nx.spring_layout(G)  # Позиции для всех узлов
    labels = nx.get_edge_attributes(G, 'label')
    
    # Рисуем граф
    plt.figure(figsize=(6, 4))  # Задайте размер графа
    nx.draw(G, pos, with_labels=True, arrows=True)
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.title("Graph of State Transitions")
    
    # Сохраняем граф как изображение
    plt.savefig("graph.png")
    plt.close()  # Закрываем текущее окно графика