# Замена состояний
def replace_name_state(transitions, old_name, new_name):
    # Проверяем, существует ли старое состояние
    if old_name not in transitions:
        print(f"Состояние {old_name} не найдено.")
        return

    # Сохраняем переходы для старого состояния
    old_transitions = transitions[old_name]

    # Удаляем старое состояние
    del transitions[old_name]

    # Обновляем все переходы, ссылающиеся на старое состояние
    for state, edges in transitions.items():
        for edge in edges.keys():
            if edges[edge] == old_name:
                edges[edge] = new_name

    # Добавляем новое состояние с сохранением переходов
    transitions[new_name] = old_transitions

    replace_all_state(transitions, old_name, new_name)

    return transitions

# Замена всех вхождений
def replace_all_state(transitions, old_name, new_name):
    # Обновляем все переходы, ссылающиеся на старое состояние
    for state, edges in transitions.items():
        for edge in edges.keys():
            if edges[edge] == old_name:
                edges[edge] = new_name