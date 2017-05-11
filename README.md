# chanscraper
linguistic data scraper for 4chan, using basc-py4chan and nltk

in use by the iGen Project at Stanford University

## usage
run chanscrape.py to collect board info as specified by the list of boards on line 10

chanscrape will output three types of files: .hist files to store board metadata, raw .txt dumps of an entire board's posts, and .xml files of individual posts (currently formatted for use in the iGen Project)

run chancheck.py to examine .hist metadata of boards