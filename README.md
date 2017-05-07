# playlist
Given text input of song names, it will create a playlist in Spotify based on those songs.
Depends on NTLK, JSON, and REQUESTS libraries.

The main method utilizes a greedy algorithm that matches ngrams (n = 5 max) to query the Spotify song titles corpora.
Once matched, it proceeds to print out the matched song result. The matched ngram is taken out from the cleaned tokens, and the process is repeated recursively with a decreasing n. If no match is found, an error is printed out.
