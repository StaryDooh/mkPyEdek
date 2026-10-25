# mkPyEdek

**mkPyEdek** to darmowe narzędzie stworzone przez Krzysztofa Markowskiego, służące jako edytor dla początkujących programistów języka Python. Interfejs jest ograniczony do minimum, tak aby nie oszałamiać ilością narzędzi.

Aktualna wersja: **1.0.6.10** – historia zmian znajduje się w pliku [CHANGELOG.md](CHANGELOG.md).

---

## 🚀 Jak pobrać i zainstalować?

Aby korzystać z programu, nie musisz pobierać kodu źródłowego. Gotowy instalator znajdziesz w sekcji **Releases**:

1. Przejdź do zakładki [Releases](https://github.com/StaryDooh/mkPyEdek/releases) (po prawej stronie ekranu).
2. Pobierz najnowszą wersję instalatora: `mkPyEdek_Setup.exe`.
3. Uruchom pobrany plik i postępuj zgodnie z instrukcjami instalacji.

### Wymagania
*   **Zainstalowany Python 3** ([python.org/downloads](https://www.python.org/downloads/)). Edytor uruchamia programy za pomocą interpretera zainstalowanego w systemie.
*   Przy instalacji Pythona w systemie Windows warto zaznaczyć opcję **„Add python.exe to PATH”** – wtedy mkPyEdek wykryje go automatycznie.
*   Jeśli Python nie zostanie wykryty, program wyświetli okno z możliwością **wskazania pliku `python.exe`** lub przejścia do strony pobierania. Wskazany plik jest sprawdzany, czy rzeczywiście jest działającym interpreterem.

## ✨ Kluczowe funkcje
*   **Prostota:** Intuicyjny interfejs użytkownika – tylko najpotrzebniejsze polecenia.
*   **Kolorowanie składni** i numeracja linii.
*   **6 motywów kolorystycznych:** Jasny, Ciemny, Kontrastowy, Monokai, Solarized Light, Oceanic.
*   **Podpowiedzi kodu (autouzupełnianie)** oparte na bibliotece Jedi – pojawiają się po kropce lub po wpisaniu kilku liter; można je też wywołać skrótem `Ctrl+Spacja`. Działają w tle, nie spowalniając pisania.
*   **Automatyczne nawiasy i cudzysłowy:** po wpisaniu `(`, `[`, `{`, `"` lub `'` edytor dopisuje znak zamykający. Wpisanie nawiasu zamykającego, który już stoi za kursorem, po prostu go przeskakuje, a `Backspace` między pustą parą usuwa oba znaki.
*   **Sprawdzanie składni przed uruchomieniem:** jeśli w kodzie jest błąd składni, program go nie uruchomi, tylko zaznaczy błędną linię i wyświetli komunikat.
*   **Uruchamianie w osobnym oknie konsoli (F5):** programy korzystające z `input()` działają poprawnie, a okno nie zamyka się samo po zakończeniu programu ani po błędzie.
*   **Łatwe wysyłanie do sprawdzenia:**
    *   **Udostępnij w Classroom** – zapisuje plik, otwiera Google Classroom i folder z zaznaczonym plikiem, gotowym do dołączenia do zadania.
    *   **Wyślij kod przez Gmail** – otwiera nową wiadomość z kodem w treści (z wyborem konta Google, co jest ważne na wspólnych komputerach w pracowni).
    *   **Skopiuj cały kod programu** – jednym kliknięciem do schowka.
*   **Ochrona przed utratą pracy:** pytanie o zapis niezapisanych zmian oraz automatyczna kopia awaryjna kodu w razie nieoczekiwanego błędu programu.
*   **Obsługa starszych plików** zapisanych w kodowaniu Windows-1250 (z pytaniem przed zapisem w UTF-8).
*   **Lista ostatnio otwieranych plików** (10 pozycji).

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
| `app.log` | Dziennik błędów – przydatny przy zgłaszaniu problemu |
| `recovery\` | Kopie awaryjne kodu zapisane po nieoczekiwanym błędzie programu |

*   **Po naciśnięciu F5 nic się nie dzieje lub konsola miga i znika** – zamknij program i usuń plik `config.json`. Przy następnym uruchomieniu edytor ponownie wykryje Pythona. (Od wersji 1.0.6.6 błędna ścieżka do interpretera jest wykrywana i usuwana automatycznie.)
*   **Program zgłasza brak Pythona, choć jest zainstalowany** – wybierz „Wskaż plik” i wskaż `python.exe`, zwykle w folderze `C:\Users\<nazwa_użytkownika>\AppData\Local\Programs\Python\Python3xx\`.
*   **Zgłaszając błąd**, dołącz opis kroków, które do niego prowadzą, oraz – jeśli to możliwe – zawartość pliku `app.log`.

## 📄 Licencja
Program jest udostępniany na zasadach **licencji niekomercyjnej**. 
*   Dozwolony użytek osobisty i edukacyjny.
*   Zakaz wykorzystania komercyjnego i odsprzedaży.
*   Pełna treść umowy znajduje się w pliku [LICENSE](LICENSE).

## 👤 Autor
**Krzysztof Markowski**
Jeśli masz pytania lub chcesz zgłosić błąd, możesz skontaktować się ze mną poprzez https://github.com/StaryDooh/mkPyEdek/issues (duży zielony przycisk "New issue" lub "Otwórz zgłoszenie").

---
*Program dostarczany w stanie "takim, w jakim jest" (as is).*

_______________________
Krzysztof Markowski
https://www.youtube.com/@StaryDooh