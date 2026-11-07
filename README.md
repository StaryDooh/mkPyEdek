# mkPyEdek

**mkPyEdek** to darmowe narzędzie stworzone przez Krzysztofa Markowskiego, służące jako edytor dla początkujących programistów języka Python. Interfejs jest ograniczony do minimum, tak aby nie oszałamiać ilością narzędzi.

Aktualna wersja: **2.0.3.0** – historia zmian znajduje się w pliku [CHANGELOG.md](CHANGELOG.md).

Program przeznaczony jest dla systemu **Windows**.

---

## 🚀 Jak pobrać i zainstalować?

Aby korzystać z programu, nie musisz pobierać kodu źródłowego. Gotowy instalator znajdziesz w sekcji **Releases**:

1. Przejdź do zakładki [Releases](https://github.com/StaryDooh/mkPyEdek/releases) (po prawej stronie ekranu).
2. Pobierz najnowszą wersję instalatora: `mkPyEdek_Setup.exe`.
3. Uruchom pobrany plik i postępuj zgodnie z instrukcjami instalacji.

### Wymagania
*   **System Windows.**
*   **Zainstalowany Python 3** ([python.org/downloads](https://www.python.org/downloads/)). Edytor uruchamia programy za pomocą interpretera zainstalowanego w systemie.
*   Przy instalacji Pythona warto zaznaczyć opcję **„Add python.exe to PATH”** – wtedy mkPyEdek wykryje go automatycznie.
*   Jeśli Python nie zostanie wykryty, program wyświetli okno z możliwością **wskazania pliku `python.exe`** lub przejścia do strony pobierania. Wskazany plik jest sprawdzany, czy rzeczywiście jest działającym interpreterem.

## ✨ Kluczowe funkcje

### Pisanie kodu
*   **Prostota:** intuicyjny interfejs – tylko najpotrzebniejsze polecenia.
*   **Kolorowanie składni** i numeracja linii, także dla f-stringów, dekoratorów i docstringów.
*   **6 motywów kolorystycznych:** Jasny, Ciemny, Kontrastowy, Monokai, Solarized Light, Oceanic.
*   **Podpowiedzi kodu (autouzupełnianie)** oparte na bibliotece Jedi:
    *   pojawiają się po kropce lub po wpisaniu kilku liter; można je też wywołać skrótem `Ctrl+Spacja`,
    *   obejmują biblioteki zainstalowane przez ucznia (np. `pygame`, `numpy`) oraz własne moduły z folderu, w którym leży plik,
    *   lista jest uporządkowana alfabetycznie; nazwy specjalne (`__doc__`, `_prywatne`) pojawiają się dopiero po wpisaniu „_”,
    *   nie wyskakują w komentarzach, napisach ani po kropce w liczbie (np. `3.`),
    *   działają w tle i nie spowalniają pisania.
*   **Automatyczne nawiasy i cudzysłowy:**
    *   po wpisaniu `(`, `[`, `{`, `"` lub `'` edytor dopisuje znak zamykający – ale tylko wtedy, gdy za kursorem nie ma tekstu (poprawianie istniejącego kodu nie tworzy zbędnych znaków),
    *   wpisanie znaku zamykającego, który już stoi za kursorem, po prostu go przeskakuje, a `Backspace` między pustą parą usuwa oba znaki,
    *   trzy cudzysłowy tworzą od razu docstring `"""|"""`,
    *   w komentarzach i napisach apostrofy i nawiasy wpisują się normalnie (`# don't`, `":("`), a w f-stringach `{` dostaje parę `{}`.
*   **Znajdź, Znajdź następny (F3) i Zamień** – działają spójnie, rozróżniając wielkość liter (tak jak Python). F3 informuje o braku wyników i o powrocie do początku pliku, a „Zamień wszystko” nie przesuwa widoku i daje się cofnąć jednym `Ctrl+Z`.

### Uruchamianie programów
*   **Sprawdzanie składni przed uruchomieniem:** jeśli w kodzie jest błąd składni, program go nie uruchomi – zaznaczy błędną linię, poda numer linii i kolumny, a kursor ustawi dokładnie w miejscu błędu.
*   **Uruchamianie w osobnym oknie konsoli (F5):**
    *   programy korzystające z `input()` działają poprawnie,
    *   okno nie zamyka się samo po zakończeniu programu, po błędzie ani po `exit()`,
    *   komunikaty z `sys.exit("…")` są wyświetlane tak jak w zwykłym Pythonie.

### Udostępnianie kodu nauczycielowi
*   **Udostępnij w Classroom** – zapisuje plik, otwiera Google Classroom i folder z zaznaczonym plikiem, gotowym do dołączenia do zadania.
*   **Wyślij kod przez Gmail** – otwiera nową wiadomość z kodem w treści (z wyborem konta Google, co jest ważne na wspólnych komputerach w pracowni). Jeśli kod jest zbyt długi, program poprosi o wysłanie go jako załącznika `.py`, zapisze plik i pokaże go w folderze.
*   **Skopiuj cały kod programu** – jednym kliknięciem do schowka.

### Bezpieczeństwo pracy
*   **Bezpieczny zapis:** plik jest najpierw zapisywany w kopii tymczasowej, a dopiero potem podmieniany. Błąd zapisu (pełny dysk, utrata połączenia z dyskiem sieciowym lub OneDrive) nie niszczy poprzedniej wersji pliku.
*   **Ochrona przed utratą zmian:** pytanie o zapis niezapisanych zmian oraz automatyczna kopia awaryjna kodu w razie nieoczekiwanego błędu programu.
*   **Kodowanie znaków:** obsługa plików UTF-8, Windows-1250, ISO-8859-2 i UTF-16 (np. z Notatnika) bez utraty polskich znaków; przed zapisem w UTF-8 program pyta o zgodę i poprawia deklarację `# -*- coding: … -*-`.
*   **Końce linii Windows (CRLF)** są zachowywane.
*   **Ochrona plików binarnych:** obrazy, archiwa czy pliki `.exe` nie są otwierane, aby nie uległy uszkodzeniu; przed otwarciem bardzo dużego pliku (> 2 MB) program prosi o potwierdzenie.
*   **Lista ostatnio otwieranych plików** (10 pozycji) – brakujący plik jest zgłaszany komunikatem i usuwany z listy.

## ⌨️ Skróty klawiszowe

| Skrót | Działanie |
|---|---|
| `Ctrl+N` | Nowy plik |
| `Ctrl+O` | Otwórz plik |
| `Ctrl+S` | Zapisz |
| `Ctrl+Shift+S` | Zapisz jako |
| `F5` | Uruchom kod |
| `Ctrl+Z` / `Ctrl+Y` | Cofnij / Ponów |
| `Ctrl+X` / `Ctrl+C` / `Ctrl+V` | Wytnij / Kopiuj / Wklej |
| `Ctrl+A` | Zaznacz wszystko |
| `Ctrl+F` | Znajdź |
| `F3` | Znajdź następny |
| `Ctrl+H` | Zamień |
| `Ctrl+Spacja` | Pokaż podpowiedzi kodu |

## 🛠️ Rozwiązywanie problemów

Ustawienia i pliki pomocnicze programu znajdują się w folderze użytkownika: `C:\Users\<nazwa_użytkownika>\.mkPyEdek\`

| Plik / folder | Zawartość |
|---|---|
| `config.json` | Ustawienia: motyw, ostatnie pliki, ostatni folder, ręcznie wskazany interpreter Pythona |
| `config.json.bak` | Kopia uszkodzonego pliku ustawień (tworzona automatycznie; ustawienia, które dało się odczytać, zostają odzyskane) |
| `app.log` | Dziennik błędów – przydatny przy zgłaszaniu problemu |
| `recovery\` | Kopie awaryjne kodu zapisane po nieoczekiwanym błędzie programu |

*   **Po naciśnięciu F5 nic się nie dzieje lub konsola miga i znika** – błędna ścieżka do interpretera jest wykrywana i usuwana automatycznie. Jeśli problem nie ustępuje, zamknij program i usuń plik `config.json`; przy następnym uruchomieniu edytor ponownie wykryje Pythona.
*   **Program zgłasza brak Pythona, choć jest zainstalowany** – wybierz „Wskaż plik” i wskaż `python.exe`, zwykle w folderze `C:\Users\<nazwa_użytkownika>\AppData\Local\Programs\Python\Python3xx\`.
*   **Podpowiedzi nie obejmują zainstalowanej biblioteki** – sprawdź, czy biblioteka jest zainstalowana w tym samym Pythonie, którego używa edytor; ewentualny problem zostanie opisany w pliku `app.log`.
*   **Nie można zapisać pliku** – poprzednia wersja pliku na dysku pozostaje bez zmian. Spróbuj ponownie lub użyj „Zapisz jako…”, aby zapisać plik w innym miejscu.
*   **Zgłaszając błąd**, dołącz opis kroków, które do niego prowadzą, oraz – jeśli to możliwe – zawartość pliku `app.log`.

## 📄 Licencja
Program jest udostępniany na zasadach **licencji niekomercyjnej**. 
*   Dozwolony użytek osobisty i edukacyjny.
*   Zakaz wykorzystania komercyjnego i odsprzedaży.
*   Pełna treść umowy znajduje się w pliku [Licencja.txt](Licencja.txt).

## 👤 Autor
**Krzysztof Markowski**
Jeśli masz pytania lub chcesz zgłosić błąd, możesz skontaktować się ze mną poprzez https://github.com/StaryDooh/mkPyEdek/issues (duży zielony przycisk "New issue" lub "Otwórz zgłoszenie").

---
*Program dostarczany w stanie "takim, w jakim jest" (as is).*

_______________________
Krzysztof Markowski