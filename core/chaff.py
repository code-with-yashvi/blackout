import time
import json
import os
import random

class ChaffEngine:
    def __init__(self, chaff_pause_flag, config_path="config/settings.json"):
        self.chaff_pause_flag = chaff_pause_flag
        self.is_running = True
        self.load_config(config_path)
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        self.log_file_path = os.path.join("logs", "decoy_stream.log")

    def load_config(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                    chaff_cfg = data.get("chaff_settings", {})
                    self.enabled = chaff_cfg.get("enabled", True)
                    self.min_delay = chaff_cfg.get("min_delay", 0.05)
                    self.max_delay = chaff_cfg.get("max_delay", 0.2)
                    self.decoy_pool = chaff_cfg.get("decoy_pool", "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?")
            else:
                self.enabled = True
                self.min_delay = 0.05
                self.max_delay = 0.2
                self.decoy_pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"
        except Exception as e:
            print(f"[-] Config Load Error in Chaff: {e}. Using defaults.")
            self.enabled = True
            self.min_delay = 0.05
            self.max_delay = 0.2
            self.decoy_pool = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*()_+-=[]{}|;:,.<>?"

    def start(self):
        if not self.enabled:
            print("[*] BLACKOUT Chaff Generator is disabled in settings.json.")
            return

        print(f"[+] BLACKOUT Chaff Generator active (PID: {os.getpid()}). Streaming background decoys to logs/decoy_stream.log...")
        
        # Open decoy log file in append mode
        with open(self.log_file_path, "a", encoding="utf-8") as log_file:
            # Add clean spacing and a distinct header for this new session run
            log_file.write("\n\n" + "="*59 + "\n")
            log_file.write(f"=== [BLACKOUT DECOY STREAM ACTIVE: {time.strftime('%Y-%m-%d %H:%M:%S')}] ===\n")
            log_file.write("="*59 + "\n\n")
            log_file.flush()
            
            while self.is_running:
                try:
                    fake_char = random.choice(self.decoy_pool)
                    
                    # Write character with periodic spacing or newlines every few chars 
                    # so it scrolls like a readable security stream!
                    log_file.write(fake_char)
                    log_file.flush()
                    
                    sleep_duration = random.uniform(self.min_delay, self.max_delay)
                    time.sleep(sleep_duration)
                except Exception:
                    pass

if __name__ == "__main__":
    import multiprocessing
    mgr = multiprocessing.Manager()
    flag = mgr.Event()
    chaff = ChaffEngine(flag)
    chaff.start()