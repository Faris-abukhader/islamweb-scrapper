<p align="center">
<img src="https://user-images.githubusercontent.com/70070951/214610785-955a62af-a5ec-4fba-b4f9-337383a48885.png" width="400" height="200">
</p>


<h1 align="center">IslamWeb scrapper</h1>
<p align="center">
📔<a href="https://github.com/Faris-abukhader/islamweb-scrapper/blob/main/README_ar.md">  بالعربي </a>📔 
 </p>


## 🚩 Table of Contents

- [Introduction](#--introduction)
- [Installation](#--installation)
- [Development setup](#--development-setup)
- [Packages](#-packages)
- [License](#-license)




## <img src="https://cdn-icons-png.flaticon.com/512/1436/1436664.png" width="25" height="25" style="padding-right:15px">  Introduction 

<p>
<b>Warning</b>: This project is only for study purpose , please don’t re-share these articles under your name , all these articles is only belongs to WebTeb . 
</br>
</br>
<h1>how to get 4k+ islamic articles and consults and  Q&A all in arabic  . . .  ?!</h1>


 ### if you want to get articles run this first 
 ``` 
asyncio.run(islamWeb.save_articles_link())
 ```
 then take the generated file name and pass it to this function
 </br>

 ```
asyncio.run(islamWeb.save_entities('articles','file_name_here'))
 ```


 ### if you want to get questions run this first 
 ```
asyncio.run(islamWeb.get_question_links())
 ```
 then take the generated file name and pass it to this function
 </br>
 ```
asyncio.run(islamWeb.save_entities('questions','file_name_here'))
```
</p>


 ### if you want to get consults run this first 
 ```
asyncio.run(islamWeb.save_consult_link())
 ```
 then take the generated file name and pass it to this function
 </br>
 ```
asyncio.run(islamWeb.save_entities('consults','file_name_here'))
```
</p>



## <img src="https://cdn-icons-png.flaticon.com/512/814/814848.png" width="25" height="25" style="padding-right:15px">  Installation 


### 🔘 Cloning repository
1. On GitHub.com, navigate to the main page of the repository.
2. Above the list of files, click  Code.
3. Copy the URL for the repository.
4. Open Terminal.
5. Change the current working directory to the location where you want the cloned directory.
6. Type git clone, and then paste the URL you copied earlier.
```
git clone github.com/Faris-abukhader/webteb-scrapper
```
Press Enter to create your local clone
```
git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
> Cloning into `webteb-scrapper`...
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.
```
<br/>


## <img src="https://cdn-icons-png.flaticon.com/512/814/814848.png" width="25" height="25" style="padding-right:15px">  Development setup

To set up this project you need to download Python in your machine or if you have it make sure you have the latest version of it.

### 🔘 Checking up Python version in mac
```
python3 -V
```
### 🔘 Checking up Python version in windows
```
python --version
```
### 🔘 Downloading Python

> for Windows  


Download the windows installer from [Python offical website](https://www.python.org/downloads/) make sure you have download the latest version of Python.
<br/>


> for Mac
- You can download Python using brew CLI
```
brew install python
```
- You can download Python mac version through [the offical website](https://www.python.org/downloads/)
<br/>
<hr/>


### 🔘 Downloading the packages

Go to project direct where  requirements.txt is exist and type in terminal :
```
pip install -r requirements.txt 
```

<br/>
<hr/>

## 📦 Packages

| Name | Description |
| --- | --- |
| [`BeautifulSoup`](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) | Beautiful Soup is a Python library for pulling data out of HTML and XML files. |
| [`selenium`](https://pypi.org/project/selenium/) |The selenium package is used to automate web browser interaction from Python. |
| [`aiohttp`](https://docs.aiohttp.org/en/stable/) |Asynchronous HTTP Client/Server for asyncio and Python. |
| [`asyncio`](https://docs.python.org/3/library/asyncio.html) |asyncio is a library to write concurrent code using the async/await syntax. |





## 📜 License

This software is licensed under the [MIT](https://github.com/Faris-abukhader/webteb-scrapper/blob/main/LICENSE) © [FaRiS](https://github.com/Faris-abukhader).
