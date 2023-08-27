# Celaigia

Celaigia is a simple desktop application to search and download audio tracks from YouTube based on user input queries. It uses yt_dlp for searching and downloading operations, and saves download logs into a MySQL database.

## Prerequisites

    Python 3.x
    MySQL

## Setup
1. Clone the repository:
    ```bash
    git clone <repository_url> celaigia
    cd celaigia
    ```
2. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

3. Setup the Database:
First, ensure your MySQL service is running.

Execute the provided setup script:
    ```bash
    chmod +x setup_database.sh
    ./setup_database.sh
    ```
You will be prompted to enter the following details:
    MySQL database name (default is celagia if you hit enter without input).
    MySQL username.
    MySQL password.

The script will then:

    Save these details as environment variables.
    Create a new database (if it doesn't exist).
    Create a new table download_logs for logging the downloaded tracks.

4. Run the application:
Now, you can run the application using:
    ```bash
    python celaigia/app.py
    ```

## Usage
    ```
    Input your search query into the "Enter search query" field.
    Set the number of search results you'd like to see.
    Define the output folder for the downloaded tracks.
    Hit the "Search" button to get a list of matches.
    Select a track from the list.
    Click on "Download Selected" to download the audio track.
    ```

## Make Desktop Entry
create a desktop entry file:
    ```bash
    vim ~/.local/share/applications/celaigia.desktop
    ```
and add the following to it:
    ```bash
    [Desktop Entry]
    Name=Celaigia
    Comment=Search and download audio tracks from YouTube
    Exec=python3 /path/to/celaigia/app.py
    Icon=/path/to/celaigia/icon.png
    Terminal=false
    Type=Application
    Categories=Audio;Multimedia;
    ```
Replace /path/to/celaigia/ with the full path to your celaigia directory.
Replace /path/to/celaigia/icon.png with the path to the app's icon if you have one. Otherwise, you can remove the Icon line.

lastly make the file executable:
    ```bash
    chmod +x ~/.local/share/applications/celaigia.desktop
    ```

## Terminal access
make celaigia/app.py executable:
    ```bash
    chmod +x celaigia/app.py
    ```
symbolic link to the app.py file:
    ```bash
    sudo ln -s /path/to/celaigia/app.py /usr/local/bin/celaigia
    ```

After doing this, you should be able to run celaigia directly from the terminal.



    