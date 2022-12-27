import spotipy
import spotipy.util as util

client_id = "CLIENT_ID"
client_secret = "CLIENT_ID_SECRET"
redirect_uri = "CLIENT_REDIRECT"

username = "CLIENT_USER"
scope = "user-library-read"

token = util.prompt_for_user_token(username, scope, client_id, client_secret, redirect_uri)

sp = spotipy.Spotify(auth=token)

while True:
    song_name = input("Enter the name of a song (Type 'exit' to quit): ")
    if song_name.lower() == "exit":
        break

    results = sp.search(q=song_name, type="track")

    song_id = results["tracks"]["items"][0]["id"]

    recommendations = sp.recommendations(seed_tracks=[song_id])
    recommendation_list = recommendations["tracks"]
    recommendation_list = recommendation_list[:20]
    recommendations["tracks"] = recommendation_list

    popularity = [recommendation["popularity"] for recommendation in recommendations["tracks"]]

    recommendations["tracks"] = [rec for rec in recommendations["tracks"] if "is_playable" not in rec or rec["is_playable"]]
    recommendations["tracks"] = [x for _, x in
                                 sorted(zip(popularity, recommendations["tracks"]), key=lambda pair: pair[0], reverse=True)]
    num = 1

    track = sp.track(song_id)
    sample_name = track["name"]
    sample_artist = track["artists"][0]["name"]

    print("")
    print(f"Searching for songs like: {sample_name} by {sample_artist}")
    print("")

    for recommendation in recommendations["tracks"]:
        song_name = recommendation["name"]
        artist = recommendation["artists"][0]["name"]
        popularity = recommendation["popularity"]

        feature = ""
        if len(recommendation["artists"]) > 1:
            feature_artist_names = [artist["name"] for artist in recommendation["artists"][1:]]
            feature = " (ft " + ", ".join(feature_artist_names) + ")"
            if any(name in song_name for name in feature_artist_names):
                feature = ""

        url = recommendation["external_urls"]["spotify"]
        length = recommendation["duration_ms"] / 1000
        minutes, seconds = divmod(length, 60)
        length_str = f"{int(minutes)}:{int(seconds):02d}"
        print(f"{num}.) {song_name} - {artist}{feature} ({length_str}): {url} - Popularity: {popularity}")
        num = num + 1
        print("")

    print('-' * 400)
    print("")
