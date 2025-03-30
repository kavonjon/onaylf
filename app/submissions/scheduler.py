import os
import time
import shutil
import logging
from django.conf import settings
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

logger = logging.getLogger(__name__)

class DemoResetScheduler:
    def __init__(self):
        self.base_dir = settings.BASE_DIR
        self.timestamp_dir = os.path.join(self.base_dir, 'demo_timestamps')
        self.modified_file = os.path.join(self.timestamp_dir, 'demo_last_modified.timestamp')
        
        # SQLite database files
        self.live_db = os.path.join(self.base_dir, 'db_demo.sqlite3')
        self.clean_db = os.path.join(self.base_dir, 'db_demo_clean.sqlite3')
        
        # Inactivity threshold of 10 minutes (600 seconds)
        self.INACTIVITY_THRESHOLD = 600
        
        # Force reset after 30 minutes (1800 seconds) regardless of activity
        self.FORCE_RESET_THRESHOLD = 1800
        
        # Track when the database was last reset
        self.last_reset_file = os.path.join(self.timestamp_dir, 'demo_last_reset.timestamp')
        
        # Create timestamp directory if it doesn't exist
        if not os.path.exists(self.timestamp_dir):
            os.makedirs(self.timestamp_dir)
            
        # Initialize the scheduler
        self.scheduler = BackgroundScheduler()
        
    def get_timestamp(self, file_path, default=0):
        """Get timestamp from a file or return default if not found"""
        try:
            with open(file_path, 'r') as f:
                return int(f.read().strip())
        except (FileNotFoundError, ValueError):
            # If file doesn't exist, create it with current time
            current_time = int(time.time())
            with open(file_path, 'w') as f:
                f.write(str(current_time))
            return current_time
    
    def get_last_modified_timestamp(self):
        """Get when the database was last modified (edits, not browsing)"""
        return self.get_timestamp(self.modified_file)
    
    def get_last_reset_timestamp(self):
        """Get when the database was last reset"""
        return self.get_timestamp(self.last_reset_file)
    
    def update_last_reset_timestamp(self):
        """Update the timestamp of when the database was last reset"""
        current_time = int(time.time())
        with open(self.last_reset_file, 'w') as f:
            f.write(str(current_time))
            
    def should_reset(self):
        """Check if the database should be reset"""
        current_time = int(time.time())
        
        # Get timestamps
        last_modified = self.get_last_modified_timestamp()
        last_reset = self.get_last_reset_timestamp()
        
        # Calculate time periods
        time_since_modification = current_time - last_modified
        time_since_reset = current_time - last_reset
        
        logger.debug(f"Time since last modification: {time_since_modification} seconds")
        logger.debug(f"Time since last reset: {time_since_reset} seconds")
        
        # Check if we need to force reset regardless of activity
        if time_since_reset >= self.FORCE_RESET_THRESHOLD:
            logger.info(f"Force resetting database - {time_since_reset} seconds since last reset")
            return True
        
        # Check if we should reset due to no edit activity
        if time_since_modification >= self.INACTIVITY_THRESHOLD:
            logger.info(f"Resetting database due to inactivity - {time_since_modification} seconds since last edit")
            return True
            
        return False
            
    def reset_database(self):
        """Reset the SQLite database by copying the clean version over the live one"""
        try:
            if not settings.DEMO_MODE:
                logger.info("Not in demo mode, skipping reset check")
                return False
                
            if not self.should_reset():
                logger.info("No reset needed at this time")
                return False
                
            if os.path.exists(self.clean_db):
                shutil.copy2(self.clean_db, self.live_db)
                
                # Update the last reset timestamp
                self.update_last_reset_timestamp()
                
                logger.info("Demo database reset successfully")
                return True
            else:
                logger.error(f"Clean database file not found: {self.clean_db}")
                return False
        except Exception as e:
            logger.error(f"Error resetting demo database: {str(e)}")
            return False
            
    def start(self):
        """Start the scheduler to check for inactivity every 5 minutes"""
        if not settings.DEMO_MODE:
            logger.info("Not in demo mode, scheduler not started")
            return
            
        # Add job to reset database if inactive for the threshold
        self.scheduler.add_job(
            self.reset_database,
            IntervalTrigger(minutes=5),
            id='demo_reset_job',
            replace_existing=True
        )
        
        self.scheduler.start()
        logger.info("Demo reset scheduler started, checking for inactivity every 5 minutes")
        
    def shutdown(self):
        """Shutdown the scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown()
            logger.info("Demo reset scheduler shutdown")

# Global scheduler instance
scheduler = None

def start_scheduler():
    """Initialize and start the scheduler"""
    global scheduler
    if settings.DEMO_MODE and scheduler is None:
        scheduler = DemoResetScheduler()
        scheduler.start()
        
def stop_scheduler():
    """Stop the scheduler"""
    global scheduler
    if scheduler is not None:
        scheduler.shutdown()
        scheduler = None 