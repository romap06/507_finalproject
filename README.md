# Genre Library with Book Sites
Roma Patel

[Link to this repository](https://github.com/romap06/507_finalproject.git)

## Project Description

This project will go through and scrape all genres from www.goodreads.com/genres/, and add to a genre list as dictionaries for each genre. The project will retrieve genre information such as: name, total books count, and a link for the most read in that genre. The initial list will be narrowed down to 4 final genres for this project. Then the code will get the all the books in each genre grabbing information like the title, author, link to stores, and rating. The final books will also be narrowed down to the top 5 per genre and then added as list to the genre dictionary. A final count of top books will be added to the genre dictionary which depicts how many books in the genre have a rating of 4.60 or higher. Following this the final genre library will be created and data will be added to the database to a Genres and Books tables. The database with then be queried to retrieve genre names and counts, genre names and top counts, rating and counts. These will then be converted and used to plot graphs via plotly. The user will first be provided graphs of the rating and counts. If user wishes to proceed they will be shown the distributions and pie chart for genre statistics and the option to enter a genre if they want to. User will also be offered a list of the 5 books in chosen genre after graphs.

## How to Run the Files
1. First, you will need to pip (or pip3) install plotly
2. Second, you need to make sure all files are in the same directory, and change your working directory when running files
3. Third, run romap_final.py first. Initial "Fetching" of data takes approximately 1 hour, once cached results take 30 minutes. 
4. Fourth, run romap_final_2 second to get user interactive portion

## Database Relations
Each Genre has five books in the Books table
