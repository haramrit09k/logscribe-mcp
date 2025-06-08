import time
import subprocess
import sys
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class RestartHandler(FileSystemEventHandler):
    def __init__(self):
        self.process = None
        self.start_server()
    
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"🔄 File changed: {event.src_path}")
            self.restart_server()
    
    def start_server(self):
        print("🚀 Starting MCP server...")
        self.process = subprocess.Popen([sys.executable, "mcp_server.py"])
    
    def restart_server(self):
        if self.process:
            self.process.terminate()
            self.process.wait()
        self.start_server()

if __name__ == "__main__":
    handler = RestartHandler()
    observer = Observer()
    observer.schedule(handler, ".", recursive=False)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        if handler.process:
            handler.process.terminate()
    observer.join()