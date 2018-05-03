import psycopg2

# Connect to an existing database
conn = psycopg2.connect("postgres://ilwxnlakhzsygl:1bb3b4c1078941d7c9cc0ec9a2df9e32c3989e3347149a259fdbd571ed51871b@ec2-107-21-103-146.compute-1.amazonaws.com:5432/demh6l5vnhecot")

# Open a cursor to perform database operations
cur = conn.cursor()

# Execute a command: this creates a new table
# cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
#
# # Pass data to fill a query placeholders and let Psycopg perform
# # the correct conversion (no more SQL injections!)
# >>> cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)",
# ...      (100, "abc'def"))
#
# # Query the database and obtain data as Python objects
fff = cur.execute("SELECT * FROM telegram_users_insta_accounts")
fdfd = cur.fetchone()
fdfdf = cur.fetchall()
fff = cur.execute('ALTER TABLE telegram_users_insta_accounts ADD column_b VARCHAR(20) NULL, column_c INT NULL')


# Make the changes to the database persistent
#>>> conn.commit()

# Close communication with the database
cur.close()
conn.close()