import os

from controllers.player_controller import PlayerController
from controllers.tournament_controller import TournamentController
from models.player_model import PlayerModel
from models.tournament_model import TournamentModel
from views.tournament_view import TournamentView
from views.player_view import PlayerView

base_dir = os.path.dirname(os.path.abspath(__file__))

player_file_path = os.path.join(base_dir, "data", "players.json")
file_path = os.path.join(base_dir, "data", "tournaments.json")

player_model = PlayerModel(player_file_path)
tournament_model = TournamentModel(file_path, player_model)

player_view = PlayerView()
tournament_view = TournamentView()

player_controller = PlayerController(player_model, player_view)
tournament_controller = TournamentController(
    tournament_model, player_model, tournament_view
)


def main():
    while True:
        print_main_menu()
        choice = input("Enter your choice: ").strip()

        match choice:
            case "1":
                player_controller.add_player()
            case "2":
                tournament_controller.add_tournament()
            case "3":
                tournament_controller.view_tournament_players()
            case "4":
                tournament_controller.add_player_to_tournament()
            case "5":
                tournament_name = tournament_view.prompt_for_tournament_name()
                tournament_controller.start_tournament(tournament_name)
            case "6":
                tournament_controller.input_match_results()
            case "7":
                tournament_name = tournament_view.prompt_for_tournament_name()
                tournament_controller.view_current_standings(tournament_name)
            case "8":
                player_controller.list_players_sorted()
            case "9":
                tournament_controller.advance_to_next_round()
            case "10":
                tournament_controller.list_all_tournaments()
            case "11":
                tournament_name = tournament_view.prompt_for_tournament_name()
                tournament_controller.view_tournament_details(tournament_name)
            case "12":
                print("Exiting program.")
                break
            case _:
                print("Invalid choice, please try again.")


def print_main_menu():
    print("\nMain Menu:")
    print("1 - Add Player")
    print("2 - Create Tournament")
    print("3 - View Tournament Players")
    print("4 - Add Player to Tournament")
    print("5 - Start Tournament")
    print("6 - Input Match Results")
    print("7 - View Current Standings")
    print("8 - View All Players")
    print("9 - Advance to Next Round")
    print("10 - View All Tournaments")
    print("11 - View Rounds Info")
    print("12 - Exit")


if __name__ == "__main__":
    main()
