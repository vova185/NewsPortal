from django.core.management.base import BaseCommand, CommandError
from news.models import Post

class Command(BaseCommand):
    help = 'Удаление публикаций выбранной категории'

    requires_migrations_checks = True

    def handle(self, *args, **options):
        self.stdout.readable()
        self.stdout.write("Публикации какой категории Вы хотели бы удалить? (SP, CUL, POL, ED, NAT, EMP, RES)")
        cat = input('Введите одну из указанных категорий: ')
        self.stdout.write(f"Вы точно хотите удалить публикации в категории {cat}? yes/no")
        answer = input()
        if answer == 'yes':
            Post.objects.filter(categories__all_category=cat).delete()
            self.stdout.write(self.style.SUCCESS(f'Публикации в категории {cat} удалены'))
            return
        self.stdout.write(self.style.ERROR('Доступ запрещён'))