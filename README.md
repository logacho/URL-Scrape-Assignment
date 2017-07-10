# URL-Scrape-Assignment
Author: Kelly Logacho
Date: July 9th, 2017

This is a data-scraping project that takes a spreadsheet of companies and compiles their top five Google search results, completed as an exercise for the Releaf Engineering Team.

Using Python and urllib3, each company listed in the input .csv file is searched for using Google Search Engine. Each search query contains the company name, city, and country. The URLs of the five most relevant search results for each company are collected using Beautiful Soup and added to an output .csv file alongside the input data.

Additional Python script that aims to collect the text content of the first search result is commented out due to inconsistent output that varies with the structure of each scraped website.