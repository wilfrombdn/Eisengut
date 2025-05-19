import mysql.connector

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="C0kec@ns"
    )

    cursor = conn.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS eisengut")
    cursor.execute("USE eisengut")

    # Create employees table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(100),
        employee_number VARCHAR(20),
        role VARCHAR(50)
    )
    """)

    # Create or update customers table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS customers (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(150),
        phone VARCHAR(20),
        email VARCHAR(100),
        address TEXT
    )
    """)

    # Ensure customer_id column exists
    cursor.execute("""
        SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE table_schema = 'eisengut' AND table_name = 'customers' AND column_name = 'customer_id'
    """)
    if cursor.fetchone()[0] == 0:
        cursor.execute("ALTER TABLE customers ADD COLUMN customer_id VARCHAR(10) UNIQUE")
        print("✅ Added column: customer_id")

    # Drop any legacy name fields
    legacy_columns = ["first_name", "middle_name", "last_name"]
    for col in legacy_columns:
        cursor.execute(f"""
            SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS 
            WHERE table_schema = 'eisengut' AND table_name = 'customers' AND column_name = '{col}'
        """)
        if cursor.fetchone()[0]:
            cursor.execute(f"ALTER TABLE customers DROP COLUMN {col}")
            print(f"🗑️ Removed legacy column: {col}")

    # Create device_intakes table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS device_intakes (
        id INT AUTO_INCREMENT PRIMARY KEY,
        customer_name VARCHAR(150),
        device VARCHAR(100),
        serial VARCHAR(100),
        problem TEXT,
        condition_received TEXT,
        internal_notes TEXT,
        urgency ENUM('Low', 'Medium', 'High'),
        priority BOOLEAN,
        warranty BOOLEAN,
        employee_id VARCHAR(20),
        intake_date DATE,
        intake_timestamp DATETIME,
        ticket_number VARCHAR(50)
    )
    """)

    # Show all tables
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print("✅ Database and tables created/updated.")
    print("Tables in 'eisengut':")
    for table in tables:
        print(f" - {table[0]}")

    cursor.close()
    conn.close()

except mysql.connector.Error as err:
    print("❌ MySQL Error:", err)

input("\nPress Enter to exit...")
