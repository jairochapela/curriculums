from dataclasses import dataclass
import sqlite3
import uuid

DATABASE = 'candidatos.db'

@dataclass
class Candidato:
    id: str
    first_name: str
    last_name: str
    email: str
    address: str
    phone: str
    education: str
    experience: str
    languages: str

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
    def save(self):
        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO candidatos (id, first_name, last_name, email, address, phone, education, experience, languages)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (self.id, self.first_name, self.last_name, self.email, self.address, self.phone, self.education, self.experience, self.languages))
            conn.commit()



if __name__ == '__main__':
    with sqlite3.connect(DATABASE) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS candidatos (
                id TEXT PRIMARY KEY,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT NOT NULL,
                address TEXT NOT NULL,
                phone TEXT NOT NULL,
                education TEXT NOT NULL,
                experience TEXT NOT NULL,
                languages TEXT NOT NULL
            )
        ''')
        conn.commit()
