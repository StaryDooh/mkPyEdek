# Changelog - mkPyEdek

---

## [1.0.3.0]

### Bezpieczeństwo i stabilność
* **Wyeliminowano Command Injection (Windows/MacOS):** Czyste uruchamianie plików `.py` bez korzystania z flagi `shell=True` (od teraz edytor opiera się o specjalny skrypt *runnera* w samym Pythonie, co dodatkowo rozwiązuje problem okna, które znikało zbyt szybko po błędach wykonania).
* **Bezpieczny odczyt/zapis środowiska:** Zmieniono funkcję zapisu konfiguracji – edytor zapamiętuje zwalidowaną ścieżkę do interpretera pomiędzy uruchomieniami. Dodano weryfikację uprawnień wykonywania plików (`os.X_OK`).
* **Zarządzanie wyjątkiem "Zapisz jako...":** Bezpieczniejsza obsługa zapisu nowo nazwanego pliku. Aplikacja robi tzw. *rollback* nazwy, jeśli użytkownik lub system anulują I/O.
* **Architektura Wątków i optymalizacja UI:**
  * Weryfikacja składni przed każdym uruchomieniem odbywa się od teraz całkowicie w tle (`QThread`), zapobiegając zamrażaniu interfejsu (GUI) przy dużych plikach.
  * Autouzupełnianie Jedi jest uodpornione na zjawisko wyścigów (*race conditions*) za pomocą systemowych blokad (`threading.Lock`).
  * Wszystkie przechwytywane wyjątki posiadają teraz system monitorowania błędów przy użyciu wbudowanego w Pythona modułu `logging`, ułatwiając potencjalne debugowanie.
* **Inteligentne pary nawiasów:** Poprawiono logikę autouzupełniania znaków cytowania i nawiasów (edycja uwzględnia omijanie podwójnych cudzysłowów podczas zamknięcia oraz sprytne zamykanie zaznaczonego tekstu parami znaków).
* **Usunięto zbędne biblioteki:** Usunięto nieużywany import klasy `QMenu`, optymalizując strukturę kodu.

---

## [1.0.2.0]

### Dodano
* **Rozbudowane Menu "Edycja":** Wprowadzono nową sekcję w pasku menu, zbierającą najważniejsze narzędzia do pracy z kodem.
* **Narzędzia schowka i historii:** Dodano natywną obsługę poleceń: Cofnij (`Ctrl+Z`), Ponów (`Ctrl+Y`), Wytnij (`Ctrl+X`), Kopiuj (`Ctrl+C`) oraz Wklej (`Ctrl+V`).
* **Szybkie zaznaczanie:** Zaimplementowano polecenie "Zaznacz wszystko" (`Ctrl+A`) wraz z dedykowaną łatką (hotfix) rozwiązującą problem konfliktów sygnałów w bibliotece PyQt.
* **Wyszukiwanie i zamiana tekstu:** Wprowadzono podstawowe narzędzia nawigacji po kodzie, wspierane przez silnik Scintilla:
  * "Znajdź..." (`Ctrl+F`)
  * "Znajdź następny" (`F3`)
  * "Zamień..." (`Ctrl+H`)

---

## [1.0.1.0]

### Naprawiono
* **Błąd pustych linii:** Rozwiązano problem automatycznego dodawania pustych linii (nadmiarowych znaków Enter) po pierwszym zapisaniu nowego pliku. Poprawiono sposób obsługi znaków końca linii (EOL) przy współpracy Scintilli z systemem plików.
* **Lokalizacja konfiguracji:** Przeniesiono plik `config.json` do folderu użytkownika (`%USERPROFILE%/.mkPyEdek/`). Zmiana ta definitywnie eliminuje błędy zapisu ustawień, gdy program jest zainstalowany w folderach systemowych typu "Program Files", które wymagają uprawnień administratora.

---

## [1.0.0.9]

### Naprawiono
* **Zapisywanie konfiguracji:** Naprawiono błąd, który uniemożliwiał zapisywanie motywu i listy ostatnich plików, gdy program był uruchamiany przez funkcję „Otwórz za pomocą” lub przez dwukrotne kliknięcie pliku .py.
* **Ścieżki bezwzględne:** Teraz plik konfiguracyjny (z motywem i listą plików) znajdziesz w folderze: C:\Users\TwojaNazwaUżytkownika\.mkPyEdek\config.json

---

## [1.0.0.8]

### Naprawiono
* **Uruchamianie plików .py:** Naprawiono błąd powodujący otwieranie pustego edytora po wybraniu opcji "Otwórz za pomocą..." lub dwukrotnym kliknięciu w plik systemowy. Aplikacja poprawnie odczytuje ścieżkę pliku przekazaną jako argument wiersza poleceń.
* **Identyfikacja użytkownika w Gmail:** Zmieniono mechanizm udostępniania kodu przez e-mail. Teraz użytkownik jest przekierowywany na stronę wyboru konta Google (`AccountChooser`) przed otwarciem nowej wiadomości. Rozwiązuje to problem wysyłania plików z cudzego konta w środowisku współdzielonych komputerów (np. w salach informatycznych).

---

## [1.0.0.7]

### Dodano
* **Menu "Udostępnij":** Nowa sekcja w Menu grupująca wszystkie metody przesyłania kodu nauczycielowi.
* **Opcja "Skopiuj cały kod":** Jednym kliknięciem uczeń kopiuje całą zawartość edytora do schowka systemowego.
* **Opcja "Wyślij przez Gmail (WWW)":** Automatyczne otwieranie nowej wiadomości w przeglądarce z wklejonym kodem programu w treści (rozwiązuje problem braku konfiguracji lokalnych programów pocztowych).

### Zmieniono
* **Reorganizacja Menu:** Przycisk "Udostępnij w Classroom" został przeniesiony do nowego, zbiorczego menu "Udostępnij".
* **Importy:** Dodano bibliotekę `urllib.parse` do poprawnego kodowania znaków w linkach e-mail.

---

## [1.0.0.6]

### Dodano
* **Nowe menu "Odwiedź":** Wprowadzono nową sekcję na głównym pasku menu, która ułatwia kontakt i śledzenie rozwoju projektu:
  * *Pobierz najnowszą wersję* – bezpośredni link do wydań (releases) na GitHubie.
  * *Zgłoś błąd* – szybkie przekierowanie do zakładki Issues na GitHubie.
  * *Zrelaksuj się* – link prowadzący na kanał YouTube twórcy (@StaryDooh).
* **Nowe motywy graficzne:** Rozszerzono paletę dostępnych stylów edytora o 3 kultowe motywy znane ze świata profesjonalnego IT:
  * *Monokai* (ciemny, wyrazisty)
  * *Solarized Light* (jasny, z optymalnym kontrastem dla zmęczonych oczu)
  * *Oceanic* (nowoczesny, w chłodnych odcieniach)

### Zmieniono
* **Reorganizacja paska Menu (UX):** Wyciągnięto opcję zmiany motywu z podmenu ("Widok" -> "Motyw") bezpośrednio na główny pasek Menu jako "Motyw". Zmniejsza to liczbę kliknięć potrzebnych do personalizacji edytora i czyni interfejs bardziej intuicyjnym.

---

## [1.0.0.5] i starsze
* Wyróżnienie zmiennych kolorem i pogrubieniem w edytorze.
* Wprowadzenie obsługi wielu motywów graficznych (Jasny, Ciemny, Kontrastowy).
* Dodanie zewnętrznej konsoli rozwiązującej problemy z funkcją `input()`.
* Mechanizm walidacji składni (SyntaxError) przed uruchomieniem kodu z podświetleniem linii.
* Ochrona przed utratą niezapisanych modyfikacji.
* Autouzupełnianie kodu (Jedi).
* Integracja i szybkie udostępnianie kodu w Google Classroom.
