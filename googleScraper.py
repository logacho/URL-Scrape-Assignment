# Import packages
import certifi
import urllib3
import csv
from bs4 import BeautifulSoup

# Define constants
inputFile = "SAMPLE_DATA.csv"
outputFile = "output.csv"
base_url = "https://www.google.com/search?q="

# Set up urllib3 with SSL certificate verification
http = urllib3.PoolManager(
	cert_reqs='CERT_REQUIRED',
	ca_certs=certifi.where())

# Define containers for output data and search queries
output_data = []
queries = []

# Read input file and format search queries
# Search queries will contain the Company Name, City, and Country
with open("SAMPLE_DATA.csv", 'rb') as myfile:
    reader = csv.DictReader(myfile)
    for row in reader:
    	output_row = {}
    	output_row["Company Name"] = row['Company Name']
    	output_row["Address Line 1"] = row['Address Line 1']
    	output_row["Address Line 2"] = row['Address Line 2']
    	output_row["City"] = row['City']
    	output_row["Country"] = row['Country']
    	output_data.append(output_row)
    	query = output_row["Company Name"].replace(" ", "+") + '+'
    	query = query + output_row["City"].replace(" ", "+") + '+'
    	query = query + output_row["Country"].replace(" ", "+")
    	queries.append(query)

# Collect the first five results for each search
with open(outputFile, 'wb') as csvFile:
	field_names = ['Company Name', 'Address Line 1', 'Address Line 2', 'City', 'Country', 'URL 1', 'URL 2', 'URL 3', 'URL 4', 'URL 5'] #, 'URL 1 Text']
	writer = csv.DictWriter(csvFile, fieldnames=field_names)
	writer.writeheader()
	for i in range(len(output_data)):
		search_url = base_url 
		search_url = search_url + queries[i]
		response = http.request('GET', search_url)
		soup1 = BeautifulSoup(response.data, "html.parser")
		# Scrape first 5 search result URLs
		links = [a for a in (h3.find('a')['href'] for h3 in soup1.findAll("h3", { "class" : "r" }, limit=5)) if a]
		# Fixed length of the string preceeding all URLs ("/url?q=")
		start = 7
		# Fixed length of the string succeeding all URLs 
		# Example: "&sa=U&ved=0ahUKEwiFzJjwnv3UAhUC_4MKHWwYDmwQFggpMAQ&usg=AFQjCNE4AmY5ko3OFupS0iV-va0NPcxHjQ"
		end = 89
		output_data[i].update({'URL 1': links[0][start:-end]})
		output_data[i].update({'URL 2': links[1][start:-end]})
		output_data[i].update({'URL 3': links[2][start:-end]})
		output_data[i].update({'URL 4': links[3][start:-end]})
		output_data[i].update({'URL 5': links[4][start:-end]})
		writer.writerow(output_data[i])

		# The following code was intended to grab the text content of the first search result

		# response = http.request('GET', output_data[i]['URL 1'])
		# soup2 = BeautifulSoup(response.data, "html.parser")
		# # Ignore unwanted tags
		# [s.extract() for s in soup2(['style', 'script', 'head', 'title', 'meta'])]
		# # Get all visible text
		# text = soup2.get_text().encode('utf-8')
		# # Split text into lines and remove leading and trailing space on each
		# lines = (line.strip() for line in text.splitlines())
		# # Separate multi-headlines
		# chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
		# # Remove blank lines and rejoin
		# text = '\n'.join(chunk for chunk in chunks if chunk)
		# # Add the text content
		# output_data[i].update({'URL 1 Text': text})
		# # Output the data to a .CSV file
		# writer.writerow(output_data[i])



