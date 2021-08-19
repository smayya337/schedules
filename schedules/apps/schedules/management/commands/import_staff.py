import argparse
import json

from django.core.management.base import BaseCommand

from ...models import Teacher


class Command(BaseCommand):
    help = "Imports a JSON of staff info from the Ion API as teachers"

    def add_arguments(self, parser: argparse.ArgumentParser):
        parser.add_argument("file_name", type=str)

    def handle(self, *args, **options):
        with open(options["file_name"], "r") as file:
            staff_list = json.load(file)["results"]

            for teacher in staff_list:
                result = Teacher.objects.update_or_create(
                    name=teacher["full_name"]
                )

                if result[1]:
                    self.stdout.write(
                        f"Added teacher {result[0].name}.",
                        style_func=self.style.SUCCESS,
                    )
                else:
                    self.stdout.write(
                        f"Did not update teacher {result[0].name}.",
                        style_func=self.style.WARNING,
                    )
