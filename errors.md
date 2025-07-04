C:\Users\past9\OneDrive\Desktop\New folder\tetris_game>clia --web
╭─ i Info (08:23:57) ──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│                                                                                                                                                  │
│  Web UI is running at http://127.0.0.1:8000                                                                                                      │
│                                                                                                                                                  │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
INFO:     Will watch for changes in these directories: ['C:\\Users\\past9\\OneDrive\\Desktop\\New folder\\tetris_game']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [20128] using WatchFiles
Process SpawnProcess-1:
Traceback (most recent call last):
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\multiprocessing\process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\asyncio\base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\server.py", line 70, in serve
    await self._serve(sockets)
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\importer.py", line 22, in import_from_string
    raise exc from None
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1310, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1324, in _find_and_load_unlocked
ModuleNotFoundError: No module named 'web_ui'