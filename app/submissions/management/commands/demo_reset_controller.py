import os
import time
import shutil
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

class DemoResetController:
    def __init__(self):
        self.base_dir = settings.BASE_DIR
        self.timestamp_dir = os.path.join(self.base_dir, 'demo_timestamps')
        self.modified_file = os.path.join(self.timestamp_dir, 'demo_last_modified.timestamp')
        self.reset_due_file = os.path.join(self.timestamp_dir, 'demo_reset_due.timestamp')
        
        # SQLite database files
        self.live_db = os.path.join(self.base_dir, 'db_demo.sqlite3')
        self.clean_db = os.path.join(self.base_dir, 'db_demo_clean.sqlite3')
        
        # Maximum delay of 15 minutes (900 seconds)
        self.MAX_DELAY = 900
        # Recent activity threshold of 5 minutes (300 seconds)
        self.RECENT_THRESHOLD = 300

    def get_timestamp(self, file_path, default=0):
        try:
            with open(file_path, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            return default

    def set_reset_due(self, timestamp):
        with open(self.reset_due_file, 'w') as f:
            f.write(str(int(timestamp)))

    def should_reset(self):
        current_time = int(time.time())
        last_modified = self.get_timestamp(self.modified_file)
        reset_due = self.get_timestamp(self.reset_due_file)
        
        # If no reset is scheduled, schedule one for the next hour
        if reset_due == 0:
            next_hour = current_time - (current_time % 3600) + 3600
            self.set_reset_due(next_hour)
            return False
        
        # If we're past the maximum delay, force reset
        if current_time >= reset_due + self.MAX_DELAY:
            return True
            
        # If it's time for reset but there's recent activity
        if current_time >= reset_due:
            time_since_modification = current_time - last_modified
            if time_since_modification < self.RECENT_THRESHOLD:
                # Delay reset but don't exceed maximum delay
                new_reset_time = min(current_time + self.RECENT_THRESHOLD,
                                   reset_due + self.MAX_DELAY)
                self.set_reset_due(new_reset_time)
                return False
            return True
            
        return False

    def reset_database(self):
        """
        Reset the SQLite database by copying the clean version over the live one
        """
        try:
            if os.path.exists(self.clean_db):
                shutil.copy2(self.clean_db, self.live_db)
                logger.info("Demo database reset successfully")
                
                # Clear the timestamps directory
                if os.path.exists(self.timestamp_dir):
                    shutil.rmtree(self.timestamp_dir)
                    os.makedirs(self.timestamp_dir)
                
                return True
            else:
                logger.error(f"Clean database file not found: {self.clean_db}")
                return False
        except Exception as e:
            logger.error(f"Error resetting demo database: {str(e)}")
            return False

def run():
    if not settings.DEMO_MODE:
        logger.info("Not in demo mode, skipping reset check")
        return
        
    controller = DemoResetController()
    if controller.should_reset():
        logger.info("Resetting demo database")
        controller.reset_database()
    else:
        logger.info("Reset not needed at this time")