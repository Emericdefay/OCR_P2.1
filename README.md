# ScrapBookin
### Projet 2 - OCR
This project can scraped informations of the website : http://books.toscrape.com/<br/>
Informations scraped are : 
* Url of the page : product_page_url
* ID of the article : universal_product_code
* Title : title
* Price including tax : price_including_tax
* Price excluding tax :price_excluding_tax
* Quantity available : number_available
* Description of the product : product_description
* Category : category
* Evaluation of the product : review_rating
* Url of the picture : image_url

# To go further :
- [x] Eraser : Propose to the user to erase datas if they might be corrupted
- [ ] Verification : if datas already exist in the file .csv
- [ ] Edit the path where files are written
- [ ] Function that give the Price according to the UPC
- [ ] Function update, which not erase datas that already exist on the .csv
- [ ] Optimization : Asyncio

## Install
Before using the program, you must set up your environment.
### 1. Clone
You have to clone this project on your computer. To do that, use Git Bash.<br/>
Type : `git clone https://github.com/Emericdefay/OCR_P2.1.git` from a folder path with Git Bash.<br/>
### 2. Virtual Environment
Activate your virtual env. at the root of the project. I use personaly virtualenv.<br/>
Type : `virtualenv env` at the root, from a terminal.<br/>
To activate it, type : `source env/scripts/activate`.
### 3. Libraries
Some libraries are a requisite to use this program: bs4, requests, lxml.<br/>
Type : `pip install -r requirements.txt`.

## Usage
You are now able to use the scraper.<br/>
To do so, stay on your terminal.<br/>
Type : `python -u ScrapBookin.py`.<br/>
-u is useful if you want to see the progression.

## Good to know
This programm create and structure the datas in two folders:
- /datas : Contains the .csv files. Each one represant one category.
- /pictures : Contains the .jpg files. Those .jpg are organized in folders named as categories.<br/>

Warning : <br/>
Currently, if you use this program more than one time. The .csv files will be corrupted.<br/>
Please, Cut and paste /datas & /pictures in another folder before another scrap.



