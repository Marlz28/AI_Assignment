
from pdfminer.high_level import extract_text

text = extract_text(r"C:\Users\MalathiV\Documents\Anto_Assignment\AI.pdf")

import re

def split_para(pdf_text):
    para = []
    for p in pdf_text.split("\n\n"):
      cleaned = re.sub(r'\n+', ' ', p)  
      para.append(cleaned)
    return para
split_para_text = split_para(text)

import sqlite3
def setup_db():
    conn = sqlite3.connect('ai_db.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE if not exists para_table (id INTEGER PRIMARY KEY AUTOINCREMENT,content TEXT NOT NULL)''')
    return cursor
 
cursor = setup_db()
def store_in_db(para_text):
  for p in para_text:
      cursor.execute("INSERT INTO para_table (content) VALUES (?)", (p,))

store_in_db(split_para_text) 


from fuzzywuzzy import fuzz
from textblob import TextBlob

def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())

def search_in_para(cursor) :

    keyword = input("Enter the search key: ")
    cor_keyword = correct_spelling(keyword)
    cursor.execute("SELECT id, content FROM para_table")

    rows = cursor.fetchall()
    results = []

    for row in rows:
        score = fuzz.partial_ratio(cor_keyword.lower(), row[1].lower())
        results.append((row[0], row[1], score))

    results.sort(key=lambda x: x[2], reverse=True)

    print(f"Paragraph: {results[0][1]}")

search_in_para(cursor) 