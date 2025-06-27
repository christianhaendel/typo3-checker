
# 🧰 TYPO3 Checker

A Python script to detect TYPO3 websites using various technical indicators such as HTTP headers, meta tags, HTML content, resource paths, and robots.txt.

---

## ✅ Requirements

- Python 3.7 or higher
- Internet access to analyze target URLs

---

## 💻 Installation

### On Windows/Linux

```bash
pip install requests beautifulsoup4 colorama
```

### On macOS

Avoid using Homebrew-Python. Instead, use the system-provided Python:

```bash
python3 -m pip install --user requests beautifulsoup4 colorama
```

Run the script with:

```bash
python3 typo3_checker.py
```

---

## 📄 Input Format

Provide a plain `.txt` file with one URL per line:

```
https://www.example.edu
https://www.university-xyz.org
```

---

## ▶️ Usage

```bash
python typo3_checker.py
```

**macOS:**

```bash
python3 typo3_checker.py
```

You will be prompted to input:
- the path to the source `.txt` file
- a name for the output `.csv` file (the `.csv` suffix is added automatically)

---

## 📊 Output

The script produces a CSV file with the following structure:

| URL                  | TYPO3 detected | Comment                            |
|----------------------|----------------|-------------------------------------|
| https://example.edu  | Yes            | Detected in HTTP header             |
| https://site.org     | No             | No TYPO3 indicator found            |
| https://offline.edu  | Error          | Error fetching URL: <description>   |

---

## 🎨 Console Feedback

For each URL, the result is printed with color-coded feedback:

- <span style="color:green;">✔️ Yes</span>: TYPO3 detected
- <span style="color:orange;">⚠️ No</span>: No indicator found
- <span style="color:red;">❌ Error</span>: Could not analyze the site

---

## 🔍 Detection Priority

The checks run in this order for optimal performance:

1. `HTTP header`
2. `<meta name="generator">`
3. `HTML content`
4. `Resource paths` (e.g. `fileadmin`, `typo3`)
5. `robots.txt`

---

## 📈 Final Summary

At the end of execution, a summary is printed with counts of:

- ✅ TYPO3 websites detected
- ⚠️ Non-TYPO3 websites
- ❌ Errors encountered

---

## 👤 Author

**Christian Händel**  
📧 [christian@christianhaendel.de](mailto:christian@christianhaendel.de)
