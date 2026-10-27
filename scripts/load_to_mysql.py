"""
Automated MySQL Database Loader:
Connects to local MySQL Server and executes schema creation, data seeding,
and analytical views automatically.
"""

import os
import sys
import getpass

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SQL_DIR = os.path.join(BASE_DIR, 'sql')

def run_sql_file_via_cli(host, user, password, port, sql_file):
    import subprocess
    cmd = [
        "mysql",
        f"-h{host}",
        f"-P{port}",
        f"-u{user}",
        f"-p{password}",
        "--default-character-set=utf8mb4"
    ]
    print(f"Executing {os.path.basename(sql_file)} via MySQL CLI...")
    with open(sql_file, 'r', encoding='utf-8') as f:
        proc = subprocess.run(cmd, stdin=f, capture_output=True, text=True)
    if proc.returncode != 0:
        print(f"Error running {sql_file}:\n{proc.stderr}")
        return False
    print(f"Successfully executed {os.path.basename(sql_file)}.")
    return True

def main():
    print("=" * 60)
    print(" Food Delivery Analytics - MySQL Automated Loader")
    print("=" * 60)
    
    host = input("Enter MySQL Host [default: localhost]: ").strip() or "localhost"
    port = input("Enter MySQL Port [default: 3306]: ").strip() or "3306"
    user = input("Enter MySQL Username [default: root]: ").strip() or "root"
    password = getpass.getpass("Enter MySQL Password: ")

    files_to_run = [
        os.path.join(SQL_DIR, '01_schema.sql'),
        os.path.join(SQL_DIR, '02_seed_data.sql'),
        os.path.join(SQL_DIR, '04_views_and_procedures.sql')
    ]

    for sql_file in files_to_run:
        if not os.path.exists(sql_file):
            print(f"File not found: {sql_file}")
            sys.exit(1)
        success = run_sql_file_via_cli(host, user, password, port, sql_file)
        if not success:
            print("\nExecution aborted due to errors.")
            sys.exit(1)

    print("\nDatabase 'food_delivery_db' created and populated successfully!")
    print("You can now open MySQL Workbench to run queries in 'sql/03_analytical_queries.sql'.")

if __name__ == '__main__':
    main()
