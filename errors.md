C:\Users\past9\OneDrive\Desktop\test>clia
╭─ i Info (04:39:41) ──────────────────────────────────────────────────╮
│                                                                      │
│  🤖 CLI SWE AI Initializing...                                       │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯
╭─ i Info (04:39:41) ──────────────────────────────────────────────────╮
│                                                                      │
│  🧠 Using Model: gemini-2.5-flash                                    │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯
╭─ i Info (04:39:41) ──────────────────────────────────────────────────╮
│                                                                      │
│  🛠️  Looking for tool server: swe_tools.run_server                    │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯
╭─ i Info (04:39:42) ──────────────────────────────────────────────────╮
│                                                                      │
│  ✅ MCP Tool Server Connected.                                       │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯
╭─ ✕ Error (04:39:42) ─────────────────────────────────────────────────╮
│                                                                      │
│  ❌ An unexpected error occurred during MCP server connection:       │
│  unhandled errors in a TaskGroup (1 sub-exception)                   │
│                                                                      │
╰──────────────────────────────────────────────────────────────────────╯
  + Exception Group Traceback (most recent call last):
  |   File "C:\Users\past9\OneDrive\Desktop\project\clia\gui\main.py", line 44, in main
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
    |   File "C:\Users\past9\OneDrive\Desktop\project\clia\gui\main.py", line 45, in main
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
      |   File "C:\Users\past9\OneDrive\Desktop\project\clia\gui\main.py", line 56, in main
      |     generation_config = types.GenerateContentConfig(
      |         tools=gemini_tools,
      |     ...<3 lines>...
      |         )
      |     )
      |   File "C:\Users\past9\AppData\Local\Programs\Python\Python313\Lib\site-packages\pydantic\main.py", line 253, in __init__
      |     validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
      | pydantic_core._pydantic_core.ValidationError: 32 validation errors for GenerateContentConfig
      | tools.0.Tool
      |   Input should be a valid dictionary or object to extract fields from [type=model_attributes_type, input_value=('function_declarations',...ECT'>), response=None)]), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_attributes_type
      | tools.0.callable
      |   Input should be callable [type=callable_type, input_value=('function_declarations',...ECT'>), response=None)]), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/callable_type
      | tools.0.Tool
      |   Input should be a valid dictionary or instance of Tool [type=model_type, input_value=('function_declarations',...ECT'>), response=None)]), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_type
      | tools.0.is-instance[ClientSession]
      |   Input should be an instance of ClientSession [type=is_instance_of, input_value=('function_declarations',...ECT'>), response=None)]), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/is_instance_of
      | tools.1.Tool
      |   Input should be a valid dictionary or object to extract fields from [type=model_attributes_type, input_value=('retrieval', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_attributes_type
      | tools.1.callable
      |   Input should be callable [type=callable_type, input_value=('retrieval', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/callable_type
      | tools.1.Tool
      |   Input should be a valid dictionary or instance of Tool [type=model_type, input_value=('retrieval', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_type
      | tools.1.is-instance[ClientSession]
      |   Input should be an instance of ClientSession [type=is_instance_of, input_value=('retrieval', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/is_instance_of
      | tools.2.Tool
      |   Input should be a valid dictionary or object to extract fields from [type=model_attributes_type, input_value=('google_search', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_attributes_type
      | tools.2.callable
      |   Input should be callable [type=callable_type, input_value=('google_search', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/callable_type
      | tools.2.Tool
      |   Input should be a valid dictionary or instance of Tool [type=model_type, input_value=('google_search', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_type
      | tools.2.is-instance[ClientSession]
      |   Input should be an instance of ClientSession [type=is_instance_of, input_value=('google_search', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/is_instance_of
      | tools.3.Tool
      |   Input should be a valid dictionary or object to extract fields from [type=model_attributes_type, input_value=('google_search_retrieval', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_attributes_type
      | tools.3.callable
      |   Input should be callable [type=callable_type, input_value=('google_search_retrieval', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/callable_type
      | tools.3.Tool
      |   Input should be a valid dictionary or instance of Tool [type=model_type, input_value=('google_search_retrieval', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_type
      | tools.3.is-instance[ClientSession]
      |   Input should be an instance of ClientSession [type=is_instance_of, input_value=('google_search_retrieval', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/is_instance_of
      | tools.4.Tool
      |   Input should be a valid dictionary or object to extract fields from [type=model_attributes_type, input_value=('enterprise_web_search', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_attributes_type
      | tools.4.callable
      |   Input should be callable [type=callable_type, input_value=('enterprise_web_search', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/callable_type
      | tools.4.Tool
      |   Input should be a valid dictionary or instance of Tool [type=model_type, input_value=('enterprise_web_search', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_type
      | tools.4.is-instance[ClientSession]
      |   Input should be an instance of ClientSession [type=is_instance_of, input_value=('enterprise_web_search', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/is_instance_of
      | tools.5.Tool
      |   Input should be a valid dictionary or object to extract fields from [type=model_attributes_type, input_value=('google_maps', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_attributes_type
      | tools.5.callable
      |   Input should be callable [type=callable_type, input_value=('google_maps', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/callable_type
      | tools.5.Tool
      |   Input should be a valid dictionary or instance of Tool [type=model_type, input_value=('google_maps', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_type
      | tools.5.is-instance[ClientSession]
      |   Input should be an instance of ClientSession [type=is_instance_of, input_value=('google_maps', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/is_instance_of
      | tools.6.Tool
      |   Input should be a valid dictionary or object to extract fields from [type=model_attributes_type, input_value=('url_context', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_attributes_type
      | tools.6.callable
      |   Input should be callable [type=callable_type, input_value=('url_context', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/callable_type
      | tools.6.Tool
      |   Input should be a valid dictionary or instance of Tool [type=model_type, input_value=('url_context', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_type
      | tools.6.is-instance[ClientSession]
      |   Input should be an instance of ClientSession [type=is_instance_of, input_value=('url_context', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/is_instance_of
      | tools.7.Tool
      |   Input should be a valid dictionary or object to extract fields from [type=model_attributes_type, input_value=('code_execution', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_attributes_type
      | tools.7.callable
      |   Input should be callable [type=callable_type, input_value=('code_execution', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/callable_type
      | tools.7.Tool
      |   Input should be a valid dictionary or instance of Tool [type=model_type, input_value=('code_execution', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/model_type
      | tools.7.is-instance[ClientSession]
      |   Input should be an instance of ClientSession [type=is_instance_of, input_value=('code_execution', None), input_type=tuple]
      |     For further information visit https://errors.pydantic.dev/2.11/v/is_instance_of
      +------------------------------------

C:\Users\past9\OneDrive\Desktop\test> @