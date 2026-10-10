from albumRating import search_album

results = search_album("Octane", "Don Toliver")  # Example album title and artist name

for album in results[:5]:  # Display the first 5 results
    print("Title: ",album["title"])
    print("Artist: ", album["artist-credit"][0]["name"])
    print("Release Date: ", album.get("first-release-date", "N/A"))


