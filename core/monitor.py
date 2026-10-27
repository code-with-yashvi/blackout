import time
import json
import os
import psutil
import win32gui
import win32process

class BehavioralMonitor:
    def __init__(self, chaff_pause_flag, config_path="config/settings.json"):
        self.chaff_pause_flag = chaff_pause_flag
        self.is_running = True
        
        # Load configuration
        self.load_config(config_path)

    def load_config(self, path):
        try:
            if os.path.exists(path):
                with open(path, 'r') as f:
                    data = json.load(f)
                    monitor_cfg = data.get("behavioral_monitor", {})
                    self.poll_interval = monitor_cfg.get("poll_interval", 0.5)
                    self.secure_windows = monitor_cfg.get("secure_windows", ["Notepad"])
            else:
                # Fallback defaults if config file is missing
                self.poll_interval = 0.5
                self.secure_windows = ["Notepad"]
        except Exception as e:
            print(f"[-] Config Load Error in Monitor: {e}. Using defaults.")
            self.poll_interval = 0.5
            self.secure_windows = ["Notepad"]

    def get_active_window_title(self):
        try:
            hwnd = win32gui.GetForegroundWindow()
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                proc = psutil.Process(pid)
                proc_name = proc.name()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                proc_name = ""
            
            window_title = win32gui.GetWindowText(hwnd)
            return window_title, proc_name
        except Exception:
            return "", ""

    def start(self):
        print(f"[+] BLACKOUT Behavioral Monitor active. Watching active focus windows...")
        
        while self.is_running:
            title, proc_name = self.get_active_window_title()
            
            # Check if active window matches any secure target in our settings.json
            is_secure_context = any(
                target.lower() in title.lower() or target.lower() in proc_name.lower() 
                for target in self.secure_windows
            )
            
            if is_secure_context:
                # Pause chaff noise so typing is crystal clean in secure windows
                self.chaff_pause_flag.set()
            else:
                # Resume chaff blinding in unsecured background contexts
                self.chaff_pause_flag.clear()
                
            time.sleep(self.poll_interval)