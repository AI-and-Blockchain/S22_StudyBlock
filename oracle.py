import cx_Oracle

# Establish a connection to the Oracle database
dsn = cx_Oracle.makedsn("host", port, service_name="service_name")
conn = cx_Oracle.connect(user="username", password="password", dsn=dsn)

# Execute a query
cursor = conn.cursor()
cursor.execute("SELECT * FROM table_name")
rows = cursor.fetchall()

# Print the results
for row in rows:
    print(row)

# Close the cursor and connection
cursor.close()
conn.close()
