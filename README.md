# Fetch Youtube Data

It searches asynchronously every 10 sec in the backgroud using Python asyncio and threading library.

Default search query: "football"


## Table of Contents

-   [Starting Server Locally](#startingserverlocally)
-   [Features](#features)
-   [Tools Used](#toolsused)


## Starting Server Locally
```bash

git clone https://github.com/iashtripathy/Youtube-Search-Api.git

cd Youtube-Search-Api

pip3 install -r requirements.txt

open the .env file and update api keys

flask run 




## Features
1. Shuffles through the provided API Key set every time it searches.
2. Sort Option is provided. In order to sort by PublishAt go to the dashboard and click on the PublishedAt Heading Column. This will sort in Asc and Desc order both
3. The data fetched from YT are latest.
4. Pagination is added.
5. Global Seach on any keyword is added in the dashboard.
6. A dropdown field inorder to give the users an option to select no. of entries to display in every page 



## Tools Used
1) Flask
2) Pymongo
4) HTML, CSS & JQuery, Bootstrap
5) os, random, datetime, requests, asyncio








