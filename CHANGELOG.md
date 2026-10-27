# Changelog - mkPyEdek

---

## [1.0.8.0]

### Naprawione (Fixed)
- **Brakujący plik:** Próba otwarcia nieistniejącego pliku (z listy „Otwórz ostatnie”, z linii poleceń lub przez „Otwórz za pomocą…”) wyświetla komunikat z pełną ścieżką pliku. Wcześniej program nie reagował w żaden widoczny sposób, a plik był po cichu usuwany z listy ostatnich.
- **Lista ostatnich plików:** Wybranie pliku, który już nie istnieje, nie wywołuje zbędnego pytania o zapis bieżących zmian – od razu pojawia się informacja o braku pliku i o usunięciu go z listy.

---

## [1.0.7.7]

### Zmienione (Changed)
- **Mniej nachalne podpowiedzi:** Lista podpowiedzi nie pojawia się automatycznie w komentarzach i napisach (wewnątrz `{…}` w f-stringach nadal działa); `Ctrl+Spacja` wywołuje ją zawsze. Kropka w liczbie (np. `3.`) nie otwiera listy metod typu float.

### Naprawione (Fixed)
- **Cudzysłowy w komentarzach i napisach:** Apostrof nie jest już dublowany – `# don't` i `"Ala's kot"` wpisują się poprawnie. W kodzie cudzysłów po literze nie jest parowany, z wyjątkiem prefiksów napisów (`f"`, `r'`, `b"`, `rb'` itp.).
- **Potrójny cudzysłów:** Wpisanie `"""` (lub `'''`) wstawia od razu zamknięcie – `"""|"""` – zamiast `""""`.

---

## [1.0.7.6]

### Dodane (Added)
- **Podpowiedzi z bibliotek ucznia:** Autouzupełnianie korzysta z zainstalowanego interpretera Pythona, więc podpowiada także biblioteki doinstalowane przez ucznia (np. `pygame`, `numpy`), a nie tylko moduły wbudowane w program.
- **Podpowiedzi z własnych modułów:** Działają importy modułów leżących w tym samym folderze co edytowany plik (np. `import moj_modul`).

### Zmienione (Changed)
- Środowisko autouzupełniania jest tworzone przy pierwszej podpowiedzi (w tle) i zapamiętywane; zmiana interpretera przez „Wskaż plik” je odświeża.
- Jeśli środowiska nie da się uruchomić, autouzupełnianie automatycznie wraca do bibliotek wbudowanych, a przyczyna jest zapisywana w `app.log`.
- Budowanie: do paczki dołączane są pliki źródłowe pakietów `jedi` i `parso` (wymagane przez proces pomocniczy autouzupełniania).

---

## [1.0.7.5]

### Naprawione (Fixed)
- **Okno konsoli po zakończeniu programu (F5):** Okno nie zamyka się już natychmiast, gdy uruchomiony program zamknie lub wyczerpie standardowe wejście (np. `sys.stdin.close()`). Edytor czeka wtedy na dowolny klawisz bezpośrednio z konsoli Windows, dzięki czemu wynik programu i ewentualny komunikat błędu pozostają widoczne.
- **Ctrl+C przy „Naciśnij Enter, aby zamknąć…”** zamyka okno bez wyświetlania zbędnego komunikatu błędu.

--- 

## [1.0.7.4]

### Zmienione (Changed)
- **Wysyłanie kodu przez Gmail:** Długość kodu jest sprawdzana na gotowym adresie wiadomości (po zakodowaniu znaków), a nie na surowym tekście – wcześniej kod z polskimi znakami mieszczący się w limicie 1500 znaków dawał adres kilkukrotnie dłuższy. Krótki kod trafia do treści wiadomości bez żadnych ostrzeżeń.
- **Długi kod jako załącznik:** Gdy kod jest zbyt długi, program wyświetla ostrzeżenie z prośbą o wysłanie go jako załącznika (plik `.py`). Po potwierdzeniu zapisuje plik, otwiera nową wiadomość w Gmailu z informacją o załączniku i pokazuje plik w folderze, gotowy do dołączenia. Usunięto dotychczasowe kopiowanie długiego kodu do schowka.
- Temat wiadomości zawiera nazwę pliku (np. „Kod programu Python - zadanie.py”), jeśli plik był zapisany.
- Kod otwierający folder z zaznaczonym plikiem został wydzielony do wspólnej metody używanej przez Gmail i Classroom.

---

## [1.0.7.3]

### Naprawione (Fixed)
- **Spójne wyszukiwanie i zamiana:** „Znajdź”, „Znajdź następny” (F3) i „Zamień” jednakowo rozróżniają wielkość liter (jak Python). Wcześniej wyszukiwanie ignorowało wielkość liter, a „Zamień wszystko” ją uwzględniało – liczba trafień i zamian mogła się różnić.
- **F3 szukał niewłaściwego tekstu:** „Znajdź następny” zawsze szuka ostatnio wpisanego wyrażenia od pozycji kursora. Wcześniej po „Zamień wszystko” powtarzał poprzednie wyszukiwanie, a bez wcześniejszego „Znajdź” nie robił nic.
- **Komunikaty F3:** Brak trafień wyświetla komunikat, a powrót wyszukiwania na początek pliku jest sygnalizowany na pasku stanu.
- **„Zamień wszystko” zachowuje widok:** Kursor i przewinięcie pozostają na swoim miejscu zamiast przeskakiwać na początek pliku; całą operację nadal cofa jedno Ctrl+Z.

### Zmienione (Changed)
- Okna „Znajdź” i „Zamień” podpowiadają ostatnio szukany tekst; komunikaty podają szukaną frazę.
- Poprawna odmiana w komunikacie o liczbie zamian (np. „Zamieniono 3 wystąpienia”).
- Zachowanie wielkości liter można zmienić jedną stałą `SEARCH_CASE_SENSITIVE`.

---

## [1.0.7.2]

### Naprawione (Fixed)
- **Wskazywanie błędu składni (F5):** Zaznaczenie obejmuje dokładnie tekst błędnej linii. Wcześniej długość linii była liczona w bajtach razem ze znakiem końca linii, przez co zaznaczenie wychodziło poza linię (zwłaszcza przy polskich znakach i w plikach CRLF), a kursor lądował na początku następnej linii.
- **Kursor w miejscu błędu:** Po zamknięciu komunikatu kursor ustawia się dokładnie w miejscu wskazanym przez Pythona (kolumna błędu), a edytor otrzymuje fokus – można od razu poprawiać kod.

### Zmienione (Changed)
- Komunikat o błędzie składni podaje także numer kolumny (np. „Błąd w linii 2, kolumna 19”). Obsługa błędu została wydzielona do metody `_show_syntax_error()`; numery linii i kolumn spoza zakresu tekstu są bezpiecznie przycinane.

---

## [1.0.7.1]

### Naprawione (Fixed)
- **Utrata danych przy nietypowym kodowaniu:** Zastąpiono nieistniejący w Pythonie kodek `latin-2` poprawnym `iso-8859-2`. Wcześniej pliki zawierające bajty nieobsługiwane przez Windows-1250 były wczytywane ze znakami zastępczymi `�` i oznaczane jako UTF-8 – przy zapisie, bez żadnego pytania, oryginalne znaki były bezpowrotnie tracone. Teraz każdy plik wczytuje się bez strat, a przed zapisem w UTF-8 pada standardowe pytanie o zmianę kodowania.
- **Deklaracja kodowania (PEP 263):** Przy zapisie deklaracja kodowania innego niż UTF-8 w pierwszych dwóch liniach (np. `# -*- coding: cp1250 -*-`) jest zamieniana na `utf-8`. Wcześniej plik zapisany w UTF-8 z pozostawioną deklaracją CP1250 wyświetlał po uruchomieniu (F5) polskie znaki jako „krzaczki”. Poprawka naprawia też pliki przekonwertowane przez starsze wersje edytora; zmianę można cofnąć skrótem Ctrl+Z.
- **Pytanie o kodowanie po błędzie zapisu:** Informacja o oryginalnym kodowaniu pliku jest kasowana dopiero po udanym zapisie.

### Zmienione (Changed)
- Usunięto gałąź awaryjnego odczytu z `errors='replace'` oraz mylący komunikat „Plik zawiera znaki spoza UTF-8”.

---

## [1.0.7.0]

### Naprawione (Fixed)
- **Zachowanie końców linii (CRLF/LF):** Pliki zapisane z końcami linii Windows (`\r\n`) zachowują je po zapisie. Wcześniej plik był wczytywany z automatyczną zamianą `\r\n` na `\n`, przez co po pierwszym zapisie końce linii były po cichu zmieniane na uniksowe.
- **Ujednolicanie mieszanych końców linii:** Plik zawierający zarówno `\r\n`, jak i `\n` jest po otwarciu ujednolicany do stylu Windows; nowe linie wstawiane klawiszem Enter mają ten sam styl co reszta pliku. Konwersja nie oznacza pliku jako zmienionego i nie trafia do historii cofania.
- **Nowy plik:** Polecenie „Nowy” zawsze przywraca końce linii LF, niezależnie od stylu poprzednio otwartego pliku.

---

## [1.0.6.11]

### Naprawione (Fixed)
- **Kolorowanie składni w motywach:** Motyw ustawia teraz wszystkie 20 stylów leksera Pythona (wcześniej 12). Dekoratory (`@...`), f-stringi (`f"..."`, `f'...'`, `f"""..."""`), bloki komentarzy (`##`) oraz niezamknięte napisy otrzymują kolory i czcionkę aktywnego motywu – w ciemnych motywach nie są już ciemne na ciemnym tle.
- **Wspólna baza stylów:** Przed nadaniem kolorów poszczególnym elementom ustawiany jest kolor, tło i czcionka dla wszystkich stylów, więc żaden styl nie zachowuje domyślnych ustawień QScintilli.
- **Trwały lekser:** Lekser składni jest tworzony z edytorem jako rodzicem. Wcześniej był usuwany przez mechanizm odśmiecania Pythona zaraz po ustawieniu motywu, przez co każda zmiana motywu tworzyła nowy lekser od zera.

---

## [1.0.6.10]

### Naprawione (Fixed)
- **Zaznaczanie pliku w Eksploratorze Windows:** Przy „Udostępnij w Classroom” Eksplorator poprawnie otwiera folder z zaznaczonym plikiem także wtedy, gdy ścieżka zawiera spacje (np. `C:\Users\Jan Kowalski\...`). Wcześniej cały argument `/select,…` był ujmowany w cudzysłów, czego Eksplorator nie rozpoznaje, i otwierał się folder „Dokumenty”.

---

## [1.0.6.9]

### Naprawione (Fixed)
- **„Udostępnij w Classroom”:** Classroom i eksplorator plików otwierają się teraz wyłącznie po udanym zapisie pliku. Wcześniej wynik zapisu był ignorowany – po odmowie zmiany kodowania (np. pliki CP1250) lub błędzie zapisu uczeń trafiał do Classroom z nieaktualną wersją pliku na dysku.
- **Podwójny zapis nowego pliku:** Usunięto zbędne drugie zapisanie pliku przy udostępnianiu nowego, jeszcze niezapisanego dokumentu.

---

## [1.0.6.8]

### Naprawione (Fixed)
- **Zamykanie programu podczas pracy Jedi:** Program czeka teraz bez limitu czasu na zakończenie wątku autouzupełniania (wcześniej `wait(500)`), co eliminuje ryzyko awaryjnego zakończenia procesu („QThread: Destroyed while thread is still running”) przy zamykaniu okna w trakcie analizy większego pliku.
- **Wyjście z okna błędu krytycznego:** Zatrzymanie wątku Jedi jest podpięte także pod `QApplication.aboutToQuit`, więc działa również przy wyjściu przyciskiem „Zakończ program”, który pomija `closeEvent`.

### Zmienione (Changed)
- **Refaktoryzacja:** Logika zatrzymywania autouzupełniania została przeniesiona do metody `PythonEditor.shutdown()`; okno główne nie odwołuje się już do prywatnych pól edytora. Po rozpoczęciu zamykania edytor nie uruchamia nowych zapytań Jedi i nie wyświetla podpowiedzi.

---

## [1.0.6.7]

### Naprawione (Fixed)
- **Filtr okna „Wskaż plik”:** Poprawiono filtr plików przy ręcznym wskazywaniu interpretera. Wzorce były rozdzielone średnikami (`*.exe; python; python3`), których Qt nie rozpoznaje, przez co pliki `.exe` nie były wyświetlane. Filtr zależy teraz od systemu: `python*.exe py.exe` w Windows oraz `python python3 python3.*` w macOS/Linux.

---

## [1.0.6.6]

### Naprawione (Fixed)
- **Weryfikacja interpretera Pythona:** Ścieżka `python_cmd` z `config.json`, plik wskazany ręcznie („Wskaż plik”) oraz wyniki autodetekcji są teraz sprawdzane przez faktyczne uruchomienie `--version` (nowa metoda `_is_valid_python`). Wcześniej w Windows akceptowany był każdy istniejący plik, co przy błędnym wpisie w konfiguracji powodowało migające i natychmiast znikające okno konsoli po F5.
- **Samonaprawa konfiguracji:** Nieprawidłowy wpis `python_cmd` jest pomijany (z ostrzeżeniem w `app.log`), program wraca do autodetekcji i usuwa błędny wpis z `config.json`.
- **Okno „Wskaż plik”:** Anulowanie wyboru nie wyświetla już komunikatu o błędzie; wskazanie pliku, który nie jest interpreterem, pokazuje czytelną podpowiedź.

---

## [1.0.6.5]

### Naprawione (Fixed)
- **Uruchamianie kodu bez interpretera (F5):** Gdy nie wykryto Pythona (np. po wybraniu „Ignoruj” w oknie startowym), naciśnięcie F5 wyświetla teraz okno „Brak interpretera Python” z opcjami „Wskaż plik” / „Pobierz Pythona” / „Ignoruj”, zamiast mylącego komunikatu „Nie uruchomiono interpretera: expected str…” (`TypeError` z `subprocess.Popen`). Po wskazaniu poprawnego interpretera kod uruchamia się od razu.
- **Kolejność operacji:** Sprawdzenie interpretera odbywa się przed zapisem pliku, więc przy jego braku nie pojawia się już niepotrzebne okno „Zapisz jako”.

---

## [1.0.6.4]

### Naprawione (Fixed)
- **Dublowanie nawiasów zamykających:** Wpisanie `)`, `]` lub `}`, gdy ten sam znak stoi bezpośrednio za kursorem, przesuwa kursor za nawias zamiast wstawiać kolejny. Ręczne wpisanie `print()` daje teraz `print()` zamiast `print())`. Przeskakiwanie działa analogicznie do istniejącej obsługi cudzysłowów i nie dotyczy sytuacji z zaznaczonym tekstem.

---

## [1.0.6.3]

### Naprawione (Fixed)
- **Utrata danych przez „Cofnij” po otwarciu pliku:** Otwarcie pliku oraz polecenie „Nowy” czyszczą teraz historię cofania edytora (`SCI_EMPTYUNDOBUFFER`). Wcześniej `Ctrl+Z` po otwarciu pliku B przywracał treść poprzedniego pliku A, a kolejne `Ctrl+S` nadpisywało plik B cudzą zawartością.

---

## [1.0.6.2]

### Naprawione (Fixed)
- **Instalator:** Dodano automatyczne usuwanie wadliwego pliku `config.json` (ze starszych wersji) z katalogu użytkownika (`{%USERPROFILE}\.mkPyEdek\`) podczas instalacji nowej wersji.
- **Stabilność GUI:** Wdrożono zabezpieczenie przed "lawiną okien" błędów (reentrancy) w przypadku powtarzających się wyjątków (np. podczas obsługi zdarzeń klawiatury).
- **Zarządzanie wątkami:** Zabezpieczono program przed błędami z wątków pobocznych (wyjątki z `QThread` są teraz logowane bez zawieszania głównej pętli GUI).

---

## [1.0.6.1]

### Zmienione (Changed)
- **Wydajność (Jedi):** Przeniesiono system autouzupełniania kodu (Jedi) do dedykowanego wątku w tle (`QThread`).
- **Optymalizacja pisania:** Wprowadzono opóźnienie (debounce timer 250ms) dla autouzupełniania, co całkowicie wyeliminowało zacinanie się edytora podczas szybkiego wpisywania kodu.
- **Weryfikacja składni:** Zastąpiono powolny wątek sprawdzający składnię na rzecz błyskawicznej weryfikacji przy pomocy wbudowanej funkcji `compile()` uruchamianej bezpośrednio przed wykonaniem kodu.
- **Zamykanie programu:** Poprawiono logikę zamykania okna (`closeEvent`) – aplikacja teraz bezpiecznie czeka na zakończenie pracy wątków pobocznych przed wyjściem.

---

## [1.0.6.0]

### Dodane (Added)
- **Globalna ochrona przed awariami:** Zaimplementowano niestandardowy `sys.excepthook` przechwytujący błędy krytyczne aplikacji. 
- **Odzyskiwanie danych (Recovery):** W przypadku wystąpienia błędu krytycznego, edytor automatycznie zapisuje kopię awaryjną aktualnego kodu w katalogu `~/.mkPyEdek/recovery/recovery_YYYYMMDD_HHMMSS.py`.
- **Okno błędu krytycznego:** Użytkownik otrzymuje czytelny komunikat o ścieżce do odzyskanego pliku oraz ma możliwość wyboru: natychmiastowe zakończenie programu lub kontynuacja pracy na własne ryzyko.

---

## [1.0.5.9]

### Dodane / Zmienione / Naprawione
- [Tutaj wpisz zmiany i poprawki, które zostały wdrożone w wersji 1.0.5.9]
- Bieżąca obsługa i stabilizacja działania edytora przed wdrożeniem nowych mechanizmów bezpieczeństwa i autouzupełniania w linii 1.0.6.x.

---

## [1.0.5.8]

### Poprawki
* **Ochrona przed awarią aplikacji:** Dodano globalną obsługę nieprzechwyconych wyjątków (`sys.excepthook`). Błędy ze slotów Qt i zdarzeń edytora wyświetlają teraz powiadomienie użytkownikowi i są logowane, zapobiegając nagłemu wyłączeniu programu i utracie niezapisanego kodu.
* **Bezpieczniejsza weryfikacja składni:** Rozszerzono przechwytywanie wyjątków w `SyntaxCheckThread` o klasę `Exception` (zamiast samego `SyntaxError`), co chroni przed awariami przy błędach alokacji lub niepoprawnych znakach bajtowych.
* **Trwały zapis logów:** Konfiguracja modułu `logging` zapisuje od teraz logi zdarzeń i błędów do pliku `~/.mkPyEdek/app.log` w kodowaniu UTF-8.

---

## [1.0.5.7]

### Poprawki
* **Zarządzanie wątkami w tle (QThread):** Zmieniono nazwy własnych sygnałów (`result_ready`), aby uniknąć przysłaniania wbudowanego sygnału `QThread.finished`. Operacja `deleteLater` jest teraz wywoływana bezpiecznie po zakończeniu pracy wątku.
* **Wielowątkowość i wyścigi:** Dodano weryfikację nadawcy (`self.sender()`) w autouzupełnianiu Jedi, zapobiegając utracie referencji do aktywnych wątków przy szybkim pisaniu.
* **Poprawa cyklu życia aplikacji:** Zmieniono kolejność w `closeEvent` – anulowanie zamknięcia okna po zapytaniu o zapis nie przerywa już działania mechanizmów weryfikacji składni (F5).

---

## [1.0.5.6]

### Poprawki
* **Naprawiono nadpisywanie plików bez pytania:** Opcja "Zapisz jako" poprawnie weryfikuje teraz istnienie pliku docelowego, nawet jeśli użytkownik nie wpisał ręcznie rozszerzenia `.py`.
* **Rozszerzenia plików:** Usunięto błąd powodujący tworzenie plików z podwójnymi rozszerzeniami (np. `plik.txt.py` lub warianty wielkości liter `skrypt.PY.py`). Zarządzanie sufiksem przejęło natywne okno dialogowe.

---

## [1.0.5.5]

### Poprawki
* **Ochrona przed utratą danych:** Otwarcie pliku z menu "Otwórz ostatnie" prawidłowo wywołuje teraz okno dialogowe z pytaniem o zapisanie aktualnych zmian. Wcześniej aplikacja po cichu nadpisywała edytor, bezpowrotnie usuwając niezapisany kod użytkownika.

---

## [1.0.5.4]

### Poprawki dla platformy macOS
* **Naprawiono błąd składni AppleScript podczas uruchamiania kodu:** Wycofano poleganie wyłącznie na systemowym `shlex.quote()` w budowaniu polecenia wywoływanego przez interpreter `osascript`. Teraz edytor prawidłowo ujmuje ścieżkę do skryptu w wymagane przez AppleScript cudzysłowy i zabezpiecza tzw. znaki ucieczki wewnątrz łańcucha (np. odwrócone ukośniki oraz wewnętrzne cudzysłowy), uniemożliwiając awarie uruchomieniowe spowodowane „gołymi” ścieżkami systemów uniksowych.
* **Automatyczne czyszczenie plików:** Dodano dyrektywę `rm -- "$0"` na końcu generowanego dla terminala systemowego pliku rozruchowego `.sh`. Dzięki temu nowa karta Terminala automatycznie usunie tymczasowy plik wykonywalny ze ścieżki (np. `/var/folders/`) bezpośrednio po zamknięciu sesji, chroniąc dysk przed zapychaniem resztkami po wciśnięciu *Uruchom*.

---

## [1.0.5.3]

### Poprawki błędów
* **Detekcja interpretera Python:** Zmieniono sposób inicjalizacji głównej komendy uruchomieniowej dla skryptów. Aplikacja dynamicznie i w konkretnej kolejności wyszukuje poprawną ścieżkę interpretera w zmiennych środowiskowych systemów poprzez `shutil.which("python3") or shutil.which("python") or "python"`.
  * Rozwiązuje to problem fałszywych weryfikacji w systemach macOS i Linux, gdy dostępna jest instalacja pod komendą `python3`, podczas gdy starsza logika i tak wymuszała użycie `python`. 
  * W systemie Windows nowa priorytetyzacja omija problem zwracania atrapy (aliasu wywołującego Microsoft Store) przez `shutil.which("python")`, znacząco zwiększając niezawodność uruchamiania kodu na różnych platformach. Pamiętano także, by nie stosować zablokowanego w środowisku PyInstaller `sys.executable`.
* Uproszczono funkcję sprawdzającą poprawność instalacji interpretera (`check_python_installed`) celem dostosowania do nowego mechanizmu ładowania ścieżek bez wywoływania pętli błędu i nieprawidłowych komunikatów o braku środowiska.

---

## [1.0.5.2]

### Główne zmiany i stabilizacja
* **Dziedziczenie katalogu roboczego:** Wprowadzono obligatoryjne przekazywanie argumentu `cwd=os.path.dirname(self.current_file)` we wszystkich trzech gałęziach systemu uruchamiania kodu (Windows, macOS, Linux). Rozwiązuje to problem zapisywania plików konfiguracyjnych w złym miejscu (np. w ścieżce edytora zamiast skryptu) oraz błędy w importach sąsiadujących modułów podczas używania polecenia `-c` w środowisku Windows.
* **Zmiana wersji:** Zaktualizowano identyfikator wydania do `v1.0.5.2`.

---

## [1.0.5.1]

### Zmienione i Ulepszone
* **Asynchroniczne autouzupełnianie (Jedi):** Przeniesiono mechanizm podpowiedzi kodu do osobnego wątku (`QThread`), co całkowicie eliminuje "zamrażanie" interfejsu graficznego podczas szybkiego pisania.
* **Weryfikacja składni w tle:** Sprawdzanie poprawności kodu (AST) przed jego uruchomieniem działa teraz asynchronicznie, zwiększając responsywność edytora.
* **Inteligentny Backspace:** Usprawniono usuwanie par znaków (nawiasy, cudzysłowy). Usuwanie pierwszej części pary automatycznie kasuje drugą, jeśli kursor znajduje się między nimi.
* **Bezpieczne zamykanie wątków:** Poprawiono obsługę zdarzenia `closeEvent`, aby aplikacja poprawnie i bezpiecznie ubijała działające w tle wątki analizy kodu podczas wychodzenia z edytora.

### Naprawione
* Usunięto błędy związane z nakładaniem się żądań autouzupełniania podczas błyskawicznego wprowadzania kolejnych znaków.

---

## [1.0.5.0]

### Optymalizacje asynchroniczności i czytelności
* **Kolejkowanie zapytań silnika Jedi (Debouncing/Throttling):** Przeprojektowano system autouzupełniania w locie. Od teraz, podczas intensywnego pisania, gdy wątek tła przetwarza zapytanie, nowe żądania są oznaczane jako oczekujące (`_pending_completion`). Po zakończeniu pracy poprzedniego wątku aplikacja weryfikuje ruch kursora: jeśli użytkownik wciąż pisze, stary, nieaktualny wynik jest natychmiastowo porzucany na rzecz nowego, świeżego zapytania dla aktualnej pozycji. Zapobiega to pojawianiu się spóźnionych podpowiedzi dla minionego tekstu.
* **Refaktoryzacja komentarzy technicznych w architekturze procesów:** Rozszerzono dokumentację metody `_on_syntax_check_done` w celu jednoznacznego opisania intencji instrukcji `return` wewnątrz konstrukcji `try/finally`. Zmiana ta gwarantuje czytelność kodu dla mechaniki zwalniania blokady uruchomieniowej `_code_running`.

---

## [1.0.4.3]

### Stabilność i Architektura Edytora (Edge Cases)
* **Wstrzymanie wykonania przy zaniechaniu konwersji kodowania:** Zabezpieczono łańcuch uruchomieniowy procesu (F5) przed wykonaniem niezapisanego kodu. W sytuacji, gdy edytor ostrzega przed konwersją przestarzałego kodowania na UTF-8 (np. starych plików CP1250), a użytkownik zaniecha operacji, kod nie zostanie uruchomiony, zapobiegając rozbieżnościom w tym, co jest na dysku, a tym, co wykonuje maszyna w pamięci RAM.
* **Optymalizacja płynności interfejsu przy zmianie kompozycji graficznej:** Zmodyfikowano metodę aktualizacji motywu graficznego `apply_theme`. Silnik tokenizacji w locie `QsciLexerPython` jest od teraz przydzielany obiektowi w sposób trwały. Zmiana kompozycji powoduje wyłącznie "przemalowanie" istniejących reguł dla aktualnego bufora tekstowego. Zapobiega to kosztownemu niszczeniu i kreowaniu obróbki syntaktycznej od zera, co całkowicie likwiduje irytujące "mruganie" okna przy dużych plikach.
* **Ochrona struktur typu potrójne cudzysłowy:** Złagodzono mechanizm inteligentnego kasowania autopar. Algorytm wciśnięcia klawisza `Backspace` nie usuwa podwójnych cudzysłowów, jeśli przylega on i znajduje się bezpośrednio w sekwencji potrójnej inicjalizacji (np. `"""` / `'''`). Gwarantuje to spójność przy wprowadzaniu wieloliniowych komentarzy dokumentujących funkcje (docstrings).

---

## [1.0.4.2]

### Optymalizacja wydajności
* **Odblokowanie wątku głównego (GUI) podczas autouzupełniania:** Silnik podpowiedzi Jedi został w pełni zrównoleglony przy użyciu architektury `QThread` (`JediCompletionThread`). Od teraz interfejs edytora działa perfekcyjnie płynnie i bez zacięć, nawet podczas analizy potężnych bibliotek zewnętrznych takich jak Numpy. Operacje wyszukiwania odbywają się nieodczuwalnie w tle.

### Zapobieganie utracie danych i UX
* **Ostrzeżenie przed naruszeniem kodowania znaków:** Edytor zyskał bezpiecznik zapobiegający bezwarunkowemu nadpisywaniu plików typu Windows-1250 / ANSI do formatu UTF-8. Aplikacja zapamiętuje źródłowe kodowanie podczas operacji otwierania, a przy próbie pierwszego zapisu wyświetla monit, czy użytkownik na pewno chce dokonać wymuszonej konwersji standardu.
* **Rozszerzona obsługa eksportu przez Gmail:** Zabezpieczono proces wklejania dużych objętościowo partii kodu (powyżej 1500 znaków). W przypadku przekroczenia limitu zapytania systemowego, aplikacja wyświetli interaktywne zapytanie o zgodę, automatycznie przerzuci tekst do schowka, po czym uruchomi oprogramowanie pocztowe bez blokowania błędem protokołu URI.
* **Naprawiono flagowanie skrótów Windows Explorer:** Zaktualizowano ustrukturyzowany wzorzec wywołania (`f"/select,{file_path}"`) stosowany do podświetlenia plików z poziomu menu "Classroom", co przywraca naturalne działanie eksploratora plików z zaznaczonym elementem (zamiast dotychczasowego otwierania samego katalogu docelowego).

---

## [1.0.4.1]

### Poprawki wizualne i UX interfejsu (UI Contrast Bug)
* **Zsynchronizowanie paska menu z motywem edytora:** Zlikwidowano błąd braku kontrastu menu bar na ciemnych i alternatywnych motywach. Porzucono dziedziczenie domyślnego przezroczystego tła na rzecz jawnego mapowania kolorów RGB dla każdego motywu (w metodzie `apply_ui_theme`). Od teraz paski menu, podmenu, przyciski oraz okna dialogowe (np. wyszukiwania lub błędów) idealnie dopasowują się barwą tła oraz czcionki do aktywnej kompozycji edytora (np. Dracula, Solarized Light, Monokai), gwarantując pełną czytelność interfejsu.

---

## [1.0.4.0]

### Optymalizacja UX i Wytrzymałość na Środowiska Lokalne
* **Throttling podsystemu IntelliSense:** Zaimplementowano programowy bezpiecznik czasu reakcji (350 ms) oparty na zegarze monotonicznym dla funkcji `request_jedi_completions`. Zapobiega to lawinowemu odpytywaniu parsera Jedi podczas szybkiego pisania kodu i całkowicie likwiduje zamrażanie wątku głównego (GUI) na dużych plikach lub obszernych importach bibliotek zewnętrznych (np. Numpy, Pandas).
* **Inteligentne cofanie autopar nawiasów (Backspace):** Zmodyfikowano natywną pętlę zdarzeń klawiatury `keyPressEvent`. Jeżeli kursor znajduje się bezpośrednio pomiędzy automatycznie wygenerowaną parą znaków otwierających i domykających (np. `()`, `[]`, `""`), naciśnięcie klawisza Backspace usuwa oba znaki jednocześnie, zapobiegając powstawaniu osieroconych struktur składniowych.
* **Wielopoziomowy algorytm fallbacku kodowania plików:** Rozszerzono odporność modułu odczytu plików tekstowych na błędy typu `UnicodeDecodeError`. W przypadku napotkania plików o niespójnym standardzie kodowania, system podejmuje kaskadowe próby dekodowania bufora przy użyciu zestawów znaków UTF-8, CP1250 (polskie kodowanie ANSI systemu Windows) oraz Latin-2. Jeśli wszystkie metody zawiodą, plik ładowany jest w trybie bezpiecznym z zamianą uszkodzonych bajtów na znaczniki zastępcze i czytelnym monitem ostrzegawczym.

---

## [1.0.3.5]

### Stabilność i Architektura Edytora (Edge Cases)
* **Zabezpieczenie flagi cyklu życia procesu:** Kod uruchomieniowy (`_on_syntax_check_done`) korzysta teraz z idiomatycznego bloku `try...finally`. Zapewnia to bezwarunkowe zwolnienie flagi bezpiecznika uruchamiania (`_code_running`), nawet w przypadku wystąpienia nieprzewidzianego błędu rzucanego podczas asynchronicznej kompilacji lub tworzenia środowiska testowego (np. brak powłoki `x-terminal-emulator` na niektórych dystrybucjach Linuxa).
* **Zachowanie historii "Cofnij" po zamianie tekstu:** Zamiana wielokrotna oparta o natywne modyfikacje stringa została udoskonalona, by nie niszczyć stosu poleceń `Undo/Redo` w Scintilli. Zastosowano metodę odświeżania bufora poprzez `replaceSelectedText()` na uprzednio zaznaczonej całości. Dzięki temu wszystkie zmiany masowe poprawnie agregują się w pojedynczą operację pod skrótem `Ctrl+Z`, zachowując poprzednią historię modyfikacji ucznia.

---

## [1.0.3.4]

### Zmiany w logice działania aplikacji (UX / Bezpieczeństwo danych)
* **Zabezpieczenie przed nadpisaniem sprawnego kodu:** Zmieniono sekwencję wykonywania polecenia "Uruchom kod" (F5). Aplikacja nie dokonuje już automatycznego zapisu pliku na dysk przed wykonaniem testu składni. Analiza AST (`SyntaxCheckThread`) jest teraz wykonywana bezpośrednio na tekście z pamięci podręcznej edytora (RAM). Zapis na dysku twardym następuje dopiero w momencie, gdy kod pomyślnie przejdzie weryfikację. Zapobiega to bezpowrotnemu uszkodzeniu działających plików źródłowych uczniów w przypadku omyłkowego wprowadzenia błędów składniowych.

### Naprawione błędy (Krytyczna stabilizacja)
* **Usunięcie nieskończonej pętli zamrażającej GUI w `replace_text`:** Przepisano mechanizm masowej zamiany tekstu ("Zamień wszystko"). Dotychczasowa pętla oparta na natywnych metodach wyszukiwania Scintilli powodowała nieskończone zapętlenie i całkowite zawieszenie edytora, gdy tekst zastępujący zawierał tekst poszukiwany (np. zamiana "i" na "if"). Nowe rozwiązanie operuje bezpośrednio w pamięci Pythona, eliminując problem zawieszania, przyspieszając operację i dając możliwość cofnięcia całej operacji masowej za pomocą jednego wywołania akcji Undo (Ctrl+Z).
* **Eliminacja wyścigu wątków (Race Condition / Double Launch):** Wprowadzono wewnętrzną flagę stanu `self._code_running`. Zapobiega to nakładaniu się żądań uruchomienia kodu w przypadku skrajnie szybkiego, wielokrotnego wciskania klawisza F5 w czasie, gdy asynchroniczny wątek sprawdzania składni nie zakończył jeszcze operacji wyrejestrowania poprzez makro `deleteLater`.
* **Korekta generatora kodu:** Naprawiono drobną literówkę składniową w definicji kolorów motywu jasnego (`Jasny`) w linii 108 (`Q000080 =`), która powodowała wystąpienie błędu `SyntaxError` przy próbie uruchomienia aplikacji.

---

## [1.0.3.3]

### Zmiany w logice działania aplikacji (UX / Bezpieczeństwo danych)
* **Zabezpieczenie przed nadpisaniem sprawnego kodu:** Zmieniono sekwencję wykonywania polecenia "Uruchom kod" (F5). Aplikacja nie dokonuje już automatycznego zapisu pliku na dysk przed wykonaniem testu składni. Analiza AST (`SyntaxCheckThread`) jest teraz wykonywana bezpośrednio na tekście z pamięci podręcznej edytora (RAM). Zapis na dysku twardym następuje dopiero w momencie, gdy kod pomyślnie przejdzie weryfikację. Zapobiega to bezpowrotnemu uszkodzeniu działających plików źródłowych uczniów w przypadku omyłkowego wprowadzenia błędów składniowych.

### Naprawione błędy (Hotfix w locie)
* **Korekta generatora kodu:** Naprawiono drobną literówkę składniową w definicji kolorów motywu jasnego (`Jasny`) w linii 108 (`Q000080 =`), która powodowała wystąpienie błędu `SyntaxError` przy próbie uruchomienia aplikacji.

---

## [1.0.3.2]

### Naprawione błędy
* **Usunięto błąd krytyczny składni (SyntaxError):** Usunięto nielegalny token `$` w linii 131 (`if next_char == key_text:`), który uniemożliwiał uruchomienie edytora.
* **Optymalizacja zarządzania pamięcią QThread:** Przeprojektowano model usuwania wątku sprawdzania składni. Przeniesiono odpowiedzialność za wywołanie `deleteLater()` bezpośrednio do połączenia sygnałowego Qt w metodzie `run_code()`. W slocie `_on_syntax_check_done` zachowano bezpieczne, natychmiastowe zerowanie referencji, całkowicie eliminując mikro-ryzyko wyścigów podczas zwalniania pamięci sterty.
* **Zabezpieczenie przed zamknięciem aplikacji:** Dodano pełną implementację zdarzenia `closeEvent()`. Jeśli użytkownik spróbuje zamknąć aplikację podczas trwania walidacji kodu w tle, edytor bezpiecznie odpina sygnały, przerywa działanie wątku tła (`quit`) i czeka na jego zakończenie (`wait`), zapobiegając awariom naruszenia ochrony pamięci (Segmentation Fault).

---

## [1.0.3.1]

### Naprawione błędy krytyczne
* **Usunięto wyciek pamięci w walidatorze składni:** Naprawiono błąd akumulowania martwych obiektów `SyntaxCheckThread` przy wielokrotnym uruchamianiu kodu klawiszem F5. Wprowadzono bezpieczne odłączanie sygnałów (`disconnect`), niszczenie obiektów przez pętlę Qt (`deleteLater`) oraz bezwzględne zerowanie referencji do wątku po zakończeniu emisji sygnału. Uniemożliwia to powstanie sytuacji wyścigu i podwójnego startu interpretera.

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