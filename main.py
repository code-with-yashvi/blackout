import os
import sys
import time
import ctypes
import multiprocessing
from cryptography.fernet import Fernet
import keyboard

# Import our core modular components
from core.interceptor import InterceptorEngine
from core.monitor import BehavioralMonitor
from core.chaff import ChaffEngine

def run_interceptor_process(secure_queue, secret_key):
    engine = InterceptorEngine(secret_key, secure_queue)
    engine.start()

def run_monitor_process(chaff_pause_flag):
    monitor = BehavioralMonitor(chaff_pause_flag)
    monitor.start()

def run_chaff_process(chaff_pause_flag):
    chaff = ChaffEngine(chaff_pause_flag)
    chaff.start()

if __name__ == "__main__":
    multiprocessing.freeze_support()
    
    # 1. Admin Rights Check
    try:
        is_admin = os.getuid() == 0 if sys.platform != 'win32' else ctypes.windll.shell32.IsUserAnAdmin() != 0
    except AttributeError:
        is_admin = True 
        
    if not is_admin:
        print("[CRITICAL] BLACKOUT must be run as Administrator/Root to hook system inputs!")
        sys.exit(1)

    print("=" * 60)
    print("      BLACKOUT - Unified Anti-Keylogging Security Suite      ")
    print("=" * 60)
    print("[+] Initializing system protection...")

    # 2. Shared IPC Memory & Keys
    manager = multiprocessing.Manager()
    chaff_pause_flag = manager.Event()
    secure_queue = manager.Queue()
    runtime_crypt_key = Fernet.generate_key()

    # 3. Process Initializations
    monitor_p = multiprocessing.Process(target=run_monitor_process, args=(chaff_pause_flag,))
    chaff_p = multiprocessing.Process(target=run_chaff_process, args=(chaff_pause_flag,))
    interceptor_p = multiprocessing.Process(target=run_interceptor_process, args=(secure_queue, runtime_crypt_key))

    # 4. Launch Subprocesses
    monitor_p.start()
    chaff_p.start()
    interceptor_p.start()

    print("[+] All BLACKOUT security engines are active and blinding spyware.")
    print("[+] EMERGENCY KILLSWITCH: Press [F12] anywhere on your keyboard to stop BLACKOUT.\n")

    try:
        # We use F12 as a single dedicated function key to avoid combo key-blocking conflicts
        while True:
            if keyboard.is_pressed('f12'):
                print("\n[!] Emergency [F12] key detected! Initiating immediate shutdown...")
                break
            
            if not monitor_p.is_alive() or not chaff_p.is_alive() or not interceptor_p.is_alive():
                print("\n[-] Warning: A security subprocess stopped unexpectedly.")
                break
                
            time.sleep(0.05)

    except Exception as e:
        print(f"\n[-] Error in orchestrator loop: {e}")
        
    finally:
        print("\n[-] Safely pulling the plug on all child cores...")
        
        # Remove the hotkey listener
        try:
            keyboard.remove_hotkey('f12')
        except:
            pass

        # Terminate all child operations cleanly
        monitor_p.terminate()
        chaff_p.terminate()
        interceptor_p.terminate()
        
        # Re-join processes safely
        monitor_p.join()
        chaff_p.join()
        interceptor_p.join()
        
        # Ensure keyboard hooks are fully unhooked
        keyboard.unhook_all()
        print("[+] BLACKOUT cleanup successful. System hooks released and returned to normal state.")
        
        # KEEP THE WINDOW OPEN FOR DEMOS:
        print("\n" + "="*50)
        input("[*] DEMO COMPLETE. Press [ENTER] to close this window...")