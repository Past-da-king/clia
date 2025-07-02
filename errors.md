🤖 CLI SWE AI Initializing...
🧠 Using Model: gemini-2.5-flash-lite-preview-06-17
🛠️  Looking for tool server: swe_tools.run_server
❌ An unexpected error occurred: unhandled errors in a TaskGroup (1 sub-exception)
  + Exception Group Traceback (most recent call last):
  |   File "C:\Users\past9\OneDrive\Desktop\project\clia\ai_agent\agent.py", line 146, in <module>
  |     asyncio.run(main())
  |     ~~~~~~~~~~~^^^^^^^^
  |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\asyncio\runners.py", line 195, in run
  |     return runner.run(main)
  |            ~~~~~~~~~~^^^^^^
  |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\asyncio\runners.py", line 118, in run
  |     return self._loop.run_until_complete(task)
  |            ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\asyncio\base_events.py", line 719, in run_until_complete
  |     return future.result()
  |            ~~~~~~~~~~~~~^^
  |   File "C:\Users\past9\OneDrive\Desktop\project\clia\ai_agent\agent.py", line 64, in main
  |     async with stdio_client(server_params) as (read, write):
  |                ~~~~~~~~~~~~^^^^^^^^^^^^^^^
  |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\contextlib.py", line 235, in __aexit__
  |     await self.gen.athrow(value)
  |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\mcp\client\stdio\__init__.py", line 179, in stdio_client
  |     anyio.create_task_group() as tg,
  |     ~~~~~~~~~~~~~~~~~~~~~~~^^
  |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\anyio\_backends\_asyncio.py", line 772, in __aexit__
  |     raise BaseExceptionGroup(
  |         "unhandled errors in a TaskGroup", self._exceptions
  |     ) from None
  | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
  +-+---------------- 1 ----------------
    | Exception Group Traceback (most recent call last):
    |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\mcp\client\stdio\__init__.py", line 185, in stdio_client
    |     yield read_stream, write_stream
    |   File "C:\Users\past9\OneDrive\Desktop\project\clia\ai_agent\agent.py", line 65, in main
    |     async with ClientSession(read, write) as mcp_session:
    |                ~~~~~~~~~~~~~^^^^^^^^^^^^^
    |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\mcp\shared\session.py", line 223, in __aexit__
    |     return await self._task_group.__aexit__(exc_type, exc_val, exc_tb)
    |            ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\anyio\_backends\_asyncio.py", line 772, in __aexit__
    |     raise BaseExceptionGroup(
    |         "unhandled errors in a TaskGroup", self._exceptions
    |     ) from None
    | ExceptionGroup: unhandled errors in a TaskGroup (1 sub-exception)
    +-+---------------- 1 ----------------
      | Traceback (most recent call last):
      |   File "C:\Users\past9\OneDrive\Desktop\project\clia\ai_agent\agent.py", line 66, in main
      |     await mcp_session.initialize()
      |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\mcp\client\session.py", line 133, in initialize
      |     result = await self.send_request(
      |              ^^^^^^^^^^^^^^^^^^^^^^^^
      |     ...<15 lines>...
      |     )
      |     ^
      |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\mcp\shared\session.py", line 297, in send_request
      |     raise McpError(response_or_error.error)
      | mcp.shared.exceptions.McpError: Connection closed
      +------------------------------------