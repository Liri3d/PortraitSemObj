import re 
from typing import List, Tuple, Any

# Вычисление значения семантической близости
def semantic_similarity(sentence1, sentence2):
    # Создаются множества для удаления повторяющихся элементов
    tokens1 = set(sentence1)
    tokens2 = set(sentence2)
    
    # Вычисляется пересечение множеств
    intersection = tokens1.intersection(tokens2)

    # Вычисляется объединение множеств
    union = tokens1.union(tokens2)
    
    sem_prox = round((len(intersection) / len(union)), 2)
    # Вычисляется семантическая близость
    return sem_prox

# Токенизация по предложениям
def tokenize(text):
    sentences = re.split(r'[.?!]', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    return sentences

# Вычисление сценария в каждом ТП
def extract_scripts(text, character):

    sentences = tokenize(text)
    sequence = []

    # Порог для проверки является ли токен характеристикой 
    threshold = 0.7
    max_sem_prox = threshold

    # Для каждого предложения проверяем, встречается ли характеристика
    for sentence in sentences:
        
        curr_key = None
        for key, pattern in character.items():
            
            curr_sem_prox = semantic_similarity(pattern, sentence)
            
            # print(curr_sem_prox, " ", max_sem_prox)
            if (curr_sem_prox >= max_sem_prox):
                print('***', sentence, pattern)
                max_sem_prox = curr_sem_prox
                curr_key = key
                # print(sentence, " ", pattern, " ", curr_sem_prox)
                
        if curr_key is not None:
            # print(curr_key)
            sequence.append(curr_key)
            max_sem_prox = threshold
    
    return sequence

# Построение словаря характеристик из сценариев
def build_dict_char(scripts):

    # Получаем уникальные элементы всех скриптов для упрощения
    unique_elements = set()
    for script in scripts:
        unique_elements.update(script)

    # Словарь для хранения множеств следования
    sequences = {elem: [] for elem in unique_elements}
    
    # Смотрим на все комбинации в скриптах
    for i in range(len(scripts)):
        for j in range(len(scripts[i]) - 1):
            primary = scripts[i][j]
            secondary = scripts[i][j + 1]
            sequences[primary].append(secondary)
     
    return sequences

# Поиск списка последних элементов из каждого списка
def get_start_elements(input_tuple: Tuple[List[Any], ...]) -> List[Any]:
    start_elements = []
    for lst in input_tuple:
        if lst:  # Проверяем, не пустой ли список
            if lst[0] not in start_elements:
                start_elements.append(lst[0])  # Добавляем последний элемент в результат
    return start_elements

# Поиск списка последних элементов из каждого списка
def get_finish_elements(input_tuple: Tuple[List[Any], ...]) -> List[Any]:
    finish_elements = []
    for lst in input_tuple:
        if lst:  # Проверяем, не пустой ли список
            if lst[-1] not in finish_elements:
                finish_elements.append(lst[-1])  # Добавляем последний элемент в результат
    return finish_elements