from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

from PySide6.QtCore import QObject, Signal
from PySide6.QtGui import QAction
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSystemTrayIcon,
    QVBoxLayout,
    QWidget,
    QMenu,
    QStyle,
)
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / "inbox"
OUTPUT = ROOT / "output"
STORAGE = ROOT / "storage"
ACTIVITY = STORAGE / "activity.jsonl"
MEMORY = STORAGE / "memory.jsonl"


class Bridge(QObject):
    file_received = Signal(str)


class InboxHandler(FileSystemEventHandler):
    def __init__(self, bridge: Bridge) -> None:
        self.bridge = bridge

    def on_created(self, event) -> None:
        if not event.is_directory:
            self.bridge.file_received.emit(event.src_path)


class SilentLearnerWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Silent Learner")
        self.resize(820, 560)
        self.observer: Observer | None = None
        self.running = False
        self.paused = False

        self.status = QLabel("Detenido")
        self.input_view = QPlainTextEdit()
        self.input_view.setReadOnly(True)
        self.output_view = QPlainTextEdit()
        self.output_view.setReadOnly(True)

        start = QPushButton("Iniciar")
        pause = QPushButton("Pausar")
        stop = QPushButton("Detener")
        open_file = QPushButton("Procesar archivo")
        open_folder = QPushButton("Abrir carpeta de entrada")

        start.clicked.connect(self.start_observation)
        pause.clicked.connect(self.toggle_pause)
        stop.clicked.connect(self.stop_observation)
        open_file.clicked.connect(self.choose_file)
        open_folder.clicked.connect(lambda: self.open_path(INBOX))

        buttons = QHBoxLayout()
        for widget in (start, pause, stop, open_file, open_folder):
            buttons.addWidget(widget)

        layout = QVBoxLayout()
        layout.addWidget(self.status)
        layout.addLayout(buttons)
        layout.addWidget(QLabel("Evento percibido"))
        layout.addWidget(self.input_view)
        layout.addWidget(QLabel("Aprendizaje producido"))
        layout.addWidget(self.output_view)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.bridge = Bridge()
        self.bridge.file_received.connect(self.process_file)
        self.tray = self.create_tray()

        for path in (INBOX, OUTPUT, STORAGE):
            path.mkdir(parents=True, exist_ok=True)

    def create_tray(self) -> QSystemTrayIcon:
        tray = QSystemTrayIcon(self.style().standardIcon(QStyle.SP_ComputerIcon), self)
        menu = QMenu()
        show_action = QAction("Abrir", self)
        start_action = QAction("Iniciar", self)
        pause_action = QAction("Pausar / continuar", self)
        stop_action = QAction("Detener", self)
        quit_action = QAction("Salir", self)
        show_action.triggered.connect(self.show_normal)
        start_action.triggered.connect(self.start_observation)
        pause_action.triggered.connect(self.toggle_pause)
        stop_action.triggered.connect(self.stop_observation)
        quit_action.triggered.connect(self.quit_application)
        for action in (show_action, start_action, pause_action, stop_action, quit_action):
            menu.addAction(action)
        tray.setContextMenu(menu)
        tray.activated.connect(lambda reason: self.show_normal() if reason == QSystemTrayIcon.DoubleClick else None)
        tray.show()
        return tray

    def show_normal(self) -> None:
        self.show()
        self.raise_()
        self.activateWindow()

    def start_observation(self) -> None:
        if self.running:
            self.paused = False
            self.status.setText(f"Observando: {INBOX}")
            return
        self.observer = Observer()
        self.observer.schedule(InboxHandler(self.bridge), str(INBOX), recursive=False)
        self.observer.start()
        self.running = True
        self.paused = False
        self.status.setText(f"Observando: {INBOX}")
        self.log("observer_started", {"folder": str(INBOX)})

    def toggle_pause(self) -> None:
        if not self.running:
            return
        self.paused = not self.paused
        self.status.setText("Pausado" if self.paused else f"Observando: {INBOX}")
        self.log("observer_paused" if self.paused else "observer_resumed", {})

    def stop_observation(self) -> None:
        if self.observer:
            self.observer.stop()
            self.observer.join(timeout=2)
            self.observer = None
        self.running = False
        self.paused = False
        self.status.setText("Detenido")
        self.log("observer_stopped", {})

    def choose_file(self) -> None:
        filename, _ = QFileDialog.getOpenFileName(self, "Procesar evento", str(ROOT), "JSON o texto (*.json *.txt);;Todos (*.*)")
        if filename:
            self.process_file(filename, manual=True)

    def process_file(self, filename: str, manual: bool = False) -> None:
        if self.paused or (not self.running and not manual):
            return
        path = Path(filename)
        try:
            event = self.normalize_event(path)
            self.input_view.setPlainText(json.dumps(event, indent=2, ensure_ascii=False))
            temp_input = STORAGE / "current_turn.json"
            temp_input.write_text(json.dumps(event, ensure_ascii=False), encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(ROOT / "core" / "run_turn.py"), "--input", str(temp_input)],
                cwd=ROOT,
                capture_output=True,
                text=True,
                timeout=60,
                check=True,
            )
            candidate_path = OUTPUT / "learner_candidate.json"
            candidate = json.loads(candidate_path.read_text(encoding="utf-8"))
            self.output_view.setPlainText(json.dumps(candidate, indent=2, ensure_ascii=False))
            self.append_jsonl(MEMORY, {"timestamp": self.now(), "source": str(path), "candidate": candidate})
            self.log("candidate_created", {"source": str(path), "stdout": result.stdout.strip()})
            self.tray.showMessage("Silent Learner", f"Procesado: {path.name}")
        except Exception as exc:
            self.log("processing_error", {"source": str(path), "error": repr(exc)})
            QMessageBox.critical(self, "Error", str(exc))

    def normalize_event(self, path: Path) -> dict:
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".json":
            data = json.loads(text)
            if isinstance(data, dict) and ("user" in data or "assistant" in data):
                return {"user": str(data.get("user", "")), "assistant": str(data.get("assistant", ""))}
        return {"user": text, "assistant": ""}

    def log(self, event_type: str, payload: dict) -> None:
        self.append_jsonl(ACTIVITY, {"timestamp": self.now(), "type": event_type, "payload": payload})

    @staticmethod
    def append_jsonl(path: Path, record: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    @staticmethod
    def now() -> str:
        return datetime.now(timezone.utc).isoformat()

    @staticmethod
    def open_path(path: Path) -> None:
        path.mkdir(parents=True, exist_ok=True)
        if sys.platform == "win32":
            import os
            os.startfile(path)  # type: ignore[attr-defined]
        else:
            subprocess.Popen(["xdg-open", str(path)])

    def closeEvent(self, event) -> None:
        event.ignore()
        self.hide()
        self.tray.showMessage("Silent Learner", "La aplicación continúa activa en la bandeja.")

    def quit_application(self) -> None:
        self.stop_observation()
        QApplication.quit()


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    window = SilentLearnerWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
