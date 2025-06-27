<<<<<<< HEAD

from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar
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

def extract_body_paragraphs(pdf_path, heading_font_threshold=12.5):
    body_paragraphs = []
    current_para = ""
    current_fontsize = None

    for page_layout in extract_pages(pdf_path):
        for element in page_layout:
            if isinstance(element, LTTextContainer):
                for text_line in element:
                    line_text = text_line.get_text().strip()
                    if not line_text:
                        continue

                    fontsizes = [char.size for char in text_line if isinstance(char, LTChar)]
                    if not fontsizes:
                        continue
                    avg_fontsize = sum(fontsizes) / len(fontsizes)

                    if avg_fontsize >= heading_font_threshold:
                        continue

                    if current_para and line_text.endswith('.'):
                        current_para += " " + line_text
                        body_paragraphs.append(current_para.strip())
                        current_para = ""
                    else:
                        current_para += " " + line_text

    if current_para.strip():
        body_paragraphs.append(current_para.strip())

    return body_paragraphs

pdf_path = r"C:\Users\MalathiV\Documents\git project\AI_assignment\PDF_search_Assignment\AI.pdf"  
split_para_text = extract_body_paragraphs(pdf_path)

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
    for para in split_para_text:
        if cor_keyword in para.split():
            print(f"\nFirst paragraph containing the word '{cor_keyword}':\n")
            print(para)
            found = True
            break

    if not found:
        print(f"\nThe word '{cor_keyword}' was not found in any paragraph.")

    max_freq = 0
    best_para = ""

    for para in split_para_text:
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
=======

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
>>>>>>> caac3cf0cab2e89474492ff045dc6ebe6cd9ee2f
