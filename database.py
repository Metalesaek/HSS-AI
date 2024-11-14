import sqlite3
import bcrypt

def init_db():
	conn = sqlite3.connect('conference.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS users
				 (id INTEGER PRIMARY KEY, 
				  name TEXT, 
				  email TEXT UNIQUE, 
				  password TEXT, 
				  affiliation TEXT,
				  is_confirmed BOOLEAN)''')
	conn.commit()
	conn.close()

def add_user(name, email, password, affiliation):
	conn = sqlite3.connect('conference.db')
	c = conn.cursor()
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	c.execute("INSERT INTO users (name, email, password, affiliation, is_confirmed) VALUES (?, ?, ?, ?, ?)",
			  (name, email, hashed_password, affiliation, False))
	conn.commit()
	conn.close()

def verify_user(email, password):
	conn = sqlite3.connect('conference.db')
	c = conn.cursor()
	c.execute("SELECT password, is_confirmed FROM users WHERE email = ?", (email,))
	result = c.fetchone()
	conn.close()
	if result:
		stored_password, is_confirmed = result
		return bcrypt.checkpw(password.encode('utf-8'), stored_password) and is_confirmed
	return False

def confirm_user(email):
	conn = sqlite3.connect('conference.db')
	c = conn.cursor()
	c.execute("UPDATE users SET is_confirmed = ? WHERE email = ?", (True, email))
	conn.commit()
	conn.close()

init_db()