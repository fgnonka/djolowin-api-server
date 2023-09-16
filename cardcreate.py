import os
import django
import random

from django.utils.text import slugify
from django.core.exceptions import ValidationError


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "djolowin.settings")
django.setup()

from custom_user.models import CustomUser
from sports.models import Player
from card.models import PlayerCard, CardRarity


# Fetch instances of the related models
owners = list(CustomUser.objects.all())
players = list(Player.objects.filter(team__id=1))
rarities = list(CardRarity.objects.all())


# Function to generate a random image file (if needed)
def random_image():
    # Replace this with the path to a folder containing images
    images_path = "/path/to/images/"
    random_image = random.choice(os.listdir(images_path))
    return os.path.join(images_path, random_image)


def create_playercards():
    for player in players:
        # for i in range(1):
        #     owner = None
        #     common_rarity = CardRarity.objects.get(name="Unique")
        #     common_price = 40000
        #     playercard_common = PlayerCard(
        #         player=player,
        #         rarity=common_rarity,
        #         for_sale=True,
        #         owner=owner,
        #         value=common_price,
        #         index=1,
        #         slug=slugify(f"{player.name}-{common_rarity}-1"),
        #         number_likes=random.randint(0, 100),
        #     )
        #     playercard_common.save()
        #     print(f"PlayerCard {playercard_common.slug} created successfully!")
        
        for i in range(51):
            owner = None
            limited_rarity = CardRarity.objects.get(name="Limited")
            limited_price = 40000
            playercard_limited = PlayerCard(
                for_sale=True,
                owner=owner,
                player=player,
                rarity=limited_rarity,
                value=limited_price,
                index=i,
                slug=slugify(f"{player.name}-{limited_rarity}-{i}"),
                number_likes=random.randint(0, 100),
            )
            playercard_limited.save()
            print(f"PlayerCard {playercard_limited.slug} created successfully!")
            
        for i in range(26):
            owner = None
            rare_rarity = CardRarity.objects.get(name="Rare")
            rare_price = 80000
            playercard_rare = PlayerCard(
                for_sale=True,
                owner=owner,
                player=player,
                rarity=rare_rarity,
                value=rare_price,
                index=i,
                slug=slugify(f"{player.name}-{rare_rarity}-{i}"),
                number_likes=random.randint(0, 100),
            )
            playercard_rare.save()
            print(f"PlayerCard {playercard_rare.slug} created successfully!")
            
        for i in range(11):
            owner = None
            super_rare_rarity = CardRarity.objects.get(name="Super Rare")
            super_rare_price = 200000
            playercard_super_rare = PlayerCard(
                for_sale=True,
                owner=owner,
                player=player,
                rarity=super_rare_rarity,
                value=super_rare_price,
                index=i,
                slug=slugify(f"{player.name}-{super_rare_rarity}-{i}"),
                number_likes=random.randint(0, 100),
            )
            playercard_super_rare.save()
            print(f"PlayerCard {playercard_super_rare.slug} created successfully!")

if __name__ == "__main__":
    create_playercards()
