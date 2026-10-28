# mkPyEdek – problemy do rozwiązania

**Wersja sprawdzana:** 1.0.8.0 · **Docelowy system:** Windows (aplikacja .exe, PyInstaller w trybie katalogu)
**Metoda:** testy automatyczne w prawdziwym PyQt6/QScintilla (tryb offscreen), uruchamianie zapisanych plików przez Pythona, testy runnera F5 z atrapą `msvcrt`, budowanie próbne PyInstallerem 6.22, `pyflakes`. Wszystkie znaleziska poniżej są potwierdzone testem, chyba że zaznaczono inaczej.

Legenda: 🔴 błąd realny · 🟠 nieścisłość / błąd brzegowy · 🟡 bezpieczeństwo i odporność · ⚪ porządki w kodzie

---

## Stan poprzednich poprawek (1.0.6.3 – 1.0.8.0)

Cały zestaw testów regresji przechodzi na wersji 1.0.8.0 – żadna z wcześniejszych poprawek nie została zepsuta.

| # | Problem | Wersja | Test |
|---|---|---|---|
| 1 | Ctrl+Z po otwarciu pliku / „Nowy” przywracał poprzedni plik | 1.0.6.3 | ✔ |
| 2 | Dublowanie nawiasów zamykających | 1.0.6.4 | ✔ |
| 3 | F5 bez Pythona – mylący `TypeError` | 1.0.6.5 | ✔ |
| 4 | Brak walidacji `python_cmd` (config, „Wskaż plik”, autodetekcja) | 1.0.6.6 | ✔ |
| 5 | Filtr okna „Wskaż plik” | 1.0.6.7 | ✔ |
| 6 | Zamknięcie programu w trakcie pracy Jedi | 1.0.6.8 | ✔ |
| 7 | „Udostępnij w Classroom” ignorował wynik zapisu | 1.0.6.9 | ✔ |
| 8 | Explorer nie zaznaczał pliku przy spacjach w ścieżce | 1.0.6.10 | ⚠ tylko linia poleceń – patrz „Do sprawdzenia na Windows” |
| 9 | Style leksera w ciemnych motywach + lekser usuwany przez GC | 1.0.6.11 | ✔ |
| 10 | Końce linii CRLF zamieniane po cichu na LF | 1.0.7.0 | ✔ |
| 11 | Nieistniejący kodek `latin-2` (utrata danych), deklaracja `coding:` | 1.0.7.1 | ✔ |
| 12 | Zaznaczanie linii z błędem składni | 1.0.7.2 | ✔ |
| 13 | Znajdź / F3 / Zamień – niespójności | 1.0.7.3 | ✔ |
| 14 | Gmail – długość kodu; długi kod jako załącznik | 1.0.7.4 | ✔ |
| 15 | Runner F5 – zamknięte stdin | 1.0.7.5 | ✔ (atrapa `msvcrt`) |
| 16 | Jedi nie znał bibliotek ucznia | 1.0.7.6 | ✔ (+ budowanie próbne PyInstallerem) |
| 17 | Nachalne autouzupełnianie i parowanie cudzysłowów | 1.0.7.7 | ✔ 24/24 przypadki |
| 18 | Brak komunikatu o nieistniejącym pliku | 1.0.8.0 | ✔ |

> Uwaga do punktu 15: wbudowane w Pythona `exit()` **zamyka `sys.stdin`**. W wersjach sprzed 1.0.7.5 każdy program ucznia kończący się `exit()` zamykał okno konsoli natychmiast (bez szansy na przeczytanie wyniku). Poprawka 1.0.7.5 usuwa ten problem – test potwierdził, że okno teraz czeka.

---

## 🔴 Błędy realne

### ~~1. Runner F5 połyka komunikat z `sys.exit("…")`~~

> Rozwiązane w 1.0.8.1: runner wypisuje na stderr tekst przekazany do `sys.exit()` / `raise SystemExit(...)`, tak jak zwykły Python. Test porównawczy (9 wariantów: `sys.exit()`, `sys.exit(0)`, `sys.exit(3)`, `sys.exit("tekst")`, `sys.exit([lista])`, `raise SystemExit("…")`, `exit()`, zwykły program, błąd) – wyjście identyczne jak przy `python plik.py`.

`except SystemExit: pass` ignoruje treść wyjątku. Zwykły Python wypisuje tekst przekazany do `sys.exit()` – w mkPyEdek uczeń nie widzi nic.

Test – program `sys.exit("Program tylko dla osób od 13 lat.")`:

| Uruchomienie | Wynik |
|---|---|
| `python plik.py` | `Program tylko dla osób od 13 lat.` (kod 1) |
| mkPyEdek (F5) | tylko „Naciśnij Enter, aby zamknąć…” |

Poprawka w tekście runnera (`_launch_process`):

```python
"except SystemExit as e:\n"
"    if e.code is not None and not isinstance(e.code, int):\n"
"        print(e.code, file=sys.stderr)\n"
```

### ~~2. Otwarcie i zapis pliku binarnego niszczy go~~

> Rozwiązane w 1.0.8.2: pliki z bajtem `0x00` w pierwszych 8 KB (PNG, ZIP, EXE, PYC…) są odrzucane komunikatem „Nieobsługiwany plik” – edytor, lista ostatnich i plik na dysku pozostają nienaruszone. Wyjątek: tekst UTF-16 z BOM (Notatnik → „Unicode”) jest wczytywany poprawnie i przy zapisie, po pytaniu, konwertowany do UTF-8. Pliki > 2 MB wymagają potwierdzenia (stała `LARGE_FILE_WARN_BYTES`).

Filtr „Wszystkie pliki (*)” pozwala otworzyć dowolny plik. Od 1.0.7.1 kodowanie `iso-8859-2` przyjmuje każdy ciąg bajtów, więc np. obrazek PNG wczytuje się jako „tekst”. Przy zapisie pada tylko standardowe pytanie „Plik był oryginalnie zapisany w kodowaniu ISO-8859-2…” – po kliknięciu „Tak” plik zostaje zapisany w UTF-8 i **jest uszkodzony** (test: PNG po zapisie różni się od oryginału).

Poprawka w `open_specific_file`, przed dekodowaniem:

```python
if b'\x00' in raw[:8192]:
    QMessageBox.warning(self, "Nieobsługiwany plik",
        f"Plik {os.path.basename(file_path)} nie jest plikiem tekstowym i nie może być edytowany.")
    return
```

Warto też ostrzegać przy bardzo dużych plikach (np. > 2 MB) – edytor i Jedi zwalniają, a dla ucznia to prawie zawsze pomyłka.

---

## 🟠 Nieścisłości i błędy brzegowe

### 3. Zapis pliku nie jest atomowy – błąd w trakcie zapisu niszczy pracę ucznia

`open(..., 'w')` najpierw czyści plik, a dopiero potem zapisuje treść. Test z symulowanym błędem zapisu (np. pełny dysk, zerwane połączenie z dyskiem sieciowym/OneDrive): komunikat „Nie można zapisać pliku” pojawia się poprawnie, ale na dysku zostaje **ucięty fragment** (`'y = 2\ny = '`) – poprzednia wersja pliku przepadła. W szkołach z dyskami sieciowymi (H:) to realne ryzyko.

```python
tmp = self.current_file + ".tmp"
with open(tmp, 'w', encoding='utf-8', newline='') as f:
    f.write(self.editor.text())
    f.flush(); os.fsync(f.fileno())
os.replace(tmp, self.current_file)      # atomowa podmiana; przy błędzie oryginał zostaje nietknięty
```

(Przy błędzie usunąć `.tmp` w `except`.) Ten sam wzorzec dla `config.json` – patrz punkt 4.

### 4. Uszkodzony `config.json` kasuje ustawienia i listę ostatnich plików

Test: ucięty plik konfiguracji (`{"recent_files": [...], "theme": "Ciemny", `). Po starcie: motyw „Jasny”, lista ostatnich pusta, a `config.json` zostaje od razu **nadpisany wartościami domyślnymi** (zapis wymusza `change_theme` przy starcie). Uczeń traci listę ostatnich plików i nie da się tego odtworzyć.

Poprawka: przy błędzie odczytu zmienić nazwę pliku na `config.json.bak` (do diagnozy) i zapisywać konfigurację atomowo (jak w punkcie 3).

### 5. Lista podpowiedzi zaczyna się od stałych i nazw z podkreśleniem

`showUserList(1, sorted(names))` sortuje alfabetycznie według kodów znaków: WIELKIE LITERY < `_` < małe litery. Test `os.`: Jedi zwraca `abc, abort, access, …`, a edytor pokazuje `CLD_CONTINUED, CLD_DUMPED, CLD_EXITED, …`; po `moj_modul.` pierwsze są `__doc__`, `__file__`, `__name__`. Dla początkującego to najmniej przydatne pozycje.

Scintilla wymaga listy posortowanej (dopasowywanie podczas pisania), chyba że ustawi się własną kolejność. Do wyboru:

```python
# a) ukryć nazwy prywatne/specjalne, chyba że uczeń sam zaczął od „_”
if not word_part.startswith('_'):
    names = [n for n in names if not n.startswith('_')]
# b) zachować kolejność Jedi (najtrafniejsze na górze)
self.SendScintilla(QsciScintilla.SCI_AUTOCSETORDER, QsciScintilla.SC_ORDER_CUSTOM)
```

### 6. Parowanie nawiasów i cudzysłowów przed istniejącym tekstem

Nawias/cudzysłów jest parowany zawsze, także tuż przed literą – typowa sytuacja przy poprawianiu kodu:

| Sytuacja | Wynik |
|---|---|
| `print x`, kursor przed `x`, wpisanie `(` | `print (|)x` |
| `s = abc`, kursor przed `abc`, wpisanie `"` | `s = "|"abc` |
| w napisie `print("…")` wpisanie `:(` | `print(":()")` |

Poprawka: parować tylko, gdy znak za kursorem jest końcem linii, spacją albo jednym z `)]}:,;`; w napisach i komentarzach nie parować nawiasów (z wyjątkiem `{` w f-stringach).

---

## 🟡 Bezpieczeństwo i odporność

- **`shutil.which` w Windows sprawdza też bieżący katalog** (zgodnie z dokumentacją Pythona – chyba że ustawiona jest zmienna `NoDefaultCurrentDirectoryInExePath`). Jeśli edytor zostanie uruchomiony z folderu ucznia (np. przez „Otwórz za pomocą”), podrzucony tam `python.exe` może zostać wybrany jako interpreter. `_is_valid_python` nie chroni – wystarczy, że program wypisze tekst zaczynający się od „Python”. Poprawka: odrzucać trafienia leżące w `os.getcwd()` albo szukać tylko w katalogach z `PATH`.
- **Log rośnie bez końca** (`filemode='a'`) – `logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1_000_000, backupCount=2, encoding='utf-8')`.
- **`AccountChooser` jest nieudokumentowanym adresem Google** – może przestać działać bez ostrzeżenia. Krótki kod nadal trafia w całości do adresu URL, a więc do historii przeglądarki (na wspólnym komputerze widać go po zalogowaniu kolejnej osoby).
- **Błędy przed utworzeniem okna są niewidoczne.** W .exe budowanym z `--noconsole` wyjątek przy `os.makedirs(USER_DIR)` lub `logging.basicConfig` (np. problem z profilem mobilnym) zatrzymuje program bez żadnego komunikatu. *(Nie testowane – analiza kodu.)*
- **Dwa okna edytora nadpisują sobie `config.json`** – ostatnio zamknięte wygrywa (lista ostatnich plików z drugiego okna znika). *(Analiza kodu.)*

---

## ⚪ Nadmiarowy kod i porządki

- **Kod dla macOS i Linuksa jest martwy** (program działa tylko w Windows): gałęzie `Darwin`/`else` w `_launch_process` (~30 linii, w tym plik tymczasowy `.sh` i AppleScript), w `_reveal_in_file_manager`, w `_detect_python` i w filtrze „Wskaż plik”. Po ich usunięciu znika też potrzeba importu `shlex`, `tempfile`, `stat` i większości wywołań `platform.system()`.
- **Nieużywany `import time`** (potwierdza `pyflakes`).
- **Motywy zdefiniowane w dwóch miejscach**: `apply_theme` i `apply_ui_theme`, do tego lista `is_dark` wpisana na sztywno. Jeden słownik `THEMES` z kompletem kolorów usunie duplikację i ryzyko rozjazdu.
- **Motyw nakładany dwa razy przy starcie** (`PythonEditor.__init__` → „Jasny”, potem `change_theme`), a `change_theme` przy każdym starcie zapisuje `config.json` (to właśnie powoduje nadpisanie uszkodzonej konfiguracji z punktu 4).
- **Nadmiarowe zapisy:** każdy zapis pliku zapisuje też `config.json` (`add_to_recent`); F5 na nowym pliku zapisuje plik i konfigurację dwukrotnie (`save_as_file` + `save_file`) – test: 2 zapisy `config.json` na jedno F5.
- `lexer.setDefaultFont(font)` jest zbędne od 1.0.6.11 (baza `lexer.setFont(font)` dla wszystkich stylów); w słowniku `styles` czcionkę wystarczy podawać tylko dla stylów pogrubionych.
- `getattr(self, '_original_encoding', 'utf-8')` – zbędne, atrybut jest zawsze ustawiany w `__init__`.
- Zbędne nawiasy w `key_text == '.' or (key_text.isalnum() or key_text == '_')`.
- Lepiej przekazywać `line` i `index` w sygnale `result_ready` niż odczytywać je przez `self.sender()`.
- `except Exception` w `resource_path` lepiej zawęzić do `AttributeError`.
- `_context_at_cursor` na końcu pliku buduje cały tekst (`self.text()[-1:]`) przy każdym naciśnięciu klawisza – wystarczy `SendScintilla(SCI_GETCHARAT, pos - 1)`. Wpływ na wydajność pomijalny (zmierzone: < 1 ms na plik 20 000 linii), ale to prosta zmiana.
- **Lista ostatnich plików:** pokazuje tylko nazwę (dwa `main.py` z różnych folderów są nie do odróżnienia – warto dodać tooltip z pełną ścieżką); porównanie ścieżek rozróżnia wielkość liter, a Windows nie (`os.path.normcase` przy porównaniu).
- Domyślny folder `~/Documents` może nie istnieć przy przekierowaniu do OneDrive (`OneDrive\Dokumenty`) – lepiej `QStandardPaths.writableLocation(QStandardPaths.StandardLocation.DocumentsLocation)`.

Wrapper `select_all` **nie jest** nadmiarowy i powinien zostać. Sygnał `triggered` przekazuje `checked=False`, więc bezpośrednie podpięcie `editor.selectAll` odznaczałoby tekst zamiast go zaznaczać.

---

## Do sprawdzenia na Windows (nie dało się przetestować w tym środowisku)

- [ ] **Explorer `/select` ze spacjami w ścieżce** (Classroom, Gmail z załącznikiem) – sprawdzona tylko postać linii poleceń.
- [ ] **Runner F5 z prawdziwym `msvcrt`**: program `import sys; sys.stdin.close(); 1/0` oraz program kończący się `exit()` – okno powinno czekać na klawisz.
- [ ] **Podpowiedzi z bibliotek ucznia w zbudowanym .exe** (nowy skrypt `Budowanie_EXE_mkPyEdek.bat`): `import pygame` → `pygame.`; istnienie `dist\mkPyEdek\_internal\jedi\inference\compiled\subprocess\__main__.py`.
- [ ] **Środowisko Jedi z launcherem `py.exe`** – autodetekcja w Windows wybiera najpierw `py`; działanie Jedi z launcherem nie było testowane.
- [ ] **Wersja w `wersja.txt`** zgodna z `VERSION` w kodzie.