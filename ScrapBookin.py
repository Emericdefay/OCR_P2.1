# Libraries :
# Already installed on virtual environments.
import os
import sys
import time
import csv
# Need to be installed on virtual environments.
import requests
import bs4


# -------------------------------------------------------------------------------
# Functions :
#

# 1. Handle the folders and files creation.
def pathtofolder():
    """
    Return the current path to ScrapBookin.py.

    :return: The path of current working directory.
    :rtype: str

    :Example:

    >>> pathtofolder()
    "C:\\Folder\\ProjectFolder"

    .. note:: os.path.realpath(sys.argv[0]) work also, but only on IDE.
    """
    return os.getcwd()

def createdatafolder(name):
    """
    Create the <name> folder at the root of ScrapBookin.py.

    :param name: Name of the folder that need to be created
    :type name: str

    :Example:

    >>> createdatafolder("folder1")
    #Will create <folder1> in the current working directory.
    """
    folder = os.path.join(pathtofolder(),name)
    os.makedirs(folder)
    pass

def datafolderexist(name):
    """
    Check if the folder <name> exists at the root and return True or False.

    :param name: Name of the folder checked
    :type name: str
    :return: A boolean : If the folder <name> exists.
    :rtype: bool

    :Example:

    >>> datafolderexist("folder1")
    True
    >>> datafolderexist("folder2")
    False
    """
    folderpath = os.path.join(pathtofolder(), name)
    return os.path.exists(folderpath)

def checkfolderdata(folder = 'datas'):
    """
    Strong verification of the folder data existence.
    Check if the <folder> exist. While not, it tries to create it.
    Then, by recurrence, check again.
    Return True when <folder> exist.

    :param folder: The folder that WILL BE created
    :type folder: str
    :return: Return True only if <folder> folder exist.
    :rtype: bool

    :Example:

    >>> checkfolderdata("folder1")
    #Will Create <folder1> if it doesn't exist yet.
    True

    .. warning:: May cause RunTimeError : maximum depth exceeded...
    """
    if datafolderexist(folder):
        return True
    else:
        createdatafolder(folder)
        checkfolderdata(folder)

def datafileexist(filename):
    """
    Check if the file <filename> in /datas exists and return True or False.

    :param filename: Name of the file that will be checked
    :type filename: str
    :return: If the file <filename>.csv exist in .././datas/
    :rtype: bool

    :Example:

    >>> datafileexist("Default")
    True
    >>> datafileexist("Laws")
    False

    .. warning:: Only check the "datas" folder
    """
    filePath = os.path.join(pathtofolder(), "datas", filename)
    fileFormat = '.csv'
    return os.path.exists(f'{filePath+fileFormat}')

def eraseDatas(folderToRemove='datas'):
    """
    Erase all the content from a folder. Then erase the folder.

    :param folderToRemove: the folder removed
    :type folderToRemove: str
    """
    directoryToRemove = os.path.join(pathtofolder(), folderToRemove)
    for i in os.listdir(directoryToRemove):
        os.remove(os.path.join(directoryToRemove, i))
    os.rmdir(directoryToRemove) # Now the folder is empty of files
    pass

def listFolders(folderRoot):
    """
    Return a list of folders in the <folderRoot> folder.

    :param folderRoot: folder's path where other directories exist.
    :type folderRoot: str
    :return: list of directories
    :rtype: list (str)
    """
    return os.listdir(folderRoot)

def erasePictures(folderPicture='pictures'):
    """
    Function that erases the /pictures folder.

    :param folderPictures: name of the folder that contains pictures.
    :type folderPictures: str
    """
    pathToPictures = os.path.join(pathtofolder(), folderPicture)
    folderList = listFolders(pathToPictures)

    for category in folderList:
        erasePath = os.path.join(folderPicture, category)
        eraseDatas(erasePath)

    eraseDatas(pathToPictures) # Now /pictures is empty of files/folders
    pass

def eraseAll():
    """Erase /pictures and /datas from the working directory."""
    user = input("Would you like to erase all data? (Y/N)")

    if 'y' in user.lower() and not 'n' in user.lower():
        if checkfolderdata():
            eraseDatas()
            print("/datas folder erased.")
        if checkfolderdata('pictures'):
            erasePictures()
            print("/pictures folder erased.")
        print("Datas are erased.")
    else:
        print("Datas not erased : Be sure they're not corrupted.")
    pass


# 2. Manage the .csv
def excelExport(choice):
    """
    A modification to .csv - add a sep definition, helping the reading in
    Excel.
    :param choice: 'excel' if you want a better reading in excel
    :type choice: str
    :return: Return the informations to add on .csv files at the first line
    :rtype: str

    .. warning::
    """
    if "excel" in choice:
        return 'sep=|\n'
    else:
        return ''

def createcsv(fileName):
    """
    Create or rewrite the csv file of each category.

    :param fileName: Name of the .csv file that'll be created in .././datas/
    :type fileName: str

    .. note:: If it exists, will erase the current <filename>.csv and write the
              informations wrote bellow.
    """
    fileName = os.path.join(pathtofolder(), 'datas', fileName)
    fileFormat = '.csv'
    file = f'{fileName + fileFormat}'

    csvKeys = ["product_page_url", "universal_product_code", "title",
               "price_including_tax", "price_excluding_tax", "number_available",
               "product_description", "category", "review_rating", "image_url"]

    addon = excelExport('excel')

    with open(file, 'w', newline="", encoding='utf-8') as csvFile:
        csvFile.write(addon) # Define the separator as <">.
        resultWriter = csv.writer(csvFile, delimiter = '|', dialect = "excel")
        resultWriter.writerow(csvKeys)
    pass

def addcsv(data, fileName):
    """
    Add new <data> on the <filename> .csv file. (at ./datas/)

    :param data: datas scraped
    :param fileName: Name of the .csv edited
    :type data: str
    :type fileName: str
    """
    fileName = os.path.join(pathtofolder(), 'datas', fileName)
    fileFormat = '.csv'
    file = f'{fileName+fileFormat}'

    with open(file, 'a', newline="", encoding='utf-8') as csvFile:
        resultWriter = csv.writer(csvFile, delimiter = '|', dialect = "excel")
        resultWriter.writerow(data)

    pass


# 3. Gestion des images
def downloadpic(url, name, path):
    """
    Download .jpg from the %url%, and name it %name% at the path : %path%.

    :param url: Url of the picture
    :param name: Name of the .jpg created
    :param path: The path where the .jpg will be placed
    :type url: str
    :type name: str
    :type path: str
    """
    a = requests.get(url)

    checkfolderdata("pictures")
    folderPath = os.path.join("pictures", path)

    checkfolderdata(folderPath)

    filePath = os.path.join(folderPath, name)
    fileFormat = '.jpg'
    file = f'{filePath + fileFormat}'

    with open(file, "wb") as pic:
        pic.write(a.content)
    pass


# 4. Scraper
def scrapOne(url):
    """
    Core function of this program:
    This function get all the informations needed for each book of the
    website. It return the datas and the category.

    :param url: The url of the book scraped
    :type url: str
    :return: First : All the datas scraped from a book | Second : the category
    :rtype: str, str
    """
    # HTML de la page web

    response = requests.get(url)

    if response.ok:
        # If the server is responding :
        soup = bs4.BeautifulSoup(response.content.decode('utf-8','ignore'),
                                 'lxml')

        # Get data :
        cellules = soup.findAll('td')
        desc = (soup.findAll('meta'))[-3]

        stars = soup.find('p', {'class': "star-rating"})
        stars = str(stars).split('\n')[0]

        dictStars = {'One':1, 'Two':2, 'Three':3, 'Four':4, 'Five':5}

        for key in dictStars:
            if key in stars:
                review_rating = dictStars[key]

        category = []
        for text in soup.findAll("ul", {"class": "breadcrumb"}):
            for link in text.findAll('a'):
                category.append(link.getText())
        # List of 3 titles, the right one is the third.
        # Use print(category) to see the list.
        # print(category)
        category = category[-1]

        picture = soup.find('img')
        picture = str(picture).split('src="../..')[1][:-3]
        picture = f'http://books.toscrape.com{picture}'

        # Write Datas :
        product_page_url = url

        universal_product_code = cellules[0].text

        title = (str(soup.title))
        title = title.split("\n")[1]
        title = title.replace(" | Books to Scrape - Sandbox", "")
        title = title.replace('    ','')

        # cellules[2] & [3] give the raw data.
        # by using .text[1:] you get the devise and the amount.
        price_including_tax = cellules[2].text[1:]

        price_excluding_tax = cellules[3].text[1:]

        number_available = str(cellules[5])
        number_available = number_available.split("(")[1]
        number_available = number_available.replace(" available)</td>", "")

        product_description = str(desc).split('\n')[1]

        category = category

        review_rating = review_rating

        image_url = picture

        datas = (list(map(str, (product_page_url,
                                         universal_product_code, title,
                                         price_including_tax,
                                         price_excluding_tax,
                                         number_available,
                                         product_description, category,
                                         review_rating, image_url
                                         )
                                         )))

        downloadpic(image_url, universal_product_code, category)

        return datas, category

    else:
        # The server is not responding :
        print("Connection issues : Verify your connection. Check in 10 sec.")
        time.time(10)
        # Retry
        scrapOne(url)


def scraplinksbooks(urlcat):
    """
    Return a list of urls (books pages) from an index page (%urlcat%)

    :param urlcat: Url : Index of the books
    :type urlcat: str
    :return: List of urls
    :rtype: list (str)
    """
    response = requests.get(urlcat)
    soup = bs4.BeautifulSoup(response.text, 'lxml')

    links = []
    articles = soup.findAll('article', {'class': "product_pod"})
    urlRoot = "http://books.toscrape.com/catalogue/"

    for article in articles:
        link = str(article.find('h3').a)
        link = link.split(" title")[0][18:-1]
        link = link.replace('catalogue/', '')

        fullLink = f'{urlRoot+link}'

        links.append(fullLink)

    return links


def detectPages(urlcat):
    """
    In a category of the site, detect if there is more than 1 page (20 books).
    Then return a list of each pages of the category ( first page : index.html)

    :param urlcat: Url of the category page
    :type urlcat: str
    :return: List of page(s) per category
    :rtype: list (str)
    """
    urlcat = urlcat.replace('index.html', '')
    linkpages = ['index.html']

    response = requests.get(urlcat+linkpages[0])

    soup = bs4.BeautifulSoup(response.text, 'lxml')

    next = None

    nextpage = soup.find('li', {'class':'next'})
    if nextpage != None:
        next = (str(nextpage.a).split('">')[0][9:])

    while next != None :
        linkpages.append(next)

        response = requests.get(urlcat + next)
        soup = bs4.BeautifulSoup(response.text, 'lxml')

        nextpage = soup.find('li', {'class':'next'})

        if nextpage != None:
            next = (str(nextpage.a).split('">')[0][9:])
        else:
            next = None

    return linkpages


def scrapcat(urlcat):
    """
    Return the url's list for each books of a category.

    Keyword arguments:
    :param urlcat: Url of the category page
    :type urlcat: str
    :return: List of each books per category
    :rtype: list (str)
    """

    linkscat = detectPages(urlcat)

    urlcat = urlcat.replace('index.html', '')

    linksbooks = []

    for i in range(len(linkscat)):
        link = f'{urlcat + linkscat[i]}'
        linksbooks += scraplinksbooks(link)

    return linksbooks


def managecsv(url):
    """
    Write datas in the category .csv respective.

    Keywords arguments:
    :param url: Url of a book
    :type url: str
    """
    datas = scrapOne(url)
    checkfolderdata()
    if not datafileexist(datas[1]):
        createcsv(datas[1])
        managecsv(url)
    else:
        addcsv(datas[0], datas[1])


def managecat(urlcat):
    """
    The <urlcat> generate the lists of every books in a category.
    Then this list is used to write datas for each books.

    :param urlcat: url of a category
    :type urlcat: str

    .. note:: There is a counter, to see the progression.
    """
    linkscat = scrapcat(urlcat)
    compteur = 1
    for link in linkscat:
        print("\t({}/{}):".format(str(compteur), len(linkscat)), end="")
        # The next print is a quick viewer
        print(link[36:-11])
        managecsv(link)
        compteur += 1
    print("Category done.\n")


def detectCat(url):
    """
    This function get all the categories' links from an <url>.

    :param url: the url of the website
    :type url: str
    :return: A list of url for each category detected.
    :rtype: list (str)
    """
    linkcat = []

    response = requests.get(url)

    soup = bs4.BeautifulSoup(response.text, 'lxml')

    categories = soup.find('ul', {'class': 'nav nav-list'})

    cats = categories.findAll('li')

    for cat in cats:
        categorie = url + str(cat.a).split('\n')[0][9:-2]
        linkcat.append(categorie)

    return linkcat


# Main function
def main(url):
    """
    The main function:
        Take all url of categories of the website and work category by category.
        At each category, take all urls of books and edit the .csv + download
        pictures of every books.
    Datas:
        The datas are transfered in ./datas/ and ranged in <category>.csv
    Pictures:
        The pictures are transfered in ./pictures/ and classed also by category.

    :param url: the url of the website
    :type url: str

    .. note:: Only work on : http://books.toscrape.com/
    """
    linkscat = detectCat(url)
    compteur = 1

    for link in linkscat[1:]:
        print("Scrap ({}/{}): ".format(compteur, len(linkscat)-1)
              + str(link[51:-11]))
        managecat(link)
        compteur += 1

    pass


# Starter
if __name__ == '__main__':
    try:
        temps1 = time.time()
        url = "http://books.toscrape.com/"
        print(f"Scraping website : {url}...")
        main(url)
        temps2 = time.time()
        lap = temps2 - temps1
        print("Whole time to scrap all the website :", end="")
        print(" {} minutes and {}seconds.".format(round(lap) // 60,
                                                  round(lap) % 60))

    except KeyboardInterrupt:
        # stop manuel
        print("WARNING : You stopped the program manually.")

        eraseAll()
        pass

    except (ConnectionError, TimeoutError, requests.exceptions.ConnectionError):
        #connection issue
        print("WARNING : Connection issue, verify your internet.")
        pass

    except (requests.exceptions.MissingSchema):
        # missing http://
        print("WARNING : The address given doesn't fit.")
        print("\t The correct format is : http://adress.com/")
        print("\t Please, modify the address.")
        pass

    except bs4.FeatureNotFound:
        # lxml issue
        print("You need to install lxml. Please look at the README.md")

        eraseAll()
        pass

    except PermissionError:
        # Read only?
        print("Not enough permission : One .csv file is probably open.")
        pass

    except:
        print("Unexpected error: ", sys.exc_info()[0])

        eraseAll()
        raise