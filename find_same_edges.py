def find_one_same_edges(state, transitions_dict):
    # Проверяем, существует ли состояние в словаре
    if state not in transitions_dict:
        return f"State '{state}' not found in the transitions dictionary."

    # Извлекаем рёбра для заданного состояния
    target_edges = transitions_dict[state]
    
    same_edge_states = []

    # Сравниваем с другими состояниями
    for other_state, edges in transitions_dict.items():
        if other_state != state and edges == target_edges:
            same_edge_states.append(other_state)

    return same_edge_states

def find_all_same_edges(transitions_dict):
    result = []  # Список для хранения наборов с одинаковыми рёбрами
    seen = set()  # Множество для отслеживания уже добавленных наборов

    for state in transitions_dict.keys():
        same_edges = find_one_same_edges(state, transitions_dict)
        if same_edges and state not in seen:
            # Создаем множество состояний, включая текущее состояние и найденные одинаковые рёбра
            edge_set = {state}
            edge_set.update(same_edges)
            edge_set = tuple(sorted(edge_set))  # Сортируем и преобразуем в кортеж
            if edge_set not in seen:  # Проверяем, были ли уже добавлены такие состояния
                result.append(edge_set)
                seen.update(edge_set)  # Помечаем все состояния в наборе как просмотренные

    return result

def same_edges(transitions_dict):
    same_edges_groups = find_all_same_edges(transitions_dict)
    return same_edges_groups