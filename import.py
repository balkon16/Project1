import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():
    f = open("books.csv")
    reader = csv.reader(f)
    # db.execute("CREATE TABLE books (\
    #             isbn VARCHAR PRIMARY KEY,\
    #             title VARCHAR NOT NULL,\
    #             author VARCHAR NOT NULL,\
    #             year VARCHAR NOT NULL)")
    # db.commit()
    firstline = True
    for i, t, a, y in reader:
        if firstline:
            firstline = False
            continue
        else:
            db.execute("INSERT INTO books (isbn, title, author, year) VALUES (:isbn, :title, :author, :year)",
            {"isbn":i, "title": t, "author": a, "year": y})
            print(f"Added book from isbn: {i}, title: {t}, by: {a}, from: {y}.")
    db.commit()
    print("Success!")

if __name__ == "__main__":
    main()



 # CREATE TABLE flights (
 #      id SERIAL PRIMARY KEY,
 #      origin VARCHAR NOT NULL,
 #      destination VARCHAR NOT NULL,
 #      duration INTEGER NOT NULL
 #  );

#  firstline = True
# for row in kidfile:
#     if firstline:    #skip first line
#         firstline = False
#         continue
