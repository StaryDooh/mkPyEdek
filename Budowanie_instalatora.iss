; Wersja pobierana automatycznie z zasobu wersji pliku .exe (nadanego przez wersja.txt
; podczas budowania PyInstallerem) – nie trzeba jej już wpisywać ręcznie.
#define MyAppExe "dist\mkPyEdek\mkPyEdek.exe"
#if !FileExists(AddBackslash(SourcePath) + MyAppExe)
  #error Nie znaleziono dist\mkPyEdek\mkPyEdek.exe – najpierw uruchom Budowanie_EXE_mkPyEdek.bat
#endif
#define MyAppVersion GetVersionNumbersString(AddBackslash(SourcePath) + MyAppExe)
#if MyAppVersion == ""
  #error Plik mkPyEdek.exe nie zawiera informacji o wersji – sprawdź wersja.txt
#endif

[Setup]
; Unikalny identyfikator aplikacji
AppId={{61000D35-DDAF-4F06-8104-0777F0173727}
AppName=mkPyEdek
AppVersion={#MyAppVersion}
; Ta sama wersja we właściwościach pliku instalatora i w „Aplikacje i funkcje”
VersionInfoVersion={#MyAppVersion}
AppVerName=mkPyEdek {#MyAppVersion}
AppPublisher=Krzysztof Markowski

; Domyślny folder instalacji
DefaultDirName={autopf}\mkPyEdek
DefaultGroupName=mkPyEdek
AllowNoIcons=yes

; Wyświetlanie licencji podczas instalacji
LicenseFile=Licencja.txt

; Gdzie ma zostać zapisany gotowy instalator
OutputDir=GitHub
OutputBaseFilename=mkPyEdek_v{#MyAppVersion}

; Ikona instalatora
SetupIconFile=ikona.ico

; Kompresja i wygląd
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: checkablealone

; --- Usunięto [InstallDelete] dla config.json (od wersji 2.0.x) ---
; Program sam wykrywa i naprawia błędną konfigurację (zła ścieżka interpretera, uszkodzony plik),
; a usuwanie config.json przy każdej aktualizacji kasowało uczniom listę ostatnich plików i motyw.

[Files]
; 1. Główny plik wykonywalny
Source: "dist\mkPyEdek\mkPyEdek.exe"; DestDir: "{app}"; Flags: ignoreversion

; 2. CAŁY KATALOG _internal wraz z podfolderami
Source: "dist\mkPyEdek\_internal\*"; DestDir: "{app}\_internal"; Flags: ignoreversion recursesubdirs createallsubdirs

; 3. Zasoby dodatkowe (Ikona i Licencja)
Source: "ikona.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "Licencja.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
; Skróty w Menu Start
Name: "{group}\mkPyEdek"; Filename: "{app}\mkPyEdek.exe"; IconFilename: "{app}\ikona.ico"
Name: "{group}\Licencja mkPyEdek"; Filename: "{app}\Licencja.txt"
Name: "{group}\{cm:UninstallProgram,mkPyEdek}"; Filename: "{uninstallexe}"

; Skrót na pulpicie
Name: "{autodesktop}\mkPyEdek"; Filename: "{app}\mkPyEdek.exe"; IconFilename: "{app}\ikona.ico"; Tasks: desktopicon

[Run]
Filename: "{app}\mkPyEdek.exe"; Description: "{cm:LaunchProgram,mkPyEdek}"; Flags: nowait postinstall skipifsilent