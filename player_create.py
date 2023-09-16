import os
import django
from django.core.exceptions import ValidationError

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()

from sports.models import Player, Team

position_choices = tuple(Player.POSITION_CHOICES)
print(position_choices)

def create_player(
    name, position, date_of_birth, jersey_number, picture, team, nationality, slug
):
    try:
        player = Player(
            name=name,
            position=position,
            date_of_birth=date_of_birth,
            jersey_number=jersey_number,
            picture=picture,
            team=team,
            nationality=nationality,
            slug=slug,
        )   
        player.full_clean()
        player.save()
        print(f"Player {name} created successfully!")
    except ValidationError as e:
        print(f"Failed to create player {name}. Error: {e}")


def main():
    # Replace the following example data with your actual player data
    for i in range(1, 24):
        position = position_choices[0][0]
        if i <= 5:
            position = position_choices[3][0]
        elif i <= 13:
            position = position_choices[1][0]
        elif i <= 21:
            position = position_choices[2][0]
        player_data = [
        {
            "name": f"Joueur Africa #{i}",
            "position": position,
            "date_of_birth": f"1970-01-{str(i).zfill(2)}",
            "jersey_number": f"{i}",
            "picture": None,
            "team_id": 2,  # Replace with the actual team ID
            "slug": f"player-africa-sports-{i}",
        }
        ]
        for player_info in player_data:
            team = Team.objects.get(pk=player_info["team_id"])
            nationality = "CI"
            create_player(
                name=player_info["name"],
                position=player_info["position"],
                date_of_birth=player_info["date_of_birth"],
                jersey_number=player_info["jersey_number"],
                picture=player_info["picture"],
                team=team,
                nationality=nationality,
                slug=player_info["slug"],
            )


if __name__ == "__main__":
    main()
