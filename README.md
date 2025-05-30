# SpreadsheetXplorer

A desktop tool for exploring and understanding complex spreadsheets. SpreadsheetXplorer helps users visualize formulas,
dependencies, and named ranges in a more interactive and accessible way.

---

## 🛠️ Getting Started

### 📦 Dependencies

* [`uv`](https://docs.astral.sh/uv/getting-started/installation/) – ultra-fast Python environment manager
* Python 3.13 (ensure it's installed and accessible)

### 💻 Platform Requirements

- Requires a **running desktop installation of Microsoft Excel** (Excel must be open during use).
- Works with:
    - ✅ **Windows** (tested with Excel 365)
    - ✅ **macOS** (requires Excel for Mac)
- ❌ Not compatible with Excel Online or other spreadsheet applications (yet).

### 📥 Install `uv`

Follow the official guide:

👉 [uv Installation Guide](https://docs.astral.sh/uv/getting-started/installation/)

### 🐍 Install Python 3.13

Make sure Python 3.13 is installed in your system. You can verify with:

```bash
python3.13 --version
```

Or download it from the official site: [https://www.python.org/downloads/](https://www.python.org/downloads/)

### 🧪 Create a Virtual Environment

```bash
uv venv
```

Or specify a custom Python interpreter:

```bash
uv venv --python=/usr/local/bin/python3.13
```

### 📦 Installing Dependencies

Once the virtual environment is created:

```bash
uv sync
```

This will install all the required dependencies listed in `pyproject.toml`.

---

## ▶️ Running the App

```bash
uv run ./src/main.py
```

This will launch the SpreadsheetXplorer interface.

---
## 📊 Using SpreadsheetXplorer

We’ve created a short YouTube video to help you understand how to use SpreadsheetXplorer.

👉 [Watch on YouTube](https://www.youtube.com/watch?v=78Zu8OcDKXY)

💡 Note: This video focuses on tool features, not installation or setup.

---

## 🔍 Running all Tests

```bash
uv run pytest
```

This will launch pytest and run all tests in ./tests.

⚠️ Make sure you do not have any Excel workbook open, as this can interfere with the tests.


---

## 📦 Packaging the App

You can create a standalone version of SpreadsheetXplorer using the provided `build.sh` script.

### 🔧 Requirements

- macOS or Windows with Python 3.13
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installed and synced (`uv sync`)
- PyInstaller (already included via `pyproject.toml`)

### 🏗️ Building the App

To build the application:

```bash
./build.sh
```

💡 Note: If you get a permission denied error when running build.sh, make sure it’s executable by running:
```bash
chmod +x build.sh
```

This will:

- Create a `.app` bundle on macOS or a `.exe` file on Windows
- Output all build artifacts to the `out/` folder:
  - `out/dist/SpreadsheetXplorer.app` (macOS, app bundle, - **see ⚠️ macOS Limitation below**)
  - `out/dist/SpreadsheetXplorer` (macOS, raw Unix executable - works directly)
  - `out/dist/SpreadsheetXplorer.exe` (Windows)

### ⚠️ macOS Limitation

Currently, the packaged `SpreadsheetXplorer.app` bundle **does not work on macOS** due to Apple security restrictions.

To enable AppleScript-based automation (used by `xlwings` to control Excel) within a packaged `.app`, the app must be **code-signed with a Developer ID and an appropriate entitlement** (`com.apple.security.automation.apple-events`). Without this, macOS denies permission with `OSERROR: -1743`.

**Workaround:** You can sign the `.app` locally with a self-signed certificate for development/testing, but general distribution requires a paid Apple Developer account.

However, the raw Unix executable file (`out/dist/SpreadsheetXplorer`) **does work** and can be run directly from the terminal:
```bash
./out/dist/SpreadsheetXplorer/SpreadsheetXplorer
```


---
## 😋 Help

For help, contact the authors or open an issue.

---

## 👥 Authors

* Ricardo Duarte — [@rduarteb1992](https://github.com/rduarteb1992)
* Patrick Schwizer — [@patrickwinti](https://github.com/patrickwinti)

---

## ⚠️ Known Limitations

* 📂 **SharePoint-hosted files are not yet supported.**

    * 💡 Workaround: Download the file locally before importing it into SpreadsheetXplorer.

---

## 🙏 Acknowledgments

* Thanks to our user testers for their invaluable feedback.
* Special thanks to **Michael Wahler** for his inputs and guidance throughout the project.
