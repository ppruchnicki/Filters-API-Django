## FILTERS-API-DJANGO

# Description

REST API zostało przygotowane w frameworku Django z wykorzystaniem Django Rest Framework - dedykowanym frameworkiem do tworzenia API.
Z racji użycia takich narzędzi na wstępie została przygotowana struktura ORM (models.py), która z poziomu Django odwzorowuje strukturę bazy dancyh podanych w plikach csv. Następnie pliki csv zostają zczytane przy użyciu funkcji z pliku populate_db.py i zapisane do bazy danych przy użyciu ORM. Komendy zawarte w plikach FTD_ELEMENTY.sql oraz FTD.sql zostały naniesione "ręcznie" poprzez stworzenie modeli tych tabel w pliku models.py. Z racji użycia Django i jego mechanizmu do mapowania struktur, użycie komendy 'python manage.py makemigrations API' tworzy takie same zapytanie SQL jak to zawarte w wymienionych plikach.
Aby zczytać strukturę tabeli Programy w formie JSON został przygotowany endpoint /programy, który na zapytanie metodą GET odpowie JSONem z pełną strukturą. Tworzenie filtra odbywa sie poprzez wywołanie metody POST na endpoint /filtry strukturę filtra należy przedstawić w formie JSON: {"nazwa": 'opis', "opis": 'opis', "ftd": JSON - struktura}. Aby edytować filtr należy wywołać metode PUT na endpoint /filtry/{pk} gdzie pk jest to primary key w tym wypadku id_ftd, które wskazuje konkretny filtr oraz wysłać w formie JSON nową strukturę filtra - analogiczna jak przy jego tworzeniu. Dodatkowo zostały stworzone metody umożliwiające zobaczenie konkretnego filtra w formie JSONA - wywołanie metody GET na endpoint /filtry/{pk} oraz możliwość usunięcia konkretnego filtra używając metody DELETE na endpoint /filtry/{pk}.
Obsługa błędów jest po części realizowana za pomocą serializatorów, które sprawdzają czy struktura JSONa zawiera wszytkie pola wymagane przez ORM,a wieć zgodne z modelem tabeli. Dodatkowo zaimplementowane natywnie funkcje w frameworku DRF dbają o poprawność metod użytych na danym endpoincie. Testy jednostkowe zostały wykonane przy użyciu dostępnych już w pakiecie narzędzi frameworka Django, testowana jest funkcja do zapełniania bazy danych, modele ORM, oraz każdy endpoint i jego dostępne metody zarówno w wypadku testu pozytywnego jak i negatywnego. Aplikacja została stworzona przy użyciu narzędzia do tworzenia wirtualnego środowiska pipenv, a wszystkie potrzebne dependencje są zapisane w pliku Pipfile. Instrukcje uruchomienia środowiska zamieszczam poniżej oraz w pliku readme.md.

# Instruction

1. Install all dependencies in virtual environment `pipenv install`
2. Run virtual environment `pipenv shell`
3. Create SQL commands `python manage.py makemigrations API`
4. Execute SQL commands `python manage.py migrate API`
5. Run test `python manage.py test`
6. Populate db `python manage.py populate_db`
7. Run API `python manage.py runserver`

# List of method and endpoints:

- Method GET /programy Read the entire list of programs
- Method GET /filtry Read the entire list of filters
- Method POST /filtry Create a filter and add it to the filters list
- Method GET /filtry/{pk} Read one filter from the filter list
- Method PUT /filtry/{pk} Update a filter in the filter list
- Method DElETE /filtry/{pk} Delete a filter in the filter list
