import mysql.connector
from mysql.connector import Error
from typing import List, Tuple

class Database:
    def __init__(self, host: str, user: str, password: str, database: str):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self._create_connection()
        self._create_table()

    def _create_connection(self):
        try:
            self.con = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cur = self.con.cursor()
        except Error as e:
            print(f"Error connecting to MySQL: {e}")
            self.con = None
            self.cur = None

    def _create_table(self):
        if self.con and self.cur:
            sql = """
            CREATE TABLE IF NOT EXISTS employees(
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                age VARCHAR(255),
                dob VARCHAR(255),
                email VARCHAR(255),
                gender VARCHAR(255),
                contact VARCHAR(255),
                address TEXT
            )
            """
            self.cur.execute(sql)
            self.con.commit()

    def insert(self, name: str, age: str, dob: str, email: str, gender: str, contact: str, address: str) -> None:
        """Insert a new record into the employees table."""
        try:
            if self.con and self.cur:
                sql = "INSERT INTO employees (name, age, dob, email, gender, contact, address) VALUES (%s, %s, %s, %s, %s, %s, %s)"
                self.cur.execute(sql, (name, age, dob, email, gender, contact, address))
                self.con.commit()
        except Error as e:
            print(f"Error inserting data: {e}")

    def fetch(self) -> List[Tuple[int, str, str, str, str, str, str, str]]:
        """Fetch all records from the employees table."""
        try:
            if self.con and self.cur:
                self.cur.execute("SELECT * FROM employees")
                rows = self.cur.fetchall()
                return rows
        except Error as e:
            print(f"Error fetching data: {e}")
            return []

    def remove(self, id: int) -> None:
        """Delete a record from the employees table by id."""
        try:
            if self.con and self.cur:
                self.cur.execute("DELETE FROM employees WHERE id=%s", (id,))
                self.con.commit()
        except Error as e:
            print(f"Error deleting data: {e}")

    def update(self, id: int, name: str, age: str, dob: str, email: str, gender: str, contact: str, address: str) -> None:
        """Update a record in the employees table."""
        try:
            if self.con and self.cur:
                sql = """
                UPDATE employees 
                SET name=%s, age=%s, dob=%s, email=%s, gender=%s, contact=%s, address=%s 
                WHERE id=%s
                """
                self.cur.execute(sql, (name, age, dob, email, gender, contact, address, id))
                self.con.commit()
        except Error as e:
            print(f"Error updating data: {e}")
