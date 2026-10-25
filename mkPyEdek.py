import sys
import os
import subprocess
import jedi
import webbrowser
import platform
import shutil
import json
import urllib.parse
import logging
import shlex
import time
import traceback
import threading
from datetime import datetime
from PyQt6.QtWidgets import (QApplication, QMainWindow, QFileDialog,
                             QMessageBox, QWidget, QVBoxLayout, QStyle, QInputDialog)
from PyQt6.QtGui import QAction, QFont, QColor, QIcon, QActionGroup
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.Qsci import QsciScintilla, QsciLexerPython

# --- KONFIGURACJA ŚCIEŻEK I LOGÓW ---
if getattr(sys, 'frozen', False):
    APP_DIR = os.path.dirname(sys.executable)
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))

USER_DIR = os.path.join(os.path.expanduser("~"), ".mkPyEdek")
CONFIG_FILE = os.path.join(USER_DIR, "config.json")
LOG_FILE = os.path.join(USER_DIR, "app.log")
RECOVERY_DIR = os.path.join(USER_DIR, "recovery")

os.makedirs(USER_DIR, exist_ok=True)

logging.basicConfig(
    filename=LOG_FILE,
    filemode='a',
    level=logging.WARNING,
    format='%(asctime)s - %(levelname)s - %(message)s',
    encoding='utf-8'
)

# --- GLOBALNA OBSŁUGA WYJĄTKÓW ---
_in_handler = False

def global_exception_handler(exctype, value, tb):
    global _in_handler
    
    # Logowanie wyjątku (bezpieczne niezależnie od wątku)
    err = "".join(traceback.format_exception(exctype, value, tb))
    logging.error("Nieobsłużony wyjątek:\n%s", err)
    
    app = QApplication.instance()
    
    # Warunki bezpieczeństwa: brak aplikacji, reentrancja lub wywołanie z wątku roboczego
    if app is None or _in_handler or threading.current_thread() is not threading.main_thread():
        return                               

    _in_handler = True
    try:
        backup_msg = "Nie udało się utworzyć kopii zapasowej."
        
        # Próba odnalezienia głównego okna i zapisania awaryjnej kopii kodu
        main_window = next((w for w in app.topLevelWidgets() if isinstance(w, QMainWindow)), None)
        if main_window and hasattr(main_window, 'editor') and main_window.editor is not None:
            try:
                code_content = main_window.editor.text()
                if code_content:
                    os.makedirs(RECOVERY_DIR, exist_ok=True)
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    recovery_path = os.path.join(RECOVERY_DIR, f"recovery_{timestamp}.py")
                    
                    with open(recovery_path, "w", encoding="utf-8") as f:
                        f.write(code_content)
                    backup_msg = f"Twój kod został awaryjnie zapisany w:\n{recovery_path}"
            except Exception as save_err:
                logging.error(f"Błąd tworzenia kopii zapasowej: {save_err}")
                backup_msg = f"Próba utworzenia kopii zapasowej nie powiodła się: {save_err}"

        # Wyświetlenie okna błędu w głównym wątku GUI
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Błąd krytyczny")
        msg.setText("Wystąpił nieoczekiwany błąd w aplikacji.")
        msg.setInformativeText(f"{backup_msg}\n\nAplikacja może działać niestabilnie.")
        msg.setDetailedText(err)
        
        btn_quit = msg.addButton("Zakończ program", QMessageBox.ButtonRole.DestructiveRole)
        msg.addButton("Kontynuuj", QMessageBox.ButtonRole.RejectRole)
        
        msg.exec()
        
        if msg.clickedButton() == btn_quit:
            app.quit()
    finally:
        _in_handler = False

sys.excepthook = global_exception_handler

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = APP_DIR
    return os.path.join(base_path, relative_path)


# ─────────────────────────────────────────────────────────────────────────────
# Autouzupełnianie Jedi w tle (QThread) - pobiera listę w tle
# ─────────────────────────────────────────────────────────────────────────────
class JediCompletionThread(QThread):
    result_ready = pyqtSignal(list)
    
    def __init__(self, source, line, index):
        super().__init__()
        self.source = source
        self.line = line
        self.index = index
        
    def run(self):
        try:
            script = jedi.Script(self.source)
            completions = script.complete(self.line + 1, self.index)
            result = [c.name for c in completions] if completions else []
            self.result_ready.emit(result)
        except Exception as e:
            logging.warning(f"Błąd autouzupełniania Jedi: {e}")
            self.result_ready.emit([])


# ─────────────────────────────────────────────────────────────────────────────
# KLASA EDYTORA
# ─────────────────────────────────────────────────────────────────────────────
class PythonEditor(QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setUtf8(True)
        self.setEolMode(QsciScintilla.EolMode.EolUnix)
        self.setMarginType(0, QsciScintilla.MarginType.NumberMargin)
        self.setMarginWidth(0, "00000")
        self.setIndentationsUseTabs(False)
        self.setTabWidth(4)
        self.setAutoIndent(True)
        self.setCaretLineVisible(True)

        self.current_completions = []
        self._jedi_thread = None
        self._pending_completion = False
        self._shutting_down = False

        self._debounce = QTimer(self)
        self._debounce.setSingleShot(True)
        self._debounce.setInterval(250)
        self._debounce.timeout.connect(self._run_jedi)

        self.userListActivated.connect(self.on_user_list_activated)
        self.apply_theme("Jasny")

    def apply_theme(self, theme_name):
        font = QFont("Consolas", 12)
        font_bold = QFont("Consolas", 12, QFont.Weight.Bold)

        if theme_name == "Ciemny":
            bg, fg, margin_bg, caret_bg = QColor("#282a36"), QColor("#f8f8f2"), QColor("#44475a"), QColor("#44475a")
            keyword_col, string_col, comment_col = QColor("#ff79c6"), QColor("#f1fa8c"), QColor("#6272a4")
            func_col, class_col, number_col, var_col = QColor("#50fa7b"), QColor("#8be9fd"), QColor("#bd93f9"), QColor("#ffb86c")
        elif theme_name == "Kontrastowy":
            bg, fg, margin_bg, caret_bg = QColor("#000000"), QColor("#00ff00"), QColor("#111111"), QColor("#222222")
            keyword_col, string_col, comment_col = QColor("#ffffff"), QColor("#ffff00"), QColor("#008800")
            func_col, class_col, number_col, var_col = QColor("#00ffff"), QColor("#ff00ff"), QColor("#ff0000"), QColor("#ffffff")
        elif theme_name == "Monokai":
            bg, fg, margin_bg, caret_bg = QColor("#272822"), QColor("#f8f8f2"), QColor("#3e3d32"), QColor("#3e3d32")
            keyword_col, string_col, comment_col = QColor("#f92672"), QColor("#e6db74"), QColor("#75715e")
            func_col, class_col, number_col, var_col = QColor("#a6e22e"), QColor("#66d9ef"), QColor("#ae81ff"), QColor("#f8f8f2")
        elif theme_name == "Solarized Light":
            bg, fg, margin_bg, caret_bg = QColor("#fdf6e3"), QColor("#657b83"), QColor("#eee8d5"), QColor("#eee8d5")
            keyword_col, string_col, comment_col = QColor("#859900"), QColor("#2aa198"), QColor("#93a1a1")
            func_col, class_col, number_col, var_col = QColor("#268bd2"), QColor("#b58900"), QColor("#d33682"), QColor("#268bd2")
        elif theme_name == "Oceanic":
            bg, fg, margin_bg, caret_bg = QColor("#1b2b34"), QColor("#d8dee9"), QColor("#343d46"), QColor("#343d46")
            keyword_col, string_col, comment_col = QColor("#c594c5"), QColor("#99c794"), QColor("#65737e")
            func_col, class_col, number_col, var_col = QColor("#6699cc"), QColor("#fac863"), QColor("#f99157"), QColor("#ffffff")
        else:  # Jasny
            bg, fg, margin_bg, caret_bg = QColor("#ffffff"), QColor("#000000"), QColor("#f0f0f0"), QColor("#e8e8e8")
            keyword_col, string_col, comment_col = QColor("#0000ff"), QColor("#008000"), QColor("#808080")
            func_col, class_col, number_col, var_col = QColor("#795e26"), QColor("#267f99"), QColor("#098658"), QColor("#000080")

        lexer = self.lexer()
        if not isinstance(lexer, QsciLexerPython):
            lexer = QsciLexerPython()
            lexer.setDefaultFont(font)
            self.setLexer(lexer)
        else:
            lexer.setDefaultFont(font)

        lexer.setDefaultPaper(bg)
        lexer.setDefaultColor(fg)
        lexer.setPaper(bg)

        styles = {
            QsciLexerPython.Default: (fg, font),
            QsciLexerPython.Comment: (comment_col, font),
            QsciLexerPython.Number: (number_col, font),
            QsciLexerPython.DoubleQuotedString: (string_col, font),
            QsciLexerPython.SingleQuotedString: (string_col, font),
            QsciLexerPython.TripleSingleQuotedString: (string_col, font),
            QsciLexerPython.TripleDoubleQuotedString: (string_col, font),
            QsciLexerPython.Keyword: (keyword_col, font),
            QsciLexerPython.ClassName: (class_col, font_bold),
            QsciLexerPython.FunctionMethodName: (func_col, font_bold),
            QsciLexerPython.Operator: (fg, font),
            QsciLexerPython.Identifier: (var_col, font_bold)
        }

        for style, (color, st_font) in styles.items():
            lexer.setColor(color, style)
            lexer.setFont(st_font, style)
            lexer.setPaper(bg, style)

        self.setMarginsBackgroundColor(margin_bg)
        self.setMarginsForegroundColor(fg)
        self.setCaretLineBackgroundColor(caret_bg)
        self.setCaretForegroundColor(fg)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Backspace and not self.hasSelectedText():
            line, index = self.getCursorPosition()
            if index > 0:
                prev = self.text(line)[index - 1:index]
                nxt  = self.text(line)[index:index + 1]
                closing = {'(': ')', '[': ']', '{': '}'}
                if prev in closing and closing[prev] == nxt:
                    self.setSelection(line, index - 1, line, index + 1)
                    self.removeSelectedText()
                    return

                if prev in ('"', "'") and nxt == prev:
                    full_line = self.text(line)
                    before = full_line[:index - 1]
                    after  = full_line[index + 1:]
                    if not (before.endswith(prev) or after.startswith(prev)):
                        self.setSelection(line, index - 1, line, index + 1)
                        self.removeSelectedText()
                        return

        key_text = event.text()
        pairs = {'(': ')', '[': ']', '{': '}', '"': '"', "'": "'"}

        # Przeskakiwanie nawiasu zamykającego, jeśli już stoi za kursorem
        if key_text in (')', ']', '}') and not self.hasSelectedText():
            line, index = self.getCursorPosition()
            if self.text(line)[index:index + 1] == key_text:
                self.setCursorPosition(line, index + 1)
                return

        if key_text in pairs:
            line, index = self.getCursorPosition()

            if self.hasSelectedText():
                sel = self.selectedText()
                self.replaceSelectedText(key_text + sel + pairs[key_text])
                return

            if key_text in ['"', "'"]:
                next_char = self.text(line)[index:index + 1]
                if next_char == key_text:
                    self.setCursorPosition(line, index + 1)
                    return

            self.insert(key_text + pairs[key_text])
            self.setCursorPosition(line, index + 1)
            return

        if event.modifiers() == Qt.KeyboardModifier.ControlModifier and event.key() == Qt.Key.Key_Space:
            self.request_jedi_completions()
            return

        super().keyPressEvent(event)

        if key_text == '.' or (key_text.isalnum() or key_text == '_'):
            line, index = self.getCursorPosition()
            word_part = self.get_word_before_cursor(line, index)
            if key_text == '.' or len(word_part) >= 2:
                self.request_jedi_completions()

    def get_word_before_cursor(self, line, index):
        full_line = self.text(line)
        part = full_line[:index]
        word = ""
        for char in reversed(part):
            if char.isalnum() or char == '_':
                word = char + word
            else:
                break
        return word

    def request_jedi_completions(self):
        if self._shutting_down:
            return
        self._debounce.start()

    def shutdown(self):
        """Zatrzymuje autouzupełnianie i czeka na zakończenie wątku Jedi.
        Wywoływane przy zamykaniu programu; można wywołać wielokrotnie."""
        if self._shutting_down:
            return
        self._shutting_down = True
        self._debounce.stop()
        self._pending_completion = False

        t = self._jedi_thread
        if t is not None:
            # Wynik nie jest już potrzebny – odłącz sygnały, aby nie trafiły do zamykanego okna
            try:
                t.result_ready.disconnect()
            except TypeError:
                pass
            if t.isRunning():
                # Bez limitu czasu: zniszczenie działającego QThread kończy proces awaryjnie
                t.wait()
        self._jedi_thread = None

    def _run_jedi(self):
        if self._shutting_down:
            return
        if self._jedi_thread is not None:
            self._pending_completion = True
            return
            
        line, index = self.getCursorPosition()
        t = JediCompletionThread(self.text(), line, index)
        t.result_ready.connect(self._on_jedi_completed)
        t.finished.connect(self._on_jedi_finished)
        t.finished.connect(t.deleteLater)
        self._jedi_thread = t
        t.start()

    def _on_jedi_completed(self, names):
        t = self.sender()
        if self._shutting_down or t is None:
            return
        if not names or (t.line, t.index) != self.getCursorPosition():
            return
        
        self.current_completions = names
        self.showUserList(1, sorted(names))

    def _on_jedi_finished(self):
        self._jedi_thread = None
        if self._pending_completion and not self._shutting_down:
            self._pending_completion = False
            self._debounce.start()

    def on_user_list_activated(self, list_id, text):
        if list_id != 1:
            return

        if text not in self.current_completions:
            return

        line, index = self.getCursorPosition()
        word_part = self.get_word_before_cursor(line, index)

        self.setSelection(line, index - len(word_part), line, index)
        self.removeSelectedText()
        self.insert(text)
        self.setCursorPosition(line, index - len(word_part) + len(text))


# ─────────────────────────────────────────────────────────────────────────────
# GŁÓWNA KLASA APLIKACJI
# ─────────────────────────────────────────────────────────────────────────────
class MkPyEdekGUI(QMainWindow):
    VERSION = "1.0.6.10"

    def __init__(self, file_to_open=None):
        super().__init__()
        self.current_file = None
        self.recent_files = []
        self.current_theme = "Jasny"
        self.last_dir = os.path.expanduser("~/Documents")
        self.last_search = ""
        self._original_encoding = 'utf-8'

        self.python_cmd = None
        self._manual_python_cmd = False

        self.load_config()
        self.init_ui()
        self.showMaximized()
        self.check_python_installed()

        if file_to_open:
            self.open_specific_file(file_to_open)

    @staticmethod
    def _is_valid_python(path):
        """Sprawdza, czy plik jest działającym interpreterem Pythona (uruchamia `--version`)."""
        if not path or not isinstance(path, str) or not os.path.isfile(path):
            return False
        try:
            flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
            r = subprocess.run([path, "--version"], capture_output=True, text=True, timeout=5,
                               creationflags=flags)
        except (OSError, subprocess.SubprocessError, ValueError):
            return False
        return r.returncode == 0 and (r.stdout + r.stderr).strip().startswith("Python")

    def _detect_python(self):
        names = ["py", "python", "python3"] if platform.system() == "Windows" else ["python3", "python"]
        for name in names:
            path = shutil.which(name)
            if path and self._is_valid_python(path):
                return path
        return None

    def load_config(self):
        invalid_stored_cmd = False
        if os.path.exists(CONFIG_FILE):
            try:
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.recent_files = data.get("recent_files", [])
                    self.current_theme = data.get("theme", "Jasny")
                    stored_dir = data.get("last_dir", "")
                    if stored_dir and os.path.isdir(stored_dir):
                        self.last_dir = stored_dir
                    
                    stored_cmd = data.get("python_cmd", "")
                    if stored_cmd:
                        if self._is_valid_python(stored_cmd):
                            self.python_cmd = stored_cmd
                            self._manual_python_cmd = True
                        else:
                            # Błędny wpis (np. zła ścieżka) – porzuć go i wróć do autodetekcji
                            logging.warning(f"Pominięto nieprawidłowy interpreter z konfiguracji: {stored_cmd!r}")
                            invalid_stored_cmd = True
            except Exception as e:
                logging.warning(f"Nie udało się wczytać konfiguracji: {e}")

        if not self.python_cmd:
            self.python_cmd = self._detect_python()

        if invalid_stored_cmd:
            # Usuń błędny wpis z config.json, aby nie był sprawdzany przy każdym starcie
            self.save_config()

    def save_config(self):
        try:
            config_data = {
                "recent_files": self.recent_files,
                "last_dir": self.last_dir,
                "theme": self.current_theme,
            }
            if self._manual_python_cmd and self.python_cmd:
                config_data["python_cmd"] = self.python_cmd

            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logging.warning(f"Nie udało się zapisać konfiguracji: {e}")

    def add_to_recent(self, file_path):
        file_path = os.path.abspath(file_path)
        if file_path in self.recent_files:
            self.recent_files.remove(file_path)
        self.recent_files.insert(0, file_path)
        self.recent_files = self.recent_files[:10]
        self.last_dir = os.path.dirname(file_path)
        self.save_config()
        self.update_recent_menu()

    def init_ui(self):
        self.setWindowIcon(QIcon(resource_path("ikona.ico")))
        main_widget = QWidget()
        layout = QVBoxLayout(main_widget)
        layout.setContentsMargins(0, 0, 0, 0)

        self.editor = PythonEditor()
        layout.addWidget(self.editor)
        self.editor.modificationChanged.connect(self.update_title)
        self.setCentralWidget(main_widget)

        self.statusBar().showMessage("Gotowy")
        self.create_menu()
        self.change_theme(self.current_theme)
        self.update_title()

    def apply_ui_theme(self):
        themes_colors = {
            "Ciemny": {"bg": "#282a36", "fg": "#f8f8f2", "status_bg": "#191a21"},
            "Kontrastowy": {"bg": "#000000", "fg": "#00ff00", "status_bg": "#111111"},
            "Monokai": {"bg": "#272822", "fg": "#f8f8f2", "status_bg": "#1e1f1c"},
            "Solarized Light": {"bg": "#fdf6e3", "fg": "#657b83", "status_bg": "#eee8d5"},
            "Oceanic": {"bg": "#1b2b34", "fg": "#d8dee9", "status_bg": "#10171d"},
            "Jasny": {"bg": "#ffffff", "fg": "#000000", "status_bg": "#f0f0f0"}
        }

        cfg = themes_colors.get(self.current_theme, themes_colors["Jasny"])
        bg = cfg["bg"]
        fg = cfg["fg"]
        status_bg = cfg["status_bg"]

        is_dark = self.current_theme in ["Ciemny", "Kontrastowy", "Monokai", "Oceanic"]
        border = "#444444" if is_dark else "#dcdcdc"

        if self.current_theme == "Kontrastowy":
            sel_bg, sel_fg = "#00ff00", "#000000"
        elif is_dark:
            sel_bg, sel_fg = "#4f5b66" if self.current_theme == "Oceanic" else "#44475a", "#ffffff"
        else:
            sel_bg, sel_fg = "#0078d7", "#ffffff"

        self.setStyleSheet(f"""
            QMainWindow {{ background-color: {bg}; }}
            QMenuBar {{ background-color: {bg}; border-bottom: 1px solid {border}; padding: 2px; color: {fg}; }}
            QMenuBar::item {{ padding: 5px 12px; background: transparent; border-radius: 4px; color: {fg}; }}
            QMenuBar::item:selected {{ background-color: {sel_bg}; color: {sel_fg}; }}
            QMenu {{ background-color: {bg}; border: 1px solid {border}; padding: 5px; color: {fg}; }}
            QMenu::item {{ padding: 6px 25px; border-radius: 4px; color: {fg}; }}
            QMenu::item:selected {{ background-color: {sel_bg}; color: {sel_fg}; }}
            QStatusBar {{ background-color: {status_bg}; color: {fg}; }}
            QMessageBox, QInputDialog {{ background-color: {bg}; color: {fg}; }}
            QMessageBox QLabel, QInputDialog QLabel {{ color: {fg}; }}
            QPushButton {{ background-color: {status_bg}; color: {fg}; border: 1px solid {border}; padding: 5px 15px; border-radius: 4px; }}
            QPushButton:hover {{ background-color: {sel_bg}; color: {sel_fg}; }}
        """)

    def update_title(self):
        title = f"mkPyEdek v{self.VERSION} - "
        title += os.path.basename(self.current_file) if self.current_file else "Nowy plik"
        if self.editor.isModified():
            title += " *"
        self.setWindowTitle(title)

    def create_menu(self):
        menubar = self.menuBar()
        menubar.clear()

        file_menu = menubar.addMenu("Plik")
        for text, slot, shortcut, icon in [
            ("Nowy",     self.new_file,  "Ctrl+N", QStyle.StandardPixmap.SP_FileIcon),
            ("Otwórz...", self.open_file, "Ctrl+O", QStyle.StandardPixmap.SP_DirOpenIcon),
        ]:
            action = QAction(self.style().standardIcon(icon), text, self)
            action.setShortcut(shortcut); action.triggered.connect(slot); file_menu.addAction(action)

        self.recent_menu = file_menu.addMenu("Otwórz ostatnie")
        self.update_recent_menu()
        file_menu.addSeparator()

        for text, slot, shortcut in [
            ("Zapisz",        self.save_file,    "Ctrl+S"),
            ("Zapisz jako...", self.save_as_file, "Ctrl+Shift+S"),
        ]:
            action = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogSaveButton), text, self)
            action.setShortcut(shortcut); action.triggered.connect(slot); file_menu.addAction(action)

        file_menu.addSeparator()
        exit_a = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_DialogCloseButton), "Zakończ", self)
        exit_a.triggered.connect(self.close); file_menu.addAction(exit_a)

        edit_menu = menubar.addMenu("Edycja")
        for text, slot, shortcut in [
            ("Cofnij", self.editor.undo, "Ctrl+Z"),
            ("Ponów",  self.editor.redo, "Ctrl+Y"),
        ]:
            action = QAction(text, self); action.setShortcut(shortcut); action.triggered.connect(slot); edit_menu.addAction(action)
        edit_menu.addSeparator()
        for text, slot, shortcut in [
            ("Wytnij",           self.editor.cut,  "Ctrl+X"),
            ("Kopiuj",           self.editor.copy, "Ctrl+C"),
            ("Wklej",            self.editor.paste,"Ctrl+V"),
            ("Zaznacz wszystko", self.select_all,  "Ctrl+A"),
        ]:
            action = QAction(text, self); action.setShortcut(shortcut); action.triggered.connect(slot); edit_menu.addAction(action)
        edit_menu.addSeparator()
        for text, slot, shortcut in [
            ("Znajdź...",        self.find_text,      "Ctrl+F"),
            ("Znajdź następny",  self.find_next_text, "F3"),
            ("Zamień...",        self.replace_text,   "Ctrl+H"),
        ]:
            action = QAction(text, self); action.setShortcut(shortcut); action.triggered.connect(slot); edit_menu.addAction(action)

        run_menu = menubar.addMenu("Uruchom")
        run_a = QAction(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay), "Uruchom kod", self)
        run_a.setShortcut("F5"); run_a.triggered.connect(self.run_code); run_menu.addAction(run_a)

        theme_menu = menubar.addMenu("Motyw")
        theme_group = QActionGroup(self)
        for t_name in ["Jasny", "Ciemny", "Kontrastowy", "Monokai", "Solarized Light", "Oceanic"]:
            action = QAction(t_name, self, checkable=True)
            if t_name == self.current_theme: action.setChecked(True)
            action.triggered.connect(lambda checked, t=t_name: self.change_theme(t))
            theme_group.addAction(action); theme_menu.addAction(action)

        share_menu = menubar.addMenu("Udostępnij")
        copy_action = QAction("Skopiuj cały kod programu", self)
        copy_action.triggered.connect(self.copy_to_clipboard); share_menu.addAction(copy_action)
        gmail_action = QAction("Wyślij kod przez Gmail (WWW)", self)
        gmail_action.triggered.connect(self.send_via_gmail); share_menu.addAction(gmail_action)
        share_menu.addSeparator()
        classroom_action = QAction("Udostępnij w Classroom", self)
        classroom_action.triggered.connect(self.share_to_classroom); share_menu.addAction(classroom_action)

        visit_menu = menubar.addMenu("Odwiedź")
        for text, url in [
            ("Pobierz najnowszą wersję", "https://github.com/StaryDooh/mkPyEdek/releases"),
            ("Zgłoś błąd",               "https://github.com/StaryDooh/mkPyEdek/issues"),
            ("Zrelaksuj się",            "https://www.youtube.com/@StaryDooh"),
        ]:
            action = QAction(text, self); action.triggered.connect(lambda checked, u=url: webbrowser.open(u)); visit_menu.addAction(action)

    def select_all(self):
        self.editor.selectAll(True)

    def find_text(self):
        text, ok = QInputDialog.getText(self, "Znajdź", "Wpisz szukany tekst:")
        if ok and text:
            self.last_search = text
            found = self.editor.findFirst(text, False, False, False, True)
            if not found:
                QMessageBox.information(self, "Znajdź", "Nie znaleziono podanego tekstu.")

    def find_next_text(self):
        if self.last_search:
            self.editor.findNext()
        else:
            self.find_text()

    def replace_text(self):
        search_text, ok1 = QInputDialog.getText(self, "Zamień", "Wpisz szukany tekst:")
        if not (ok1 and search_text):
            return
        replace_with, ok2 = QInputDialog.getText(self, "Zamień", f"Zastąp '{search_text}' na:")
        if not ok2:
            return

        self.last_search = search_text
        reply = QMessageBox.question(
            self, "Zamień", "Czy chcesz zamienić WSZYSTKIE wystąpienia?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No | QMessageBox.StandardButton.Cancel
        )
        if reply == QMessageBox.StandardButton.Cancel:
            return

        if reply == QMessageBox.StandardButton.Yes:
            full_text = self.editor.text()
            count = full_text.count(search_text)
            if count:
                new_text = full_text.replace(search_text, replace_with)
                self.editor.beginUndoAction()
                self.editor.selectAll()
                self.editor.replaceSelectedText(new_text)
                self.editor.endUndoAction()
                self.statusBar().showMessage(f"Zamieniono {count} wystąpień.", 4000)
            else:
                QMessageBox.information(self, "Zamień", "Nie znaleziono podanego tekstu.")
        else:
            found = self.editor.findFirst(search_text, False, False, False, True)
            if found:
                self.editor.replace(replace_with)
                self.statusBar().showMessage("Zamieniono 1 wystąpienie.", 4000)
            else:
                QMessageBox.information(self, "Zamień", "Nie znaleziono podanego tekstu.")

    def copy_to_clipboard(self):
        QApplication.clipboard().setText(self.editor.text())
        self.statusBar().showMessage("Kod skopiowany do schowka!", 3000)

    def send_via_gmail(self):
        code = self.editor.text()
        subject = urllib.parse.quote("Kod programu Python - mkPyEdek")
        
        if len(code) > 1500:
            reply = QMessageBox.question(
                self, "Kod zbyt długi",
                "Kod jest zbyt długi, aby wstawić go automatycznie do treści maila.\n\n"
                "Kod zostanie skopiowany do schowka – wklej go ręcznie w oknie Gmail.\n\n"
                "Czy chcesz otworzyć Gmail?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply != QMessageBox.StandardButton.Yes:
                return
            QApplication.clipboard().setText(code)
            body = urllib.parse.quote("(wklej kod ze schowka)")
        else:
            body = urllib.parse.quote(code)
            
        gmail_url = f"https://mail.google.com/mail/?view=cm&su={subject}&body={body}"
        webbrowser.open(
            f"https://accounts.google.com/AccountChooser?continue={urllib.parse.quote(gmail_url, safe='')}"
        )

    def share_to_classroom(self):
        # save_file() sam przechodzi do "Zapisz jako", gdy plik jest nowy.
        # Bez udanego zapisu nie otwieramy Classroom (plik na dysku byłby nieaktualny).
        if not self.save_file():
            return
        webbrowser.open("https://classroom.google.com")
        try:
            file_path = os.path.normpath(self.current_file)
            if platform.system() == "Windows":
                # Polecenie jako tekst, nie lista: z listą Popen ujmuje cały argument w cudzysłów
                # ("/select,C:\...\Jan Kowalski\..."), czego Explorer nie rozumie przy spacjach w ścieżce.
                # Znak " nie może wystąpić w ścieżce Windows, więc takie cytowanie jest bezpieczne.
                subprocess.Popen(f'explorer /select,"{file_path}"')
            elif platform.system() == "Darwin":
                subprocess.Popen(["open", "-R", file_path])
            else:
                subprocess.Popen(["xdg-open", os.path.dirname(file_path)])
        except Exception as e:
            logging.warning(f"Błąd integracji z przeglądarką plików: {e}")

    def change_theme(self, theme_name):
        self.current_theme = theme_name
        self.editor.apply_theme(theme_name)
        self.apply_ui_theme()
        self.save_config()

    def open_recent_file(self, file_path):
        if self.maybe_save():
            self.open_specific_file(file_path)

    def update_recent_menu(self):
        self.recent_menu.clear()
        if not self.recent_files:
            self.recent_menu.addAction("Brak ostatnich plików").setEnabled(False)
            return
        for path in self.recent_files:
            action = QAction(os.path.basename(path), self)
            action.triggered.connect(lambda checked, p=path: self.open_recent_file(p))
            self.recent_menu.addAction(action)

    def check_python_installed(self):
        if self.python_cmd:
            return

        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Warning)
        msg.setWindowTitle("Brak interpretera Python")
        msg.setText("Nie wykryto instalacji języka Python.")
        btn_locate   = msg.addButton("Wskaż plik",     QMessageBox.ButtonRole.ActionRole)
        btn_download = msg.addButton("Pobierz Pythona", QMessageBox.ButtonRole.ActionRole)
        msg.addButton("Ignoruj", QMessageBox.ButtonRole.RejectRole)
        msg.exec()

        if msg.clickedButton() == btn_locate:
            # Qt rozdziela wzorce w filtrze spacją (nie średnikiem)
            if platform.system() == "Windows":
                py_filter = "Interpreter Python (python*.exe py.exe)"
            else:
                py_filter = "Interpreter Python (python python3 python3.*)"
            path, _ = QFileDialog.getOpenFileName(
                self, "Wskaż interpreter Pythona", "",
                f"{py_filter};;Wszystkie pliki (*)"
            )
            if not path:
                return
            if self._is_valid_python(path):
                self.python_cmd = path
                self._manual_python_cmd = True
                self.save_config()
            else:
                QMessageBox.warning(self, "Błąd",
                    "Wskazany plik nie jest działającym interpreterem Pythona.\n\n"
                    "Wskaż plik python.exe (np. C:\\Users\\...\\AppData\\Local\\Programs\\Python\\Python3xx\\python.exe).")
        elif msg.clickedButton() == btn_download:
            webbrowser.open("https://www.python.org/downloads/")

    def maybe_save(self):
        if not self.editor.isModified():
            return True
        msg_box = QMessageBox(self)
        msg_box.setIcon(QMessageBox.Icon.Warning)
        msg_box.setWindowTitle("Niezapisane zmiany")
        msg_box.setText("Czy chcesz zapisać zmiany?")
        btn_save    = msg_box.addButton("Zapisz",      QMessageBox.ButtonRole.AcceptRole)
        btn_discard = msg_box.addButton("Nie zapisuj", QMessageBox.ButtonRole.DestructiveRole)
        msg_box.addButton("Anuluj",                    QMessageBox.ButtonRole.RejectRole)
        msg_box.exec()
        if msg_box.clickedButton() == btn_save:
            return self.save_file()
        return msg_box.clickedButton() == btn_discard

    def closeEvent(self, event):
        if not self.maybe_save():
            event.ignore()
            return

        # Bezpieczne zatrzymanie autouzupełniania i wątku Jedi przed wyjściem
        self.editor.shutdown()
        event.accept()

    def new_file(self):
        if self.maybe_save():
            self.editor.clear()
            # Wyczyść historię cofania, aby Ctrl+Z nie przywracał poprzedniego pliku
            self.editor.SendScintilla(QsciScintilla.SCI_EMPTYUNDOBUFFER)
            self.current_file = None
            self.editor.setModified(False)
            self._original_encoding = 'utf-8'
            self.update_title()

    def open_file(self):
        if self.maybe_save():
            file_name, _ = QFileDialog.getOpenFileName(
                self, "Otwórz plik", self.last_dir,
                "Pliki Python (*.py);;Wszystkie pliki (*)"
            )
            if file_name:
                self.open_specific_file(file_name)

    def open_specific_file(self, file_path):
        file_path = os.path.abspath(file_path)
        if os.path.exists(file_path):
            try:
                content = None
                detected_enc = 'utf-8'
                for enc in ('utf-8', 'cp1250', 'latin-2'):
                    try:
                        with open(file_path, 'r', encoding=enc) as f:
                            content = f.read()
                        detected_enc = enc
                        break
                    except (UnicodeDecodeError, LookupError):
                        continue

                if content is None:
                    with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                        content = f.read()
                    detected_enc = 'utf-8'
                    QMessageBox.warning(self, "Kodowanie",
                        "Plik zawiera znaki spoza UTF-8. Część znaków może być wyświetlona niepoprawnie.")

                self._original_encoding = detected_enc

                self.editor.setText(content)
                # Wyczyść historię cofania, aby Ctrl+Z nie przywracał poprzedniego pliku
                self.editor.SendScintilla(QsciScintilla.SCI_EMPTYUNDOBUFFER)
                self.current_file = file_path
                self.editor.setModified(False)
                self.add_to_recent(file_path)
                self.update_title()
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie można otworzyć pliku:\n{e}")
        else:
            if file_path in self.recent_files:
                self.recent_files.remove(file_path)
                self.save_config()
                self.update_recent_menu()

    def save_file(self):
        if self.current_file:
            original_enc = getattr(self, '_original_encoding', 'utf-8')
            if original_enc != 'utf-8':
                reply = QMessageBox.question(
                    self, "Zmiana kodowania",
                    f"Plik był oryginalnie zapisany w kodowaniu {original_enc.upper()}.\n"
                    f"Zapisanie go w UTF-8 może być niezgodne z innymi programami.\n\n"
                    f"Czy chcesz zapisać w UTF-8?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.Cancel
                )
                if reply != QMessageBox.StandardButton.Yes:
                    return False
                self._original_encoding = 'utf-8'

            try:
                with open(self.current_file, 'w', encoding='utf-8', newline='') as f:
                    f.write(self.editor.text())
                self.editor.setModified(False)
                self.add_to_recent(self.current_file)
                self.update_title()
                return True
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie można zapisać pliku:\n{e}")
                return False
        return self.save_as_file()

    def save_as_file(self):
        dialog = QFileDialog(self, "Zapisz jako", self.last_dir, "Pliki Python (*.py)")
        dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        dialog.setDefaultSuffix("py")

        if dialog.exec() == QFileDialog.DialogCode.Accepted:
            file_name = dialog.selectedFiles()[0]
            old_file = self.current_file
            self.current_file = file_name

            if self.save_file():
                return True
            else:
                self.current_file = old_file
                return False

        return False

    def run_code(self):
        # Brak interpretera – zaproponuj wskazanie/pobranie zamiast mylącego błędu Popen
        if not self.python_cmd:
            self.check_python_installed()
            if not self.python_cmd:
                return

        if not self.current_file:
            if not self.save_as_file():
                return

        source = self.editor.text()
        
        # Szybka synchroniczna walidacja za pomocą built-in compile()
        try:
            compile(source, self.current_file or "<string>", "exec", dont_inherit=True)
        except SyntaxError as e:
            line = e.lineno - 1 if e.lineno else 0
            self.editor.setCursorPosition(line, 0)
            self.editor.setSelection(line, 0, line, self.editor.lineLength(line))
            QMessageBox.critical(self, "Błąd składni", f"Błąd w linii {e.lineno}:\n{e.msg}")
            return
        except (ValueError, RecursionError, MemoryError) as e:
            QMessageBox.critical(self, "Błąd analizy kodu", f"Nie udało się zweryfikować składni:\n{e}")
            return

        if not self.save_file():
            return
            
        self._launch_process()

    def _launch_process(self):
        try:
            working_dir = os.path.abspath(os.path.dirname(self.current_file))

            if platform.system() == "Windows":
                env = os.environ.copy()
                env["PYTHON_COLORS"] = "1"
                
                runner = (
                    "import sys, os, runpy, traceback\n"
                    "path = sys.argv[1]; sys.argv = sys.argv[1:]\n"
                    "sys.path.insert(0, os.path.dirname(path))\n"
                    "try:\n    runpy.run_path(path, run_name='__main__')\n"
                    "except SystemExit:\n    pass\n"
                    "except BaseException:\n    traceback.print_exc()\n"
                    "finally:\n    input('\\nNaciśnij Enter, aby zamknąć...')\n"
                )
                flags = getattr(subprocess, 'CREATE_NEW_CONSOLE', 0)
                subprocess.Popen(
                    [self.python_cmd, "-c", runner, self.current_file],
                    cwd=working_dir,
                    creationflags=flags,
                    env=env
                )

            elif platform.system() == "Darwin":
                import tempfile, stat
                script_content = (
                    "#!/bin/bash\n"
                    'rm -- "$0"\n'
                    f"cd {shlex.quote(working_dir)} || exit 1\n"
                    "export PYTHON_COLORS=1\n"
                    f"{shlex.quote(self.python_cmd)} {shlex.quote(self.current_file)}\n"
                    "echo\nread -n 1 -s -p 'Naciśnij klawisz...'\n"
                )
                with tempfile.NamedTemporaryFile(mode='w', suffix='.sh', delete=False, encoding='utf-8') as tmp:
                    tmp.write(script_content)
                    tmp_path = tmp.name
                os.chmod(tmp_path, stat.S_IRWXU)
                
                cmd = shlex.quote(tmp_path).replace("\\", "\\\\").replace('"', '\\"')
                osa = f'tell application "Terminal"\nactivate\ndo script "{cmd}"\nend tell'
                
                subprocess.Popen(["osascript", "-e", osa])

            else:
                safe_cmd = (
                    f"cd {shlex.quote(working_dir)} || exit 1; "
                    "export PYTHON_COLORS=1; "
                    f"{shlex.quote(self.python_cmd)} {shlex.quote(self.current_file)}; "
                    f'echo; read -n 1 -s -p "Naciśnij klawisz..."'
                )
                subprocess.Popen(
                    ["x-terminal-emulator", "-e", "bash", "-c", safe_cmd]
                )

        except Exception as e:
            QMessageBox.critical(self, "Błąd", f"Nie uruchomiono interpretera: {e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    file_path = sys.argv[1] if len(sys.argv) > 1 else None
    win = MkPyEdekGUI(file_to_open=file_path)
    # Zabezpieczenie także dla wyjścia z pominięciem closeEvent (np. „Zakończ program” w oknie błędu krytycznego)
    app.aboutToQuit.connect(win.editor.shutdown)
    sys.exit(app.exec())