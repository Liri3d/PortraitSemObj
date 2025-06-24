import re

def build_regex(state, transitions_dict):
    # Проверяем, есть ли переходы из этого состояния
    if state not in transitions_dict or not transitions_dict[state]:
        print(f"Нет переходов из состояния '{state}', возвращаем пустую строку.")
        return ""

    transitions = transitions_dict[state]

    # Словарь для хранения следующего состояния и связанных меток
    next_states = {}

    # Обходим все переходы от текущего состояния
    for label, next_state in transitions.items():
        if next_state not in next_states:
            next_states[next_state] = []
        next_states[next_state].append(label)

    # Список для хранения подвыражений
    sub_expressions = []

    # Обрабатываем все следующие состояния
    for next_state, labels in next_states.items():
        print(f"Обрабатываем переходы в состояние '{next_state}' с метками {labels}")

        # Проверка на переход в себя
        if next_state == state:
            unique_labels = set(labels)  # Уникальные метки для предотвращения дублирования
            sub_expr = f"{{{'|'.join(unique_labels)}}}"
            print(f"Переход в само себя, добавляем: {sub_expr}")
            sub_expressions.append(sub_expr)
        else:
            # Рекурсивно строим регулярное выражение для следующего состояния
            sub_expr = build_regex(next_state, transitions_dict)

            # Уникальные метки для перехода
            label_combined = '|'.join(set(labels))
            if len(labels) > 1:
                combined_expr = f"{label_combined}{sub_expr}"
            else:
                combined_expr = f"{labels[0]}{sub_expr}"
                
            print(f"Собранное выражение для перехода в состояние '{next_state}': '{combined_expr}'")
            sub_expressions.append(combined_expr)

    # Объединение подвыражений попарно
    if len(sub_expressions) > 1:
        combined_exprs = []
        for i in range(0, len(sub_expressions), 2):
            # Берём пары подвыражений
            if i + 1 < len(sub_expressions):
                pair_expr = f"(({sub_expressions[i]})|({sub_expressions[i + 1]}))"

                combined_exprs.append(pair_expr)
                print(f"Объединяем пару: {sub_expressions[i]} и {sub_expressions[i + 1]} в: {pair_expr}")
            else:
                combined_exprs.append(sub_expressions[i])  # Не хватает пары, добавляем последнее

        # Если объединяли пары, возвращаем результат
        for comb_expr in combined_expr:
            comb_expr = "(" + comb_expr + ")"
        result_expr = "(" + "|".join(combined_exprs) + ")"
        print(f"Объединяем все: {combined_exprs} в: {result_expr}")
        return result_expr
    
    # Возвращаем единственное подвыражение без лишних скобок
    final_expr = sub_expressions[0] if sub_expressions else ""
    print(f"Возвращаем выражение для состояния '{state}': '{final_expr}'")


    cleaned_expression = remove_extra_parentheses(final_expr)

    return cleaned_expression

def find_inner_expressions(expr):
    """ Находит все подвыражения с вертикальной чертой, включая вложенные. """
    stack = []
    inner_expressions = []
    for i, char in enumerate(expr):
        if char == '(':
            stack.append(i)
        elif char == ')':
            if stack:
                start = stack.pop()
                if '|' in expr[start:i]:  # Проверяем наличие вертикальной черты
                    inner_expressions.append(expr[start + 1:i])  # Добавляем содержимое без скобок
    return inner_expressions

def longest_common_suffix(str1, str2):
    """Находит общую подстроку максимальной длины, расположенную в конце двух строк."""
    print(str1, str2)
    # Длина двух строк
    len1, len2 = len(str1), len(str2)
    
    # Устанавливаем начальную длину общей подстроки
    common_length = 0
    
    # Сравниваем строки с конца до начала
    while common_length < len1 and common_length < len2 and str1[len1 - 1 - common_length] == str2[len2 - 1 - common_length]:
        common_length += 1
    
    common_suffix = str1[len1 - common_length:] if common_length > 0 else ""

    # Условие, чтобы суффикс не совпадал с одной из строк
    if common_suffix == str1 or common_suffix == str2:
        common_length = max(0, common_length - 2)  # Убираем 2 символа, если это возможно
        common_suffix = str1[len1 - common_length:] if common_length > 0 else ""
    print(common_suffix)
    return common_suffix


def remove_duplicate_inner_expressions(inner_expressions):
    seen = set()  # Множество для отслеживания уникальных подвыражений
    unique_expressions = []  # Список для хранения уникальных выражений

    for exp in inner_expressions:
        if exp not in seen:
            seen.add(exp)
            unique_expressions.append(exp)

    return unique_expressions

def remove_unpaired_parentheses(s):
    result = []
    last_close_index = -1  # Индекс последней закрывающей скобки
    
    for index, char in enumerate(s):
        if char == '(':
            # Если встречаем открывающую скобку, добавляем её в результат
            result.append(char)
        elif char == ')':
            # Если встречаем закрывающую скобку, закрываем
            if result:
                result.append(char)  # Добавляем закрывающую скобку, только если есть открывающая
                last_close_index = index  # Запоминаем индекс закрывающей скобки
            else:
                continue  # Пропускаем, если нет соответствующей открывающей скобки
        else:
            # Добавляем другие символы в результат
            result.append(char)
    
    # Удаляем все символы до последней закрывающей скобки и её саму:
    if last_close_index != -1:
        final_result = ''.join(result).rstrip()[:last_close_index]  # Создаем строку вплоть до закрывающей скобки
        return final_result
    
    return ''.join(result)  # Если не было ни одной закрывающей скобки, просто возвращаем результат.

def normalize_expression(expr):
    """ Нормализует регулярное выражение, вынося дублирующиеся завершающие части. """
    while True:
        print("НОВАЯ ИТТЕРАЦИЯ")
        
        inner = remove_duplicate_inner_expressions(find_inner_expressions(expr))
        
        if not inner:
            break  # Если нет подвыражений, выходим из цикла

        changed = False
        
        for i in range(len(inner)):
            print("Подвыражение", inner[i], expr)
            parts = inner[i].split('|')
            print("parts", parts[0], parts[1])
            
            common_suffix = longest_common_suffix(parts[0], parts[1])
            common_suffix = remove_unpaired_parentheses(common_suffix)
            print("Общая завершающая", common_suffix)
            if common_suffix:  # Если есть общие завершающие части

                new_parts = []
                for part in parts:
                    print("part:", part)
                    # Убираем общую завершающую часть из каждого подвыражения
                    new_part = part.removesuffix(common_suffix)
                    new_parts.append(new_part)
                print("new_parts:", new_parts)

                # Создаём новое подвыражение с общей частью
                new_inner = f"({'I'.join(new_parts)}){common_suffix}"
                print(new_inner)
               
                if i != len(inner):
                    j = i + 1
                    for j in range(len(inner)):
                        old_string = "(" + inner[i] + ")"
                        inner[j] = inner[j].replace(old_string, new_inner)
                    
                # Обновляем основное выражение, заменяем только найденное
                expr = expr.replace(f"({inner[i]})", new_inner)
                print("expr", expr)
                # changed = True
        
            print("\n")

        if not changed:
            break
        
        print("\n\n\n")
    
    return expr.replace("I", "|")

def remove_extra_parentheses(expression):
    stack = []
    result = []
    skip_indices = set()  # Для хранения индексов, которые нужно пропустить

    for i, char in enumerate(expression):
        if char == '(':
            stack.append(len(result))  # Сохраняем текущую позицию в результат
            result.append(char)
        elif char == ')':
            if stack:
                start_index = stack.pop()  # Получаем позицию открывающей скобки
                # Проверяем содержимое между скобками
                content = ''.join(result[start_index + 1:])  # Содержимое между скобками
                if '|' in content:  # Если есть '|' в содержимом
                    result.append(char)  # Оставляем скобки
                else:
                    skip_indices.add(start_index)  # Запоминаем, что нужно пропустить
                    result.append('')  # Вместо закрывающей скобки добавляем пустую строку
            else:
                result.append(char)  # Закрывающая скобка без соответствующей открывающей
        else:
            result.append(char)  # Добавляем другие символы

    # Удаляем элементы по индексам, которые были отмечены для пропуска
    final_result = []
    for i in range(len(result)):
        if i not in skip_indices:
            if result[i]:  # Добавляем только непустые элементы
                final_result.append(result[i])
    
    return ''.join(final_result)