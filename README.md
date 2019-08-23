## Wordsworth: Word Frequency Ranker

https://ankiweb.net/shared/info/696663192

<img src="https://github.com/lovac42/Wordsworth/blob/master/screenshots/title.png?raw=true">  

## About:
The idea is to rank these words from most frequent to least. Depending on your needs, you would study the most frequent one's first, or separate them into multiple decks and use large interval modifiers to skim over the easy ones. In addition, it can be used to seed MorphMan.

This addon is intended to work with any language and you will need to supply your own list which can be found on the internet in various formats. No actual wordlist is included, a sample list of 500 english words are included in the ```user_files``` folder for testing.


## Technical:
Warning: list is loaded into ram first, 10mb file is about 300mb in ram.  

## Screenshots:

<img src="https://github.com/lovac42/Wordsworth/blob/master/screenshots/menuitem.png?raw=true">  
<img src="https://github.com/lovac42/Wordsworth/blob/master/screenshots/wordsworth.png?raw=true">  
<img src="https://github.com/lovac42/Wordsworth/blob/master/screenshots/result.png?raw=true">  
<img src="https://github.com/lovac42/Wordsworth/blob/master/screenshots/result2.png?raw=true">  


## Word lists:

<img src="https://github.com/lovac42/Wordsworth/blob/master/screenshots/format.png?raw=true">  

### Line Count Word List (English):
File extension must end with ```.line```  
Format: ```{word}``` This is ranked by line number.  


Google - 10K words:  
https://github.com/first20hours/google-10000-english  
Unfortunately, this list seems to have alot of issues.  
Rename your download from ```.txt``` to ```.line```  


Words from nursing journals - 1K words:  
https://www.ncbi.nlm.nih.gov/pmc/articles/PMC6298166/  
This list is in .tif, so you need an OCR program to translate it to text first.


### Frequency Count Word List (English):
File extension must end with ```.txt```  
Format: ```{word}{space or tab}{frequency count}```  


Vocabulary for students of English - 15K words:  
http://www.audiencedialogue.net/susteng.html  
You will need to remove a few of the lines to comply with the word-space-frequency format here.

Word list from movie subtitles - 50K words:  
https://github.com/hermitdave/FrequencyWords/tree/master/content/2016/en  
This word list has 50k words, mostly from english subtitled movies. It might be good for ESL students, but highly inaccurate for advanced english.

