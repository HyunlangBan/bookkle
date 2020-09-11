from django.core.management.base import BaseCommand
from review.models import Book, Review
from django_seed import Seed
import random
from user.models import User

class Command(BaseCommand):

    help = "This command generated users"

    def add_arguments(self, parser):
        parser.add_argument(
            "--number", default=1, help="How many do you want create User"
        )

    def handle(self, *args, **options):
        number = int(options.get("number"))
        seeder = Seed.seeder()

        # 모든 유저를 가져옵니다.
        users = User.objects.all()
        
        # 모든 방을 가져옵니다.
        books = Book.objects.all()
        
        seeder.add_entity(
            Review,
            number,
            {
                "rating": lambda x: random.randint(0, 3),
                "recommand_count": lambda x: random.randint(0, 20),
               
                # user 이름으로 users 중 하나를 choice합니다.
                "user": lambda x: random.choice(users),
                
                # room 이름으로 rooms 중 하나를 choice합니다.
                "book": lambda x: random.choice(books),
            },
        )


        seeder.execute()
        # 성공했다고 확인 메세지
        self.stdout.write(self.style.SUCCESS(f"{number} Reviews created!"))


