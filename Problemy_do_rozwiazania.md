### 🔴 Błędy realne (do poprawy w pierwszej kolejności)

~~**1. Ctrl+Z po otwarciu pliku przywraca poprzedni plik.**  
`setText()` i `clear()` nie czyszczą historii cofania w QScintilla. Wystarczy otworzyć plik B i nacisnąć Ctrl+Z, a w oknie pojawi się treść pliku A. Następne Ctrl+S nadpisze wtedy plik B treścią pliku A. To samo dzieje się po „Nowy”.~~

~~python~~

```python
self.editor.setText(content)
self.editor.SendScintilla(QsciScintilla.SCI_EMPTYUNDOBUFFER)
```

~~To samo trzeba dodać w `new_file()` po `clear()`.~~

~~**2. Nawiasy zamykające się dublują.**~~  
Program obsługuje „przeskakiwanie” tylko dla cudzysłowów. Gdy uczeń wpisze ręcznie `print()`, dostanie `print())`. Na lekcjach będzie to najczęstsza skarga.

~~python~~

```python
if key_text in (')', ']', '}') and not self.hasSelectedText():
    line, index = self.getCursorPosition()
    if self.text(line)[index:index + 1] == key_text:
        self.setCursorPosition(line, index + 1)
        return
```

~~**3. F5 bez wykrytego Pythona pokazuje mylący komunikat.**~~  
~~Gdy użytkownik wybierze „Ignoruj”, `python_cmd` ma wartość `None`. Wtedy `Popen([None, ...])` rzuca `TypeError`, a uczeń widzi komunikat „Nie uruchomiono interpretera: expected str…”. Na początku `run_code` warto dodać:~~

~~python~~

```python
if not self.python_cmd:
    self.check_python_installed()
    if not self.python_cmd:
        return
```

~~**4. Ścieżka `python_cmd` z config.json nie jest sprawdzana.**  ~~
~~`os.path.isfile` i `os.access(X_OK)` w Windows przepuszczą każdy istniejący plik. Błędny wpis w konfiguracji daje dokładnie ten objaw, który już raz się pojawił: konsola mignie i zniknie. Proponuję wydzielić `_is_valid_python(path)`, czyli uruchomienie `--version` i sprawdzenie, czy wynik zaczyna się od „Python”. Tej funkcji należy użyć w `load_config`, w „Wskaż plik” i w `_detect_python`. Jeśli zapisana ścieżka okaże się zła, program powinien ją porzucić i wrócić do autodetekcji.~~

~~**5. Filtr w oknie „Wskaż plik” nie działa.**  ~~
~~`"Python Executable (*.exe; python; python3)"`: Qt rozdziela wzorce spacją, nie średnikiem. Wzorzec `*.exe;` zawiera dosłowny średnik, więc pliki .exe nie zostaną pokazane. Poprawny zapis to `"Interpreter Python (python*.exe py.exe)"` w Windows oraz `"(python python3)"` w pozostałych systemach.~~

~~**6. Zamknięcie programu w trakcie pracy Jedi może zakończyć się awarią.**  ~~
~~`wait(500)` czeka najwyżej pół sekundy. Pierwsze wywołanie Jedi na większym pliku trwa dłużej, więc obiekt QThread zostaje zniszczony w trakcie działania i pojawia się „QThread: Destroyed while thread is still running”, czyli twarde przerwanie procesu. Należy użyć `wait()` bez limitu. Lepiej też przenieść tę logikę do metody `editor.shutdown()` zamiast sięgać z okna do prywatnych pól `_debounce` i `_jedi_thread`.~~

~~**7. „Udostępnij w Classroom” ignoruje wynik zapisu.**  ~~
~~Gdy plik jest nowy, zapisuje się dwukrotnie: najpierw w `save_as_file`, potem w `save_file`. Co gorsza, wynik `save_file()` nie jest sprawdzany. Po nieudanym zapisie albo anulowaniu pytania o kodowanie Classroom i tak się otworzy z nieaktualnym plikiem. Cała obsługa sprowadza się do:~~

~~python~~

```python
if not self.save_file():   # save_file sam przechodzi do save_as
    return
```

~~**8. Explorer nie zaznacza pliku, gdy ścieżka zawiera spacje.**  ~~
~~Lista `["explorer", f"/select,{path}"]` zamienia się w `"/select,C:\Users\Jan Kowalski\..."`. Explorer nie rozumie argumentu objętego w całości cudzysłowem i otwiera „Dokumenty”. Działa wersja tekstowa:~~

~~python~~

```python
subprocess.Popen(f'explorer /select,"{file_path}"')
```

**9. Część kodu źle wygląda w ciemnych motywach.**  
Pętla kolorów obejmuje tylko 12 stylów. Dekoratory, f-stringi (`DoubleQuotedFString` i pokrewne), `CommentBlock` i `UnclosedString` zachowują domyślne kolory leksera, często ciemne na ciemnym tle. Mają też inną czcionkę, bo `setDefaultFont` nie zmienia już istniejących stylów. Przed pętlą wystarczy ustawić bazę dla wszystkich stylów:

python

```python
lexer.setColor(fg); lexer.setFont(font); lexer.setPaper(bg)
```

Potem warto dopisać brakujące style do słownika.

### 🟠 Nieścisłości i błędy brzegowe

**10. Mieszane końce linii.** Edytor wymusza `EolUnix`, ale plik z `\r\n` jest wczytywany bez zmian, a zapis z `newline=''` zachowuje mieszankę. Po wczytaniu warto wykryć styl: jeśli plik zawiera `'\r\n'`, ustawić `setEolMode(EolWindows)`.

**11. Wykrywanie kodowania:**

-   Plik UTF-8 z BOM wczyta się z niewidocznym `\ufeff`, a `compile()` zgłosi błąd składni w linii 1. Na pierwszej pozycji listy powinno być `'utf-8-sig'`.
-   `cp1250` dekoduje prawie każdy ciąg bajtów, a `latin-2` dekoduje każdy. Gałąź `if content is None` jest więc martwym kodem.
-   Deklaracja `# -*- coding: ... -*-` (PEP 263) jest ignorowana.

**12. Zaznaczenie linii z błędem.** `lineLength()` zwraca liczbę **bajtów** razem ze znakiem końca linii, a `setSelection` oczekuje znaków. Przy polskich znakach zaznaczenie wychodzi poza linię. Należy użyć `len(self.editor.text(line).rstrip('\r\n'))`. Przy okazji można ustawić kursor na `e.offset`, czyli dokładnie w miejscu błędu.

**13. „Zamień” działa niespójnie.**

-   `findFirst(..., cs=False)` szuka bez rozróżniania wielkości liter, a `str.replace` przy „zamień wszystko” ją rozróżnia. Liczba trafień i zamian może się więc różnić.
-   „Zamień wszystko” podmienia cały tekst, przez co kursor i przewinięcie lądują na początku pliku.
-   F3 po końcu wyników niczego nie komunikuje.

**14. Limit długości kodu w Gmailu.** Limit 1500 znaków jest liczony na surowym kodzie. Po kodowaniu URL polska litera zajmuje 6 znaków, a cały adres jest kodowany jeszcze raz w `continue=`. Należy mierzyć `len(urllib.parse.quote(code))`. Endpoint `AccountChooser` jest nieudokumentowany i może przestać działać bez ostrzeżenia.

**15. Uruchamianie przez `runpy` różni się od zwykłego `python plik.py`.**

-   `multiprocessing` w Windows (spawn) i `pickle` klas z `__main__` mogą nie działać.
-   Gdy skrypt zamknie stdin, `input()` w `finally` rzuci `EOFError`.
-   W systemach macOS i Linux skrypt startuje bez runnera, więc zachowanie zależy od systemu. Do drobnych zadań szkolnych to wystarcza, ale warto o tym pamiętać.

**16. Autouzupełnianie nie zna bibliotek ucznia.**  
`jedi.Script(source)` dostaje kod bez `path` i bez `environment`. W zbudowanym .exe Jedi zna tylko to, co spakowano do programu, więc `pygame` czy `numpy` z Pythona ucznia nie będą podpowiadane. Importy względne też nie zadziałają. Rozwiązanie:

python

```python
env = jedi.create_environment(python_cmd, safe=False)   # utworzyć raz i zachować
jedi.Script(source, path=current_file, environment=env)
```

**17. Autouzupełnianie bywa nachalne.**

-   Lista podpowiedzi wyskakuje także w komentarzach i napisach.
-   Wpisanie `3.` pokazuje metody typu float.
-   Auto-cudzysłów psuje `don't` w komentarzu.
-   Potrójne `"""` daje `"""|"`.

Warto sprawdzać styl pod kursorem (`SCI_GETSTYLEAT`) i nie parować ani nie podpowiadać wewnątrz komentarzy i napisów.

**18. Plik podany w linii poleceń albo z listy ostatnich, który nie istnieje,** jest pomijany bez żadnego komunikatu.

### 🟡 Bezpieczeństwo i odporność

-   **`shutil.which` w Windows przeszukuje najpierw bieżący katalog.** W pracowni ktoś może podrzucić `python.exe` do folderu, z którego startuje edytor. Bezpieczniej szukać wyłącznie w `PATH` albo odrzucać trafienia z `os.getcwd()`.
-   **Zapis nie jest atomowy** ani dla pliku z kodem, ani dla config.json. Awaria w trakcie zapisu może zniszczyć plik. Bezpieczniejszy wzorzec to zapis do `plik.tmp`, a potem `os.replace()`. Uszkodzony config.json jest dziś po cichu nadpisywany wartościami domyślnymi, więc lista ostatnich plików znika.
-   **Log rośnie bez końca** (`filemode='a'`). Lepiej użyć `RotatingFileHandler`.
-   **Kod wysyłany przez Gmail trafia w całości do adresu URL,** a więc do historii przeglądarki.

### ⚪ Nadmiarowy kod i porządki

-   Nieużywany `import time`.
-   **Motywy są zdefiniowane w dwóch miejscach**: w `apply_theme` i `apply_ui_theme`, do tego lista `is_dark` jest wpisana na sztywno. Jeden słownik `THEMES` z kompletem kolorów usunie duplikację i ryzyko rozjazdu.
-   `getattr(self, '_original_encoding', 'utf-8')` jest zbędne, bo atrybut jest zawsze ustawiany w `__init__`.
-   Motyw edytora jest nakładany dwa razy przy starcie: w `PythonEditor.__init__` i w `change_theme`. Do tego `change_theme` zapisuje config przy każdym uruchomieniu programu.
-   Nawiasy w `key_text == '.' or (key_text.isalnum() or ...)` są zbędne.
-   Lepiej przekazywać `line` i `index` w sygnale `result_ready` niż odczytywać je przez `self.sender()`.
-   `_detect_python` przy starcie może blokować GUI nawet przez 3 × 5 s.
-   `except Exception` w `resource_path` lepiej zawęzić do `AttributeError`.
-   Na liście ostatnich plików dwa pliki `main.py` z różnych folderów są nie do odróżnienia. Warto dodać tooltip z pełną ścieżką.

Wrapper `select_all` **nie jest** nadmiarowy i powinien zostać. Sygnał `triggered` przekazuje `checked=False`, więc bezpośrednie podpięcie `editor.selectAll` odznaczałoby tekst zamiast go zaznaczać.