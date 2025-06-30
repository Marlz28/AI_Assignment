
from pdfminer.high_level import extract_text
import string
from fuzzywuzzy import fuzz
from textblob import TextBlob

text = extract_text(r"C:\Users\MalathiV\Documents\Anto_Assignment\AI.pdf")

import re

def split_para(pdf_text):
    para = []
    for p in pdf_text.split("\n\n"):
      cleaned = re.sub(r'\n+', ' ', p)  
      para.append(cleaned)
    return para

split_para_text1 = split_para(text)

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

store_in_db(split_para_text1) 


def correct_spelling(text):
    blob = TextBlob(text)
    return str(blob.correct())

def search_in_para(cursor) :

    keyword = input("Enter the search key: ")
    cor_keyword = correct_spelling(keyword)
    cursor.execute("SELECT id, content FROM para_table")

    rows = cursor.fetchall()
    results = []

    found = False
    for para in split_para_text1:
        if cor_keyword in para.split():
            print(f"\nFirst paragraph containing the word '{cor_keyword}':\n")
            print(para)
            found = True
            break

    if not found:
        print(f"\nThe word '{cor_keyword}' was not found in any paragraph.")

    max_freq = 0
    best_para = ""

    for para in split_para_text1:
        words = para.split()
        freq = words.count(cor_keyword)
        if freq > max_freq:
            max_freq = freq
            best_para = para

    if max_freq > 0:
        print(f"\nParagraph with highest frequency of '{cor_keyword}' ({max_freq} times):\n")
        print(best_para)
    else:
        print(f"\nThe word '{cor_keyword}' was not found in the PDF.")

    
    for row in rows:
        score = fuzz.partial_ratio(cor_keyword.lower(), row[1].lower())
        results.append((row[0], row[1], score))

    results.sort(key=lambda x: x[2], reverse=True)

    print(f"\nParagraph with high relevance: \n\n{results[0][1]}")

search_in_para(cursor)