# Lesson 2: How Computers Store Data

## Where we are

In Lesson 1 you learned what a data engineer does, moved around with the terminal, and ran your first scripts. In the tiny pipeline you saw that `"120.50"` (text) and `120.50` (a number) behave completely differently. This lesson explains why. We'll open up files to see what's really inside them, learn the basic **types** of data, and meet the two file formats you'll handle more than any others: **CSV** and **JSON**.

## What you'll learn

- What's actually inside a file, and why the £ sign sometimes turns into `Â£`
- The six basic data types: text, whole numbers, decimals, true/false, dates, and missing
- How Python tells you what type something is
- What tabular data is (rows, columns, headers) and what one row should mean
- CSV files: what they are, how to write one, and how they break
- JSON files: what they are, why websites use them, and how they differ from CSV
- Your first look at reading both kinds of file with Python

## Why this matters at work

As a BA you've almost certainly seen these: a report where some shops' sales were missing because their file had a different date format; a customer phone number that lost its leading zero in Excel; a total that came out wrong because some values were stored as text. **Most real data problems are problems of type and format.** A data engineer's first question about any new data source is: *what format is it in, and what types are the values?* After this lesson, you'll ask it too.

Before we start, set up today's folder. In VS Code, open your `de-course` folder, open the terminal (**Terminal → New Terminal**), and run:

```bash
mkdir lesson02
cd lesson02
```

(If you've forgotten what these do: `mkdir` makes a folder, `cd` walks into it. Lesson 1, section 5.)

---

## 1. What's really inside a file

### Everything is numbers

Computers only store numbers. Every file on your computer, whether it's a photo, a song, a spreadsheet or your `hello.py`, is a long row of numbers.

The smallest unit is a **bit**: a single 0 or 1, like a light switch that's off or on. Bits are grouped in eights, called **bytes**. One byte can hold any number from 0 to 255. When you see a file size like "2 KB", that means about 2,000 bytes.

**Metaphor: a bead necklace.** Picture a file as a very long necklace of numbered beads, each bead showing a number from 0 to 255. On its own, the necklace means nothing. You need to know *how to read it*.

### Encoding: the codebook

For text files, the rule for reading the beads is called an **encoding**. An encoding is a codebook that says "number 72 means `H`, number 105 means `i`" and so on.

**Metaphor: Morse code.** Dots and dashes mean nothing until both sides agree on the codebook. If you send a message in Morse and the receiver decodes it with semaphore rules, they get rubbish.

The codebook almost everyone uses today is called **UTF-8**. It covers every letter, symbol and emoji in every language. Older systems sometimes use different codebooks, such as one called **Latin-1** (also known as ISO-8859-1) or Windows-1252.

### The £ sign problem

Here's a bug you've probably seen in a report. Open the Python REPL (type `python` in the terminal, or `python3` on Mac, or `py` on Windows if that's what worked for you in Lesson 1) and try:

```python
"£".encode("utf-8")
```

Python shows:

```
b'\xc2\xa3'
```

| Part | Meaning |
|------|---------|
| `"£"` | The text containing just a pound sign |
| `.encode("utf-8")` | "Turn this text into the beads (bytes), using the UTF-8 codebook." The dot means "do this action to the thing before the dot". You'll use dots constantly from now on |
| `b'...'` | Python's way of showing **bytes** rather than text. The `b` stands for bytes |
| `\xc2\xa3` | Two beads. `\x` means "the next two characters are a number written in hexadecimal", a counting system computers like. You don't need to read hexadecimal. The point is: **in UTF-8, a £ sign takes two beads** |

Now read those same two beads with the *wrong* codebook:

```python
"£".encode("utf-8").decode("latin-1")
```

Python shows:

```
'Â£'
```

| Part | Meaning |
|------|---------|
| `"£".encode("utf-8")` | Same as before: the two beads |
| `.decode("latin-1")` | "Turn these beads back into text using the Latin-1 codebook." Latin-1 thinks each bead is its own character, so the first bead becomes `Â` and the second becomes `£` |

That's exactly what happens when a file written in UTF-8 is opened by a system expecting Latin-1. The data wasn't damaged; it was **read with the wrong codebook**. Whenever you see `Â£`, `â€™` (a mangled apostrophe) or `Ã©` (a mangled é), think "encoding mismatch".

Type `exit()` to leave the REPL.

**The rule to remember:** always use UTF-8 when you create files, and when you receive a file, find out its encoding. You'll see us write `encoding="utf-8"` in Python code later in this lesson for exactly this reason.

### Text files and binary files

Files come in two broad kinds:

| Kind | What it is | Examples | Can you read it in VS Code? |
|------|-----------|----------|------------------------------|
| **Text file** | The beads are characters, read with an encoding | `.py`, `.csv`, `.json`, `.txt`, `.sql` | Yes |
| **Binary file** | The beads follow a program's own private rules | `.xlsx`, `.docx`, `.pdf`, `.png`, `.parquet` | No, you'll see gibberish |

**Metaphor:** a text file is a handwritten letter anyone can read. A binary file is a locked box that only the right program has the key to. An `.xlsx` file needs Excel (or a Python library that understands Excel) to open it.

Data engineers love text formats for moving data around, because any tool, in any language, can read them. That's why CSV and JSON are everywhere.

> **Try it now 2.1**
> 1. In VS Code's Explorer, click on your `hello.py` from Lesson 1. It opens as readable text. Why?
> 2. If you have any `.xlsx` file on your computer, think about what you'd see if you forced VS Code to open it as text. Which kind of file is it?
> 3. A colleague's report shows a customer named `ZoÃ«`. What's most likely gone wrong, and what was her name probably meant to be?

---

## 2. Data types: what kind of value is it?

### The metaphor: kitchen containers

In a kitchen, you store things in containers that suit them: liquids in jugs, eggs in egg boxes, flour in jars. The container decides what you can do. You can pour from a jug, but you can't pour from an egg box. You can count eggs, but you can't really count flour.

Data types are the containers. A value's type decides what you can do with it: you can add numbers, but not names; you can ask how many days are between two dates, but not between two postcodes.

### The six types you need now

| Type | Plain English | Brightside examples | Python name |
|------|---------------|---------------------|-------------|
| **Text** | Letters, words, symbols, anything in quotes | `"Brightside Leeds"`, `"LS1 4AP"`, `"01131234567"` | `str` (string) |
| **Whole number** | A number without a decimal point | `14` helmets, order number `10452` | `int` (integer) |
| **Decimal number** | A number with a decimal point | `89.99`, `0.2` | `float` |
| **True/false** | Only ever one of two values | Is it in stock? `True` | `bool` (boolean) |
| **Date (and time)** | A point in the calendar or clock | `2026-09-13`, `2026-09-13 11:42` | `date` / `datetime` (lesson 10 and 14) |
| **Missing** | "There's no value here" | A customer with no phone number | `None` in Python, `NULL` in SQL |

A few notes on these:

- **Boolean** is named after George Boole, a mathematician. You'll hear "bool" and "boolean" all the time. They're just yes/no values.
- **Missing is not zero, and it's not blank text.** A shop with £0 sales had a bad day. A shop with *missing* sales means we don't know. Treating missing as zero is one of the most common causes of wrong reports. We'll spend real time on missing values in lessons 5 and 26.
- **Dates** are tricky enough to get their own section below.

### Looking at types in Python

Python has a function called `type` that tells you the type of any value. Open the REPL again and try each line:

```python
type("120.50")
type(120.50)
type(14)
type(True)
type(None)
```

You'll see:

```
<class 'str'>
<class 'float'>
<class 'int'>
<class 'bool'>
<class 'NoneType'>
```

| Line | Meaning |
|------|---------|
| `type("120.50")` | Ask "what type is this?" It's in quotes, so it's text, a `str`, even though it looks like a number |
| `type(120.50)` | No quotes and a decimal point, so it's a `float` |
| `type(14)` | No quotes, no decimal point, so it's an `int` |
| `type(True)` | `True` (capital T, no quotes) is one of Python's two boolean values. The other is `False` |
| `type(None)` | `None` (capital N, no quotes) is Python's special "nothing here" value |
| `<class '...'>` | Python's way of saying "this is of type...". "Class" is Python's word for a type. Lesson 30 explains classes properly |

### Why types matter: the same symbol does different things

Still in the REPL, try:

```python
14 + 1
"14" + "1"
"14" + 1
```

| Line | Result | Why |
|------|--------|-----|
| `14 + 1` | `15` | Two numbers, so `+` means "add" |
| `"14" + "1"` | `'141'` | Two pieces of text, so `+` means "glue together". This is called **concatenation** |
| `"14" + 1` | `TypeError: can only concatenate str (not "int") to str` | Text and a number. Python refuses to guess whether you meant add or glue, so it stops with an error |

The third one is Python being helpful. Some tools (including Excel, sometimes) *do* guess, and guess wrong silently. A loud error is far better than a quietly wrong number on a dashboard.

### Looks like a number, but isn't

Some values are made of digits but should be stored as **text**:

- **Phone numbers:** `01131234567`. Stored as a number, the leading zero disappears and it becomes `1131234567`.
- **Postcodes, account numbers, product codes:** `007`, `0012345`.
- **IDs you'd never do maths on:** you'd never add two order numbers together.

**The test:** *would it ever make sense to add or average this?* If not, it's probably text, even if it's all digits. This is why Excel "eating" leading zeros is such a well-known problem: Excel guesses the type, and guesses number.

### Dates: the trickiest type

What date is `01/02/2026`? In the UK it's 1 February. In the US it's January 2. Same characters, different meaning. When Brightside's Leeds till writes `13/09/2026` and an American-built system reads it, it either errors (there's no 13th month) or, worse, for days up to 12, silently swaps day and month.

The fix used across data engineering is the international standard **ISO 8601**: `YYYY-MM-DD`, biggest unit first, like `2026-09-13`. It has two big advantages:

1. **No ambiguity.** Nobody writes year-day-month.
2. **It sorts correctly as text.** `2026-01-05` comes before `2026-09-13` alphabetically and in time. `05/01/2026` and `13/09/2025` don't sort correctly at all.

**Metaphor:** ISO dates are like addresses written country first, then city, then street. Sorting them groups everything sensibly. UK-style dates are like writing the house number first: sort by that and every "No. 1" ends up together, whatever the city.

From now on in this course, dates are always written `YYYY-MM-DD`.

> **Try it now 2.2**
> For each Brightside value, say which type it *should* be stored as (text, whole number, decimal, true/false, date, or missing):
> 1. A customer's email address
> 2. The number of bikes in stock at Leeds
> 3. A bike's price, £749.00
> 4. Whether a customer has signed up to the newsletter
> 5. The date a shop opened
> 6. A shop's phone number, `01619876543`
> 7. A customer's middle name, for a customer who doesn't have one
> 8. A product code, `00412`
>
> Then in the REPL, predict the result of `"89.99" + "30.51"` before you run it. Were you right?

---

## 3. Tabular data: rows and columns

You know tables from spreadsheets. Data engineering uses the same idea, with stricter rules.

| shop_id | shop_name | city | region |
|---------|-----------|------|--------|
| 1 | Brightside Leeds | Leeds | North |
| 2 | Brightside Manchester | Manchester | North |

| Word | Meaning |
|------|---------|
| **Column** | One kind of information, running down the table (`city`). Also called a **field** |
| **Row** | One complete thing, running across (the Leeds shop). Also called a **record** |
| **Header** | The first row, holding the column names |
| **Value** | A single box where a row meets a column (`Leeds`) |

### The strict rules

Spreadsheets let you do anything: merged cells, totals halfway down, colours meaning something, two tables side by side on one sheet. Data tables don't allow any of that. The rules are:

1. **One header row**, at the top, with a unique name for each column.
2. **Every row describes the same kind of thing.** In a shops table, every row is a shop. No total rows, no blank spacer rows.
3. **Every value in a column has the same type.** The `opened_date` column is all dates. No "TBC" or "see note".
4. **One value per box.** Not `"Leeds, Bradford"` in a single city box.

**Metaphor:** a spreadsheet is a whiteboard, where anyone can write anything anywhere. A data table is a paper form, where every person fills in the same boxes in the same way. Forms are less flexible, but you can process a thousand of them without reading each one.

Column names in data engineering are usually written in **snake_case**: all lower case, with underscores instead of spaces (`opened_date`, not `Opened Date`). Spaces in names cause problems in code, as you saw with folder names in Lesson 1.

### Granularity: what does one row mean?

As a BA you'll know this one, even if you didn't call it this. **Granularity** (or **grain**) means *what one row represents*. In an orders table, is each row one order, or one item within an order? If an order has a helmet and lights, the first table has 1 row and the second has 2.

Getting the grain wrong is how totals end up double-counted. Always be able to finish the sentence: *"In this table, one row is one ______."* We'll come back to this constantly, especially in lessons 9 and 31.

> **Try it now 2.3**
> Finish the sentence "one row is one ______" for each table:
> 1. A table of every bike Brightside sells, with its price
> 2. A table of every click on Brightside's website
> 3. A table showing total sales for each shop for each day
> 4. A table of every item on every order

---

## 4. CSV files

### What CSV is

**CSV** stands for **Comma-Separated Values**. It's a table saved as plain text: each row is a line, and the values in a row are separated by commas. That's all.

**Metaphor:** a CSV is a table that's been put through a shredder in a very tidy way. Each line is one row, and the commas show where the cuts between columns were. Anyone can tape it back together, as long as they know where the cuts are.

CSV is the most common way data moves between companies and systems: exports from tills, downloads from websites, files emailed by suppliers. You'll handle thousands of them.

### Make your first CSV

In VS Code, create a new file in `lesson02` called `shops.csv` and type (or paste) exactly this:

```text
shop_id,shop_name,city,region,opened_date,phone
1,Brightside Leeds,Leeds,North,2015-03-14,01131234567
2,Brightside Manchester,Manchester,North,2016-07-01,01619876543
3,Brightside Bristol,Bristol,South West,2018-11-23,01175550123
4,Brightside London Bridge,London,South East,2019-05-10,02079460000
5,Brightside Online,,Online,2017-01-09,
```

Save it (Ctrl + S or Cmd + S).

### Line by line

| Line | Meaning |
|------|---------|
| Line 1: `shop_id,shop_name,...` | The **header**: six column names, separated by commas |
| Line 2: `1,Brightside Leeds,Leeds,...` | The first row. Read it as: shop_id is `1`, shop_name is `Brightside Leeds`, city is `Leeds`, region is `North`, opened_date is `2015-03-14`, phone is `01131234567` |
| `South West` | Spaces inside a value are fine. Only commas mark the cuts |
| Line 6: `5,Brightside Online,,Online,2017-01-09,` | Two commas side by side (`,,`) mean "there's an empty value here": the online shop has no city. The comma at the very end means the last value (phone) is empty too |

Notice what CSV **doesn't** have:

- **No types.** Everything is just text. `1`, `2015-03-14` and `01131234567` are all just characters. Whatever reads the file has to decide what type each column is. That's why phone numbers lose their zeros when Excel opens a CSV: Excel decides "that looks like a number".
- **No formatting.** No bold, no colours, no column widths.
- **No difference between empty and missing.** Is the online shop's phone an empty piece of text, or genuinely unknown? CSV can't say. You'll have to decide.

### When a value contains a comma

What if a product name has a comma in it, like **Lock, D-shape**? This line would break:

```text
5001,Lock, D-shape,Accessories,24.99
```

Anything reading it sees five values instead of four: `5001`, `Lock`, ` D-shape`, `Accessories`, `24.99`. Every column after the name is shifted one place to the right.

The fix is to wrap the value in double quotes:

```text
5001,"Lock, D-shape",Accessories,24.99
```

| Part | Meaning |
|------|---------|
| `"Lock, D-shape"` | The quotes say "everything in here is one value, even the comma". The quotes themselves aren't part of the value |

**Metaphor:** quotes are bubble wrap around a fragile item. The shredder knows not to cut inside the bubble wrap.

Other variations you'll meet: some files use semicolons `;` or tabs instead of commas (a tab-separated file is often called **TSV**). The separator is called the **delimiter**. When a file "looks wrong" when opened, a wrong delimiter is the first thing to check.

### Reading a CSV with Python (a preview)

Here's how Python reads your file. As in Lesson 1's tiny pipeline, you're not expected to master all of this yet. Lesson 22 covers reading files in full. The aim is to see it working and understand each piece.

Create `read_shops.py` in `lesson02`:

```python
import csv

with open("shops.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        print(row["shop_name"], "opened", row["opened_date"])
```

Save it, then run it in the terminal (make sure you're in `lesson02`):

```bash
python read_shops.py
```

(Use `python3` or `py` if that's what works for you.) You should see:

```
Brightside Leeds opened 2015-03-14
Brightside Manchester opened 2016-07-01
Brightside Bristol opened 2018-11-23
Brightside London Bridge opened 2019-05-10
Brightside Online opened 2017-01-09
```

#### Line by line

**`import csv`**

| Part | Meaning |
|------|---------|
| `import` | "Bring in a toolkit." Python comes with many ready-made toolkits, called **modules**, but they sit on the shelf until you ask for them |
| `csv` | The name of the toolkit that knows how to read and write CSV files, including the bubble-wrap quote rules |

**Metaphor:** your workshop has a big storeroom of specialist tools. `import csv` fetches the CSV toolbox and puts it on your bench.

The blank line after it is just for readability. Python ignores blank lines.

**`with open("shops.csv", newline="", encoding="utf-8") as file:`**

| Part | Meaning |
|------|---------|
| `open(...)` | A function that opens a file so Python can read it |
| `"shops.csv"` | Which file. No full path, so Python looks in the folder you're standing in (Lesson 1, section 7.2) |
| `newline=""` | A setting the `csv` toolkit asks for. It stops line endings being handled twice, which differs between Windows and Mac. Just always include it when reading CSVs |
| `encoding="utf-8"` | "Read the beads with the UTF-8 codebook." This is the encoding rule from section 1 in action |
| `name="value"` | This pattern, used three times here, is how you give a function **named settings**. Lesson 19 covers it in full |
| `with ... as file:` | "Open the file, call it `file` while we work with it, and close it automatically when we're done." Like borrowing a library book that returns itself |
| `:` | As with `for` in Lesson 1: the indented lines that follow belong to this |

**`    reader = csv.DictReader(file)`**

| Part | Meaning |
|------|---------|
| `csv.DictReader` | A tool from the `csv` toolbox (the dot means "the `DictReader` that lives inside `csv`"). It reads a CSV row by row and uses the header row to label every value |
| `(file)` | Which open file to read |
| `reader = ` | Put that reading tool in a box called `reader` |

**`    for row in reader:`**

Go through the file one row at a time, exactly like the loop over sales in Lesson 1. Each time round, `row` holds one shop.

**`        print(row["shop_name"], "opened", row["opened_date"])`**

| Part | Meaning |
|------|---------|
| `row["shop_name"]` | "From this row, get the value labelled `shop_name`." The square brackets with a name inside mean "look up by label". This is called a **dictionary** lookup, and it's what the "Dict" in `DictReader` means. Lesson 16 covers dictionaries |
| `"opened"` | Plain text to print in the middle |
| `row["opened_date"]` | The value labelled `opened_date` |

Notice the indentation: 8 spaces on the last line, because it's inside the `for`, which is inside the `with`. Each level of "belonging" adds 4 spaces.

> **Try it now 2.4**
> 1. Change the `print` line so it shows each shop's name and its region instead.
> 2. Change `"shop_name"` to `"shopname"` (no underscore) and run it. Read the last line of the error. What is Python telling you?
> 3. Add `print(type(row["shop_id"]))` as a new line inside the loop (same indentation as `print`). What type does Python think the shop_id is? Why?

---

## 5. JSON files

### What JSON is

**JSON** stands for **JavaScript Object Notation**. Despite the name, it has nothing much to do with JavaScript nowadays; it's just the most common way for websites and apps to send data to each other. When Brightside's website talks to the payment provider, or the till sends a sale to head office, it's almost certainly JSON.

The big difference from CSV: **CSV is flat, JSON can be nested.** Things can sit inside other things.

**Metaphor:** a CSV is one row of a register, every row the same shape. A JSON document is a filled-in paper form with sections: a "Customer details" box, then an "Items ordered" section with as many lines as needed, then a "Payment" box. Some sections have sub-sections. That's very natural for something like an order, which has one customer but any number of items.

### Make your first JSON file

Remember the Leeds sale from Lesson 1, the £120.50 helmet and lights? Here's how it might arrive from the till. Create `order.json` in `lesson02`:

```json
{
  "order_id": 10452,
  "order_date": "2026-09-13",
  "shop_id": 1,
  "customer": {
    "customer_id": 2087,
    "first_name": "Priya",
    "last_name": "Shah",
    "email": "priya.shah@example.com"
  },
  "items": [
    {"product_id": 301, "product_name": "Commuter Helmet", "quantity": 1, "unit_price": 89.99},
    {"product_id": 412, "product_name": "LED Light Set", "quantity": 1, "unit_price": 30.51}
  ],
  "paid": true,
  "discount_code": null
}
```

### Piece by piece

JSON has only a handful of building blocks:

| Symbol | Name | Meaning | Example from the file |
|--------|------|---------|-----------------------|
| `{ }` | **Object** | A set of labelled values. Like a form section | The whole order; the `customer` section |
| `"key": value` | **Key-value pair** | A label, a colon, then the value. The label (key) is always text in double quotes | `"order_id": 10452` |
| `,` | Separator | Between pairs, and between list items. No comma after the last one | |
| `[ ]` | **Array** (a list) | Several values in order | `"items": [ ... ]`, holding two items |
| `"..."` | String | Text | `"Priya"`, `"2026-09-13"` |
| `10452`, `89.99` | Number | No quotes. JSON doesn't distinguish whole numbers from decimals | |
| `true` / `false` | Boolean | Lower case in JSON (Python writes `True`/`False`) | `"paid": true` |
| `null` | Missing | JSON's word for "no value" (Python's `None`, SQL's `NULL`) | `"discount_code": null` |

Reading the file from top to bottom:

- The outer `{` ... `}` is the whole order.
- `"order_id": 10452`: the order number, as a number.
- `"order_date": "2026-09-13"`: JSON has **no date type**, so dates travel as text, ideally in ISO format.
- `"customer": { ... }`: a section *inside* the order with four fields of its own. This is **nesting**.
- `"items": [ ... ]`: a list of two items. Each item is its own little `{ }` with four fields. If Priya had bought five things, there would be five.
- `"paid": true`: a boolean.
- `"discount_code": null`: no code was used. Notice the difference from CSV: JSON can clearly say "missing".

Indentation and line breaks in JSON are only for humans. The whole thing could be on one line and mean the same.

Notice too that, unlike CSV, **JSON has some types built in**: numbers, text, true/false and null are all distinguishable. `10452` is a number, `"10452"` would be text. But it still has no dates.

### Reading JSON with Python (a preview)

Create `read_order.py` in `lesson02`:

```python
import json

with open("order.json", encoding="utf-8") as file:
    order = json.load(file)

print(order["order_id"])
print(order["customer"]["first_name"])
print(order["items"][0]["product_name"])
print(order["paid"])
print(order["discount_code"])
```

Run it with `python read_order.py`. You should see:

```
10452
Priya
Commuter Helmet
True
None
```

#### Line by line

| Line | Meaning |
|------|---------|
| `import json` | Fetch the JSON toolbox from Python's storeroom |
| `with open("order.json", encoding="utf-8") as file:` | Open the file with the UTF-8 codebook, call it `file`, and close it automatically afterwards. (No `newline=""` this time; that's only for the `csv` toolbox) |
| `    order = json.load(file)` | `json.load` reads the whole file and turns it into Python values. The result goes in a box called `order` |
| (blank line, no indent) | We've finished with the file, so the following lines are back at the left edge, outside the `with`. The file is now closed, but `order` still holds everything we read |
| `print(order["order_id"])` | Look up the label `order_id` and print it: `10452` |
| `print(order["customer"]["first_name"])` | Two lookups in a row: first open the `customer` section, then inside it get `first_name`. Like "go to the Customer box, then read the First name field" |
| `print(order["items"][0]["product_name"])` | Open `items` (the list), then `[0]` takes the **first** item, then get its `product_name` |
| `print(order["paid"])` | JSON's `true` has become Python's `True` |
| `print(order["discount_code"])` | JSON's `null` has become Python's `None` |

**Why `[0]` for the first item?** Python counts positions in a list starting from **0**, not 1. So `[0]` is the first item, `[1]` is the second. It feels odd at first. Think of it as "how many steps from the start": the first item is zero steps in. Lesson 15 covers this in depth.

> **Try it now 2.5**
> 1. Add a line to `read_order.py` that prints the customer's email address.
> 2. Add a line that prints the unit price of the **second** item.
> 3. In `order.json`, change `"paid": true` to `"paid": True` (capital T), save, and run the script. Read the error, then change it back. What does this tell you about JSON's rules?

---

## 6. Choosing a format

You'll meet many formats, but here's how the main ones compare:

| Format | Shape | Has types? | Readable as text? | You'll see it when... |
|--------|-------|-----------|-------------------|------------------------|
| **CSV** | Flat table | No, everything is text | Yes | Exports, downloads, files from suppliers |
| **JSON** | Nested | Some (no dates) | Yes | Websites and apps sending data (APIs, lesson 29) |
| **Excel (.xlsx)** | Sheets of cells | Excel guesses | No (binary) | Business users send you things |
| **Parquet** | Flat table, stored by column | Yes, strict | No (binary) | Big data and cloud warehouses (lesson 40) |
| **Database table** | Flat table | Yes, strict | Not a file you open directly | Next lesson |

There's no "best" format. Each one suits a job, like the containers in the kitchen.

---

## Common mistakes

| What you see | What it means | Fix |
|--------------|---------------|-----|
| `Â£`, `â€™`, `Ã©` in text | The file was read with the wrong encoding | Read it as UTF-8 (`encoding="utf-8"`), or find out what encoding it really uses |
| Phone numbers or codes lose their leading zeros | Something treated a text column as a number | Store them as text; don't round-trip CSVs through Excel without care |
| Columns shifted one place to the right on some rows | A value contained a comma and wasn't quoted | Wrap values with commas in double quotes |
| `KeyError: 'shopname'` | You asked for a label that doesn't exist. Labels must match exactly, including underscores and capitals | Check the header row or JSON keys for the exact spelling |
| `TypeError: can only concatenate str (not "int") to str` | You tried to `+` text and a number | Convert one of them first, e.g. `float("89.99")` |
| `json.decoder.JSONDecodeError` | The JSON breaks the rules: a missing comma, a comma after the last item, single quotes instead of double, or `True` instead of `true` | Read the line and column number in the error and check there |
| `FileNotFoundError: [Errno 2] No such file or directory` | You're not standing in the folder with the file | `pwd`, `ls`, then `cd lesson02` |

---

## End-of-lesson exercises

Do these in your `lesson02` folder. Answers are at the bottom.

### Warm-up

**W1.** In one or two sentences each, explain:
- (a) what an encoding is, using the Morse code metaphor
- (b) the difference between a missing value and zero, with a Brightside example
- (c) the main difference between CSV and JSON

**W2.** What type will Python report for each of these? Predict first, then check each one with `type(...)` in the REPL.
- (a) `749`
- (b) `"749"`
- (c) `749.0`
- (d) `False`
- (e) `"False"`
- (f) `None`

### Core

**C1.** Create `products.csv` in `lesson02` with this content:

```text
product_id,product_name,category,price,in_stock
301,Commuter Helmet,Accessories,89.99,TRUE
412,LED Light Set,Accessories,30.51,TRUE
105,Trailblazer Mountain Bike,Bikes,749.00,FALSE
220,Puncture Repair Kit,Parts,6.50,TRUE
```

Then answer:
- (a) What is the grain of this table? ("One row is one ______.")
- (b) What type *should* each of the five columns be?
- (c) Add a new row for product `5001`, called `Lock, D-shape`, in `Accessories`, costing `24.99`, in stock. Be careful with the comma.

**C2.** Here's a CSV exported from an old Brightside till system. Without running anything, list every problem you can find. (There are at least seven.)

```text
order_id,order_date,shop,total
10452,13/09/2026,Leeds,120.50
10453,2026-09-13,leeds ,£89.99
10454,2026-09-13,Brightside Manchester,15
10454,2026-09-13,Brightside Manchester,15
10455,,Bristol,two hundred
10456,2026-09-14,London, Bridge,250.00
```

**C3.** Write a JSON file called `customer.json` describing one Brightside customer. It must include: a customer ID (number), first name, last name, email, whether they're signed up to the newsletter (true/false), a phone number that's missing, and an `address` section containing `line_1`, `city` and `postcode`. Then write `read_customer.py` that prints the customer's first name and their city.

### Stretch

**S1.** Combine Lesson 1 and Lesson 2. Write `total_prices.py` that reads `products.csv` (from C1, but use the original four rows, without the lock) and adds up the `price` column, printing `Total of all prices: £` followed by the total. Hint: start from `read_shops.py`, and use the running-total pattern from Lesson 1's tiny pipeline. Remember every value from a CSV arrives as text.

**S2.** Lesson 1's order was "one order with two items" in JSON. Imagine you have to turn `order.json` into a CSV table for an analyst. Write out by hand (in a new file `order_items.csv`) what that CSV would look like if **one row is one item**. Which values end up repeated on every row? Why might that be a problem if someone adds up a column? (This is a preview of a big idea in lesson 31.)

---

## Recap

- Every file is a row of numbers (bytes). An **encoding** is the codebook for turning them into text. Use **UTF-8**. `Â£` means the wrong codebook was used.
- **Text files** (`.csv`, `.json`, `.py`) can be read by anything. **Binary files** (`.xlsx`, `.parquet`) need the right program.
- The six basic types: **text, whole number, decimal, true/false, date, missing**. In Python: `str`, `int`, `float`, `bool`, dates (later), `None`. Use `type(...)` to check.
- A value's type decides what you can do with it. `"14" + "1"` is `"141"`.
- Digits that you'd never add up (phone numbers, codes) should be **text**.
- Write dates as **`YYYY-MM-DD`**.
- In a data table: one header, every row the same kind of thing, every column one type, one value per box. Know the **grain**.
- **CSV** is a flat table as text, with commas between values and quotes around values that contain commas. It has no types.
- **JSON** is nested: objects `{ }`, lists `[ ]`, `"key": value`. It knows text, numbers, `true`/`false` and `null`, but not dates.

## Key terms

| Term | Plain-English meaning |
|------|----------------------|
| Bit | The smallest unit of storage: a single 0 or 1 |
| Byte | Eight bits; holds a number from 0 to 255 |
| Encoding | The codebook for turning bytes into text and back |
| UTF-8 | The standard encoding that covers every language and symbol |
| Text file | A file whose bytes are characters, readable in any editor |
| Binary file | A file whose bytes follow a specific program's rules |
| Data type | What kind of value something is, which decides what you can do with it |
| String (`str`) | Text |
| Integer (`int`) | A whole number |
| Float | A number with a decimal point |
| Boolean (`bool`) | A true/false value |
| `None` / `NULL` / `null` | "No value here" in Python / SQL / JSON |
| Concatenation | Gluing pieces of text together |
| ISO 8601 | The `YYYY-MM-DD` date standard |
| Column / field | One kind of information in a table |
| Row / record | One complete thing in a table |
| Header | The first row, with the column names |
| Grain / granularity | What one row of a table represents |
| snake_case | Naming style using lower case and underscores: `opened_date` |
| CSV | Comma-Separated Values: a flat table as plain text |
| Delimiter | The character that separates values (comma, semicolon, tab) |
| JSON | A text format for nested data, used by websites and apps |
| Object (JSON) | A `{ }` set of labelled values |
| Array (JSON) | A `[ ]` list of values |
| Key-value pair | A label and its value, e.g. `"city": "Leeds"` |
| Nesting | Putting one structure inside another |
| Module | A ready-made toolkit you bring in with `import` |
| Index | A position in a list. Python's start at 0 |

## Next lesson

**Lesson 3: Databases explained.** Files are like boxes on a shelf: fine for moving data around, but not for keeping it organised, checked and quick to search. Next we'll see how a database solves that, learn what primary and foreign keys are, and build the Brightside Bikes practice database you'll use for all the SQL lessons.

---

## Answers

### Try it now 2.1
1. `.py` files are **text files**: their bytes are characters, so any text editor can show them.
2. An `.xlsx` file is a **binary file** (it's actually a compressed bundle of files). As text it would look like random symbols.
3. An **encoding mismatch**: a UTF-8 file read with the wrong codebook. Her name was probably **Zoë**.

### Try it now 2.2
1. Text
2. Whole number
3. Decimal
4. True/false
5. Date
6. Text (you'd never add phone numbers, and the leading zero matters)
7. Missing (not empty text, and certainly not `"None"` written as a word)
8. Text (the leading zeros matter)

`"89.99" + "30.51"` gives `'89.9930.51'`: two pieces of text glued together, not £120.50.

### Try it now 2.3
1. One product
2. One click (one web event)
3. One shop on one day
4. One item on one order (so an order with three items has three rows)

### Try it now 2.4
1. `print(row["shop_name"], "is in", row["region"])` (any wording is fine as long as it uses `row["region"]`).
2. `KeyError: 'shopname'`. Python is saying "there's no column with the label `shopname`". Labels must match the header exactly.
3. `<class 'str'>`, printed five times. CSV has no types, so everything read from a CSV arrives as text, even values that look like numbers. You'd have to convert it yourself, e.g. `int(row["shop_id"])`.

### Try it now 2.5
1. `print(order["customer"]["email"])` prints `priya.shah@example.com`.
2. `print(order["items"][1]["unit_price"])` prints `30.51`. The second item is position `[1]`, because counting starts at 0.
3. You get a `json.decoder.JSONDecodeError` (something like `Expecting value: line 15 column 11`). JSON is strict: booleans must be lower case `true`/`false`. Python and JSON have similar but not identical rules.

### W1 (example answers)
- (a) An encoding is the codebook that says which number stands for which character. Like Morse code, if the sender and receiver use different codebooks, the message comes out as rubbish (e.g. `Â£` instead of `£`).
- (b) Zero is a known value; missing means we don't know. If Bristol sold nothing on Tuesday, sales are £0. If Bristol's till file never arrived, sales are missing, and reporting them as £0 would be wrong.
- (c) CSV is a flat table where every row has the same columns, and everything is text. JSON can be nested (sections inside sections, lists inside records) and knows some types (numbers, true/false, null).

### W2
- (a) `<class 'int'>`
- (b) `<class 'str'>`
- (c) `<class 'float'>`
- (d) `<class 'bool'>`
- (e) `<class 'str'>` (it's in quotes, so it's just the word "False")
- (f) `<class 'NoneType'>`

### C1
- (a) One row is one **product**.
- (b) `product_id`: text is safest (it's an ID; you'd never add them), though many systems store IDs as whole numbers, which is fine if there are never leading zeros. `product_name`: text. `category`: text. `price`: decimal. `in_stock`: true/false.
- (c) The new line is:
```text
5001,"Lock, D-shape",Accessories,24.99,TRUE
```

### C2
Problems (you may find even more):
1. **Mixed date formats:** `13/09/2026` (UK style) on row 1, `2026-09-13` (ISO) elsewhere.
2. **Missing date:** order 10455 has no date.
3. **Inconsistent shop names:** `Leeds`, `leeds ` (lower case and a trailing space), `Brightside Manchester` (full name), `Bristol`.
4. **Currency symbol inside a number:** `£89.99` will fail if converted with `float(...)`.
5. **Inconsistent decimals:** `15` vs `120.50` (not wrong as such, but it hints at different systems).
6. **Duplicate row:** order 10454 appears twice. Adding up the total would count it twice.
7. **Text instead of a number:** `two hundred`.
8. **Unquoted comma:** `London, Bridge` splits into two values, so that row has five values instead of four and the total ends up in the wrong column.

Every one of these is something a data engineer's **Transform** step has to handle. Python's `csv` toolbox would read the last row as `{'order_id': '10456', ..., 'shop': 'London', 'total': ' Bridge', None: ['250.00']}`: the total column gets `' Bridge'` and the real total spills into an unlabelled extra column.

### C3
`customer.json`:
```json
{
  "customer_id": 2087,
  "first_name": "Priya",
  "last_name": "Shah",
  "email": "priya.shah@example.com",
  "newsletter": true,
  "phone": null,
  "address": {
    "line_1": "22 Park Row",
    "city": "Leeds",
    "postcode": "LS1 5HD"
  }
}
```
`read_customer.py`:
```python
import json

with open("customer.json", encoding="utf-8") as file:
    customer = json.load(file)

print(customer["first_name"])
print(customer["address"]["city"])
```
Output:
```
Priya
Leeds
```
Check your JSON has: double quotes around every key and text value, `true` and `null` in lower case, a comma between every pair, and **no** comma after the last pair in each `{ }`.

### S1
```python
import csv

total = 0
with open("products.csv", newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)
    for row in reader:
        total = total + float(row["price"])

print("Total of all prices: £", total)
```
Output: `Total of all prices: £ 876.0`

Line by line, the new parts:
- `total = 0` comes **before** the loop, so the running total starts at zero once, not every row.
- `float(row["price"])` converts the price from text (CSV has no types) to a number. Without `float`, you'd get the `TypeError` from section 2.
- The `print` is back at the left edge, so it runs once, after the file has been read, rather than once per row.

If you left the lock row in, that's fine too: the `csv` toolbox understands the quotes, so the total would be `900.99`. If you get an error instead, check the lock row's quotes and price were typed exactly as in the C1 answer.

### S2
`order_items.csv`:
```text
order_id,order_date,shop_id,customer_id,first_name,last_name,email,product_id,product_name,quantity,unit_price,paid,discount_code
10452,2026-09-13,1,2087,Priya,Shah,priya.shah@example.com,301,Commuter Helmet,1,89.99,TRUE,
10452,2026-09-13,1,2087,Priya,Shah,priya.shah@example.com,412,LED Light Set,1,30.51,TRUE,
```
Everything about the **order** and the **customer** (order ID, date, shop, customer details, paid, discount code) is repeated on every item row. That's a problem if, say, the order also had a delivery charge column: adding it up would count the delivery charge once per item instead of once per order. This is the "grain" problem from section 3, and it's exactly why databases split data into separate tables, which is what Lesson 3 is about.
