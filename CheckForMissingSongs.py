import re

import requests
from bs4 import BeautifulSoup
import spotipy
import spotipy.util as util
import os
from dotenv import load_dotenv
import sqlite3


def get_billboard_song_titles_for_year(year):
    """
    Scrapes Wikipedia  for billboard song titles for a given year, There might be better sources to parse from
    but i've chosen wikipeida for this first iteration because the page format is really standard, lightweight and
    hasn't changed for the last 18 years.
    :return: List of billboard songs and artists in a tuple '(song, artist)'
    """
    if year >= 1959:
        billboard_page = "https://en.wikipedia.org/wiki/Billboard_Year-End_Hot_100_singles_of_"
    elif 1956 <= year <= 1958:
        billboard_page = "https://en.wikipedia.org/wiki/Billboard_year-end_top_50_singles_of_"
    else:
        billboard_page = "https://en.wikipedia.org/wiki/Billboard_year-end_top_30_singles_of_"

    page = requests.get(billboard_page + str(year))
    soup = BeautifulSoup(page.content, 'html.parser')
    doc = soup.find("table", {"class": "wikitable"})
    year_data = []
    for row in doc.find_all(["tr"])[1:]:
        # The th is required because ~2000+ uses that format instead
        row_data = [cell.text.strip() for cell in row.findAll(["td", "th"])]
        if len(row_data) != 3:
            print("Error Processing Row: ", row)
        else:
            year_data.append(tuple(row_data))
    return year_data

def parse_song(content):
    for split_token in ["\\", "/"]:
        content = content.partition(split_token)[0]
    return content

def check_if_song_is_missing(year, list_from_wiki):
    connect = sqlite3.connect("data/Sing-Dev.db")
    cursor = connect.cursor()

    list_of_songs_in_db = []


    for x in cursor.execute("select title, year from songs where year=" + str(year)):
        if str(x[0]).lower() == "dance with me henry (wallflower)":
            list_of_songs_in_db.append("the wallflower (dance with me, henry)")
        # elif "(" in x[0]:
        #     temp = re.sub("[\(\[].*?[\)\]]", "", x[0])
        #     list_of_songs_in_db.append(temp)
        #     print(re.sub("[\(\[].*?[\)\]]", "", x[0]))
        else:
            list_of_songs_in_db.append(str(x[0]))

    for x in range(len(list_of_songs_in_db)):
        list_of_songs_in_db[x] = list_of_songs_in_db[x].lower()
        list_of_songs_in_db[x] = list_of_songs_in_db[x].strip()


    list_of_songs_in_db.sort()


    print("Wiki length: ", len(list_from_wiki))
    print("DB length: ", len(list_of_songs_in_db))

    missing_song_tracker = 0
    if len(list_from_wiki) > len(list_of_songs_in_db):
        print('a')
    for x in range(len(list_from_wiki)):
        is_found = False
        found_at = 0

        for y in range(len(list_of_songs_in_db)):

            if(list_from_wiki[x] == list_of_songs_in_db[y] or list_from_wiki[x] in list_of_songs_in_db[y]) or list_of_songs_in_db[y] in list_from_wiki[x]:
                is_found = True

        if not is_found:
            print("From Wiki: " + list_from_wiki[x])


def check_for_missing_songs(year):
    data = get_billboard_song_titles_for_year(year)
    data_clean = []

    for x,y,z  in data:
        data_clean.append(parse_song(y).replace("\"", "").lower())

    data_clean.sort()

    check_if_song_is_missing(list_from_wiki=data_clean, year=year)



if __name__ == "__main__":
    check_for_missing_songs(1959)