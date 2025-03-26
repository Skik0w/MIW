import numpy as np
from itertools import combinations

# Zbiór danych; ostatnia kolumna to decyzja
dane = np.array([
    [1, 1, 1, 1, 3, 1, 1],
    [1, 1, 1, 1, 3, 2, 1],
    [1, 1, 1, 3, 2, 1, 0],
    [1, 1, 1, 3, 3, 2, 1],
    [1, 1, 2, 1, 2, 1, 0],
    [1, 1, 2, 1, 2, 2, 1],
    [1, 1, 2, 2, 3, 1, 0],
    [1, 1, 2, 2, 4, 1, 1]
])

indeks_decyzji = dane.shape[1] - 1
pokryte = np.zeros(len(dane), dtype=bool)
reguly = []


def sprawdz_regule(warunki):
    """Sprawdza, czy zestaw warunków daje jednoznaczną decyzję."""
    decyzje = {wiersz[indeks_decyzji] for wiersz in dane if all(wiersz[a] == val for a, val in warunki)}
    return decyzje.pop() if len(decyzje) == 1 else None


dlugosc = 1
maks_dlugosc = dane.shape[1] - 1

while not all(pokryte) and dlugosc <= maks_dlugosc:
    nowa_regula_znaleziona = False

    for i, wiersz in enumerate(dane):
        if pokryte[i]:
            continue

        for idx_combo in combinations(range(dane.shape[1] - 1), dlugosc):
            warunki = [(a, wiersz[a]) for a in idx_combo]
            decyzja = sprawdz_regule(warunki)

            if decyzja is not None:
                wsparcie = 0
                for j, inny_wiersz in enumerate(dane):
                    if all(inny_wiersz[a] == val for a, val in warunki) and inny_wiersz[indeks_decyzji] == decyzja:
                        wsparcie += 1
                        pokryte[j] = True

                reguly.append((warunki, decyzja, wsparcie))
                nowa_regula_znaleziona = True
                break

        if nowa_regula_znaleziona:
            break

    if not nowa_regula_znaleziona:
        dlugosc += 1

# Wypisanie reguł
def wypisz_reguly(lista_regul):
    for warunki, decyzja, wsparcie in lista_regul:
        opis = ' oraz '.join([f'a{a+1}={val}' for a, val in warunki])
        print(f'{opis} => decyzja={decyzja} [{wsparcie}]')

if __name__ == '__main__':
    wypisz_reguly(reguly)
