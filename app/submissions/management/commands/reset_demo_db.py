import os
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings

class Command(BaseCommand):
    help = 'Manually resets the demo database to its clean state'

    def handle(self, *args, **options):
        if not settings.DEMO_MODE:
            self.stdout.write(self.style.WARNING('Not in DEMO_MODE, command aborted'))
            return

        base_dir = settings.BASE_DIR
        live_db = os.path.join(base_dir, 'db_demo.sqlite3')
        clean_db = os.path.join(base_dir, 'db_demo_clean.sqlite3')
        timestamp_dir = os.path.join(base_dir, 'demo_timestamps')

        # Check if clean database exists
        if not os.path.exists(clean_db):
            self.stdout.write(self.style.ERROR(f'Clean database not found: {clean_db}'))
            return

        try:
            # Copy clean database to live database
            shutil.copy2(clean_db, live_db)
            
            # Reset timestamp directory
            if os.path.exists(timestamp_dir):
                shutil.rmtree(timestamp_dir)
            os.makedirs(timestamp_dir)
            
            self.stdout.write(self.style.SUCCESS('Demo database manually reset successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error resetting database: {str(e)}')) 