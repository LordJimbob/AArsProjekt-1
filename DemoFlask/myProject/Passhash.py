import bcrypt
import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()


password_var = "Jensen"
password = password_var.encode("utf-8")

hashable_pw = bytes(password)
hashed_pw = bcrypt.hashpw(hashable_pw, bcrypt.gensalt())
print(hashed_pw)
c.execute("INSERT INTO users (username, password) VALUES(?, ?)", ("ole", hashed_pw))
conn.commit()
conn.close()