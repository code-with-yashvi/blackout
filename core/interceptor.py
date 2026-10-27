import time
from cryptography.fernet import Fernet
import keyboard

class InterceptorEngine:
    def __init__(self, secret_key, secure_queue):
        self.cipher = Fernet(secret_key)
        self.secure_queue = secure_queue
        self.is_running = True

    def _on_key_event(self, event):
        # Ignore programmatic injections & function keys (like F12 killswitch)
        if event.is_keypad or getattr(event, 'scan_code', 0) == 0:
            return

        # Do NOT suppress or intercept F12 so it can trigger the emergency killswitch
        if event.name == 'f12':
            return

        if event.event_type == keyboard.KEY_DOWN:
            if len(event.name) == 1:
                token = self.cipher.encrypt(event.name.encode())
                self.secure_queue.put(token)

    def start(self):
        print(f"[+] BLACKOUT Interceptor active. Trapping raw hardware events...")
        keyboard.hook(self._on_key_event, suppress=False)
        
        try:
            while self.is_running:
                if not self.secure_queue.empty():
                    encrypted_data = self.secure_queue.get()
                    decrypted_char = self.cipher.decrypt(encrypted_data).decode()
                time.sleep(0.01)
        except Exception as e:
            print(f"[-] Interceptor Error: {e}")
        finally:
            keyboard.unhook_all()

if __name__ == "__main__":
    import multiprocessing
    mgr = multiprocessing.Manager()
    q = mgr.Queue()
    key = Fernet.generate_key()
    engine = InterceptorEngine(key, q)
    engine.start()