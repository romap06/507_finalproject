import json
import sqlite3
import plotly.graph_objs as go
import romap_final_1

# QUERY FUNCTIONS
def get_genre_counts():
    ''' Constructs and executes SQL query to retrieve genre names and total book counts
    and formats to be used for graphs

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    query_for_total = '''
        SELECT Name, Count
        FROM Genres
    '''

    #get data from database
    connection = sqlite3.connect("genre_library.sqlite")
    cursor = connection.cursor()
    result = cursor.execute(query_for_total).fetchall()
    connection.close()

    #creating usable results
    x_var = []
    y_var = []
    for tups in result:
        x.append(tup[0])
        y.append(tup[1])

    return x_var, y_var



def get_genre_top_counts():
    ''' Constructs and executes SQL query to retrieve genre names and book counts for books over 4.55 rating

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    query_for_top = '''
        SELECT Name, Top_Books_Count
        FROM Genres
    '''

    connection = sqlite3.connect("genre_library.sqlite")
    cursor = connection.cursor()
    result = cursor.execute(query_for_top).fetchall()
    connection.close()


    #creating usable results
    x_var = []
    y_var = []
    for tups in result:
        x.append(tup[0])
        y.append(tup[1])

    return x_var, y_var



def count_ratings():
    ''' Constructs and executes SQL query to retrieve the range of ratings and how many books belong to each value

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    query_for_ratings = '''
        SELECT COUNT (DISTINCT Rating)
        FROM Books
    '''

    query_for_rating = '''
    SELECT Rating as [rating RANGE], COUNT (*)
    FROM (
        SELECT CASE
            WHEN rating BETWEEN 4.00 AND 4.55 THEN 4.5
            WHEN rating BETWEEN 4.56 AND 4.65 THEN 4.6
            WHEN rating BETWEEN 4.65 AND 4.75 THEN 4.7
            WHEN rating BETWEEN 4.76 AND 4.85 THEN 4.8
            WHEN rating BETWEEN 4.86 AND 4.95 THEN 4.9
            WHEN rating BETWEEN 4.96 AND 5 THEN 5.0
        FROM RATING
    ) BOOKS
    GROUP BY RATING
    '''
    connection = sqlite3.connect("genre_library.sqlite")
    cursor = connection.cursor()
    result = cursor.execute(query_for_ratings).fetchall()
    connection.close()

    #creating usable results
    x_var = []
    y_var = []
    for tups in result:
        x.append(tup[0])
        y.append(tup[1])

    return x_var, y_var

#PLOTLY FUNCTIONS

def create_bar_chart(x_variables, y_variables, category):
    '''Make a bar chart.

    Parameters
    ----------
    x_variables: list of values for x axis
    y_variables: list of values for y axis

    Returns
    -------
    bar_graph
    '''
    if category == "genre_counts":
        category_title = "Total Books Count per Genre"
        category_x = "Genres"
        category_y = "Total Books"
    if category == "ratings_count":
        category_title = "Amount of Books in Library by Ratings"
        category_x = "Rating"
        category_y = "Count"


    bar_data = go.Bar(x=x_variables, y=y_variables)
    basic_layout = go.Layout(title=category_title, xaxis=category_x, yaxis=category_y)
    fig = go.Figure(data = bar_data, layout=basic_layout)

    fig.show()

def create_scatter_plot(x_variables, y_variables, category):
    '''Make a scatter plot.

    Parameters
    ----------
    x_variables: list of values for x axis
    y_variables: list of values for y axis

    Returns
    -------
    scatter_plot
    '''

    if category == "ratings_count":
        category_title = "Amount of Books in Library by Ratings"
        category_x = "Rating"
        category_y = "Count"


    scatter_data = go.Scatter(x=x_variables, y=y_variables, mode='markers', marker={'color': 'teal'})
    basic_layout = go.Layout(title=category_title, xaxis=category_x, yaxis=category_y)
    fig = go.Figure(data = scatter_data, layout=basic_layout)

    fig.show()

def create_pie_chart(x_variables, y_variables, category):
    '''Make a pie chart.

    Parameters
    ----------
    x_variables: list of values for x axis
    y_variables: list of values for y axis

    Returns
    -------
    pie_chart
    '''

    if category == "genre_top_counts":
        category_title = "Amount of Books in Genre with 4.55 or Higher Rating"
        category_x = "Genre"
        category_y = "Count"


    pie_data = go.Pie(labels=x_variables, values=y_variables)
    basic_layout = go.Layout(title=category_title)
    fig = go.Figure(data = scatter_data, layout=basic_layout)

    fig.show()

if __name__ == "__main__":

    #run queries for graphing variables
    overall_genre_count_variables = get_genre_counts()
    top_genre_count_variables = get_genre_top_counts()
    rating_variables = count_ratings()

    #get graphs
    overall_counts_bar = create_bar_chart(overall_genre_count_variables, category="genre_counts")
    top_counts_pie = create_pie_chart(top_genre_count_variables, category = "genre_top_counts")
    rating_bar = create_bar_chart(rating_variables, category="ratings_count")
    rating_scatter = create_scatter_plot(rating_variables, category = "ratings_count")

    #interactive code
    while True:
        search1 = input("If you would link to see graphs breaking down the amount of books for a range of ratings enter 'Yes' or 'exit': ")
        if search1.lower() != "exit":
            print("Here are two graphs that display the amount of books in library across the Rating criteria in different ways")
            rating_bar
            rating_scatter
            search2 = input("If you would link to see breakdown of the total and top counts per genre enter 'Yes' or 'exit': ")
            if search2.lower() != "exit":
                overall_counts_bar
                top_counts_pie
                search3 = input("To view the top 5 books in a specific genre enter genre name here (Please enter only one genre): ")
                for genre in final_genre_library:
                    for k, v in genre:
                        if search3.lower() == k["genre_name"]:
                            genre_name = search3
                    list_for_genre = romap_final_1.create_book_instance(romap_final_1.final_genre_library, genre_name)
                print("List of Books")
                print("----------------------------------------------")
                for i in range(len(list_for_genre)):
                    print(f"{[i+1]} {list_for_genre[i]}")
                search3 = input("If you want to see a different genre enter 'back' or 'exit' if done: ")
                if search3.lower() == "back":
                    continue
                elif search3.lower() == "exit":
                    exit()
            elif search2.lower() != "yes" or search2.lower() != "exit":
                print("Error. Invalid input.")
                continue
            elif search2.lower() == "exit":
                exit()
        elif search1.lower() != "yes" or search1.lower() != "exit":
            print("Error. Invalid input.")
            continue
        elif search1.lower == "exit":
            exit()