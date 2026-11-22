import sqlite3

def run_sql_demo():
    conn = sqlite3.connect(":memory:")
    cur = conn.cursor()

    # 1) Schema must be defined upfront
    cur.executescript("""
        CREATE TABLE customer (
            customer_id INTEGER PRIMARY KEY,
            first_name TEXT, last_name TEXT,
            email TEXT, dob TEXT, annual_spend REAL
        );
        CREATE TABLE address (
            address_id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customer(customer_id),
            location TEXT, street TEXT, city TEXT,
            postal_code TEXT, country TEXT
        );
        CREATE TABLE phone (
            phone_id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customer(customer_id),
            location TEXT, number TEXT
        );
        CREATE TABLE interest (
            interest_id INTEGER PRIMARY KEY,
            customer_id INTEGER REFERENCES customer(customer_id),
            subject TEXT
        );
    """)

    # 2) The same John Doe, split across 4 tables
    cur.execute("INSERT INTO customer VALUES (12345,'John','Doe','john.doe@acme.com','1977-04-01',1292815.75)")
    cur.execute("INSERT INTO address VALUES (1,12345,'work','16 Hatfields','London','SE1 8DJ','United Kingdom')")
    cur.execute("INSERT INTO phone VALUES (1,12345,'work','+44-1234567890')")
    cur.executemany("INSERT INTO interest VALUES (?,12345,?)", [(1, "devops"), (2, "data science")])
    conn.commit()

    # 3) Reading it back needs JOINs
    query = """
        SELECT c.first_name, c.last_name, a.city, p.number, i.subject
        FROM customer c
        JOIN address  a ON a.customer_id = c.customer_id
        JOIN phone    p ON p.customer_id = c.customer_id
        JOIN interest i ON i.customer_id = c.customer_id
        WHERE c.customer_id = 12345
    """
    print("SQL: 4 tables, 3 JOINs needed to rebuild one customer:")
    for row in cur.execute(query):
        print(row)

    # 4) Adding a new attribute requires a schema change
    cur.execute("ALTER TABLE customer ADD COLUMN twitter_handle TEXT")
    print("\nSQL: 'ALTER TABLE' was required to add one new field.")
    conn.close()

if __name__ == "__main__":
    run_sql_demo()
