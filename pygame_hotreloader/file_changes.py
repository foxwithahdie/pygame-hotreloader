import sys, os, time, asyncio

import watchdog
from watchdog.observers import Observer, ObserverType
from watchdog.events import FileSystemEventHandler, PatternMatchingEventHandler, FileModifiedEvent


class DirectoryWatcher(FileSystemEventHandler):
    def __init__(self, dir: str):
        self.dir = dir
        
    def on_any_event(self, event):
        print(f"{event.event_type}, {event.src_path}")


def main():
    path = os.path.join(".", "test_dir")
    event_handler: DirectoryWatcher = DirectoryWatcher(path)
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
    
if __name__ == "__main__":
    main()