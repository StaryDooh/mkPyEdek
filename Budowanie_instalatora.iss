#define MyAppVersion "1.0.6.2"

[Setup]
; Unikalny identyfikator aplikacji
AppId={{61000D35-DDAF-4F06-8104-0777F0173727}
AppName=mkPyEdek
AppVersion={#MyAppVersion}
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

; --- Czyszczenie nieprawidłowego pliku konfiguracyjnego ze starszych wersji ---
[InstallDelete]
Type: files; Name: "{%USERPROFILE}\.mkPyEdek\config.json"

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