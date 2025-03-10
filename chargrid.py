import requests
from bs4 import BeautifulSoup

def DisplayGrid(url):     #This method takes the URL and uses it to attempt to make the grid
    table = GetTable(url)   
    if isinstance(table, str):
        print(table)  # Print error message if the table wasn't found
        return
    
    grid = ParseTableToArray(table)
    gridToDisplay = UpdateGrid(grid)
    GridDisplay(gridToDisplay)   

def GetTable(url):  # uses Requests and BeautifulSoup to scrape the table from the website
    response  = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        tables = soup.find_all('table')

        if tables:
            return tables[0]
        else:
            return "No table found."
    else:
        return f"Error fetching the document. Status code: {response.status_code}"
    
def ParseTableToArray(table): #converts the scraped table into a list
    grid = []
    rows = table.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        grid_row = [col.get_text(strip=True) for col in cols]
        grid.append(grid_row)
    
    return grid

def GetMaxSize(grid): #finds the largest int value in the list
    xSize = 0
    ySize = 0
    for row in grid[1:]:        ##first row is a header row on the table
        if int(row[0])> xSize:
            xSize = int(row[0])
        if int(row[2])> ySize:
            ySize = int(row[2])    
    return [xSize+1, ySize+1]

def UpdateGrid(grid): #creates a grid of the right size in spaces and then replaces the non spaces with the chars
    size = GetMaxSize(grid)
    GridToDisplay = [[' ' for _ in range(size[0])] for _ in range(size[1])] 
    for row in grid[1:]:
        x = int(row[2])
        y = int(row[0])
        GridToDisplay[x][y] = row[1]
    
    return GridToDisplay

def GridDisplay(grid): #converts the row into strings of text and then displays it
    for row in grid:
        text = ''
        for char in row:
            text = text + char
        print(text)


DisplayGrid("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")