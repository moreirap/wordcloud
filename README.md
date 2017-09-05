## Useful commands

# Performs a google search
clear && scrapy crawl googlesearch -a query="bill gates microsoft" -o results.jl -L ERROR
clear && scrapy crawl googlesearch -a query="tomer shiran dremio" -o results.jl -L ERROR

# Runs a console on scrapy container
docker run -it --rm -v //c/Dev/prosapienttest://code -w //code prosapienttest_dev //bin/sh

# Tests sanitizeHTML on a given url
clear && python wordcloud/sanitizeHtml.py https://mapr.com/blog/author/tomer-shiran/ > result.html

# Connect to Redis
docker-compose.exe exec redis //bin/bash

