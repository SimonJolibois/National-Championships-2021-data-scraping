# National-Championships-2021-data-scraping
## Context
The french National Swimming Championships were organised at Chartres from Tuesday, 15th June to Sunday, 20th June.
The results from the competition are collected by the FFN ("Federation Française de Natation") and shared on their website (https://www.liveffn.com/cgi-bin/index.php?competition=70185).

## Description
The .py script can be used to scrap results on the FFN website with BeautifulSoup.

## How to use
In the .py choose the path of the directory you want to stock the output files at (path variable)

First, you need to download the webpage from which you want to collect data (Right click -> Save as).
After that, point where the html file is in the .py (adress of page variable)

As you can see on the website, each race results are decomposed in multiple 'Finals' results and one 'Series' results. The script takes it into account and create a separate .csv file for each race.

The output is a collection of different .csv containing the on each line the time of one swimmer used to swim a swimming pool length(0m, 50m, 100m ....), but also an id, which is the ranking of the swimmer during the race, his or her name. An additionnal "lane" column is left empty as it is not stored on the FFN website.

## Current limitations
The script cannot handle medley races.
It also have trouble with "barrage" races that are meant to rank several swimmers who got the same timing in the series.
