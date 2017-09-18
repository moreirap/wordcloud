## Useful commands

# Performs a google search
scrapy crawl googlesearch -a query="bill gates microsoft" -o results.jl -L ERROR

# Runs a console on scrapy container
docker run -it --rm -v //c/Dev/prosapienttest://code -w //code prosapienttest_dev //bin/sh

# Tests sanitizeHTML on a given url
python wordcloud/sanitizeHtml.py https://mapr.com/blog/author/tomer-shiran/ > result.html
