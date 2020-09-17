from django.core.management.base import BaseCommand
from review.models import Book, Review
from django_seed import Seed
import random
from user.models import User

class Command(BaseCommand):

    help = "This command generated users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many do you want create Review"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        seeder = Seed.seeder()

        users = User.objects.all()

        books = Book.objects.all()
        
        seeder.add_entity(
            Review,
            number,
            {
                "rating": lambda x: random.randint(0, 3),
                "recommend_count": lambda x: random.randint(0, 20),              
                "user": lambda x: random.choice(users),
                "book": lambda x: random.choice(books),
            },
        )


        seeder.execute()
        self.stdout.write(self.style.SUCCESS(f"{number} Reviews created!"))


