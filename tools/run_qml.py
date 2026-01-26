#!/usr/bin/env python3
import sys
from pathlib import Path

from PySide6.QtCore import QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: run_qml.py path/to/file.qml")
        return 2

    qml_path = Path(sys.argv[1]).resolve()
    if not qml_path.exists():
        print(f"QML not found: {qml_path}")
        return 2

    app = QGuiApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    if not engine.rootObjects():
        print("Failed to load QML.")
        return 1

    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
