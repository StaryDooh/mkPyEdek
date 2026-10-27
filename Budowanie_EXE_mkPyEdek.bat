@echo off
echo ==========================================
echo Budowanie mkPyEdek (Tryb Katalogu)
echo ==========================================

:: 1. Czyszczenie starych kompilacji
if exist build rd /s /q build
if exist dist rd /s /q dist

echo.
echo [1/3] Stare pliki usuniete.

:: 2. Lokalizacja zrodel jedi i parso (od wersji 1.0.7.6)
:: Autouzupelnianie uruchamia w Pythonie ucznia proces pomocniczy Jedi, ktory potrzebuje
:: plikow zrodlowych .py pakietow jedi i parso. PyInstaller domyslnie pakuje je w postaci
:: skompilowanej, dlatego dolaczamy oba katalogi jako dane (--add-data).
echo [2/3] Szukam pakietow jedi i parso...
set "JEDI_DIR="
set "PARSO_DIR="
for /f "delims=" %%i in ('python -c "import jedi, os; print(os.path.dirname(jedi.__file__))"') do set "JEDI_DIR=%%i"
for /f "delims=" %%i in ('python -c "import parso, os; print(os.path.dirname(parso.__file__))"') do set "PARSO_DIR=%%i"

if not defined JEDI_DIR goto brak_pakietow
if not defined PARSO_DIR goto brak_pakietow
if not exist "%JEDI_DIR%\inference\compiled\subprocess\__main__.py" goto brak_pakietow
echo       jedi:  %JEDI_DIR%
echo       parso: %PARSO_DIR%

echo [3/3] Rozpoczynam prace PyInstallera...

:: 3. Kompilacja do katalogu (--onedir)

python -m PyInstaller ^
	--noconsole ^
	--icon="ikona.ico" ^
	--version-file="wersja.txt" ^
	--add-data "ikona.ico;." ^
	--add-data "%JEDI_DIR%;jedi" ^
	--add-data "%PARSO_DIR%;parso" ^
	mkPyEdek.py

echo.
if %ERRORLEVEL% EQU 0 (
    echo ==========================================
    echo SUKCES: Gotowe w dist\mkPyEdek
    echo ==========================================
) else (
    echo ##########################################
    echo BLAD: Cos poszlo nie tak przy budowaniu!
    echo ##########################################
)
goto koniec

:brak_pakietow
echo.
echo ##########################################
echo BLAD: Nie znaleziono pakietow jedi/parso.
echo Zainstaluj je poleceniem: python -m pip install jedi
echo ##########################################

:koniec
pause