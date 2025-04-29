# FinalProject-Music

idea influence: looking to possibly create a music app using python that helps users explore new songs and 
artists based on their preference using a music data api to track details for a final project

Final Presentation explaining the rest of the information: https://docs.google.com/presentation/d/1OQiLcGwHk2iexwyl7CmzQB6SnGkZ3FYH7twFElUC7kk/edit?usp=sharing

# Description
The **Music App** is a command-line Python application that allows users to explore music through the Spotify Web API. Users can:
- Search for their favorite artists
- View an artist's top tracks
- Analyze audio features such as danceability, energy, tempo, and valence
- Discover related artists based on Spotify’s recommendation engine
The goal of the app is to provide a tool for music enthusiasts, built with Spotify API integration and user-friendly functionality.

# Installation
{Prerequisites}
- Python Access
- A Spotify Developer account
- Your own Spotify API credentials (Client ID & Secret)
      - Can be done through Spotify api website

{Setup Instructions}
1. Clone the repository

2.
      ```bash
      git clone https://github.com/yourusername/music-discovery-app.git
      cd music-discovery-app

4. pip install spotipy

5. Include you own client id and client secret

6. Run the app

# System Architecture
This project is host on Github and Built using Visual Studio code on a Dell Inspiron 16 7630 2-in-1

# Component Design
create_spotify_client() --	Handles authentication and returns a Spotify client
search_track() -- Searches for tracks using a query string
get_recommendations()	-- Retrieves similar tracks based on a seed track
get_top_tracks()	-- Gets an artist’s top 5 tracks
get_audio_features()	-- Fetches audio features of a selected track
get_related_artists()	-- Finds artists related to a given artist
main()	-- Coordinates the user interaction and function calls

# Usage/Help
Throughout building this python project I have used Copilot Chat 4.0 to help with errors and documentation throughout my program.
This has allowed me to remove unnecessary code and focus on the goal of the program.
Each time I was faced with an error I could not directly fix myself, I used this to define the problem and simplify the error message
in order that I can solve the problem and eliminate random information. 
