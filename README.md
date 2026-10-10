# musicbrainz-album-rating
Python album rating application that integrates the MusicBrainz API to search for album information and allow users to rate and view albums

## Issues

1. the function album_rating() is being called twice in the program therefore user is asked if they would like to rate an album back to back. 
Solution:
Commented out the function call so that the user is only prompted once to rate an album.

2. when I was importing the search_album() function into my test file, the original album rating program started running instead of just the search function. 
Solution:
So I added if __name__ == "__main__": condition so that only that main only runs when albumRating.py is executed directly.

3. While testing the API, I received a KeyError because I tried to access the artist using album["artist"], which was the wrong field name to retrieve the artist's name. 
Solution:
I had to change it to album["artist-credit"][0]["name"] and use first-release-date for the release date.

