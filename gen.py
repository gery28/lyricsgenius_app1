import os
import random
import lyricsgenius

# CLIENT ACCESS TOKEN stored in environment variable
genius = lyricsgenius.Genius(os.getenv("CLIENT_ACCESS"), verbose=False)



def get_albums(artist):
    result = genius.search_artists(search_term=artist)
    album = genius.artist_albums(artist_id=result["sections"][0]["hits"][0]["result"]["id"])
    return album


def choose_albums(album):
    for i in range(len(album["albums"])):
        print(str(i + 1) + ".", album["albums"][i]["name"])
    while True:
        choice = int(input("choose album: "))
        if choice > len(album["albums"]) or choice <= 0:
            print("album number does not exists")
        else:
            break
    return choice


def get_lyrics(album, artist):
    tracks = genius.album_tracks(album_id=album["albums"][choose_albums(album) - 1]["id"])
    lyrics = genius.search_song(title=random.choice(tracks["tracks"])["song"]["title"], artist=artist,
                                get_full_info=False)
    return lyrics


def main():
    artist = input("give artist name: ")
    album = get_albums(artist)
    lyrics = get_lyrics(album, artist)
    if lyrics is None:
        print("this song has no lyrics")
    else:
        print("\n", lyrics.to_dict()["lyrics"].split("Lyrics")[1].strip("Embed"))
        while True:
            answer = input("name of this song(press ENTER ot type 0 to get answer): ")
            if answer.lower() == lyrics.to_dict()["title"].lower():
                print("\nCorrect the answer was:", lyrics.to_dict()["title"])
                break
            if answer == "" or answer == "0":
                print("\nThe ansver was:", lyrics.to_dict()["title"])
                break


main()
