import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime, timedelta
import time

def scrape_bonoloto_results(num_months=4):
    """
    Scrapes Bonoloto results from the official lottery website.
    Returns a list of dictionaries with the results.
    """
    results = []

    # Try multiple sources and methods
    try:
        # Method 1: Try the official website
        url = "https://www.loteriasyapuestas.es/es/bonoloto/resultados"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Look for result tables or data
        results_data = parse_results_page(soup)
        if results_data:
            results.extend(results_data)

    except Exception as e:
        print(f"Error scraping official site: {e}")
        print("Using alternative method...")

    # If no results, use a simpler alternative or return instructions
    if not results:
        print("Web scraping encountered issues. Using manual data entry mode.")
        results = get_manual_data()

    return results

def parse_results_page(soup):
    """Parse the results from the BeautifulSoup object."""
    results = []

    # Look for common HTML patterns used by lottery sites
    tables = soup.find_all('table')

    for table in tables:
        rows = table.find_all('tr')
        for row in rows[1:]:  # Skip header
            cols = row.find_all('td')
            if len(cols) >= 7:
                try:
                    fecha = cols[0].get_text(strip=True)
                    n1 = cols[1].get_text(strip=True)
                    n2 = cols[2].get_text(strip=True)
                    n3 = cols[3].get_text(strip=True)
                    n4 = cols[4].get_text(strip=True)
                    n5 = cols[5].get_text(strip=True)
                    n6 = cols[6].get_text(strip=True)
                    complementario = cols[7].get_text(strip=True) if len(cols) > 7 else ""

                    results.append({
                        'Fecha': fecha,
                        'N1': n1.zfill(2),
                        'N2': n2.zfill(2),
                        'N3': n3.zfill(2),
                        'N4': n4.zfill(2),
                        'N5': n5.zfill(2),
                        'N6': n6.zfill(2),
                        'Complementario': complementario.zfill(2) if complementario else ""
                    })
                except (IndexError, ValueError):
                    continue

    return results

def get_manual_data():
    """
    Interactive mode to manually enter Bonoloto results.
    This is a fallback when web scraping fails.
    """
    results = []
    print("\nModo manual: Introduce los resultados de Bonoloto")
    print("(Deja en blanco para terminar)")

    while True:
        try:
            fecha = input("\nFecha (YYYY-MM-DD) o Enter para terminar: ").strip()
            if not fecha:
                break

            n1 = input("N1: ").strip().zfill(2)
            n2 = input("N2: ").strip().zfill(2)
            n3 = input("N3: ").strip().zfill(2)
            n4 = input("N4: ").strip().zfill(2)
            n5 = input("N5: ").strip().zfill(2)
            n6 = input("N6: ").strip().zfill(2)
            complementario = input("Complementario: ").strip().zfill(2)

            results.append({
                'Fecha': fecha,
                'N1': n1,
                'N2': n2,
                'N3': n3,
                'N4': n4,
                'N5': n5,
                'N6': n6,
                'Complementario': complementario
            })
        except Exception as e:
            print(f"Error: {e}")
            continue

    return results

def save_to_csv(results, filename):
    """Save the results to a CSV file."""
    if not results:
        print("No results to save.")
        return False

    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Fecha', 'N1', 'N2', 'N3', 'N4', 'N5', 'N6', 'Complementario']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            writer.writerows(results)

        print(f"✓ Resultados guardados en {filename}")
        print(f"  Total de resultados: {len(results)}")
        return True

    except Exception as e:
        print(f"Error al guardar el archivo: {e}")
        return False

if __name__ == "__main__":
    print("Bonoloto Scraper - Obtener últimos 4 meses de resultados\n")

    output_file = "data/Bonoloto_Last4Months.csv"

    results = scrape_bonoloto_results(num_months=4)

    if save_to_csv(results, output_file):
        print("\nProceso completado exitosamente.")
    else:
        print("\nNo se pudo guardar los resultados.")
