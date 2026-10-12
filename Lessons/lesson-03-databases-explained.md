# Lesson 3: Databases Explained

## Where we are

In Lesson 2 you saw how data lives in files: CSV for flat tables, JSON for nested data. You also saw the problems: CSV has no types, nothing stops someone typing `two hundred` into a price column, and turning one order into a flat table repeated the customer's details on every row. This lesson introduces the tool that solves those problems: the **database**. By the end you'll have the Brightside Bikes practice database running on your computer, ready for the SQL lessons that start next time.

## What you'll learn

- Why files alone aren't enough for running a business's data
- What a database is, what a relational database is, and where SQL fits in
- Why data is split across several tables instead of one big one
- **Primary keys** and **foreign keys**, the two ideas that hold a database together
- The three kinds of relationship between tables: one-to-one, one-to-many and many-to-many
- Column types and **constraints**: the rules a database enforces for you
- How to build the Brightside database and run your first SQL file against it

## Why this matters at work

As a BA you've probably seen an "entity relationship diagram" in a design document, or heard a developer say "that's a foreign key to the customer table". You may have nodded along. After this lesson you'll understand exactly what it means, and why it matters. Almost every data source you'll extract from, and almost every warehouse you'll load into, is a database. Understanding how tables link together is the single most important skill for writing correct SQL. Most wrong numbers on dashboards come from joining tables without understanding their keys.

---

## 1. Why files aren't enough

Imagine Brightside ran everything from CSV files on a shared drive. Here's what would go wrong:

| Problem | What happens |
|---------|-------------|
| **No rules** | Someone types `two hundred` in a price column, or leaves a date blank. Nothing stops them |
| **Duplication** | Priya's email appears on every order row. When she changes it, someone has to find and fix every copy. Miss one, and now she has two emails |
| **Many people at once** | Two shop managers open `orders.csv` at the same time, both save, and one person's changes vanish |
| **Finding things is slow** | To find one order out of ten million, you'd read the file from the top until you hit it |
| **No links** | Nothing checks that the shop on an order actually exists |

**Metaphor: a pile of boxes versus a library.** Files on a shared drive are like books stacked in boxes in a garage. You can store a lot, but finding something means rummaging, anyone can scribble in the books, and nobody notices when one goes missing. A **database** is a proper library: every book has a catalogue number, there's a catalogue to find things quickly, and a librarian enforces the rules ("you can't take a book out without a library card", "you can't have two books with the same catalogue number").

---

## 2. What a database is

A **database** is an organised collection of data, managed by a program that controls how it's stored, checked, and found.

Strictly speaking, the program is called a **database management system**, or **DBMS**. In the library metaphor, the database is the books and shelves, and the DBMS is the librarian. In everyday speech people call both "the database", and so will we.

### Relational databases

The most common kind is the **relational database**. It stores data in **tables** (rows and columns, exactly as in Lesson 2), and lets tables **relate** to each other through shared values. That's where the name comes from.

### SQL: the language you speak to the librarian

You don't walk into the stacks yourself. You hand the librarian a request slip, and they fetch what you asked for. With a relational database, the request slip is written in **SQL**, short for **Structured Query Language**. (People say it either "S-Q-L" or "sequel". Both are fine.)

A request is called a **query**. Here's one, which you'll run later in this lesson:

```sql
SELECT * FROM shops;
```

Read it as: "Fetch everything from the shops table." Lesson 4 explains each part properly.

This is how the Argos metaphor from before applies here too: your query is the order slip, the database is the warehouse, and the DBMS is the worker who knows where everything is. You never need to know *where* on the shelves the data physically sits. You just say *what* you want.

### Which database?

There are many relational databases. The big names you'll hear at work:

| Database | What it's like |
|----------|---------------|
| **SQLite** | A whole database in a single file. No setup. Built into Python, phones and browsers. What we'll use |
| **PostgreSQL** ("Postgres"), **MySQL** | Free, full-size databases that run as a server many people connect to |
| **Microsoft SQL Server**, **Oracle** | Commercial databases common in large companies |
| **Snowflake**, **BigQuery**, **Redshift**, **Databricks** | Cloud **data warehouses**, built for analysing huge amounts of data (lesson 39) |

**Metaphor:** SQLite is a personal notebook you carry around. Postgres or SQL Server is a library building that many people visit at once. Snowflake is a national archive. They differ in size and features, but they all speak SQL. About 90% of the SQL you learn on SQLite works unchanged on all of them. Where they differ, I'll point it out.

> **Try it now 3.1**
> Think about a system from your BA work (a CRM, a finance system, an ordering system).
> 1. What were the main "things" it kept track of? (Customers? Invoices? Tickets?) Each of these was probably a table.
> 2. Can you think of a time when the same information was stored in two places and they disagreed? What caused it?

---

## 3. Splitting data into tables

In Lesson 2's stretch exercise S2, you flattened Priya's order into a CSV with one row per item:

```text
order_id,order_date,shop_id,customer_id,first_name,last_name,email,product_id,product_name,quantity,unit_price
10452,2026-09-13,1,2087,Priya,Shah,priya.shah@example.com,301,Commuter Helmet,1,89.99
10452,2026-09-13,1,2087,Priya,Shah,priya.shah@example.com,412,LED Light Set,1,30.51
```

Everything about the order and the customer is repeated. Multiply that by thousands of orders, and Priya's name and email might be stored hundreds of times.

The database answer is: **store each fact once, in the table where it belongs, and link tables together using IDs.**

Ask "what are the *things* here?" and give each thing its own table:

| Thing | Table | One row is one... |
|-------|-------|-------------------|
| Customers | `customers` | customer |
| Shops | `shops` | shop |
| Products | `products` | product |
| Orders | `orders` | order |
| The items on each order | `order_items` | item on an order |

Now Priya's details live in exactly one row of `customers`. Her order lives in one row of `orders`, which just says "customer 2087" instead of copying her details. Each item lives in `order_items`, which just says "order 10452, product 301".

**Metaphor: a filing system with cross-references.** In a well-run office, there's one folder per customer, holding their details. An invoice doesn't photocopy the whole customer folder; it just writes the customer number at the top. If you need the customer's address, you look up their folder by number. Change the address once in the folder, and every invoice "knows" the new address.

This idea of storing each fact once is called **normalisation**. Lesson 31 covers it properly, along with the times data engineers deliberately *break* this rule for speed.

---

## 4. Primary keys: every row's ID card

### What a primary key is

A **primary key** is a column (or occasionally a few columns together) whose value **uniquely identifies each row** in a table.

In Brightside's tables:

| Table | Primary key |
|-------|-------------|
| `shops` | `shop_id` |
| `products` | `product_id` |
| `customers` | `customer_id` |
| `orders` | `order_id` |
| `order_items` | `order_item_id` |

**Metaphor: a National Insurance number, or a car's registration plate.** There are lots of people called James Walker, but only one has a particular NI number. Names can be shared and can change; the number can't.

### The three rules of a primary key

1. **Unique.** No two rows can have the same value. Two shops can't both be shop 1.
2. **Never missing.** Every row must have one. A customer without a customer ID would be impossible to refer to.
3. **Doesn't change.** Once Priya is customer 2087, she stays 2087, even if she changes her name, email and address. Everything else points at that number, so changing it would break every link.

### Why not just use the name?

Why not identify customers by name, or by email?

- **Names aren't unique:** there could be two Priya Shahs.
- **Emails change:** Priya might switch to a new email next year.
- **Text is messy:** `Brightside Leeds`, `brightside leeds` and `Brightside Leeds ` (with a space) look the same to a person but not to a computer. You saw this in Lesson 2's messy CSV.

So most tables use a made-up number that means nothing except "this row". This is called a **surrogate key**. A key that's a real-world value, like an email or a car registration, is called a **natural key**. You'll meet both at work; surrogate keys are more common.

> **Try it now 3.2**
> For each item below, would it make a good primary key? Say yes or no, and why.
> 1. A customer's surname
> 2. An order number generated by the till, never reused
> 3. A product's name
> 4. A UK postcode, for a table of customers
> 5. A shop's ID number

---

## 5. Foreign keys: the links between tables

### What a foreign key is

A **foreign key** is a column in one table that holds the **primary key of a row in another table**. It's how tables point at each other.

Look at the `orders` table:

| order_id | customer_id | shop_id | order_date | status |
|----------|-------------|---------|------------|--------|
| 10452 | 2087 | 1 | 2026-09-13 | completed |

- `order_id` is this table's **primary key**: it identifies the order.
- `customer_id` is a **foreign key**: it points to row 2087 in the `customers` table (Priya).
- `shop_id` is a **foreign key**: it points to row 1 in the `shops` table (Brightside Leeds).

It's called "foreign" simply because it belongs to a *different* (foreign) table.

**Metaphor: a cloakroom ticket.** When you hand in your coat, you get a ticket with a number. The ticket isn't the coat, but it tells the attendant exactly which coat is yours. A foreign key is that ticket: `customer_id 2087` on an order isn't the customer, but it tells you exactly which customer to fetch.

### The rule a foreign key enforces

A foreign key brings a rule with it: **you can't point at something that doesn't exist.** The database will refuse an order for shop 99 if there's no shop 99. This is called **referential integrity**, a fancy way of saying "all the cross-references are valid". You'll see the database refuse exactly this later in the lesson.

The cloakroom metaphor works here too: the attendant won't give you a ticket for a peg that doesn't exist.

### Missing foreign keys

Brightside's `orders.customer_id` is allowed to be empty (`NULL`). Why? Because someone can walk into the Leeds shop and buy an inner tube with cash without giving their name. The order still happened; we just don't know who the customer was. Remember from Lesson 2: missing isn't zero. These **walk-in** orders will matter a lot in the joins lessons (8 and 9).

---

## 6. Relationships between tables

Keys create **relationships**. There are three kinds.

### One-to-many (the most common)

**One** shop has **many** orders. Each order belongs to exactly **one** shop.

The rule for building it: **the foreign key goes on the "many" side.** The `orders` table has a `shop_id` column. The `shops` table does *not* have an `order_id` column, because a shop has many orders and you can't fit many values in one box (Lesson 2's "one value per box" rule).

**Metaphor:** a mother and her children. Each child's birth certificate names one mother. The mother's own birth certificate doesn't list her children. To find her children, you look for every certificate that names her.

Other one-to-many examples at Brightside: one customer has many orders; one order has many items; one product appears on many order items.

### Many-to-many

**One** order can contain **many** products, and **one** product can appear on **many** orders. That's many-to-many.

You can't put a foreign key on either side (you'd need many values in one box). The solution is a table in the middle, called a **junction table** (also known as a bridge or link table). At Brightside, that's `order_items`. Each row links one order to one product:

| order_item_id | order_id | product_id | quantity | unit_price |
|---------------|----------|------------|----------|------------|
| 116 | 10452 | 301 | 1 | 89.99 |
| 117 | 10452 | 412 | 1 | 30.51 |

Two foreign keys: `order_id` points at the order, `product_id` points at the product. Together these two rows say "order 10452 contained one Commuter Helmet and one LED Light Set", which is Priya's £120.50 purchase from Lesson 1.

**Metaphor: a class register.** Many students take many classes. The school doesn't write every class on the student's record card, or every student on the class's card. It keeps a register where each line says "this student is in this class".

Notice that `order_items` has its own useful information too: `quantity`, and `unit_price`, the price *at the time of sale*. If Brightside puts the helmet's price up next month, Priya's order should still say she paid £89.99. That's why the price is stored on the order item, not just looked up from `products`.

### One-to-one (rare)

Each row in one table matches at most one row in another. For example, a `customer_preferences` table with exactly one row per customer. It's usually used to keep sensitive or rarely needed columns separate. You won't see it much.

### Drawing it: the entity relationship diagram

Data teams draw tables and their links as an **entity relationship diagram (ERD)**. "Entity" just means "a thing you store data about" (a table). Here's Brightside's:

```text
 ┌─────────────┐         ┌─────────────┐         ┌──────────────┐
 │  customers  │         │   orders    │         │    shops     │
 ├─────────────┤         ├─────────────┤         ├──────────────┤
 │ customer_id │◄────────┤ customer_id │         │ shop_id      │
 │ first_name  │  1    * │ order_id    │ *     1 │ shop_name    │
 │ last_name   │         │ shop_id     ├────────►│ city         │
 │ email       │         │ order_date  │         │ region       │
 │ phone       │         │ status      │         │ opened_date  │
 │ city        │         └──────▲──────┘         │ phone        │
 │ signup_date │                │ 1              └──────────────┘
 │ newsletter  │                │
 └─────────────┘                │ *
                         ┌──────┴────────┐       ┌──────────────┐
                         │  order_items  │       │   products   │
                         ├───────────────┤       ├──────────────┤
                         │ order_item_id │       │ product_id   │
                         │ order_id      │ *   1 │ product_name │
                         │ product_id    ├──────►│ category     │
                         │ quantity      │       │ price        │
                         │ unit_price    │       │ in_stock     │
                         └───────────────┘       └──────────────┘
```

How to read it:

- Each box is a table, listing its columns.
- An arrow goes **from a foreign key to the primary key it points at**.
- `1` and `*` show the relationship. `*` means "many". So `customers 1 ── * orders` reads "one customer, many orders".

Keep this diagram handy. You'll look at it constantly during the SQL lessons. I'd suggest copying it into a file called `brightside_erd.txt` in your course folder.

> **Try it now 3.3**
> Using the diagram, answer:
> 1. Which table would you look in to find out what city the Bristol shop is in?
> 2. To find out which products Priya bought, which tables would you need to go through, in order?
> 3. Why is there no `product_id` column in the `orders` table?

---

## 7. Column types and constraints: the librarian's rules

### Column types in SQLite

When a table is created, each column is given a type, like the kitchen containers from Lesson 2. SQLite has a small set:

| SQLite type | Holds | Brightside examples |
|-------------|-------|---------------------|
| `INTEGER` | Whole numbers | `shop_id`, `quantity` |
| `REAL` | Decimal numbers | `price`, `unit_price` |
| `TEXT` | Text | `shop_name`, `email`, `phone` |
| `NULL` | Missing | (not a column type, but any column can hold it unless told otherwise) |

Two things SQLite *doesn't* have, and how we handle them:

- **No date type.** Dates are stored as `TEXT` in ISO format, `YYYY-MM-DD`. Because ISO dates sort correctly as text (Lesson 2), this works well. Bigger databases have a proper `DATE` type.
- **No true/false type.** True/false is stored as an `INTEGER`: `1` for yes, `0` for no. So `in_stock = 1` means "in stock".

An honest note: SQLite is more relaxed about types than most databases. It will usually let you put text in an `INTEGER` column without complaining. Postgres, SQL Server or Snowflake would refuse. Our setup script puts the right types in, so you won't notice, but don't rely on SQLite to catch type mistakes.

Also, `REAL` numbers show with a `.0` on whole amounts, like `1199.0`. That's the same thing you saw with Python's floats in Lesson 1.

### Constraints

A **constraint** is a rule attached to a column that the database enforces on every row, forever. This is the librarian refusing to break the rules.

| Constraint | Rule | Brightside example |
|------------|------|--------------------|
| `PRIMARY KEY` | Unique and never missing | `shop_id` |
| `NOT NULL` | Can't be missing | Every product must have a `product_name` |
| `UNIQUE` | No two rows can have the same value | No two customers can share an `email` |
| `REFERENCES` (foreign key) | Must match a row in another table | `orders.shop_id` must be a real shop |

This is the big advantage over CSV files: **bad data gets stopped at the door, not discovered in a report three weeks later.**

---

## 8. Building the Brightside database

Time to build it. We'll keep all the SQL work for lessons 3 to 12 in one folder, so the database is always in one place.

### Step 1: make the folder

In VS Code, open your `de-course` folder and open the terminal. Run:

```bash
mkdir brightside
cd brightside
mkdir lesson03
```

| Command | What it does |
|---------|-------------|
| `mkdir brightside` | Makes a folder for everything SQL: the database, the helper scripts, and a subfolder per lesson |
| `cd brightside` | Walks into it |
| `mkdir lesson03` | A folder for today's SQL files |

**From now until lesson 12, always start by opening the terminal and running `cd brightside`** (from `de-course`). All the SQL commands assume you're standing there.

### Step 2: get the two scripts

My message that delivered this lesson has two files attached:

- `setup_brightside.py`: builds the database
- `run_sql.py`: runs your SQL files and shows the results as a neat table

Download both and save them into your `de-course/brightside` folder. Check in VS Code's Explorer that they're inside `brightside`, not inside `lesson03`.

Your folder should look like this:

```text
de-course/
├── lesson01/
├── lesson02/
└── brightside/
    ├── lesson03/
    ├── run_sql.py
    └── setup_brightside.py
```

### Step 3: look inside the setup script

Open `setup_brightside.py` in VS Code. It's long, but most of that length is data. It has three parts, marked with comment banners:

1. **Create the tables:** SQL that builds the five empty tables, with their types and constraints.
2. **The data:** a Python list for each table, one line per row.
3. **Put the data on the shelves:** loads each list into its table.

You'll learn to write all of this yourself (SQL table creation in lesson 12, Python and databases in lesson 28). For now, let's read just one table's definition, because it puts everything from sections 4 to 7 together:

```sql
CREATE TABLE orders (
    order_id     INTEGER PRIMARY KEY,
    customer_id  INTEGER REFERENCES customers (customer_id),
    shop_id      INTEGER NOT NULL REFERENCES shops (shop_id),
    order_date   TEXT    NOT NULL,
    status       TEXT    NOT NULL
);
```

| Line | Meaning |
|------|---------|
| `CREATE TABLE orders (` | "Make a new table called `orders`." The column definitions go inside the brackets |
| `order_id INTEGER PRIMARY KEY,` | A column called `order_id`, holding whole numbers. It's the **primary key**: unique and never missing. The comma separates it from the next column |
| `customer_id INTEGER REFERENCES customers (customer_id),` | A whole-number column that's a **foreign key**: its value must match a `customer_id` in the `customers` table. There's no `NOT NULL`, so it *can* be missing, for walk-in customers |
| `shop_id INTEGER NOT NULL REFERENCES shops (shop_id),` | Another foreign key, this time to `shops`. `NOT NULL` means every order must have a shop |
| `order_date TEXT NOT NULL,` | Dates stored as text (ISO format) and required |
| `status TEXT NOT NULL` | `completed`, `refunded` or `cancelled`. No comma, because it's the last column |
| `);` | Close the brackets. The semicolon `;` marks the end of a SQL statement, like a full stop at the end of a sentence |

The spacing that lines everything up is just for readability. SQL doesn't care about spaces or line breaks. SQL keywords are written in CAPITALS by convention (SQL doesn't care about that either, but it makes queries easier to read).

Near the top of the script, you'll also see:

```python
connection.execute("PRAGMA foreign_keys = ON")
```

That line switches on foreign key checking. SQLite, unusually, has it switched off by default. Both scripts switch it on for you.

### Step 4: run it

Make sure you're in the `brightside` folder (`pwd` should end in `brightside`), then:

```bash
python setup_brightside.py
```

(Remember to use `python3` or `py` if that's what works on your computer.) You should see:

```text
Brightside database built at: C:\Users\...\de-course\brightside\brightside.db
  shops:       6 rows
  products:    20 rows
  customers:   30 rows
  orders:      80 rows
  order_items: 127 rows
```

A new file called `brightside.db` has appeared in the Explorer. That single file *is* the whole database: five tables and all their rows. Don't open it in VS Code; it's a binary file (Lesson 2), so you'd see gibberish.

**Your reset button:** if you ever break the data (and in lesson 12 you'll be deliberately changing it), just run `python setup_brightside.py` again. It throws everything away and rebuilds it exactly as it was.

### What's in it

| Table | Rows | What's in it |
|-------|------|-------------|
| `shops` | 6 | The five shops from Lesson 2, plus **Brightside York**, which only opened on 2026-10-01 |
| `products` | 20 | Bikes, parts, accessories and clothing, including the five from Lesson 2 |
| `customers` | 30 | Including Priya Shah, customer 2087 |
| `orders` | 80 | Orders from July to September 2026, including Priya's order 10452 |
| `order_items` | 127 | The items on those orders |

The data has been designed with a few realistic awkward bits for later lessons to discover. Some values are missing, some orders were refunded or cancelled, and not everything in one table has a match in another. We'll find these together.

---

## 9. Your first look inside

### Running a SQL file

Here's how SQL works for the rest of the course: you write SQL in a file ending `.sql`, then run it with `run_sql.py`.

In VS Code, create a new file **inside `lesson03`** called `first_look.sql`:

```sql
-- My first look at the Brightside database
SELECT * FROM shops;
```

| Line | Meaning |
|------|---------|
| `-- My first look...` | Two dashes start a **comment** in SQL, just like `#` in Python. The database ignores it |
| `SELECT * FROM shops;` | "Fetch every column (`*`) from the `shops` table." The `;` ends the statement. Lesson 4 covers this in depth |

Save it, then in the terminal (still in `brightside`):

```bash
python run_sql.py lesson03/first_look.sql
```

| Part | Meaning |
|------|---------|
| `python run_sql.py` | Run the helper script |
| `lesson03/first_look.sql` | Which SQL file to run. It's a **relative path** (Lesson 1): "from here, go into `lesson03` and find `first_look.sql`". On Windows, `lesson03\first_look.sql` works too |

You should see:

```text
shop_id | shop_name                | city       | region     | opened_date | phone
--------+--------------------------+------------+------------+-------------+------------
1       | Brightside Leeds         | Leeds      | North      | 2015-03-14  | 01131234567
2       | Brightside Manchester    | Manchester | North      | 2016-07-01  | 01619876543
3       | Brightside Bristol       | Bristol    | South West | 2018-11-23  | 01175550123
4       | Brightside London Bridge | London     | South East | 2019-05-10  | 02079460000
5       | Brightside Online        | NULL       | Online     | 2017-01-09  | NULL
6       | Brightside York          | York       | North      | 2026-10-01  | 01904555210
(6 rows)
```

That's your first query result from a real database. Notice:

- `NULL` shows where values are missing (the online shop's city and phone). This is the database's word for Python's `None` and JSON's `null`.
- The phone numbers kept their leading zeros, because the column is `TEXT`. The database respected the type.
- `(6 rows)` at the bottom is added by `run_sql.py` to tell you how many rows came back.

**Why `run_sql.py` and not something fancier?** There are good free tools for browsing databases (for example **DB Browser for SQLite**, or VS Code extensions such as **SQLite Viewer**), and you're welcome to install one to look around. But writing SQL in files and running them is how data engineers actually work: the files can be saved, shared, version-controlled (lesson 24) and run automatically. So the course sticks to that.

> **Try it now 3.4**
> 1. Change `shops` to `products` in `first_look.sql`, save and run it again. How many products are there? Which ones have `in_stock` set to `0`?
> 2. Now try `customers`. Find Priya. What's her customer ID and city?
> 3. Change it to `SELECT * FROM shop;` (no "s"). Run it and read the error. What is the database telling you?

### Watching the librarian enforce the rules

Now let's prove the constraints actually work. Create `lesson03/rules_demo.sql`. You don't need to understand `INSERT` yet (that's lesson 12); just read the comments to see what each statement tries to do:

```sql
-- Try to add a second shop with the ID 1
INSERT INTO shops VALUES (1, 'Brightside Leeds Two', 'Leeds', 'North', '2026-10-11', NULL);

-- Try to add an order for a shop that doesn't exist
INSERT INTO orders VALUES (99999, 2087, 99, '2026-10-11', 'completed');

-- Try to add a customer with an email someone already has
INSERT INTO customers VALUES (2999, 'Pat', 'Shah', 'priya.shah@example.com', NULL, 'Leeds', '2026-10-11', 0);

-- Try to add a product with no name
INSERT INTO products VALUES (999, NULL, 'Bikes', 499.00, 1);
```

Run it:

```bash
python run_sql.py lesson03/rules_demo.sql
```

Every statement is refused:

```text
ERROR: UNIQUE constraint failed: shops.shop_id
...
ERROR: FOREIGN KEY constraint failed
...
ERROR: UNIQUE constraint failed: customers.email
...
ERROR: NOT NULL constraint failed: products.product_name
...
```

(Under each error, `run_sql.py` also prints the statement that caused it.)

| Error | Which rule stopped it |
|-------|----------------------|
| `UNIQUE constraint failed: shops.shop_id` | **Primary key**: shop 1 already exists |
| `FOREIGN KEY constraint failed` | **Foreign key**: there's no shop 99 to point at |
| `UNIQUE constraint failed: customers.email` | **Unique**: Priya already has that email |
| `NOT NULL constraint failed: products.product_name` | **Not null**: products must have a name |

Because every statement failed, the data hasn't changed at all. Compare that with Lesson 2's messy CSV, where every one of these mistakes would have quietly gone in.

---

## Common mistakes

| What you see | What it means | Fix |
|--------------|---------------|-----|
| `can't open file '...setup_brightside.py'` | You're not in the `brightside` folder, or the file was saved somewhere else | `pwd` and `ls`; `cd brightside`; check the file is in `brightside`, not `lesson03` or `Downloads` |
| `Can't find brightside.db. Run python setup_brightside.py first.` | The database hasn't been built yet | Run the setup script |
| `Can't find the file lesson03/first_look.sql` | Wrong file name or folder | Check the `.sql` file is inside `lesson03` and the name matches exactly |
| `ERROR: no such table: shop` | A misspelt table name | Check against the ERD: tables are `shops`, `products`, `customers`, `orders`, `order_items` |
| `ERROR: near "SELCT": syntax error` | A misspelt SQL keyword | Check the spelling near the word mentioned |
| The file saved as `first_look.sql.txt` | Some download or save dialogs add `.txt` | Rename it in VS Code's Explorer (right-click → Rename) |
| Downloaded file called `run_sql (1).py` | Downloaded twice | Delete the extra copy and make sure the remaining one is named exactly `run_sql.py` |

---

## End-of-lesson exercises

Save any SQL files in `brightside/lesson03`. Answers are at the bottom.

### Warm-up

**W1.** In your own words, explain:
- (a) the difference between a primary key and a foreign key, using the cloakroom metaphor
- (b) why `order_items` exists, rather than putting product IDs straight onto `orders`
- (c) what a constraint is, and why it's better than checking data afterwards

**W2.** For each of the five Brightside tables, write down its primary key and any foreign keys (and which table each one points to).

### Core

**C1.** Run `SELECT * FROM orders;` and look through the results.
- (a) Some orders have `NULL` in `customer_id`. What does that mean in real life?
- (b) Is there any order for shop 6 (York)? Why might that be? (Look at its `opened_date`, and the range of order dates.)
- (c) What values appear in the `status` column?

**C2.** Brightside is launching a **bike servicing** business. A customer books their bike in at a shop; a mechanic (a member of staff) does the service; the service can involve several parts from the `products` table (brake pads, a chain, and so on).

Design the new tables on paper or in a text file. For each table, give:
- its name and what one row means
- its columns, with a SQLite type for each
- its primary key
- its foreign keys, and which tables they point to

Hint: think about what the *things* are (you'll need at least three new tables), and remember the junction table pattern for many-to-many.

**C3.** Add your new tables to a copy of the ERD from section 6, using arrows and `1` / `*` labels.

### Stretch

**S1.** Run `SELECT * FROM order_items;`. Find the rows for order 10452. Check they match Priya's purchase from Lesson 1 and Lesson 2. Then answer: Brightside doesn't store an order's total anywhere. Why not? How would you work it out? (We'll do this in SQL in lesson 7.)

**S2.** Run `SELECT * FROM products;` and `SELECT * FROM order_items;`. Is there any product that has never been sold? (You'll have to look carefully; in lesson 8 you'll learn a query that does this in one line.) Why would a business care?

**S3.** In section 5 we said `orders.customer_id` can be `NULL` but `orders.shop_id` can't. Think of a reason why a company *might* choose to allow a missing `shop_id` instead. What would go wrong in reports if it did?

---

## Recap

- A **database** is an organised, rule-enforcing store of data, like a library with a librarian. The program running it is a **DBMS**.
- **Relational databases** store data in **tables** that link to each other. You talk to them in **SQL**, by writing **queries**.
- Store each fact **once**, in the table it belongs in (**normalisation**), and link tables with IDs.
- A **primary key** uniquely identifies each row: unique, never missing, never changes.
- A **foreign key** holds another table's primary key, like a cloakroom ticket. It can't point at something that doesn't exist.
- **One-to-many:** the foreign key goes on the "many" side. **Many-to-many:** use a **junction table** (`order_items`).
- An **ERD** draws tables and their links.
- SQLite types: `INTEGER`, `REAL`, `TEXT`. Dates are ISO text; true/false is `1`/`0`. Missing is `NULL`.
- **Constraints** (`PRIMARY KEY`, `NOT NULL`, `UNIQUE`, `REFERENCES`) stop bad data at the door.
- Your SQL workflow: write a `.sql` file in `brightside/lessonNN/`, then `python run_sql.py lessonNN/file.sql` from inside `brightside`. Rebuild the data any time with `python setup_brightside.py`.

## Key terms

| Term | Plain-English meaning |
|------|----------------------|
| Database | An organised collection of data, with rules about what goes in |
| DBMS | Database management system: the program that runs the database (the librarian) |
| Relational database | A database that stores data in linked tables |
| SQL | Structured Query Language: the language for asking a database for data |
| Query | A request written in SQL |
| SQLite | A small database that lives in a single file; built into Python |
| Table | A set of rows and columns about one kind of thing |
| Normalisation | Storing each fact once, in the right table |
| Primary key | The column that uniquely identifies each row |
| Surrogate key | A made-up ID with no real-world meaning, e.g. `customer_id` |
| Natural key | A real-world value used as an ID, e.g. an email |
| Foreign key | A column holding another table's primary key, linking the two |
| Referential integrity | All foreign keys point at rows that really exist |
| One-to-many | One row here relates to many rows there (one shop, many orders) |
| Many-to-many | Many rows on both sides (orders and products) |
| Junction table | A table in the middle of a many-to-many, e.g. `order_items` |
| ERD | Entity relationship diagram: a drawing of tables and how they link |
| Entity | A thing you store data about; usually becomes a table |
| Constraint | A rule the database enforces on a column |
| `NULL` | The database's word for a missing value |
| Statement | One complete SQL instruction, ending with `;` |

## Next lesson

**Lesson 4: Your first queries, SELECT and FROM.** You've run `SELECT * FROM shops;` without really knowing what it does. Next lesson takes it apart word by word, and you'll learn to pick exactly the columns you need, in the order you want, and to start asking the Brightside database real business questions.

---

## Answers

### Try it now 3.1
Your own answers. For example, a CRM might track customers, contacts, opportunities and activities: four tables. A classic example of disagreeing data is a customer's address held in both the CRM and the billing system, updated in one but not the other. That's exactly the duplication problem normalisation solves.

### Try it now 3.2
1. **No.** Surnames aren't unique (many Shahs) and can change.
2. **Yes.** Unique, always present, never changes.
3. **No.** Names can change ("LED Light Set" might be renamed), and two products might share a name.
4. **No.** Many customers can live at the same postcode, and people move.
5. **Yes.** That's exactly what `shop_id` is.

### Try it now 3.3
1. `shops`.
2. `customers` (find Priya's `customer_id`, 2087) → `orders` (find her orders by `customer_id`) → `order_items` (find the items on those orders by `order_id`) → `products` (find each product's name by `product_id`). Four tables. Lesson 9 will show you how to do this in one query.
3. Because an order can contain many products, and you can't fit many values in one box. That's why `order_items` exists.

### Try it now 3.4
1. **20 products.** The two with `in_stock` = `0` are **105 Trailblazer Mountain Bike** and **223 Chain**.
2. Priya is customer **2087**, city **Leeds**.
3. `ERROR: no such table: shop`. The database doesn't have a table with that exact name. Names must match exactly.

### W1 (example answers)
- (a) A primary key is the coat's own unique peg number: it identifies the row. A foreign key is the ticket in your hand: it's stored somewhere else, and it tells you which coat (row) to go and fetch from the other table.
- (b) Because one order can contain many products and one product can be on many orders. A single `product_id` column on `orders` could only hold one product per order. `order_items` gives each order-and-product pairing its own row, and also records the quantity and the price paid.
- (c) A constraint is a rule the database checks every time data goes in, such as "must be unique" or "can't be missing". It's better than checking afterwards because bad data is refused immediately, at the source, rather than discovered later when it's already in reports and harder to trace.

### W2

| Table | Primary key | Foreign keys |
|-------|-------------|--------------|
| `shops` | `shop_id` | none |
| `products` | `product_id` | none |
| `customers` | `customer_id` | none |
| `orders` | `order_id` | `customer_id` → `customers`; `shop_id` → `shops` |
| `order_items` | `order_item_id` | `order_id` → `orders`; `product_id` → `products` |

### C1
- (a) A walk-in sale: someone bought something in a shop without giving their details, so we don't know which customer it was. You'll see these have a physical shop, never shop 5 (online), because online orders need an account.
- (b) **No.** York opened on 2026-10-01, and the orders run from 2026-07-02 to 2026-09-30, so it hadn't opened yet. A shop with no orders is perfectly valid, and it's going to be a useful example when we learn joins.
- (c) `completed`, `refunded` and `cancelled`.

### C2
One good design (yours can differ and still be right):

**`staff`**: one row is one member of staff.

| Column | Type | Notes |
|--------|------|-------|
| `staff_id` | INTEGER | Primary key |
| `first_name` | TEXT | |
| `last_name` | TEXT | |
| `shop_id` | INTEGER | Foreign key → `shops` (the shop they work at) |
| `role` | TEXT | e.g. mechanic, sales |

**`services`**: one row is one service booking.

| Column | Type | Notes |
|--------|------|-------|
| `service_id` | INTEGER | Primary key |
| `customer_id` | INTEGER | Foreign key → `customers` |
| `shop_id` | INTEGER | Foreign key → `shops` |
| `staff_id` | INTEGER | Foreign key → `staff` (the mechanic) |
| `booked_date` | TEXT | ISO date |
| `completed_date` | TEXT | ISO date; `NULL` until it's done |
| `labour_charge` | REAL | |

**`service_parts`**: one row is one part used on one service (the junction table, because a service uses many parts and a part is used on many services).

| Column | Type | Notes |
|--------|------|-------|
| `service_part_id` | INTEGER | Primary key |
| `service_id` | INTEGER | Foreign key → `services` |
| `product_id` | INTEGER | Foreign key → `products` |
| `quantity` | INTEGER | |
| `unit_price` | REAL | Price charged at the time |

If you also stored the customer's bike (make, model, frame number) as its own `bikes` table, with `customer_id` as a foreign key and `bike_id` on `services`, that's an excellent extra: one customer can own many bikes.

### C3
Your diagram should show, at least: `shops 1 ── * staff`, `customers 1 ── * services`, `shops 1 ── * services`, `staff 1 ── * services`, `services 1 ── * service_parts`, `products 1 ── * service_parts`. Arrows go from each foreign key to the primary key it points at.

### S1
Order 10452 has two rows: order items **116** (product 301, Commuter Helmet, quantity 1, £89.99) and **117** (product 412, LED Light Set, quantity 1, £30.51). Together that's £120.50, the same sale as Lesson 1's first Leeds sale and Lesson 2's `order.json`.

The total isn't stored because it can always be **calculated** from the items: for each item, quantity × unit price, then add them up. Storing it as well would be duplication: if an item were corrected and the stored total wasn't, they'd disagree, and nobody would know which was right. (Data warehouses sometimes *do* store totals for speed; lesson 31 explains when that's a good trade.)

### S2
Yes: **106, Kids Balance Bike** never appears in `order_items`. A business would care because it might be overstocked (money tied up in unsold stock), badly priced, badly displayed, or a candidate to discontinue. Spotting things that *don't* appear in another table is a very common data engineering and analysis task.

### S3
A company might allow a missing shop if orders can come from places that aren't shops, like a pop-up stall at a cycling event or a phone order taken by head office. The danger: any report of "sales by shop" would silently leave those orders out (or lump them into a blank group), so total sales by shop wouldn't add up to total sales overall. A common fix is to create a real row for them instead, e.g. a shop called "Events" or "Head office", so every order still has a valid `shop_id`.
