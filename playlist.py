#!/usr/bin/env python3
import nltk
import requests
import json

# NLTK part

# Tokenization and cleaning. Could have used the NLTK word_tokenize, but avoided it for
# it doesn't let the use of "'" which is very common on music songs (i.e. doesn't, that's)
def tokenator(text):
    clean_tokens =[]
    punctuation = [",", ":", ";", ".", '"', "’", "?", "/", "-", "+", "&", "(", ")"] #"'" has been excluded
    tokens = text.split(' ') 
    for token in tokens:
        token = token.lower()
        for punc in punctuation:
            token = token.replace(punc,"")
        if len(token):
            clean_tokens.append(token)
    return clean_tokens

# Makes sure that the API request has the name on the track title. 1 if good, None no good
def score(name, r_json):
    scoring = [1 for i in r_json['tracks']['items'] if (name in i['name'].lower())]
    return sum(scoring)

# Makes the API call and returns the name used, the score (1 if good, None no good),
# and the request in JSON format
def call_score(name):
    qvalue = '"%s"' %(name)
    parameters = {'q': qvalue,'type': 'track', 'market': 'US', 'limit': 1}
    r = requests.get('https://api.spotify.com/v1/search', params = parameters)
    return name, score(name, r.json()), r.json()

# Receives an ngram and n, joins the ngram into a proper word, and makes the API call.
# Returns the same as call_score (if successful, of course. Otherwise None)
# Something to note is that it's a type of greedy algorithm. It will STOP at the FIRST ngram that matches.
def ngram_scoring(ngram, n):
    joined_ngram = []
    if n == 1:
        joined_ngram = ngram
    else:
        joined_ngram = [' '.join(i) for i in ngram]
    for j in joined_ngram:
        name_score = call_score(j)
        if name_score[1] == 1:
            return name_score
    return

# Receives the a list of tokens and compares it to a validated ngram.
# After comparing it returns the left side and the right side of the ngram
# (i.e. left + validated ngram + right)
def remove_ngram(clean_tokens, validated_ngrams):
    if len(validated_ngrams) ==1:
        validated_tokens = validated_ngrams
    else:
        validated_tokens = validated_ngrams.split(' ')
        left_index = clean_tokens.index(validated_tokens[0])
        right_index = clean_tokens.index(validated_tokens[len(validated_tokens)-1])
        left = clean_tokens[:left_index]
        right = clean_tokens[right_index+1:]
    return left, right

# The main method. It receives cleaned tokens list and the initial n for creating n grams.
# Depending of the size of the cleaned tokens list AND n (that is ever decreasing), it makes the API calls,
# prints out the results, handles non-existent words, and recursively calls itself on the left side and the
# right side of the cleaned tokens that have matched until the end!
# I have arbitrarily chosen the initial n=5, since statiscally anything above five-grams are extremely rare.
def create_playlist(cleaned_tokens, n):
    if len(cleaned_tokens) == 1:
        song = ngram_scoring(cleaned_tokens, 1)
        if song:
            track = song[2]['tracks']['items'][0]['name'] #Song Name
            artist = song[2]['tracks']['items'][0]['artists'][0]['name'] #Artist Name
            link = song[2]['tracks']['items'][0]['external_urls']['spotify'] #Track on Spotify
            print("%s=> %s by %s: %s" %(song[0],track,artist,link))
        else:
            print('We could not find this word "%s"' %(cleaned_tokens[0]))
        return
    else:
        if n==1:
            token_ngrams = cleaned_tokens
        else:
            token_ngrams = list(nltk.ngrams(cleaned_tokens, n))
        song = ngram_scoring(token_ngrams, n)
        if song:
            track = song[2]['tracks']['items'][0]['name'] #Song Name
            artist = song[2]['tracks']['items'][0]['artists'][0]['name'] #Artist Name
            link = song[2]['tracks']['items'][0]['external_urls']['spotify'] #Track on Spotify
            print("%s=> %s by %s: %s" %(song[0],track,artist,link))
            left, right = remove_ngram(cleaned_tokens, song[0])
            if len(left):
                create_playlist(left, len(left))
            if len(right):
                create_playlist(right, len(right))
            return
        elif n>1:
            create_playlist(cleaned_tokens, n-1)
            return
        else:
            print('We could not find these words: %s' %(cleaned_tokens))
        return

# Requests input
text=input('Enter your input: ')
clean_tokens = tokenator(text)

print(text)
create_playlist(clean_tokens, 5)