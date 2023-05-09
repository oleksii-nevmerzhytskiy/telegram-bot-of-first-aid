from django.core.management.base import BaseCommand
from app.bot import start_polling

class Command(BaseCommand):
    help = 'Starts the Telegram bot.'

    def handle(self, *args, **options):
        start_polling()