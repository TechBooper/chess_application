# Chess Application

This chess application is an MVC application that allows users to create chess tournaments, enroll players, and manage tournament progress including rounds, player standings, and match results.

## Getting Started

These instructions will get you a copy of the project up and get it running on your machine.

### Prerequisites

Before you can run the program, you need to install Python:

# Clone the repository to your local machine
git clone https://github.com/TechBooper/chess-application.git

# Navigate to the project directory
cd chess-application

# Install required Python packages
pip install -r requirements.txt

# Running the Program
To run the Chess-application, execute the following command from the root of the project directory:
python main.py

Follow the on-screen prompts to navigate through the application menu for various operations like adding players, creating tournaments, and viewing standings.

Usage
After starting the application, you will be presented with the following options in the main menu. Here is a brief explanation of each:

Main Menu Options

1 - Add Player
Prompts you to enter player information (name, chess ID...). This option registers a new player into the system.

2 - Create Tournament
Allows you to create a new tournament by specifying details like name, location, start and end dates, and the total number of rounds.

3 - View Tournament Players
Shows a list of all players registered in a specific tournament. You will be prompted to enter the tournament name.

4 - Add Player to Tournament
Adds an existing player to a specific tournament. You'll need to provide the tournament name and player's chess ID.

5 - Start Tournament
Initiates the rounds of a specified tournament. This option is used to begin the rounds after setting up a tournament.

6 - Input Match Results
Enter the results of individual matches by providing scores or indicating a draw. This updates the tournament standings based on match outcomes.

7 - View Current Standings
Shows the current standings or rankings of players within a specified tournament, based on their performance.

8 - View All Players
Lists all players registered in the system, sorted by their names or chess IDs.

9 - Advance to Next Round
Moves a tournament forward to the next round, once all matches in the current round are completed.

10 - View All Tournaments
Lists all the tournaments that have been created in the system, including all their info.

11 - View Rounds Info
Displays detailed information about all rounds and matches for a specific tournament, including match outcomes and player pairings.

12 - Exit
Exits the application.


# Generating Flake8 HTML Report
Flake8 is a tool to check the style and quality of Python code. To generate an HTML report using Flake8:

# Installation
Ensure you have Flake8 and flake8-html installed. If not, you can install them using pip:
pip install flake8 flake8-html

# Generate Report
Run the following command to analyze your project and generate an HTML report:
flake8 --format=html --htmldir=flake8-report

The HTML report will be saved in the same directory as the main. Open index.html in a browser to view the report.
