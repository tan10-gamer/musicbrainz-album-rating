import requests

# Search for an album using the MusicBrainz API
def search_album(album_title, artist_name):
    url = "https://musicbrainz.org/ws/2/release-group/"             # MusicBrainz API endpoint for release groups
    headers = {
        "User-Agent": "AlbumRatingApp/1.0 (tanchirenda10@gmail.com)"        # User-Agent header to identify the application making the request
    }

    params = {
        "query":f'releasegroup:"{album_title}" AND artist:"{artist_name}"', "fmt":"json"        # Query parameters for the API request, including the album title and artist name, and specifying the response format as JSON
    }

    # Try-except block to handle potential errors during the API request
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()  # Raise an exception for HTTP errors
        data = response.json()
        return data.get("release-groups", [])

    except requests.exceptions.RequestException as error:
        print(f"Error occurred while searching for the album: {error}")
        return []

# Function to display the search results in a user-friendly format
def display_search(search):
    if not search:
        print("No albums found.")
        return

    print("\nSearch Results:")

    for index, album in enumerate(search[:5], start=1):
        title = album.get("title", "N/A")
        artist_credit = album.get("artist-credit", [])
        artist_name = artist_credit[0].get("name", "N/A") if artist_credit else "N/A"
        release_date = album.get("first-release-date", "N/A")

        print(f"{index}. Title: {title} | Artist: {artist_name} | Release Date: {release_date}")


    
# get_valid_rating function to ensure the user inputs a valid rating between 1 and 10
def get_valid_rating():
    while True:
        try:
            rating = int(input("Enter your rating for the album (1-10):"))
            if 1 <= rating <=10:
                return rating
            else:
                print("Invalid rating. Please enter a rating between 1 and 10.")
        except ValueError:
            print("Please enter a number.")          # handles user's input


# recommend_album function to provide a recommendation based on the rating
def recommend_album(rating):
    if rating >= 8:
        print("Good! Would recommend this album.")
        return True
    elif rating >= 5:
        print("Fair. Might recommend this album.")
        return False
    else:
        print("Bad. Would not recommend this album.")
        return False

# album_rating function to get album title, artist name, and rating from the user and provide a summary and recommendation summary    
def album_rating():
    album_title = input("Enter the album title: ")
    artist_name = input("Enter the artist name: ")

    genre_choice = input("Choose a genre:\n"
    "1. Rock\n"
    "2. Pop\n"
    "3. Hip-Hop\n"
    "4. Country\n"
    "5. EDM\n"
    "6. Rap\n"
    "7. Other\n"

    "Choice: "
)

    # match/case 
    match genre_choice:
        case "1":
            genre = "Rock"
        case "2":
            genre = "Pop"
        case "3":
            genre = "Hip-Hop"
        case "4":
            genre = "Country"
        case "5":
            genre = "EDM"
        case "6":
            genre = "Rap"
        case "7":
            genre = "Other"
        case _:
            genre = "Unknown"

    print("You chose a", genre, "album!")
      

    # condition to check that rating stays between 1 and 10
    rating = get_valid_rating()

    print("\n----Album Summary----")
    print("Album Title: ", album_title)
    print("Artist Name: ", artist_name)
    print("Genre: ", genre)
    print("Rating: ", rating)

    print("\n----Recommendation----")
    recommend = recommend_album(rating)         # recommendation returns True or False based on the rating

    # decision statement to recommend more albums by the artist based on user input
    if recommend:
        print("You might also like other albums by this artist.")
    else:
        print("You might not like other albums by this artist.")

    return album_title

# album_rating()   # calls the album_rating function to start the program



# main program. Loop to ask the user if they want to rate another album or exit the program
if __name__ == "__main__":   # condition used to only run the following code if the script is executed directly.
    print("Welcome to the Album Rating Program!")
    albums = []
    album = album_rating()
    albums.append(album)

    while True:
        next_album = input("\nWould you like to rate another album? (yes/no): ")
        if next_album == "yes":
                album_rating()
        elif next_album == "no":
            print("Thank you for using the album rating program!")
            break
        else:
            print("Invalid input. Please enter 'yes' or 'no'.")