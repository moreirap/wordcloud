# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup, Comment
import re
import htmlentitydefs
import urllib2
import string
import sys
import unicodedata

blacklist = ["script", "style"]

# remove these tags, complete with contents.
whitelist = [
     "div", "span", "p", "br", "pre", "a"
     "table", "tbody", "thead", "tr", "td",
     "blockquote",
     "ul", "li", "ol",
     "b", "em", "i", "strong", "u", "font",
]

uninterestingSections = dict([
    ('class', ['side-bar-list', 'navbar-header', 'footer']),
    ('id',['footer', 'navigation-mainbar', 'navbar-topbar']),
])


def removeKnownSections(html):
    if not html:
        return None
    try:
        # BeautifulSoup is catching out-of-order and unclosed tags, so markup
        # can't leak out of comments and break the rest of the page.
        soup = BeautifulSoup(html, "lxml")
    except:
        # special handling?
        raise

    # now strip HTML we don't like.
    for attr,attrvalue in uninterestingSections.iteritems():
        for tag in soup.findAll(attrs = {attr:attrvalue}):
            tag.replace_with('')

    return str(soup.body)

def plaintext(html):
    """Converts HTML to plaintext, preserving whitespace."""
    if not html:
        return None
    try:
        # BeautifulSoup is catching out-of-order and unclosed tags, so markup
        # can't leak out of comments and break the rest of the page.
        soup = BeautifulSoup(html, "lxml")
    except:
        # special handling?
        raise

    # now strip HTML we don't like.
    for tag in soup.findAll():
        # Remove all attributes
        tag.attrs = None
        if tag.name.lower() in blacklist:
            # blacklisted tags are removed in their entirety
            tag.extract()
        elif not (tag.name.lower() in whitelist):
            # not a whitelisted tag. I'd like to remove it from the tree
            # and replace it with its children. But that's hard. It's much
            # easier to just replace it with an empty span tag.
            tag.name = "span"
            tag.attrs = []

    # scripts can be executed from comments in some cases
    comments = soup.findAll(text=lambda text: isinstance(text, Comment))
    for comment in comments:
        comment.extract()

    safe_html = str(soup)

    safe_html = "".join(BeautifulSoup("<body>%s</body>" % safe_html, 'lxml').body(text=True))
    return safe_html

def cleanInput(input):
    input = re.sub('\n+|\t+', " ", input)
    input = re.sub('\[[0-9]*\]', " ", input)
    input = re.sub('https?\:\/\/.+ '," ", input)
    input = re.sub(' +', " ", input)
    input = bytearray(input, 'utf-8')
    input = input.decode("ascii", "ignore")
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

# Run this file as a scrypt
def main():
    # print command line arguments
    if len(sys.argv) != 2 :
        print("Usage: python sanitizeHtml <url>")
        return
    url = sys.argv[1]
    html = urllib2.urlopen(url)
    result = removeKnownSections(html)
    #plainText = plaintext(html)
    #result = ' '.join(cleanInput(plainText))
    print(result)

if __name__ == '__main__':
    main()

