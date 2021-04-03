import sqlite3

DB_FILENAME = 'scraped_data.sqlite'


def run_commands(commands):
    # takes a list of SQL commands and executes them all
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()

    for command in commands:
        print(f'running command: {command}', "\n")
        if type(command) is tuple:
            cur.execute(*command)
        else:
            cur.execute(command)

    conn.commit()
    conn.close()


def drop_tables():
    # drop tables to delete the previous runs
    run_commands([
        'DROP TABLE IF EXISTS "wiki_category";',
        'DROP TABLE IF EXISTS "wiki_food_category";',
        'DROP TABLE IF EXISTS "wiki_food";',
    ])


def create_tables():
    wiki_category = '''CREATE TABLE IF NOT EXISTS "wiki_category" (
        "id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"             TEXT NOT NULL,
        "description"      TEXT,
        "wiki_url"         TEXT,
        "parent_category"  INTEGER);'''

    wiki_food = '''CREATE TABLE IF NOT EXISTS "wiki_food" (
        "id"               INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "name"             TEXT NOT NULL,
        "description"      TEXT,
        "wiki_url"         TEXT,
        "image_src"        TEXT);'''

    wiki_food_category = '''CREATE TABLE IF NOT EXISTS "wiki_food_category" (
        "id"                INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
        "food_id"           INTEGER,
        "category_id"       INTEGER);'''

    run_commands([
        wiki_category,
        wiki_food,
        wiki_food_category
    ])


def insert_all(categories):

    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()

    for category in categories:
        if category.name:
            cur.execute(*category.insert_cmd())
            category.update_id(cur.lastrowid)

            if category.foods:
                insert_foods(cur, category)

            if category.child_categories:
                for child in category.child_categories:
                    if child.name:
                        cur.execute(*child.insert_cmd(category._id))
                        child.update_id(cur.lastrowid)
                        insert_foods(cur, child, category)

    conn.commit()
    conn.close()


WIKI_FOOD_INSERT = "INSERT INTO wiki_food_category VALUES(NULL, ?, ?)"


def insert_foods(cur, category, parent_category=None):
    for food in category.foods:
        if food.name and food.description:
            cur.execute(*food.insert_cmd())
            food_id = cur.lastrowid

            cur.execute(*(WIKI_FOOD_INSERT, (food_id, category._id)))

            if parent_category:
                cur.execute(*(WIKI_FOOD_INSERT, (food_id, parent_category._id)))


def query_db_by(term):
    # Queries the foods by name and description
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()
    cur.execute('SELECT * FROM wiki_food WHERE name LIKE ?', (term, ))
    in_name = cur.fetchall()
    cur.execute('SELECT * FROM wiki_food WHERE description LIKE ?', (term, ))
    in_desc = cur.fetchall()
    conn.commit()
    conn.close()
    return in_name + in_desc


def get_category_name(_id):
    conn = sqlite3.connect(DB_FILENAME)
    cur = conn.cursor()
    cur.execute('SELECT name FROM wiki_category WHERE id = ?', (_id, ))
    result = cur.fetchone()
    conn.commit()
    conn.close()

    return result[0] if result else None

