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

## ▶️ Running the Program

```bash
uv run ./src/main.py
```

This will launch the SpreadsheetXplorer interface.

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

* Huge thanks to our user testers for their invaluable feedback.
* Special thanks to **Michael Wahler** for his guidance throughout the project.
