# Lesson 1: What Data Engineering Is, and Setting Up Your Workshop

## Where we are

This is the very start. You don't need to know anything technical yet. By the end of this lesson you'll be able to explain what a data engineer does in plain English, find your way around VS Code and the terminal, and run your first Python program. Everything else in the course builds on the habits you set up today.

## What you'll learn

- What data engineering is, and how it fits next to analysts, data scientists and business analysts
- The journey data takes from "something happened" to "a number on a dashboard"
- What files, folders and paths are
- What the terminal is and the five commands you'll use constantly
- What Python actually is, and the two ways to run it
- Your first Python script, explained line by line
- A tiny "pipeline" that shows the shape of everything to come

## Why this matters at work

As a business analyst you've probably written a requirement like *"The weekly sales dashboard should show revenue by shop"*, and then a few weeks later a dashboard appeared. Something happened in between. Somebody worked out where the sales data lived, copied it out of the till system, cleaned it, combined it with the list of shops, stored it somewhere safe and fast, and made sure it refreshed every week without anyone touching it. **That somebody was a data engineer.** From today, that's you.

---

## 1. What is data engineering?

### The metaphor: a city's water supply

Think about the water that comes out of your kitchen tap.

- It started as rain in hills, rivers and reservoirs, scattered all over the place. → These are **data sources**: the till system, the website, the stock system, spreadsheets someone emails every Friday.
- Pipes and pumping stations carry it towards the city. → This is **ingestion**: moving data out of the sources.
- A treatment works filters out mud and makes it safe to drink. → This is **transformation**: cleaning, fixing and reshaping data.
- It's held in water towers and tanks so there's always some ready. → This is **storage**: databases and data warehouses.
- It comes out of the tap whenever you turn it on. → This is **serving**: the dashboard, the report, the spreadsheet download.

**The data engineer is the water company.** They don't drink the water or decide what to cook with it. They make sure clean water reliably arrives at every tap, every day, and they get the phone call when it stops.

Where the metaphor stops being accurate: water is all the same, but data comes in thousands of different shapes, and the "treatment" is different for every source. That's what makes the job interesting.

### Who does what

Let's use a second metaphor, a restaurant, to see how the roles fit together.

| Role | Restaurant equivalent | What they actually do |
|------|----------------------|-----------------------|
| **Business analyst** (your old role) | Front of house, taking the order | Finds out what the business needs and writes it down clearly |
| **Data engineer** (your new role) | Suppliers, delivery drivers, the storeroom and the prep cooks | Gets raw data in, cleans it, organises it and keeps it flowing |
| **Data analyst** | The chef | Takes prepared data and turns it into answers, reports and dashboards |
| **Data scientist** | The chef developing new recipes | Uses data to build predictions and models |

If the storeroom is a mess, the chef can't cook, however talented they are. Analysts often say they spend most of their time cleaning data. A good data engineer gives them that time back.

Your BA background is a real advantage here. Many engineers can build a pipeline but struggle to understand *why* the business wants it, or to spot that a number "looks wrong". You already do that.

> **Try it now 1.1**
> Think of a report or dashboard from a project you worked on as a BA. Write down, in plain English:
> 1. Where did the data originally come from? (the "reservoir")
> 2. What had to be cleaned or fixed? (the "treatment")
> 3. Who used it at the end? (the "tap")
>
> Don't worry if you don't know every answer. Noticing the gaps is the point.

---

## 2. The journey of a piece of data

Let's follow one sale at Brightside Bikes, the made-up company we'll use for the whole course. Brightside is a UK chain of bike shops with an online store.

**Saturday, 11:42am.** A customer buys a £120.50 helmet and lights at the Leeds shop. The till records it.

1. **Source:** the sale sits in the till system's own database at the Leeds shop.
2. **Extract (ingestion):** overnight, a program copies every new sale from every shop's till.
3. **Transform:** the program fixes problems. The Leeds till writes dates as `13/09/2026` and the online store writes `2026-09-13`, so they're made the same. Test sales made by staff are removed. Each sale is matched to the shop's region.
4. **Load (storage):** the cleaned sales go into one central database, the **data warehouse**, where every shop's sales sit side by side.
5. **Serve:** on Monday morning the regional manager opens a dashboard and sees "North region sales, last week: £48,210".

Steps 2 to 4 have a famous name: **ETL**, which stands for **Extract, Transform, Load**. You'll hear it constantly. There's a close cousin, **ELT**, where you load the raw data first and transform it inside the warehouse afterwards. We'll cover the difference properly in lesson 39. For now, just remember ETL: *get it, fix it, put it somewhere useful*.

The set of programs that does all this automatically is called a **data pipeline**, which fits nicely with the water metaphor.

> **Try it now 1.2**
> For each job below, say whether it's **Extract**, **Transform** or **Load**:
> 1. Copying yesterday's orders from the online store
> 2. Changing "leeds", "LEEDS" and "Leeds " all into "Leeds"
> 3. Writing the finished table of sales into the warehouse
> 4. Working out the total of each order from its individual items
> 5. Downloading a spreadsheet a supplier emails every week

---

## 3. Your workshop: the four tools

Before a carpenter builds anything they need to know their workshop. Ours has four things in it.

| Tool | Workshop equivalent | What it is |
|------|---------------------|------------|
| **Files and folders** | Shelves and boxes | Where everything is stored on your computer |
| **The terminal** | Talking to the workshop manager | A way to give your computer typed instructions |
| **VS Code** | The workbench | The program where you write and run code |
| **Python** | The power tool | The programming language that does the work |

### 3.1 Files, folders and paths

You already use files and folders. The important new idea is the **path**: the full address of a file.

**Metaphor: a postal address.** "Flat 2, 14 High Street, Leeds" works from the biggest area down to the exact door. A path does the same, from the top of your drive down to the file:

- Windows: `C:\Users\Jamie\Documents\de-course\lesson01\hello.py`
- Mac: `/Users/jamie/Documents/de-course/lesson01/hello.py`

Reading the Mac one left to right: start at the very top of the computer (`/`), go into `Users`, then `jamie`, then `Documents`, then `de-course`, then `lesson01`, and there's the file `hello.py`. Windows uses backslashes `\` and starts with a drive letter like `C:`; Mac uses forward slashes `/`. Same idea.

Two more ideas you'll need:

- **File extension:** the bit after the dot (`.py`, `.csv`, `.xlsx`). It tells you and the computer what kind of file it is. `.py` means a Python file.
- **Current folder (working directory):** wherever you're "standing" right now. Like being in a particular room of a house: you can say "the kettle" instead of "the kettle in the kitchen at 14 High Street" because you're already in the kitchen.

### 3.2 The terminal

**What it is:** a window where you type instructions to your computer instead of clicking.

**Metaphor:** using normal Windows or Mac is like browsing in a shop: you walk around, look, and pick things up. The terminal is like the counter at Argos: you say exactly what you want, and it's fetched. It feels less friendly at first, but it's faster, precise, and, crucially, *it can be written down and repeated*. Pipelines run on servers with no mouse and no screen, so everything a data engineer builds is ultimately run by typed commands.

You don't need to open a separate terminal app. VS Code has one built in, which we'll use in a moment.

### 3.3 VS Code

**What it is:** a code editor. Think of it as Word, but for code. It colours your code so it's easier to read, spots mistakes, and has a terminal built in at the bottom. It doesn't run Python itself; it hands your code to Python.

### 3.4 Python

**What it is:** a programming language, meaning a set of words and rules for writing instructions a computer can follow.

**Metaphor:** a recipe and a cook. Your Python file is a recipe, written in a strict language the cook understands. **Python** (the program you installed) is the cook: it reads your recipe from top to bottom, one line at a time, and does exactly what each line says. The cook is very fast and never gets bored, but is also completely literal. If the recipe says "add salt" and you meant sugar, you're getting salt. If there's a typo, the cook stops and complains.

The proper name for the cook is the **Python interpreter**, because it *interprets* (reads and carries out) your code line by line.

Data engineers use Python because it's easy to read, and because there are free add-ons for almost everything: talking to databases, reading spreadsheets, calling websites, scheduling jobs.

---

## 4. Setting up your course folder

Let's make one folder that will hold everything you do in this course.

**Step 1.** Open VS Code.

**Step 2.** Create the folder and open it:
- Go to **File → Open Folder...** (on Mac: **File → Open...**).
- Go to your `Documents` folder.
- Create a new folder called `de-course` (on Windows click **New folder**, on Mac click **New Folder**), select it, and click **Select Folder** / **Open**.
- If VS Code asks *"Do you trust the authors of the files in this folder?"*, click **Yes**. It's your folder.

You'll see `DE-COURSE` in the left-hand panel. That panel is called the **Explorer**, and it shows what's in your folder.

**Step 3.** Open the terminal inside VS Code: **Terminal → New Terminal** from the top menu (shortcut: `` Ctrl + ` `` on Windows, `` Ctrl + ` `` on Mac too; the `` ` `` key is usually top-left, under Esc).

A panel opens at the bottom with something like:

```
PS C:\Users\Jamie\Documents\de-course>
```
or on Mac:
```
jamie@MacBook de-course %
```

This is the **prompt**: the terminal telling you it's ready and showing you which folder you're standing in. On Windows, `PS` means you're using **PowerShell**, the Windows terminal language. The `>` or `%` is where your typing goes.

---

## 5. Your first five terminal commands

Type each one after the prompt and press **Enter**. The good news: in VS Code's terminal these same commands work on both Windows (PowerShell) and Mac.

### `pwd`: where am I?

```bash
pwd
```

| Part | Meaning |
|------|---------|
| `pwd` | Short for **p**rint **w**orking **d**irectory. "Print" here means "show on screen", not send to a printer. **Directory** is just another word for folder. |

It shows the path of the folder you're standing in. It should end in `de-course`.

### `mkdir`: make a folder

```bash
mkdir lesson01
```

| Part | Meaning |
|------|---------|
| `mkdir` | **m**a**k**e **dir**ectory: create a new folder |
| (space) | Separates the command from what it should act on |
| `lesson01` | The name of the new folder. We avoid spaces in names because the terminal uses spaces to separate things |

You'll see `lesson01` appear in the Explorer on the left.

### `ls`: what's in here?

```bash
ls
```

| Part | Meaning |
|------|---------|
| `ls` | **l**i**s**t: show what's in the current folder |

You should see `lesson01` listed.

### `cd`: move into a folder

```bash
cd lesson01
```

| Part | Meaning |
|------|---------|
| `cd` | **c**hange **d**irectory: walk into a different folder |
| `lesson01` | Which folder to walk into |

Look at the prompt: it now ends in `lesson01`. You've moved rooms.

### `cd ..`: go back up one level

```bash
cd ..
```

| Part | Meaning |
|------|---------|
| `cd` | change directory |
| `..` | Two dots always mean "the folder above this one", like "go back out to the hallway" |

You're back in `de-course`. Now go back into `lesson01`, because that's where we'll work today:

```bash
cd lesson01
```

**Handy trick:** type `cd les` and press **Tab**. The terminal finishes the name for you. This saves time and typos.

> **Try it now 1.3**
> 1. Run `pwd` and check you're in `lesson01`.
> 2. Make a folder called `scratch` inside `lesson01`, move into it, run `pwd` to prove it, then move back up to `lesson01`.
> 3. Run `ls`. What do you see?

---

## 6. Checking Python is installed

In the terminal, type:

```bash
python --version
```

| Part | Meaning |
|------|---------|
| `python` | Run the Python program (the cook) |
| `--version` | An **option**, an extra instruction that changes what a command does. Options often start with `--`. This one says "don't run anything, just tell me your version number" |

You should see something like `Python 3.12.4`. Any version starting with **3.10 or higher** is fine.

**If it doesn't work:**
- **Mac:** try `python3 --version`. On Macs the command is usually `python3`. If that works, use `python3` everywhere this course says `python`.
- **Windows:** if you get *"python is not recognized"*, try `py --version`. If that works, use `py` everywhere this course says `python`.
- If none work, tell me in the thread what you see and we'll fix it before moving on.

---

## 7. Two ways to run Python

### 7.1 Interactive mode: Python as a calculator

Type:

```bash
python
```

The prompt changes to `>>>`. You're now talking **directly to Python**, not to the terminal. This is called the **REPL** (**R**ead, **E**valuate, **P**rint, **L**oop): it **reads** what you type, **evaluates** (works out) the answer, **prints** it, and **loops** back to wait for more.

**Metaphor:** this is like chatting with the cook directly ("what's 2 add 2?") instead of handing over a written recipe. Great for quick experiments, but nothing is saved.

Try these, pressing Enter after each:

```python
2 + 2
120.50 + 89.99
10 * 3
100 / 8
```

| Line | Meaning |
|------|---------|
| `2 + 2` | Add. Python shows `4` |
| `120.50 + 89.99` | Add numbers with decimals. Shows `210.49` |
| `10 * 3` | `*` is how computers write "times". Shows `30` |
| `100 / 8` | `/` means "divided by". Shows `12.5` |

To leave and get back to the normal terminal:

```python
exit()
```

| Part | Meaning |
|------|---------|
| `exit` | The name of an instruction that closes the Python session |
| `()` | Brackets after a name mean "do it now". You'll see this pattern everywhere in Python |

The prompt goes back to `PS ...>` or `%`.

> **Important habit:** always check which prompt you're at. `>>>` means you're talking to Python. `PS ...>` or `%` means you're talking to the terminal. Typing a terminal command into Python (or the other way round) is the most common beginner mix-up.

> **Try it now 1.4**
> Start Python, then work out:
> 1. Brightside sold 14 helmets at £35 each. What's the revenue?
> 2. A £600 bike has 20% off. What's 20% of 600? (Hint: 20% is `0.2`.)
> 3. Three sales: £15.00, £250.00 and £42.75. What's the total?
>
> Then `exit()`.

### 7.2 Script mode: writing a recipe and saving it

Real work is saved in files called **scripts**, so it can be run again tomorrow, by someone else, or automatically at 2am. That's what pipelines are.

**Step 1.** In VS Code's Explorer, right-click the `lesson01` folder → **New File** → name it `hello.py` and press Enter. The `.py` tells everyone it's Python.

(If VS Code suggests installing the **Python extension** from Microsoft, click **Install**. It adds the Run button and helpful highlighting. If it doesn't ask, click the Extensions icon on the left bar, the four small squares, search "Python", and install the one by Microsoft.)

**Step 2.** Type this into `hello.py`:

```python
# My first Python script
print("Hello, Brightside Bikes!")
print("I am learning data engineering.")
```

**Step 3.** Save: **Ctrl + S** (Windows) or **Cmd + S** (Mac). A white dot on the file's tab means "not saved yet". Python runs the *saved* version, so always save first.

**Step 4.** Run it. In the terminal (make sure you're in `lesson01` and at the normal prompt, not `>>>`):

```bash
python hello.py
```

You should see:

```
Hello, Brightside Bikes!
I am learning data engineering.
```

Congratulations, you've written and run a program.

#### Line by line: the script

**Line 1:** `# My first Python script`

| Part | Meaning |
|------|---------|
| `#` | Starts a **comment**. Python ignores everything after `#` on that line |
| `My first Python script` | A note for humans |

Comments are like sticky notes on the recipe for the next person who reads it (often you, three months from now). The cook skips them.

**Line 2:** `print("Hello, Brightside Bikes!")`

| Part | Meaning |
|------|---------|
| `print` | A **function**: a named, ready-made instruction. `print` means "show this on the screen" |
| `(` `)` | The brackets hold whatever you're handing to the function. Like passing a parcel through a hatch |
| `"` `"` | Quote marks say "this is text, use it exactly as written". Text in quotes is called a **string** (short for "string of characters") |
| `Hello, Brightside Bikes!` | The text itself |

**Metaphor for functions:** a function is like a machine with a slot. `print` is a machine that displays whatever you put in the slot. Functions are one of the most important ideas in all of programming, and you'll spend lessons 18 to 20 learning to build your own. For now, just notice the shape: **name, then brackets, then the input inside**.

**Line 3:** `print("I am learning data engineering.")`

The same again, with different text. Python runs line 2 first, then line 3: **top to bottom, one line at a time.**

#### Line by line: the command

`python hello.py`

| Part | Meaning |
|------|---------|
| `python` | Start the cook |
| `hello.py` | The recipe to follow. Because there's no full path, Python looks in the folder you're standing in. That's why you needed to be in `lesson01` |

**Shortcut:** with the Python extension installed, you can also click the ▷ **Run** button at the top-right of the editor. It runs the same command for you. Learn the typed way too, though, because servers don't have Run buttons.

> **Try it now 1.5**
> 1. Change the first message to say hello to you by name. Save and run again.
> 2. Add a fourth line that prints `Lesson 1 complete`.
> 3. Add a comment above it saying what it does.

---

## 8. A taste of a real pipeline

Here's a tiny script with the same shape as every pipeline you'll build: **Extract, Transform, Load.** You are **not** expected to understand all of it yet. Each piece gets a full lesson later. The goal is to see the shape and recognise the ideas when they come back.

Create a new file in `lesson01` called `tiny_pipeline.py` and type (don't copy and paste; typing builds the habit):

```python
# A tiny pipeline: Extract, Transform, Load

# EXTRACT: raw sales from the Leeds shop till (pretend data, stored as text)
raw_sales = ["120.50", "89.99", "15.00", "250.00"]

# TRANSFORM: turn each piece of text into a number and add it to a running total
total = 0
for sale in raw_sales:
    total = total + float(sale)

# LOAD: deliver the result (here, just to the screen)
print("Leeds shop total sales: £", total)
```

Save and run:

```bash
python tiny_pipeline.py
```

You should see:

```
Leeds shop total sales: £ 475.49
```

### Line by line

**`raw_sales = ["120.50", "89.99", "15.00", "250.00"]`**

| Part | Meaning |
|------|---------|
| `raw_sales` | A **variable**: a name for a piece of data. Like a labelled box. Lesson 13 covers these properly |
| `=` | In Python, `=` means "put this into the box", **not** "is equal to". Read it as "becomes" |
| `[` `]` | Square brackets make a **list**: several items in order, like a shopping list. Lesson 15 |
| `"120.50"` ... | Each sale, in quotes, so they're **text**, not numbers yet. This is realistic: data from other systems very often arrives as text |
| `,` | Separates the items in the list |

**`total = 0`**

Create a box called `total` and put `0` in it. It's like zeroing a till at the start of the day.

**`for sale in raw_sales:`**

| Part | Meaning |
|------|---------|
| `for` | Start a **loop**: do the next bit once for every item |
| `sale` | A temporary name for "the item we're on right now". First it's `"120.50"`, then `"89.99"`, and so on |
| `in raw_sales` | Which list to go through |
| `:` | The colon says "the instructions to repeat are coming next" |

**Metaphor:** a cashier going through a pile of receipts, picking each one up in turn.

**`    total = total + float(sale)`**

| Part | Meaning |
|------|---------|
| (4 spaces) | The **indentation** (the gap at the start) is how Python knows this line belongs *inside* the loop. It isn't decoration; it's required. VS Code adds it automatically after a `:` |
| `float(sale)` | `float` is a function that turns text like `"120.50"` into a real number `120.50`. "Float" is the computer name for a number with a decimal point. Lesson 13 |
| `total + float(sale)` | Take what's already in the `total` box and add this sale |
| `total = ...` | Put the new answer back in the `total` box |

So the box goes 0 → 120.50 → 210.49 → 225.49 → 475.49.

Why convert? Try it in the REPL: `"120.50" + "89.99"` gives `'120.5089.99'`. Adding two pieces of text just glues them together. That's a real data bug you'll meet at work, and a perfect example of what the **Transform** step fixes.

**`print("Leeds shop total sales: £", total)`**

`print` can take more than one thing, separated by commas. It shows each one with a space in between, which is why there's a space after the `£`. We'll learn neater ways to format money in lesson 14.

> **Try it now 1.6**
> 1. A late sale of £42.75 comes in. Add it to the list (remember the quotes and a comma). Run it. What's the new total?
> 2. Remove the 4 spaces before `total = total + float(sale)` and run it. Read the error, then put the spaces back.

---

## Common mistakes

| What you see | What it means | Fix |
|--------------|---------------|-----|
| `python is not recognized...` (Windows) or `command not found: python` (Mac) | The terminal can't find the cook under that name | Use `py` (Windows) or `python3` (Mac) |
| `can't open file '...hello.py': No such file or directory` | You're standing in the wrong folder, or the name is misspelt | Run `pwd` and `ls`, then `cd` to the right folder |
| Old output appears even after you changed the code | The file isn't saved | Look for the white dot on the tab; press Ctrl/Cmd + S |
| `NameError: name 'Hello' is not defined` | You forgot the quotes, so Python thought `Hello` was the name of a box, and there's no box with that name | Put text in quotes: `"Hello"` |
| `SyntaxError: unterminated string literal` | You opened a quote but didn't close it. ("Syntax" means the grammar rules of the language.) | Make sure every `"` has a partner |
| `IndentationError: expected an indented block` | A line after a `:` wasn't indented | Add 4 spaces (or press Tab) |
| Typing `python hello.py` and getting `SyntaxError` | You're inside the REPL (`>>>`), not the terminal | Type `exit()` first |

**Reading error messages:** Python's errors look scary but are really helpful. Read from the **bottom up**. The last line says *what* went wrong. Just above it, a little `^` arrow points to *where*.

---

## End-of-lesson exercises

Do these in your `lesson01` folder. Answers are at the bottom, but try properly first. Getting stuck and working it out is how it sticks.

### Warm-up

**W1.** In your own words (one or two sentences each), explain to a non-technical friend:
- (a) what a data engineer does
- (b) what ETL stands for and what each step means
- (c) the difference between the terminal and the Python REPL

**W2.** Using only the terminal, create this structure inside `lesson01`, then use `ls` to check it:

```
lesson01/
└── practice/
    ├── raw/
    └── clean/
```

(Real data projects are often organised exactly like this: a place for raw data as it arrived, and a place for cleaned data.)

### Core

**C1.** Create `about_me.py` that prints three lines:
- your name
- your new job title
- one thing you're looking forward to learning

Add a comment at the top describing what the script does. Run it.

**C2.** Break things on purpose (this is genuinely useful practice). For each change, run the script, read the last line of the error, write down what it says, then fix it:
- (a) remove the closing `"` from one of your `print` lines
- (b) remove the closing `)` from one of your `print` lines
- (c) misspell `print` as `prnt`

**C3.** Brightside's online store had these orders yesterday, as text: `"59.99"`, `"1200.00"`, `"8.50"`, `"34.00"`, `"249.99"`. Copy `tiny_pipeline.py` into a new file `online_pipeline.py`, change it to use these orders, and change the message to say `Online store total sales: £`. What's the total?

### Stretch

**S1.** Write `two_shops.py` that works out the totals for **two** shops and prints three lines: Leeds total, Manchester total, and the combined total. Use:
- Leeds: `"120.50"`, `"89.99"`, `"15.00"`, `"250.00"`
- Manchester: `"300.00"`, `"45.50"`, `"19.99"`

Hint: you'll need two lists, two totals, and two loops. For the combined total, you can add two boxes together: `leeds_total + manchester_total`.

**S2.** Think back to Try it now 1.1 and your own BA project. Draw (on paper is fine) the pipeline as boxes and arrows: sources on the left, the tap on the right, with Extract, Transform and Load in between. Under the Transform box, list every cleaning step you can think of. Keep this; we'll come back to it in lesson 34 when you build a real pipeline.

---

## Recap

- A **data engineer** builds and looks after the pipes that move data from where it's created to where it's used, like a water company.
- The core pattern is **ETL**: Extract (get it), Transform (fix it), Load (put it somewhere useful).
- A **path** is a file's full address. Your **working directory** is the folder you're standing in.
- The **terminal** lets you give typed instructions: `pwd`, `ls`, `mkdir`, `cd`, `cd ..`.
- **Python** is the cook that follows your recipe top to bottom. Run it interactively (`>>>`, the REPL) for quick tests, or as a **script** (`python file.py`) for real work.
- `print(...)` shows things on screen. Text goes in quotes. `#` starts a comment.
- Errors are read **bottom up**.

## Key terms

| Term | Plain-English meaning |
|------|----------------------|
| Data engineering | Building and maintaining the systems that move and prepare data |
| Data source | Where data is created (till, website, app, spreadsheet) |
| Data pipeline | A set of automated steps that moves data from source to destination |
| ETL | Extract, Transform, Load |
| Data warehouse | A central database built for reporting, holding data from many sources |
| Path | The full address of a file or folder |
| Directory | Another word for folder |
| Working directory | The folder you're currently "standing in" |
| Terminal | A window for typing commands to the computer |
| Command | An instruction typed into the terminal (`cd`, `ls`) |
| Option | An extra setting for a command, often starting with `--` |
| Python interpreter | The program that reads and runs Python code |
| REPL | Interactive Python, with the `>>>` prompt |
| Script | A saved file of code, run from start to finish |
| Function | A named, ready-made instruction, used as `name(input)` |
| String | A piece of text, written in quotes |
| Comment | A note for humans, starting with `#`; Python ignores it |
| Variable | A named box that holds a value (preview; lesson 13) |
| Syntax | The grammar rules of a programming language |

## Next lesson

**Lesson 2: How computers store data.** We'll open up the boxes: what's really inside a file, why CSV and JSON are everywhere in data engineering, and why the difference between `"120.50"` (text) and `120.50` (a number) causes so many real-world bugs.

---

## Answers

### Try it now 1.1
There's no single right answer. A typical example: *"The sales dashboard. Data came from the till system and the e-commerce platform (reservoirs). Store names were spelt differently and refunds had to be removed (treatment). Regional managers used it every Monday (tap)."* If you couldn't answer one part, that's probably the part a data engineer handled quietly behind the scenes.

### Try it now 1.2
1. **Extract**: copying data out of a source.
2. **Transform**: cleaning and standardising values.
3. **Load**: putting finished data into its destination.
4. **Transform**: calculating new values from existing ones.
5. **Extract**: getting data from a source (an email attachment is still a source).

### Try it now 1.3
```bash
pwd                # shows a path ending in lesson01
mkdir scratch      # makes the folder
cd scratch         # walks into it
pwd                # path now ends in lesson01/scratch (or lesson01\scratch on Windows)
cd ..              # back up to lesson01
ls                 # shows: scratch (plus hello.py etc. if you've made them already)
```

### Try it now 1.4
```python
14 * 35              # 490
600 * 0.2            # 120.0, so the discount is £120 and the price is £480
15.00 + 250.00 + 42.75   # 307.75
```
Don't worry that Python shows `120.0` with a `.0` on the end; that's just how it displays decimal numbers. Lesson 13 explains why.

### Try it now 1.5
```python
# My first Python script
print("Hello, Jamie!")
print("I am learning data engineering.")
# Tell me I've finished the lesson
print("Lesson 1 complete")
```

### Try it now 1.6
1. The list becomes `raw_sales = ["120.50", "89.99", "15.00", "250.00", "42.75"]` and the output is `Leeds shop total sales: £ 518.24`.
2. You get `IndentationError: expected an indented block after 'for' statement on line ...`. Python is saying "you started a loop with `:` but didn't tell me what to repeat". The indentation is how it knows.

### W1 (example answers)
- (a) A data engineer builds the automated "plumbing" that collects data from the systems where it's created, cleans it, and stores it so analysts and dashboards can use it reliably.
- (b) Extract, Transform, Load: get the data out of its source, clean and reshape it, then put it into the place it'll be used (like a data warehouse).
- (c) The terminal is for talking to the computer (moving between folders, running programs). The Python REPL (`>>>`) is for talking directly to Python, one line at a time. You start the REPL by typing `python` in the terminal and leave it with `exit()`.

### W2
From inside `lesson01`:
```bash
mkdir practice
cd practice
mkdir raw
mkdir clean
ls          # shows: clean  raw
cd ..       # back to lesson01
```

### C1
```python
# Prints a short introduction about me
print("Jamie")
print("Data Engineer")
print("I'm looking forward to building my first real pipeline.")
```
Run with `python about_me.py`.

### C2
- (a) `SyntaxError: unterminated string literal (detected at line N)`: the text was opened with `"` but never closed.
- (b) `SyntaxError: '(' was never closed`: the bracket was opened but never closed.
- (c) `NameError: name 'prnt' is not defined. Did you mean: 'print'?`: Python doesn't know any instruction called `prnt`. Newer versions of Python even suggest the fix.

(The exact wording can differ slightly between Python versions. The important part is learning to find the last line and the `^` arrow.)

### C3
```python
# A tiny pipeline for the online store

# EXTRACT
raw_sales = ["59.99", "1200.00", "8.50", "34.00", "249.99"]

# TRANSFORM
total = 0
for sale in raw_sales:
    total = total + float(sale)

# LOAD
print("Online store total sales: £", total)
```
Output: `Online store total sales: £ 1552.48`

### S1
```python
# Totals for two shops, and combined

# EXTRACT
leeds_sales = ["120.50", "89.99", "15.00", "250.00"]
manchester_sales = ["300.00", "45.50", "19.99"]

# TRANSFORM
leeds_total = 0
for sale in leeds_sales:
    leeds_total = leeds_total + float(sale)

manchester_total = 0
for sale in manchester_sales:
    manchester_total = manchester_total + float(sale)

combined_total = leeds_total + manchester_total

# LOAD
print("Leeds total: £", leeds_total)
print("Manchester total: £", manchester_total)
print("Combined total: £", combined_total)
```
Output:
```
Leeds total: £ 475.49
Manchester total: £ 365.49
Combined total: £ 840.98
```
Notice we wrote nearly the same loop twice. That repetition is a sign a **function** would help: write the "add up a list" recipe once, then use it for any shop. That's exactly what you'll learn to do in lesson 18.

(Small heads-up: with some numbers, Python might show something like `840.9799999999999` instead of `840.98`. That's a quirk of how computers store decimals, not a mistake in your code. Lesson 14 explains it and shows how to round.)

### S2
Your own drawing. A good one has at least two sources, clearly labelled E, T and L steps, and three or more specific cleaning steps (for example: fix date formats, remove test transactions, standardise shop names, remove duplicates, convert text to numbers).
