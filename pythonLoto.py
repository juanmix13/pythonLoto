import logging
import csv
import random
from collections import Counter

# Configuración de logging
logging.basicConfig(
    filename="Loto_output.log",
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

CSV_FILE = "data/May14-June13_2025.csv"

def main_menu():
    logging.info("Programa iniciado.")
    while True:
        print("\nMenú Principal:")
        print("1 - Combinación caliente de números")
        print("2 - Combinación aleatoria de números")
        print("3 - Salir")

        option = input("Seleccione una opción: ").strip()

        if option == '3':
            logging.info("El usuario ha salido del programa.")
            print("Saliendo del programa.")
            break
        elif option in {'1', '2'}:
            columns = input("¿Cuántas combinaciones desea generar? (1-7): ").strip()
            if columns.isdigit() and 1 <= int(columns) <= 7:
                columns = int(columns)
                logging.info(f"Opción seleccionada: {option} - Combinaciones: {columns}")

                if option == '1':
                    combinations = generate_hot_combinations(CSV_FILE, columns)
                    print(f"\n{columns} combinaciones calientes generadas:")
                else:
                    combinations = [generate_random_combination() for _ in range(columns)]
                    print(f"\n{columns} combinaciones aleatorias generadas:")

                for i, combo in enumerate(combinations, 1):
                    print(f"Columna {i}: {combo}")
                    logging.info(f"Columna {i}: {combo}")
            else:
                print("Entrada inválida. Por favor, introduzca un número del 1 al 7.")
                logging.warning(f"Entrada inválida para número de columnas: {columns}")
        else:
            print("Opción no válida. Intente de nuevo.")
            logging.warning(f"Opción no válida seleccionada: {option}")

def generate_random_combination():
    combination = sorted(random.sample(range(1, 50), 6))
    logging.debug(f"Combinación aleatoria generada: {combination}")
    return combination

def get_number_frequencies(csv_path):
    frequency_counter = Counter()
    try:
        with open(csv_path, newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                for i in range(1, 7):
                    number = int(row[f'N{i}'])
                    frequency_counter[number] += 1
        logging.info(f"Frecuencias de números cargadas correctamente desde {csv_path}.")
    except FileNotFoundError:
        logging.error(f"Archivo no encontrado: {csv_path}")
        print(f"Error: No se encontró el archivo '{csv_path}'.")
    except Exception as e:
        logging.error(f"Error al leer el archivo CSV: {e}")
        print("Se produjo un error al leer los datos.")
    return frequency_counter

def generate_hot_combinations(csv_path, num_combinations, top_n=15):
    frequencies = get_number_frequencies(csv_path)
    if not frequencies:
        return []

    hot_numbers = [num for num, _ in frequencies.most_common(top_n)]
    logging.info(f"Números calientes seleccionados (top {top_n}): {hot_numbers}")

    combinations = []
    for _ in range(num_combinations):
        combination = sorted(random.sample(hot_numbers, 6))
        combinations.append(combination)

    return combinations

if __name__ == "__main__":
    main_menu()