from bs4 import BeautifulSoup
import requests
import json
from collections import Counter
from operator import itemgetter
import sqlite3

CACHE_FILENAME = "practice_library.json"
CACHE_DICT = {}

#CACHING FUNCTIONS
def open_cache():
    ''' Opens the cache file if it exists and loads the JSON into
    the CACHE_DICT dictionary.
    if the cache file doesn't exist, creates a new cache dictionary

    Parameters
    ----------s
    None

    Returns
    -------
    The opened cache: dict
    '''
    try:
        cache_file = open(CACHE_FILENAME, 'r')
        cache_contents = cache_file.read()
        cache_dict = json.loads(cache_contents)
        cache_file.close()
    except:
        cache_dict = {}
    return cache_dict

def save_cache(cache_dict):
    ''' Saves the current state of the cache to disk

    Parameters
    ----------
    cache_dict: dict
        The dictionary to save

    Returns
    -------
    None
    '''
    dumped_json_cache = json.dumps(cache_dict)
    fw = open(CACHE_FILENAME,"w")
    fw.write(dumped_json_cache)
    fw.close()


def construct_unique_key(url):
    ''' constructs a key that is guaranteed to uniquely and
    repeatably identify a html request by a url

    Parameters
    ----------
    url: string
        The URL for the html request

    Returns
    -------
    string
        the unique key as a string
    '''

    return url


def make_request_with_cache(url):
    '''Check the cache for a saved result for this baseurl:values
    combo. If the result is found, return it. Otherwise send a new
    request, save it, then return it.

    Parameters
    ----------
    url: string
        The URL for the html request

    Returns
    -------
    dict
        the results of the query as a dictionary loaded from cache
        JSON
    '''

    unique_key = construct_unique_key(url)
    CACHE_DICT = open_cache()
    if unique_key in CACHE_DICT.keys():
        print("Using Cache")
        return CACHE_DICT[unique_key]
    else:
        print("Fetching")
        html = requests.get(url).text
        CACHE_DICT[unique_key] = html
        save_cache(CACHE_DICT)
        return CACHE_DICT[unique_key]


class Book:
    '''book site

    Instance Attributes
    -------------------
    title: string
        the title of the book (e.g. 'November 9')

    author: string
        the name of the author (e.g. 'Colleen Hoover')

    rating: integer
        the review rating of the book (e.g. 4.5)

    link: string
        the link to go to a page with different direct links to purchase book

    genre_name: string
        name of genre book belongs to
    '''

    def __init__(self, title, author, rating, link, genre_name):
        self.title = title
        self.author = author
        self.rating = rating
        self.link = link
        self.genre_name = genre_name

    def info(self):
        return f"{self.title} by {self.author} has a rating of {self.rating}. Belongs to {self.genre_name}. Stores link is: {self.link}"

#SCRAPING FUNCTIONS
def get_pages():
    ''' Make a list of with the links to each page in genre section

    Parameters
    ----------
    None

    Returns
    -------
    list
        list of links to pages
    '''

    get_link = "https://www.goodreads.com/genres/list?utf8=%E2%9C%93&filter=none"

    unique_key = construct_unique_key(get_link)
    CACHE_DICT = open_cache()
    if unique_key in CACHE_DICT.keys():
        print("Using Cache")
        html = make_request_with_cache(get_link)
        soup = BeautifulSoup(html, 'html.parser')
    else:
        print("Fetching")
        html = make_request_with_cache(get_link)
        CACHE_DICT[unique_key] = html
        save_cache(CACHE_DICT)

    soup = BeautifulSoup(html, "html.parser")

    get_shelves_pt1 = soup.find('div', class_='leftContainer')
    get_pages_pt1 = get_shelves_pt1.find_all('div')[-2]
    get_pages_pt2 = get_pages_pt1.find_all('a')[:-1]
    pages = []
    pages.append("https://www.goodreads.com/genres/list?utf8=%E2%9C%93&filter=none")
    for links in get_pages_pt2:
        baseurl = "https://www.goodreads.com"
        link_to_page = baseurl+links.get('href')
        pages.append(link_to_page)

    return pages

def build_genre_list(pages):
    ''' Make a list of dictionaries with genre information from page links

    Parameters
    ----------
    None

    Returns
    -------
    list
        list of dictionaries where dictionaries contains genre details (e.g. [{'genre_name':'adventure', ...}])
    '''
    baseurl_1 = "https://www.goodreads.com"

    genres = []
    #pages = get_pages()

    for other_shelves in pages:

        unique_key = construct_unique_key(other_shelves)
        CACHE_DICT = open_cache()
        if unique_key in CACHE_DICT.keys():
            print("Using Cache")
            html = make_request_with_cache(other_shelves)
            soup = BeautifulSoup(html, 'html.parser')
        else:
            print("Fetching")
            html = make_request_with_cache(other_shelves)
            CACHE_DICT[unique_key] = html
            save_cache(CACHE_DICT)

        soup = BeautifulSoup(html, "html.parser")
        get_genre_info_pt1 = soup.find_all('div', class_='shelfStat')
        for stats in get_genre_info_pt1:
            genre_dict = {}
            get_genres_pt1 = stats.find('a')
            get_book_counts_pt1 = stats.find('div', class_= 'smallText greyText')
            get_counts_pt2 = get_book_counts_pt1.text.replace(',', '').strip()
            genre_dict['genre_name'] = get_genres_pt1.text.lower()
            genre_dict['genre_link'] = baseurl_1+get_genres_pt1.get('href')
            genre_dict['genre_count'] = int(get_counts_pt2[:-6])
            genres.append(genre_dict)

    return genres


def get_top_genres(genres_list):
    ''' Narrow all_genres list to the top 15 genres based on highest book counts

    Parameters
    ----------
    None

    Returns
    -------
    list
        final list of dictionaries for top 15 genres
    '''
    #genres_list = build_genre_list()
    final_genres = sorted(genres_list, key=itemgetter('genre_count'), reverse=True)[:4]
    return final_genres

def get_most_read_link(final_genres_list):
    ''' get the most_read link for each genre in the final_genres list and add to respective genre dictionary

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''

    #final_genres_list = get_top_genres()

    baseurl = "https://www.goodreads.com"
    for genre in final_genres_list:
        genre_page = genre["genre_link"]

        unique_key = construct_unique_key(genre_page)
        CACHE_DICT = open_cache()
        if unique_key in CACHE_DICT.keys():
            print("Using Cache")
            html = make_request_with_cache(genre_page)
            soup = BeautifulSoup(html, 'html.parser')
        else:
            print("Fetching")
            html = make_request_with_cache(genre_page)
            CACHE_DICT[unique_key] = html
            save_cache(CACHE_DICT)

        soup = BeautifulSoup(html, "html.parser")

        most_reads_pt1 = soup.find_all('h2')

        for links in most_reads_pt1:
            try:
                if links.text == "Most Read This Week":
                    most_reads_pt2 = links.find('a')
                    most_read_link = baseurl+most_reads_pt2.get('href')
                    genre["genre_most_read_link"] = most_read_link
            except:
                genre["genre_most_read_link"] = None

    return final_genres_list



def getting_books(final_genres_list):
    ''' get the books from the most_read link for genres and add to final_genres list

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    #final_genres_list = get_top_genres() #maybe make param and then call in main?
    for genre in final_genres_list:

        most_read_page = genre["genre_most_read_link"]

        if most_read_page != None:
            unique_key = construct_unique_key(most_read_page)
            CACHE_DICT = open_cache()
            if unique_key in CACHE_DICT.keys():
                print("Using Cache")
                html = make_request_with_cache(most_read_page)
                soup = BeautifulSoup(html, 'html.parser')
            else:
                print("Fetching")
                html = make_request_with_cache(most_read_page)
                CACHE_DICT[unique_key] = html
                save_cache(CACHE_DICT)

            soup_most_read = BeautifulSoup(html, "html.parser")

            get_books_pt1 = soup_most_read.find_all('div', class_="coverWrapper")
            baseurl = "https://www.goodreads.com"
            books_list = []

            for books in get_books_pt1:
                book_dict = {}

                #grabbing link to book
                get_book_pt2 = books.find('a')
                get_book_pt3 = get_book_pt2.get('href')
                get_book_pt4 = baseurl+get_book_pt3

                #caching link
                unique_key = construct_unique_key(get_book_pt4)
                CACHE_DICT = open_cache()
                if unique_key in CACHE_DICT.keys():
                    print("Using Cache")
                    html = make_request_with_cache(get_book_pt4)
                    soup = BeautifulSoup(html, 'html.parser')
                else:
                    print("Fetching")
                    html = make_request_with_cache(get_book_pt4)
                    CACHE_DICT[unique_key] = html
                    save_cache(CACHE_DICT)

                soup_book_page = BeautifulSoup(html, "html.parser")

                #get title
                get_title = soup_book_page.find('h1', id="bookTitle").text.strip()
                book_dict["title"] = get_title

                #get author
                get_author = soup_book_page.find('a', class_="authorName").text.strip()
                book_dict["author"] = get_author

                #get rating
                get_rating_pt1 = soup_book_page.find('div', id="bookMeta")
                get_rating_pt2 = get_rating_pt1.find('span', itemprop="ratingValue").text.strip()
                book_dict["rating"]= float(get_rating_pt2)

                #get stores link
                get_link_pt1 = soup_book_page.find('div', id="buyDropButtonStores")
                get_link_pt2 = get_link_pt1.find('a').get('href')
                get_link_pt3 = baseurl+get_link_pt2
                book_dict["link"] = get_link_pt3

                #append book distionary to list
                books_list.append(book_dict)

                #reduce book list to five books
                final_books = sorted(books_list, key=itemgetter('rating'), reverse=True)[:5]

            genre["books"] = final_books

    for genre in final_genres_list:
        book_list = genre["books"]
        top_books_list = []
        for book in book_list:
            if book["rating"] >= 4.60:
                top_books_list.append(book)

        top_books_count = len(genre["books"])
        genre["top_books_count"] = int(top_books_count)

    return final_genres_list

def create_book_instance(final_genres_list, genre_name):
    '''Make an instances from a book URL and input parameter.

    Parameters
    ----------
    final_genres_list: list of dictionaries that contains book information
    genre_name: user input parameter

    Returns
    -------
    book_instances_list: an list of info of for each book instance in genre_name
    '''
    book_instances_list = []
    for each_genre in final_genres_list:
        if genre_name.lower() == each_genre["genre_name"].lower():
            for each_book in each_genre["books"]:
                for k, v in each_book.items():
                    title = k["title"]
                    author = k["author"]
                    rating = k["rating"]
                    link = k["link"]
                    genre_name = k["genre_name"]
                    book_instance = Book(title=title, author=author, rating=rating, link=link, genre_name=genre_name)
                    book_instances_list.append(book_instance.info())


    return book_instances_list

#INSERTING INTO DATABASE

def insert_genres(final_genres_list):
    ''' Constructs and executes SQL query to insert genre information into table

    Parameters
    ----------
    final_genres_list: list of dictionaries including genre and book information

    Returns
    -------
    None
    '''
    conn = sqlite3.connect("genre_library.sqlite")
    cursor = conn.cursor()

    insert_genre_info ='''
    INSERT INTO Genres
    VALUES (?, ?, ?, ?)
    '''

    for each_genre in final_genres_list:
        genre_info_list = []
        for k, v in each_genre.items():
            if k == "genre_name":
                genre_info_list.append(v)
            if k == "genre_link":
                genre_info_list.append(v)
            if k == "genre_count":
                genre_info_list.append(v)
            if k == "top_books_count":
                genre_info_list.append(v)

        cursor.execute(insert_genre_info, genre_info_list)
        conn.commit()

def insert_books(final_genres_list):
    ''' Constructs and executes SQL query to retrieve insert book information into table

    Parameters
    ----------
    final_genres_list: list of dictionaries including genre and book information

    Returns
    -------
    None
    '''

    conn = sqlite3.connect("genre_library.sqlite")
    cursor = conn.cursor()

    insert_book_info ='''
    INSERT INTO Books
    VALUES (NULL, ?, ?, ?, ?, ?)
    '''

    for each_genre in final_genres_list:
        book_info_list = []
        for each_book in each_genre["books"]:
            for k, v in each_book.items():
                if k == "title":
                    book_info_list.append(v)
                if k == "author":
                    book_info_list.append(v)
                if k == "rating":
                    book_info_list.append(v)
                if k == "link":
                    book_info_list.append(v)
                if k == "genre_name":
                    book_info_list.append(v)

        cursor.execute(insert_genre_info, book_info_list)
        conn.commit()


if __name__ == "__main__":

    getting_pages = get_pages()
    initial_genre_list = build_genre_list(pages=getting_pages)
    top_genres = get_top_genres(genres_list=initial_genre_list)
    added_link = get_most_read_link(final_genres_list=top_genres)
    final_genre_library = getting_books(final_genres_list = added_link)

    insert_genre = insert_genres(romap_final_1.final_genre_library)
    insert_book = insert_books(romap_final_1.final_genre_library)
    # #run queries for graphing variables
    # overall_genre_count_variables = get_genre_counts()
    # top_genre_count_variables = get_genre_top_counts()
    # rating_variables = count_ratings()


