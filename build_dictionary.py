import dictionary_of_transitions.find_same_edges as find_same_edges
import dictionary_of_transitions.find_duplicate as find_duplicate
import dictionary_of_transitions.replace as replace

transitions = {}
state_counter = -1

# Функция для создания нового состояния
def get_new_state_name():
    global state_counter
    state_counter += 1
    state_name = f'S{state_counter}'
    
    return state_name
        
# Построение начального словаря
def build_transitions(graph, start_edges, last_elements):
    global state_counter
    # Получаем начальное состояние
    initial_state = get_new_state_name()
    transitions[initial_state] = {}  # Создаем начальное состояние

    # Создание завершающего состояния
    final_state = 'Z'
    transitions[final_state] = {} 

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
    for edge in start_edges:
        process_edge(edge, initial_state)

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

# Объединение вершин с одинаковыми вход и выход характеристиками
def replace_pre_aft_duplicate(transitions):

    # Замена состояний с одинаковыми вход и выход характеристиками
    duplicates = find_duplicate.main_find_duplicate(transitions)

    while duplicates:
        duplicates = find_duplicate.main_find_duplicate(transitions)  

        if duplicates:
            new_state = get_new_state_name()
            for duplicate in duplicates[0]: 
                # Переименуем состояние
                transitions = replace.replace_name_state(transitions, duplicate, new_state)
    return transitions

def delete_repeat_edges(transitions):
    # Создаём новый словарь для хранения переходов без повторений
    unique_transitions = {}

    for state, edges in transitions.items():
        # Используем множество для удаления повторяющихся ребер
        # edges можно преобразовать в множество и затем обратно в список
        unique_transitions[state] = list(set(edges))

    return unique_transitions

def build_main_dict(transitions, start_edges, last_elements):
    
    # Удаляем дублирующиеся ребра (характеристики)
    transitions = delete_repeat_edges(transitions)

    print("Граф без повторений ", transitions)

    # Построение стартового словаря переходов
    transitions = build_transitions(transitions, start_edges, last_elements)
    print("Стартовый словарь\n", transitions)

    # Ищем состояния с одинаковыми вход и выход характеристикам, объединяем их
    transitions = replace_pre_aft_duplicate(transitions)
    print("Словарь после замены дублирующихся\n", transitions)

    # Найдём состояния с одинаковыми рёбрами для состояния 'S0'
    same_edges_groups = find_same_edges.same_edges(transitions)

    # Объеденим состояния
    for group in same_edges_groups:
        new_name = get_new_state_name()
        for state in group:
            
            replace.replace_name_state(transitions, state, new_name)

    print("Словарь после замены сост с одинаковыми edges", transitions)

    return transitions