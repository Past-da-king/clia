 this is what i get on the terminal when running thet same  app

 
C:\Users\past9\OneDrive\Desktop\project\data_ui\backend>uvicorn main:app --reload --port 9000
INFO:     Will watch for changes in these directories: ['C:\\Users\\past9\\OneDrive\\Desktop\\project\\data_ui\\backend']
INFO:     Uvicorn running on http://127.0.0.1:9000 (Press CTRL+C to quit)
INFO:     Started reloader process [3672] using WatchFiles
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
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "C:\Users\past9\OneDrive\Desktop\project\data_ui\backend\main.py", line 7, in <module>
    from backend import crud, models, schemas, auth
ModuleNotFoundError: No module named 'backend'



this is what in the log std out   file form the tools 


NFO:     Will watch for changes in these directories: ['C:\\Users\\past9\\OneDrive\\Desktop\\project\\data_ui\\backend']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [7292] using WatchFiles
C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\pydantic\_internal\_config.py:373: UserWarning: Valid config keys have changed in V2:
* 'orm_mode' has been renamed to 'from_attributes'
  warnings.warn(message, UserWarning)
INFO:     Started server process [17316]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
WARNING:  WatchFiles detected changes in 'main.py'. Reloading...

and the sterr is empty 

