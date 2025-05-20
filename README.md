# ✂️ Cutlist Optimizer CLI

This is a command-line application written in Python that helps woodworkers, builders, and makers calculate the most efficient way to cut materials (like lumber) from available stock boards.

It takes a list of cuts and matches them to available board lengths, minimizing waste and helping you plan real-world projects.

---

## 🚀 Features

- Accepts cut lengths in **decimals or fractions** (e.g., `24.5` or `12 1/2`)
- Accepts quantities like `12:4` (four cuts of 12")
- Supports **multiple board sizes** (e.g., `24, 36, 96`)
- Handles **fixed board inventory** (e.g., one of each board)
- Filters and displays **only used boards** in the output
- Shows total boards used, cuts made, and waste left
- Polished, user-friendly output using Rich tables

---

## 📦 Example Use

```bash
$ python main.py
Do you know the board length you want to use? [Y/n]: y
Enter stock length (in inches).
Separate multiple boards with a comma: 36,24,12

Let's build your cut list.
Format each entry as length:quantity — e.g., 24.5:2
Enter a cut(s) in the format [length]:[quantity], or press Enter to finish: 12:4
Enter a cut(s) in the format [length]:[quantity], or press Enter to finish: 24:1
Enter a cut(s) in the format [length]:[quantity], or press Enter to finish:

                    Final Cutlist
┏━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━┓
┃ Board #         ┃ Cuts          ┃ Unused Board (in.) ┃
┡━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━┩
│ Board 1 (36.0") │ [24.0, 12.0]  │ 0.0"               │
│ Board 2 (24.0") │ [12.0, 12.0]  │ 0.0"               │
│ Board 3 (12.0") │ [12.0]        │ 0.0"               │
├─────────────────┼───────────────┼────────────────────┤
│ Total Boards: 3 │ Total Cuts: 5 │ Total Unused: 0.0  │
└─────────────────┴───────────────┴────────────────────┘
```

## 🛠️ How to Run

1. Clone or download this repo
2. Make sure you have Python 3.10+
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the app:

```bash
$ python main.py
```

## 📐 Input Format

### 🪵 Stock Boards

When prompted:

```bash
Do you know the board length you want to use? [Y/n]:
```

Type y to manually enter the stock board sizes

Enter board lengths separated by commas, e.g.: 96, 72, 48

This tells the program you have one of each board length listed

You can enter whole numbers, decimals, or fractions (e.g., 96, 72.25, 24 1/2)

If you type n, the program will fall back to trying common standard sizes.

### ✂️ Cuts

When prompted:

```bash
Enter a cut(s) in the format [length]:[quantity], or press Enter to finish:
```

Each cut should be in the format: [length]:[quantity]

Example entries:

- 24:3 → three cuts of 24"
- 18.5:2 → two cuts of 18.5"
- 12 1/2:4 → four cuts of 12.5"

You can keep entering new cut sizes and quantities one at a time.

Just press Enter on a blank line when you're done.

## 🧑‍💻 Built With

- Python 3.10+
- Typer — for CLI input
- Rich — for beautiful output
