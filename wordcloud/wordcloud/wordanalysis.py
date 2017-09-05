import argparse
import json

from nltk import FreqDist, ngrams, PorterStemmer

MAX_COMMON_RESULTS = 50

irrelevant_words = [
    "and", "or", "follow", "the", "of", "a", "i", "view", "sign", "from" , "registration", "in", "how", "to", "on"
    "that", "he"
]

irrelevant_bigrams = [
    "subscribe now",
]

irrelevant_trigrams = [
    "like this page",
]

def process(args, text):
    wordlist = list(map(lambda s: s.lower(), text.split()))
    
    wordlist = [w for w in wordlist if w not in irrelevant_words]
    
    # Apply a stemmer?
    if args.use_stemmer:
        porter = PorterStemmer()
        wordlist = [porter.stem(w) for w in wordlist]

    result = None
    if args.mode == 1:
        fdist = FreqDist(wordlist)
        result = fdist.most_common(MAX_COMMON_RESULTS)
    elif args.mode == 0:
        ngrams_words = ngrams(wordlist, 2)
        fdist = FreqDist(ngrams_words)
        result = fdist.most_common(MAX_COMMON_RESULTS)
    return result

def main():
    # Configure arguments
    parser = argparse.ArgumentParser(description='Produces statistical information about word counts, frequency, and diversity in sections of text.')
    parser.add_argument("-us", "--use_stemmer", help="Use a stemmer",action="store_true")
    parser.add_argument("mode", type = int, help="Stats to return: one of 0 = freqdist or 1 = ngrams", choices=[0,1])
    parser.add_argument("-uj", "--use_json", help="Using Json",action="store_true")
    parser.add_argument("-cc", "--concatenate", help="Concatenate texts before analysis?",action="store_true")
    parser.add_argument("filename", help="File containing either text or Json with html element to process")
    args = parser.parse_args()

    with open(args.filename, 'r') as inputfile:
        texts = ''
        if args.use_json:
            lines = inputfile.readlines()
            for line in lines:
                jsonObj = json.loads(line)
                text = jsonObj.get("html")
                if not args.concatenate:
                    title = jsonObj.get("title")
                    print("\nJson document:" + str(title) + "\n" + str(process(args, text)))
                else:
                    texts += text
            if args.concatenate:
                print("\nAll Json concatenated:\n" + str(process(args, texts)))
        else:
            text = inputfile.read()
            print(process(args, text))

if __name__ == '__main__':
    main()
