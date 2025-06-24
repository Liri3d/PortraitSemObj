def main_find_duplicate(transitions_dict):
    # Находим входные и выходные рёбра
    edges_info = find_edges(transitions_dict)
    # Ищем дубликаты
    duplicates = find_duplicate_states(edges_info)
    return duplicates

# Находим входные и выходные рёбра
def find_edges(transitions):
    edges_info = {}

    # Инициализация словаря для всех состояний
    for state in transitions.keys():
        edges_info[state] = {
            'incoming': set(),
            'outgoing': set()
        }
    # Заполнение выходных и входных рёбер
    for state, edges in transitions.items():
        for edge, next_state in edges.items():
            edges_info[state]['outgoing'].add(edge)
            edges_info[next_state]['incoming'].add(edge)

    return edges_info

# Ищем дубликаты
def find_duplicate_states(edges_info):
    seen_states = {}
    duplicates = []

    # Проходим по состояниям в обратном порядке
    for state in reversed(edges_info.keys()):
        key = (frozenset(edges_info[state]['incoming']), frozenset(edges_info[state]['outgoing']))

        if key in seen_states:
            seen_states[key].add(state)  # Добавляем состояние в множество дубликатов
        else:
            seen_states[key] = {state}  # Создаем новое множество с текущим состоянием

    # Преобразуем множества дубликатов в список пар
    for states in seen_states.values():
        if len(states) > 1:  # Если есть более одного дубликата
            duplicates.append(states)

    return duplicates