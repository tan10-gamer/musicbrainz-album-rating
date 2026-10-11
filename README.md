# musicbrainz-album-rating
Python album rating application that integrates the MusicBrainz API to search for albums, retrieve information, and allow users to rate, store and view albums.

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

4. While testing one of the search features, I encountered a 503 Server Error. Which prevented the program from retrieving album information.
Solution:
Updated the error handling messages to output the appropriate error message.

5. During testing, I intentionally typed in albums that did not exist. And the ouput message was correct, "No Album found". However, I had print statements in my display_search function and select_album function that both returned "No Album found". So the user would receive a duplicated output message.
Solution:
Removed the print statement from select_album to just return an empty list is no album was found from the display_search function.

6. Originally in my plan I wanted to use the display additionally information endpoint to show artist name, and album title. However, I discovered that was redundant and I was already duplicating information from my display_search function.
Solution:
Changed my plan a bit to show information that would be relevant to the album rating program such as genres.

7. When trying to display genres and tags the program was returning an empty list. After looking at the MusicBrainz documentation I misinterpreted the API paramater and used "include" instead if "inc". 
Solution:
Used correct request parameter.

8. During testing I occasionally ran into a HTTP 503 Error, which prevented the application from retrieving album information.
Solution:
I added error handling by added logic that would automatically retry whenever the server is temporarily unavailable. Also added a short delay between API requests to observe MusicBrainz's rate limit.

9. Issue with user visibility.
Solution:
Added separators and delays for the convenience of users.

10. A second json file was created when the application was executed from a different working directory.
Solution:
Ran program from terminal.


