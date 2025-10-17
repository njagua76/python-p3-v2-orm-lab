# lib/database.py
import sqlite3

# __define-ocg__: database connection setup
CONN = sqlite3.connect('company.db')
CURSOR = CONN.cursor()
