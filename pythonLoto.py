import logging
import csv
import random
from collections import Counter

logging.basicConfig(filename="Loto_output.log", level=logging.INFO)
csv_file = "data/May14-June13_2025.csv"
def main_menu():
    while True:
        print("Menú Principal:")
        print("1 - Combinación caliente de números")
        print("2 - Combinación aleatoria de números")
        print("3 - Salir")
        option = input("Seleccione una opción: ")

        if option == '3':
            print("Saliendo del programa.")
            break
        elif option in ['1', '2']:
            columns = input("Indique cuántas columnas necesita (1-7): ")
            if columns.isdigit() and 1 <= int(columns) <= 7:
                columns = int(columns)
                selected = "Caliente" if option == '1' else "Aleatoria"
                if option == '1':
                    hot_combos = generate_hot_combinations(csv_file, columns)
                    print(f"{columns} combinaciones {selected.lower()} generadas.\n")
                    for i, combo in enumerate(hot_combos, 1):
                        print(f"Columna {i}: {combo}")
                else:
                    combinations = []
                    for _ in range(columns):
                        combinations.append(generate_random())
                    print(f"{columns} combinaciones {selected.lower()} generadas.\n")
                    print(combinations)
            else:
                print("Entrada inválida. Regresando al menú principal...\n")
        else:
            print("Opción no válida. Intente de nuevo.\n")

def generate_random():
    random_numbers = random.sample(range(1, 50), 6)
    random_numbers.sort()
    return random_numbers

def get_number_frequencies(csv_path):
    frequency_counter = Counter()
    with open(csv_path, newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            for i in range(1, 7):
                number = int(row[f'N{i}'])
                frequency_counter[number] += 1
    return frequency_counter

def generate_hot_combinations(csv_path, num_combinations, top_n=15):
    frequencies = get_number_frequencies(csv_path)
    hot_numbers = [num for num, _ in frequencies.most_common(top_n)]

    combinations = []
    for _ in range(num_combinations):
        combination = sorted(random.sample(hot_numbers, 6))
        combinations.append(combination)

    return combinations

main_menu()