import requests
import json 
import time

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
    for attempt in range(3):  # Retry the request up to 3 times
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 503:  # Handle temporary unavailability (HTTP 503)
                if attempt < 2:  # Only print the retry message for the first two attempts
                    print("MusicBrainz temporarily unavailable. Retrying in 5 seconds...")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                    continue
                return None
            
            response.raise_for_status()  # Raise an exception for HTTP errors
            data = response.json()
            return data.get("release-groups", [])

        except requests.exceptions.RequestException as error:
            print(f"MusicBrainz API request failed: {error}")
            return None
    print("MusicBrainz still unavailable. Please try again later.")
    return None

# retrieve detailed information about a selected album
def get_album_details(album_id):
    url = f"https://musicbrainz.org/ws/2/release-group/{album_id}"  # MusicBrainz API endpoint for a specific release group
    headers = {
        "User-Agent": "AlbumRatingApp/1.0 (tanchirenda10@gmail.com)"
    }

    params = {
        "inc": "artist-credits+genres+tags", "fmt": "json"
    }   # Include additional information such as artist credits, genres, and tags in the response

    for attempt in range(3):  # Retry the request up to 3 times
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)

            if response.status_code == 503:  # Handle temporary unavailability (HTTP 503)
                if attempt < 2:  # Only print the retry message for the first two attempts
                    print("MusicBrainz temporarily unavailable. Retrying in 5 seconds...")
                    time.sleep(5)  # Wait for 5 seconds before retrying
                    continue
                return None

            response.raise_for_status()  # Raise an exception for HTTP errors
            return response.json()

        except requests.exceptions.RequestException as error:
            print(f"MusicBrainz API request failed: {error}")
            return None
    print("MusicBrainz still unavailable. Please try again later.")
    return None



# Function to display the search results in a user-friendly format
def display_search(search):
    if not search:
        print("No albums found.")
        return

    print("\n-----Search Results-----")

    for index, album in enumerate(search[:5], start=1):
        title = album.get("title", "N/A")
        artist_credit = album.get("artist-credit", [])
        artist_name = artist_credit[0].get("name", "N/A") if artist_credit else "N/A"
        release_date = album.get("first-release-date", "N/A")

        print(f"{index}. Title: {title} | Artist: {artist_name} | Release Date: {release_date}")

# allow the user to search for an album

def search_for_album():
    album_title = input("Enter the album title: ")
    artist_name = input("Enter the artist name: ")
    results = search_album(album_title, artist_name)

    if results is None:
        print("An error occurred while searching for the album.")
        return
    
    display_search(results)

    selected_album = select_album(results)  # Call the select_album function to allow the user to select an album from the search results
    if selected_album:
        print("Title:", selected_album.get("title", "N/A"))
        print("MusicBrainz ID:", selected_album.get("id", "N/A"))

        # retrieves additional details for the selected album using album's MusicBrainz ID
        time.sleep(1.1)
        album_details = get_album_details(selected_album.get("id"))

        if album_details:
            print("\n-----Album Details-----")
            print("Type: ", album_details.get("primary-type", "N/A"))
            print("First Release Date: ", album_details.get("first-release-date", "N/A"))

            genres = album_details.get("genres", [])
            print("\nGenres: ")
            if genres:
                for genre in genres[:5]:
                    print("-", genre.get("name", "N/A"))
            else:
                print("No genres found.")

            tags = album_details.get("tags", [])
            print("\nTags: ")
            if tags:
                for tag in tags[:5]:
                    print("-", tag.get("name", "N/A"))
            else:
                print("No tags found.")

        # allow the user to rate the selected album
        print("------------------------------")
        print("\nRate the selected album:")
        rating = get_valid_rating()
        time.sleep(1)  # Add a delay of 1 seconds before displaying the rating summary


        # display the rating summary
        print("\n-----Rating Summary-----")
        print("Album: ", selected_album.get("title", "N/A"))
        print("Rating:", rating, "/10")

        print("\nGenerating recommendation...")
        time.sleep(1)  # Add a delay of 1 seconds before providing the recommendation
        recommend_album(rating)             # provide a recommendation based on the rating
        
        print("----------------------------------")  # Print a separator line for better readability
        
        # store the album rating in a JSON file
        artist = selected_album.get("artist-credit", [])
        artist_name = artist[0].get("name", "N/A") if artist else "N/A"

        rated_album = {
            "id": selected_album.get("id", "N/A"),
            "title": selected_album.get("title", "N/A"),
            "artist": artist_name,
            "rating": rating
        }

        save_album_rating(rated_album)
        print("\nAlbum rating saved to album_ratings.json.")


# allow the user to select an album 
def select_album(search):
    if not search:
        return None

    while True:
        try:
            choice = int(input(f"Select an album (1-{min(len(search), 5)}): "))
            if 1 <= choice <= min(len(search), 5):
                select_album = search[choice - 1]
                return select_album
            else:
                print(f"Invalid choice. Please select a number between 1 and {min(len(search), 5)}.")

        except ValueError:
            print("Invalid input. Please enter a number.")

# functions to load and save album ratings to a JSON file
def load_album_ratings():
    try:
        with open("album_ratings.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []
    
def save_album_rating(album):
    albums = load_album_ratings()
    albums.append(album)

    with open("album_ratings.json", "w") as file:
        json.dump(albums, file, indent=4)

# display rated albums from the JSON file
def display_rated_albums():
    albums = load_album_ratings()

    if not albums:
        print("No rated albums found.")
        return

    print("\n----Rated Albums----")
    for index, album in enumerate(albums, start=1):
        print(f"{index}. {album.get('title', 'N/A')}")
        print("Artist:", album.get("artist", "N/A"))
        print("Rating:", album.get("rating", "N/A"), "/10")
        print()

#display the top-rated albums from the JSON file
def display_top_albums():
    albums = load_album_ratings()

    if not albums:
        print("No rated albums found.")
        return

    # Sort albums by rating in descending order
    top_albums = sorted(albums, key=lambda album: album["rating"], reverse=True)

    print("\nTop Rated Albums:")
    for index, album in enumerate(top_albums, start=1):
        print(f"{index}. {album.get('title', 'N/A')}")
        print("Artist:", album.get("artist", "N/A"))
        print("Rating:", album.get("rating", "N/A"), "/10")
    
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
    elif rating >= 5:
        print("Fair. Might recommend this album.")
    else:
        print("Bad. Would not recommend this album.")


# main menu 
def main_menu():
    while True:
        print("\n MusicBrainz Album Rating Program")
        print("----------------------------------")
        print("1. Search for an album")
        print("2. View rated albums")
        print("3. View Top Albums")
        print("4. Exit")
        print("----------------------------------")


        choice = input("\nEnter your choice (1-4): ")

        match choice:
            case "1":
                search_for_album()
            case "2":
                display_rated_albums()
            case "3":
                display_top_albums()
            case "4":
                print("Thank you for using the MusicBrainz Album Rating Program!")
                break
            case _:
                print("Invalid choice. Please enter a number between 1 and 4.")

if __name__ == "__main__":
    main_menu()  # Start the main menu when the script is executed directly



# --------------------- OLD ABLUM RATING LOGIC ----------------------------------------------------------------

# def album_rating():
#     album_title = input("Enter the album title: ")
#     artist_name = input("Enter the artist name: ")

#     genre_choice = input("Choose a genre:\n"
#     "1. Rock\n"
#     "2. Pop\n"
#     "3. Hip-Hop\n"
#     "4. Country\n"
#     "5. EDM\n"
#     "6. Rap\n"
#     "7. Other\n"

#     "Choice: "
# )

#     # match/case 
#     match genre_choice:
#         case "1":
#             genre = "Rock"
#         case "2":
#             genre = "Pop"
#         case "3":
#             genre = "Hip-Hop"
#         case "4":
#             genre = "Country"
#         case "5":
#             genre = "EDM"
#         case "6":
#             genre = "Rap"
#         case "7":
#             genre = "Other"
#         case _:
#             genre = "Unknown"

#     print("You chose a", genre, "album!")
      

#     # condition to check that rating stays between 1 and 10
#     rating = get_valid_rating()

#     print("\n----Album Summary----")
#     print("Album Title: ", album_title)
#     print("Artist Name: ", artist_name)
#     print("Genre: ", genre)
#     print("Rating: ", rating)

#     print("\n----Recommendation----")
#     recommend = recommend_album(rating)         # recommendation returns True or False based on the rating

#     # decision statement to recommend more albums by the artist based on user input
#     if recommend:
#         print("You might also like other albums by this artist.")
#     else:
#         print("You might not like other albums by this artist.")

#     return album_title

# album_rating()   # calls the album_rating function to start the program

# main program. Loop to ask the user if they want to rate another album or exit the program
# if __name__ == "__main__":   # condition used to only run the following code if the script is executed directly.
#     print("Welcome to the Album Rating Program!")
#     albums = []
#     album = album_rating()
#     albums.append(album)

#     while True:
#         next_album = input("\nWould you like to rate another album? (yes/no): ")
#         if next_album == "yes":
#                 album_rating()
#         elif next_album == "no":
#             print("Thank you for using the album rating program!")
#             break
#         else:
#             print("Invalid input. Please enter 'yes' or 'no'.")