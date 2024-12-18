import asyncio
import sys
import os

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class DirectoryWatcher(FileSystemEventHandler):
    def __init__(self, directory: str):
        self.directory = directory
    def on_any_event(self, event):
        print(f"{event.event_type}, {event.src_path}")


async def main() -> None:
    path: str = "."
    event_handler: DirectoryWatcher = DirectoryWatcher(path)
    observer: Observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            await asyncio.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
    
if __name__ == "__main__":
    asyncio.run(main())