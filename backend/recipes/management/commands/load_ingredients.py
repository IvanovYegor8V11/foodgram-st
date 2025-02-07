import json
import os
from django.core.management.base import BaseCommand
from django.conf import settings
from recipes.models import Ingredient

class Command(BaseCommand):
    help = "Загрузка ингредиентов из JSON в базу данных"

    def handle(self, *args, **kwargs):
        try:
            file_path = os.path.join(settings.BASE_DIR, "data", "ingredients.json")

            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

            ingredients = [Ingredient(**item) for item in data]
            count = len(Ingredient.objects.bulk_create(ingredients))

            self.stdout.write(self.style.SUCCESS(f"Загружено продуктов: {count}"))

        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"Файл {file_path} не найден."))
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR("Ошибка при чтении JSON-файла."))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"Произошла ошибка: {str(e)}"))