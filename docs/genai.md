TITLE: Initialize Gen AI Client for Vertex AI
DESCRIPTION: Creates an instance of the 'genai.Client' configured for the Vertex AI API. This setup requires specifying 'vertexai=True' along with your Google Cloud 'project' ID and 'location'.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google import genai

# Only run this block for Vertex AI API
client = genai.Client(
    vertexai=True, project='your-project-id', location='us-central1'
)
```

----------------------------------------

TITLE: Initialize Gen AI Client Using Environment Variables
DESCRIPTION: Creates an instance of the 'genai.Client' that automatically detects and uses configuration settings provided through environment variables. This simplifies client setup in various deployment environments.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google import genai

client = genai.Client()
```

----------------------------------------

TITLE: Initialize Gen AI Client for Gemini Developer API
DESCRIPTION: Creates an instance of the 'genai.Client' specifically configured for the Gemini Developer API. This requires providing your 'GEMINI_API_KEY' for authentication.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google import genai

# Only run this block for Gemini Developer API
client = genai.Client(api_key='GEMINI_API_KEY')
```

----------------------------------------

TITLE: Import Google Gen AI Modules
DESCRIPTION: Imports the core 'genai' module and the 'types' module from the Google Gen AI SDK. These imports are essential for accessing the SDK's functionalities and data structures.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google import genai
from google.genai import types
```

----------------------------------------

TITLE: Send Synchronous Streaming Chat Messages
DESCRIPTION: Shows how to establish a chat session and send messages synchronously with streaming. The response is received in chunks, which are then printed incrementally as they arrive, providing a more interactive experience.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
chat = client.chats.create(model='gemini-2.0-flash-001')
for chunk in chat.send_message_stream('tell me a story'):
    print(chunk.text, end='')  # end='' is optional, for demo purposes.
```

----------------------------------------

TITLE: Send Synchronous Non-Streaming Chat Messages
DESCRIPTION: Illustrates how to create a chat session and send messages synchronously without streaming. The full response text is received and printed after each message, allowing for multi-turn conversations.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
chat = client.chats.create(model='gemini-2.0-flash-001')
response = chat.send_message('tell me a story')
print(response.text)
response = chat.send_message('summarize the story you told me in 1 sentence')
print(response.text)
```

----------------------------------------

TITLE: Generate Content with Text Input using Gemini API
DESCRIPTION: Shows a basic example of generating content by passing a simple text string to the 'client.models.generate_content' method and printing the response.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
response = client.models.generate_content(
    model='gemini-2.0-flash-001', contents='Why is the sky blue?'
)
print(response.text)
```

----------------------------------------

TITLE: Install Google Gen AI Python SDK
DESCRIPTION: Installs the Google Gen AI Python SDK using pip, the Python package installer. This command ensures the necessary libraries are available for development.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Shell
CODE:
```
pip install google-genai
```

----------------------------------------

TITLE: Send Asynchronous Streaming Chat Messages
DESCRIPTION: Illustrates how to send chat messages asynchronously with streaming. It utilizes `client.aio.chats.create` for an asynchronous chat session and `async for chunk in await chat.send_message_stream` to process streaming responses in a non-blocking manner.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
chat = client.aio.chats.create(model='gemini-2.0-flash-001')
async for chunk in await chat.send_message_stream('tell me a story'):
    print(chunk.text, end='') # end='' is optional, for demo purposes.
```

----------------------------------------

TITLE: Generate Content with Structured JSON Response
DESCRIPTION: This example demonstrates how to configure the `generate_content` method to return a structured JSON response. It defines an `InstrumentEnum` class and uses `response_mime_type` and `response_schema` to guide the model's output format.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
class InstrumentEnum(Enum):
    PERCUSSION = 'Percussion'
    STRING = 'String'
    WOODWIND = 'Woodwind'
    BRASS = 'Brass'
    KEYBOARD = 'Keyboard'

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What instrument plays multiple notes at once?',
    config={
        'response_mime_type': 'application/json',
        'response_schema': InstrumentEnum,
    },
)
print(response.text)
```

----------------------------------------

TITLE: Stream Content Asynchronously from Gemini Model
DESCRIPTION: This snippet demonstrates asynchronous streaming of content from the Gemini model. It uses `async for` with `client.aio.models.generate_content_stream` to process chunks of text as they become available.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
async for chunk in await client.aio.models.generate_content_stream(
    model='gemini-2.0-flash-001', contents='Tell me a story in 300 words.'
):
    print(chunk.text, end='')
```

----------------------------------------

TITLE: SDK Conversion of List of Strings for 'contents' Argument
DESCRIPTION: Illustrates how the SDK processes a list of strings, converting them into a single 'types.UserContent' object with multiple text parts, maintaining the 'user' role.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
[
types.UserContent(
    parts=[
    types.Part.from_text(text='Why is the sky blue?'),
    types.Part.from_text(text='Why is the cloud white?'),
    ]
)
]
```

----------------------------------------

TITLE: Embed Single Text Content String
DESCRIPTION: This snippet shows how to generate an embedding for a single piece of text using `client.models.embed_content`. Embeddings are numerical representations of text, useful for similarity searches and other NLP tasks.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
response = client.models.embed_content(
    model='text-embedding-004',
    contents='why is the sky blue?',
)
print(response)
```

----------------------------------------

TITLE: Configure Gemini Developer API Key via Environment Variable
DESCRIPTION: Sets the 'GOOGLE_API_KEY' environment variable, allowing the Gen AI client to automatically pick up the API key for the Gemini Developer API without explicit code configuration.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Shell
CODE:
```
export GOOGLE_API_KEY='your-api-key'
```

----------------------------------------

TITLE: Set Proxy Environment Variables for HTTP/S
DESCRIPTION: Demonstrates how to set standard HTTPS_PROXY and SSL_CERT_FILE environment variables, which are used by httpx and aiohttp libraries for proxy configuration before client initialization.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Shell
CODE:
```
export HTTPS_PROXY='http://username:password@proxy_uri:port'
export SSL_CERT_FILE='client.pem'
```

----------------------------------------

TITLE: Define JSON Response Schema with Dictionary in Google GenAI
DESCRIPTION: This example illustrates how to provide a JSON schema directly as a Python dictionary to the `response_schema` parameter. This allows for defining the structure, required fields, and data types of the expected JSON output without relying on external libraries like Pydantic.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Give me information for the United States.',
    config=types.GenerateContentConfig(
        response_mime_type='application/json',
        response_schema={
            'required': [
                'name',
                'population',
                'capital',
                'continent',
                'gdp',
                'official_language',
                'total_area_sq_mi',
            ],
            'properties': {
                'name': {'type': 'STRING'},
                'population': {'type': 'INTEGER'},
                'capital': {'type': 'STRING'},
                'continent': {'type': 'STRING'},
                'gdp': {'type': 'INTEGER'},
                'official_language': {'type': 'STRING'},
                'total_area_sq_mi': {'type': 'INTEGER'},
            },
            'type': 'OBJECT',
        },
    ),
)
print(response.text)

```

----------------------------------------

TITLE: Send Asynchronous Non-Streaming Chat Messages
DESCRIPTION: Demonstrates how to send chat messages asynchronously without streaming. This approach uses `client.aio.chats.create` for an asynchronous chat session and `await chat.send_message` to send messages, suitable for non-blocking operations.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
chat = client.aio.chats.create(model='gemini-2.0-flash-001')
response = await chat.send_message('tell me a story')
print(response.text)
```

----------------------------------------

TITLE: Configure Gen AI Client for Vertex AI with v1 API Version
DESCRIPTION: Initializes the Gen AI client for Vertex AI, explicitly setting the API version to 'v1' using 'http_options'. This ensures the client interacts with the stable API endpoints.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google import genai
from google.genai import types

client = genai.Client(
    vertexai=True,
    project='your-project-id',
    location='us-central1',
    http_options=types.HttpOptions(api_version='v1')
)
```

----------------------------------------

TITLE: Retrieve Cached Content by Name
DESCRIPTION: Shows how to retrieve previously created cached content using its name via the `client.caches.get` method.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
cached_content = client.caches.get(name=cached_content.name)
```

----------------------------------------

TITLE: Delete File from Google GenAI API
DESCRIPTION: Illustrates how to delete an uploaded file from the Google GenAI API using its `name` property via `client.files.delete`. This permanently removes the file from the API's storage.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
file3 = client.files.upload(file='2312.11805v3.pdf')

client.files.delete(name=file3.name)
```

----------------------------------------

TITLE: Copy Files for Google GenAI File Management
DESCRIPTION: Provides command-line examples using `gsutil cp` to copy PDF files from a Google Cloud Storage bucket to the local environment. These files are then ready for upload to the Gemini Developer API for file-based operations.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: bash
CODE:
```
gsutil cp gs://cloud-samples-data/generative-ai/pdf/2312.11805v3.pdf .
gsutil cp gs://cloud-samples-data/generative-ai/pdf/2403.05530.pdf .
```

----------------------------------------

TITLE: Enable Automatic Function Calling with Python Functions
DESCRIPTION: Shows how to enable automatic function calling by passing a Python function directly as a tool to the GenAI model. The model can then automatically invoke this function based on the user's prompt and incorporate its return value into the response, simplifying tool usage.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
      location: The city and state, e.g. San Francisco, CA
    """
    return 'sunny'

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
    ),
)

print(response.text)
```

----------------------------------------

TITLE: Structure 'contents' Argument with 'types.Content' Instance
DESCRIPTION: Illustrates the canonical way to structure the 'contents' argument by explicitly creating a 'types.Content' instance with a role and parts, ensuring precise control over the input format.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google.genai import types

contents = types.Content(
role='user',
parts=[types.Part.from_text(text='Why is the sky blue?')]
)
```

----------------------------------------

TITLE: Configure Gen AI Client for Gemini Developer API with v1alpha Version
DESCRIPTION: Initializes the Gen AI client for the Gemini Developer API, explicitly setting the API version to 'v1alpha' using 'http_options'. This allows access to preview features.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google import genai
from google.genai import types

# Only run this block for Gemini Developer API
client = genai.Client(
    api_key='GEMINI_API_KEY',
    http_options=types.HttpOptions(api_version='v1alpha')
)
```

----------------------------------------

TITLE: Google GenAI Python API Type Definitions
DESCRIPTION: This section outlines the structure of key data types and their members found in the `genai.types` module of the Google GenAI Python library. It serves as a quick reference for understanding the available classes and their properties or enum values.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
class Modality:
  - AUDIO
  - IMAGE
  - MODALITY_UNSPECIFIED
  - TEXT

class ModalityTokenCount:
  - modality
  - token_count

class ModalityTokenCountDict:
  - modality
  - token_count

class Mode:
  - MODE_DYNAMIC
  - MODE_UNSPECIFIED

class Model:
  - checkpoints
  - default_checkpoint_id
  - description
  - display_name
  - endpoints
  - input_token_limit
  - labels
  - name
  - output_token_limit
  - supported_actions
  - tuned_model_info
  - version

class ModelContent:
  - parts
  - role

class ModelDict:
  - checkpoints
  - default_checkpoint_id
  - description
  - display_name
  - endpoints
  - input_token_limit
  - labels
  - name
  - output_token_limit
  - supported_actions
  - tuned_model_info
  - version

class ModelSelectionConfig:
  - feature_selection_preference

class ModelSelectionConfigDict:
  - feature_selection_preference

class MultiSpeakerVoiceConfig:
  - speaker_voice_configs

class MultiSpeakerVoiceConfigDict:
  - speaker_voice_configs

class Operation:
  - done
  - error
  - metadata
  - name

class OperationDict:
  - done
  - error
  - metadata
  - name

class Outcome:
  - OUTCOME_DEADLINE_EXCEEDED
  - OUTCOME_FAILED
```

----------------------------------------

TITLE: GenAI Python API Type Definitions Reference
DESCRIPTION: Comprehensive listing of data structures and enumerations used in the `genai` library, including their respective fields and values. This section details the `genai.types` module, providing a reference for configuring authentication, managing automatic activity detection, and handling batch jobs.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
AuthConfigOauthConfigDict:
  access_token
  service_account

AuthConfigOidcConfig:
  id_token
  service_account

AuthConfigOidcConfigDict:
  id_token
  service_account

AuthToken:
  name

AuthTokenDict:
  name

AuthType:
  API_KEY_AUTH
  AUTH_TYPE_UNSPECIFIED
  GOOGLE_SERVICE_ACCOUNT_AUTH
  HTTP_BASIC_AUTH
  NO_AUTH
  OAUTH
  OIDC_AUTH

AutomaticActivityDetection:
  disabled
  end_of_speech_sensitivity
  prefix_padding_ms
  silence_duration_ms
  start_of_speech_sensitivity

AutomaticActivityDetectionDict:
  disabled
  end_of_speech_sensitivity
  prefix_padding_ms
  silence_duration_ms
  start_of_speech_sensitivity

AutomaticFunctionCallingConfig:
  disable
  ignore_call_history
  maximum_remote_calls

AutomaticFunctionCallingConfigDict:
  disable
  ignore_call_history
  maximum_remote_calls

BatchJob:
  create_time
  dest
  display_name
  end_time
  error
  model
  name
  src
  start_time
  state
  update_time
```

----------------------------------------

TITLE: Google GenAI Python API Type Definitions
DESCRIPTION: This section details the structure and properties of various configuration and response types used in the Google GenAI Python library. It includes definitions for authentication, batch job, cached content, and file handling configurations, as well as their corresponding dictionary representations and response objects.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
CreateAuthTokenConfigDict:
  http_options
  live_connect_constraints
  lock_additional_fields
  new_session_expire_time
  uses
CreateAuthTokenParameters:
  config
CreateAuthTokenParametersDict:
  config
CreateBatchJobConfig:
  dest
  display_name
  http_options
CreateBatchJobConfigDict:
  dest
  display_name
  http_options
CreateCachedContentConfig:
  contents
  display_name
  expire_time
  http_options
  kms_key_name
  system_instruction
  tool_config
  tools
  ttl
CreateCachedContentConfigDict:
  contents
  display_name
  expire_time
  http_options
  kms_key_name
  system_instruction
  tool_config
  tools
  ttl
CreateFileConfig:
  http_options
  should_return_http_response
CreateFileConfigDict:
  http_options
  should_return_http_response
CreateFileResponse:
  sdk_http_response
CreateFileResponseDict:
  sdk_http_response
CreateTuningJobConfig:
```

----------------------------------------

TITLE: Google Cloud GenAI Python API Data Types and Structures
DESCRIPTION: Defines the various data structures and configuration dictionaries used across the Google Cloud GenAI Python library, including types for video generation, operation tracking, and generated media attributes.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
GenerateVideosConfigDict:
  - last_frame
  - negative_prompt
  - number_of_videos
  - output_gcs_uri
  - person_generation
  - pubsub_topic
  - resolution
  - seed
GenerateVideosOperation:
  - done
  - error
  - metadata
  - name
  - response
  - result
GenerateVideosOperationDict:
  - done
  - error
  - metadata
  - name
  - response
  - result
GenerateVideosResponse:
  - generated_videos
  - rai_media_filtered_count
  - rai_media_filtered_reasons
GenerateVideosResponseDict:
  - generated_videos
  - rai_media_filtered_count
  - rai_media_filtered_reasons
GeneratedImage:
  - enhanced_prompt
  - image
  - rai_filtered_reason
  - safety_attributes
GeneratedImageDict:
  - enhanced_prompt
  - image
  - rai_filtered_reason
  - safety_attributes
GeneratedVideo:
  - video
GeneratedVideoDict:
  - video
GenerationConfig:
  - audio_timestamp
  - candidate_count
  - frequency_penalty
  - logprobs
  - max_output_tokens
```

----------------------------------------

TITLE: API Reference for genai.types Classes and Properties
DESCRIPTION: Comprehensive API documentation for data structures and configuration objects used in the Google Cloud Generative AI Python library, specifically focusing on usage metadata for content generation and various settings for image generation.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
GenerateContentResponseUsageMetadata:
  prompt_token_count: property
  prompt_tokens_details: property
  thoughts_token_count: property
  tool_use_prompt_token_count: property
  tool_use_prompt_tokens_details: property
  total_token_count: property
  traffic_type: property

GenerateContentResponseUsageMetadataDict:
  cache_tokens_details: property
  cached_content_token_count: property
  candidates_token_count: property
  candidates_tokens_details: property
  prompt_token_count: property
  prompt_tokens_details: property
  thoughts_token_count: property
  tool_use_prompt_token_count: property
  tool_use_prompt_tokens_details: property
  total_token_count: property
  traffic_type: property

GenerateImagesConfig:
  add_watermark: property
  aspect_ratio: property
  enhance_prompt: property
  guidance_scale: property
  http_options: property
  include_rai_reason: property
  include_safety_attributes: property
  language: property
  negative_prompt: property
  number_of_images: property
  output_compression_quality: property
  output_gcs_uri: property
  output_mime_type: property
  person_generation: property
  safety_filter_level: property
  seed: property

GenerateImagesConfigDict:
  add_watermark: property
```

----------------------------------------

TITLE: Google Cloud Generative AI Python Library API Type Definitions
DESCRIPTION: This section details the various data structures and configuration objects used within the Google Cloud Generative AI Python library, specifically focusing on types related to listing batch jobs, cached contents, files, models, and tuning jobs, along with their dictionary representations. Each entry specifies a type and its associated members.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
ListBatchJobsResponse:
  next_page_token

ListBatchJobsResponseDict:
  batch_jobs
  next_page_token

ListCachedContentsConfig:
  http_options
  page_size
  page_token

ListCachedContentsConfigDict:
  http_options
  page_size
  page_token

ListCachedContentsResponse:
  cached_contents
  next_page_token

ListCachedContentsResponseDict:
  cached_contents
  next_page_token

ListFilesConfig:
  http_options
  page_size
  page_token

ListFilesConfigDict:
  http_options
  page_size
  page_token

ListFilesResponse:
  files
  next_page_token

ListFilesResponseDict:
  files
  next_page_token

ListModelsConfig:
  filter
  http_options
  page_size
  page_token
  query_base

ListModelsConfigDict:
  filter
  http_options
  page_size
  page_token
  query_base

ListModelsResponse:
  models
  next_page_token

ListModelsResponseDict:
  models
  next_page_token

ListTuningJobsConfig:
  filter
```

----------------------------------------

TITLE: Google Generative AI Python Types Reference
DESCRIPTION: Detailed API documentation for the core data types and their properties available in the `genai.types` module of the Google Generative AI Python library. This includes structures for checkpoints, citations, code execution results, token computation, content representation, and embedding statistics.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
CheckpointDict:
  checkpoint_id:
  epoch:
  step:
Citation:
  end_index:
  license:
  publication_date:
  start_index:
  title:
  uri:
CitationDict:
  end_index:
  license:
  publication_date:
  start_index:
  title:
  uri:
CitationMetadata:
  citations:
CitationMetadataDict:
  citations:
CodeExecutionResult:
  outcome:
  output:
CodeExecutionResultDict:
  outcome:
  output:
ComputeTokensConfig:
  http_options:
ComputeTokensConfigDict:
  http_options:
ComputeTokensResponse:
  tokens_info:
ComputeTokensResponseDict:
  tokens_info:
Content:
  parts:
  role:
ContentDict:
  parts:
  role:
ContentEmbedding:
  statistics:
  values:
ContentEmbeddingDict:
  statistics:
ContentEmbeddingStatistics:
  token_count:
  truncated:
ContentEmbeddingStatisticsDict:
  token_count:
  truncated:
ContextWindowCompressionConfig:
  sliding_window:
  trigger_tokens:
ContextWindowCompressionConfigDict:
  sliding_window:
  trigger_tokens:
```

----------------------------------------

TITLE: Disable Automatic Function Calling in Google GenAI
DESCRIPTION: This Python snippet demonstrates how to disable automatic function calling when using the 'ANY' tool configuration mode. By setting `automatic_function_calling.disable` to `True` within `GenerateContentConfig`, the SDK will not automatically invoke the provided tools, even if the model suggests a function call.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

def get_current_weather(location: str) -> str:
    """Returns the current weather.

    Args:
        location: The city and state, e.g. San Francisco, CA
    """
    return "sunny"

response = client.models.generate_content(
    model="gemini-2.0-flash-001",
    contents="What is the weather like in Boston?",
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
        tool_config=types.ToolConfig(
            function_calling_config=types.FunctionCallingConfig(mode='ANY')
        ),
    ),
)
```

----------------------------------------

TITLE: Manually Declare and Pass Function as Tool (Python)
DESCRIPTION: Explains how to manually define a function's schema using `google.genai.types.FunctionDeclaration` and `google.genai.types.Schema`. This declared function is then wrapped in a `types.Tool` object and passed to the model, which will return a function call part in the response for manual invocation.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

function = types.FunctionDeclaration(
    name='get_current_weather',
    description='Get the current weather in a given location',
    parameters=types.Schema(
        type='OBJECT',
        properties={
            'location': types.Schema(
                type='STRING',
                description='The city and state, e.g. San Francisco, CA',
            ),
        },
        required=['location'],
    ),
)

tool = types.Tool(function_declarations=[function])

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        tools=[tool],
    ),
)
print(response.function_calls[0])
```

----------------------------------------

TITLE: Generate Content Asynchronously (Non-Streaming)
DESCRIPTION: This example shows how to use the asynchronous version of `generate_content` via `client.aio.models.generate_content`. It awaits the full response before printing the generated text, suitable for non-streaming use cases.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
response = await client.aio.models.generate_content(
    model='gemini-2.0-flash-001', contents='Tell me a story in 300 words.'
)

print(response.text)
```

----------------------------------------

TITLE: Retrieve and Monitor Tuning Job Status
DESCRIPTION: Demonstrates how to retrieve the status of a tuning job using `client.tunings.get` and how to poll its state until it's no longer running, providing updates on its progress.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
tuning_job = client.tunings.get(name=tuning_job.name)
print(tuning_job)
```

LANGUAGE: python
CODE:
```
import time

running_states = set(
    [
        'JOB_STATE_PENDING',
        'JOB_STATE_RUNNING',
    ]
)

while tuning_job.state in running_states:
    print(tuning_job.state)
    tuning_job = client.tunings.get(name=tuning_job.name)
    time.sleep(10)
```

----------------------------------------

TITLE: Update Tuned Model Configuration (Python)
DESCRIPTION: Demonstrates how to update an existing tuned model's display name and description using the `client.models.update` method. The model object is typically retrieved from a list or pager.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
model = pager[0]

model = client.models.update(
    model=model.name,
    config=types.UpdateModelConfig(
        display_name='my tuned model', description='my tuned model description'
    ),
)

print(model)
```

----------------------------------------

TITLE: List Tuned Models Asynchronously
DESCRIPTION: Illustrates how to list tuned models asynchronously using `client.aio.models.list` with pagination and iteration. This is suitable for non-blocking operations in asynchronous applications.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
async for job in await client.aio.models.list(config={'page_size': 10, 'query_base': False}):
    print(job)
```

LANGUAGE: python
CODE:
```
async_pager = await client.aio.models.list(config={'page_size': 10, 'query_base': False})
print(async_pager.page_size)
print(async_pager[0])
await async_pager.next_page()
print(async_pager[0])
```

----------------------------------------

TITLE: Update Tuned Model Display Name and Description
DESCRIPTION: Updates the metadata (display name and description) of a tuned model using `client.models.update`. This helps in organizing and identifying models within your project.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

tuned_model = client.models.update(
    model=tuning_job.tuned_model.model,
    config=types.UpdateModelConfig(
        display_name='my tuned model', description='my tuned model description'
    ),
)
print(tuned_model)
```

----------------------------------------

TITLE: Initiate Model Fine-tuning Job
DESCRIPTION: Initiates a model fine-tuning job using `client.tunings.tune`. It takes a base model and a training dataset, along with configuration for epoch count and display name for the tuned model.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

tuning_job = client.tunings.tune(
    base_model=model,
    training_dataset=training_dataset,
    config=types.CreateTuningJobConfig(
        epoch_count=1, tuned_model_display_name='test_dataset_examples model'
    ),
)
print(tuning_job)
```

----------------------------------------

TITLE: List Tuned Models Synchronously
DESCRIPTION: Demonstrates how to list tuned models synchronously using `client.models.list` with pagination configuration. It shows iterating through models and accessing pager properties for sequential retrieval.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
for model in client.models.list(config={'page_size': 10, 'query_base': False}):
    print(model)
```

LANGUAGE: python
CODE:
```
pager = client.models.list(config={'page_size': 10, 'query_base': False})
print(pager.page_size)
print(pager[0])
pager.next_page()
print(pager[0])
```

----------------------------------------

TITLE: Stream Content with Image Input from Google Cloud Storage
DESCRIPTION: This example demonstrates how to include an image from Google Cloud Storage as part of the input for content generation. It uses `types.Part.from_uri` to reference the image and streams the model's text response.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

for chunk in client.models.generate_content_stream(
    model='gemini-2.0-flash-001',
    contents=[
        'What is this image about?',
        types.Part.from_uri(
            file_uri='gs://generativeai-downloads/images/scones.jpg',
            mime_type='image/jpeg',
        ),
    ],
):
    print(chunk.text, end='')
```

----------------------------------------

TITLE: Define and Convert Single Non-Function Call Part to UserContent (Python)
DESCRIPTION: Demonstrates creating a single content part from a URI (e.g., an image) using `types.Part.from_uri` and illustrates how the Google GenAI SDK converts this into a `types.UserContent` object with a 'user' role, suitable for user input.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google.genai import types

contents = types.Part.from_uri(
file_uri: 'gs://generativeai-downloads/images/scones.jpg',
mime_type: 'image/jpeg',
)
```

LANGUAGE: Python
CODE:
```
[
types.UserContent(parts=[
    types.Part.from_uri(
    file_uri: 'gs://generativeai-downloads/images/scones.jpg',
    mime_type: 'image/jpeg',
    )
])
]
```

----------------------------------------

TITLE: Configure Safety Settings for Content Generation (Python)
DESCRIPTION: Demonstrates how to apply safety settings to content generation requests using `google.genai.types.SafetySetting`. This allows specifying categories (e.g., HARM_CATEGORY_HATE_SPEECH) and thresholds (e.g., BLOCK_ONLY_HIGH) to control the type of content generated or blocked by the model.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='Say something bad.',
    config=types.GenerateContentConfig(
        safety_settings=[
            types.SafetySetting(
                category='HARM_CATEGORY_HATE_SPEECH',
                threshold='BLOCK_ONLY_HIGH',
            )
        ]
    ),
)
print(response.text)
```

----------------------------------------

TITLE: TunedModelInfo Type Definition
DESCRIPTION: Provides information about a tuned model, such as its base model, creation, and update times.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
TunedModelInfo:
  base_model
  create_time
  update_time
```

----------------------------------------

TITLE: SupervisedTuningSpec API Reference
DESCRIPTION: Specifies the configuration for a supervised tuning job, including options for exporting checkpoints, hyperparameters, and URIs for training and validation datasets.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
SupervisedTuningSpec:
  export_last_checkpoint_only
  hyper_parameters
  training_dataset_uri
  validation_dataset_uri
```

----------------------------------------

TITLE: SupervisedTuningSpecDict API Reference
DESCRIPTION: Defines a dictionary-like structure for the configuration of a supervised tuning job, including options for exporting checkpoints and hyperparameters.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
SupervisedTuningSpecDict:
  export_last_checkpoint_only
  hyper_parameters
```

----------------------------------------

TITLE: TunedModelDict Type Definition
DESCRIPTION: Dictionary representation of a tuned model, including its checkpoints, endpoint, and base model information.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
TunedModelDict:
  checkpoints
  endpoint
  model
```

----------------------------------------

TITLE: TunedModel Type Definition
DESCRIPTION: Describes a tuned model, including its checkpoints, endpoint, and base model information.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
TunedModel:
  checkpoints
  endpoint
  model
```

----------------------------------------

TITLE: Configure Model Generation with Advanced Typed Parameters (Python)
DESCRIPTION: Shows how to use `types.GenerateContentConfig` with a comprehensive set of parameters like `temperature`, `top_p`, `top_k`, `candidate_count`, `seed`, `max_output_tokens`, `stop_sequences`, `presence_penalty`, and `frequency_penalty` for fine-grained control over model response generation.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=types.Part.from_text(text='Why is the sky blue?'),
    config=types.GenerateContentConfig(
        temperature=0,
        top_p=0.95,
        top_k=20,
        candidate_count=1,
        seed=5,
        max_output_tokens=100,
        stop_sequences=['STOP!'],
        presence_penalty=0.0,
        frequency_penalty=0.0,
    ),
)

print(response.text)
```

----------------------------------------

TITLE: Stream Text Content Synchronously from Gemini Model
DESCRIPTION: This snippet shows how to stream text responses from the Gemini model. The `generate_content_stream` method returns chunks of text as they are generated, allowing for real-time display of the model's output.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
for chunk in client.models.generate_content_stream(
    model='gemini-2.0-flash-001', contents='Tell me a story in 300 words.'
):
    print(chunk.text, end='')
```

----------------------------------------

TITLE: Disable Automatic Function Calling for GenAI Models (Python)
DESCRIPTION: Illustrates how to explicitly disable automatic function calling when passing a Python function as a tool. By setting `automatic_function_calling.disable=True`, the model will return a list of function call parts in the response instead of directly invoking the function, allowing for manual handling.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents='What is the weather like in Boston?',
    config=types.GenerateContentConfig(
        tools=[get_current_weather],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        ),
    ),
)
```

----------------------------------------

TITLE: API Definition: UpscaleImageParameters Type
DESCRIPTION: API definition for the UpscaleImageParameters type, detailing its structure and members within the `genai` library.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
UpscaleImageParameters
  .image
  .model
  .upscale_factor
```

----------------------------------------

TITLE: API Definition: UpscaleImageParametersDict Type
DESCRIPTION: API definition for the UpscaleImageParametersDict type, detailing its structure and members within the `genai` library.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
UpscaleImageParametersDict
  .config
  .image
  .model
  .upscale_factor
```

----------------------------------------

TITLE: Define SubjectReferenceImageDict Type (APIDOC)
DESCRIPTION: Documents the `SubjectReferenceImageDict` type, a dictionary representation of `SubjectReferenceImage`, detailing its `config`, `reference_id`, and `reference_image` properties.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
SubjectReferenceImageDict:
  config
  reference_id
  reference_image
```

----------------------------------------

TITLE: Define SubjectReferenceConfig Type (APIDOC)
DESCRIPTION: Documents the `SubjectReferenceConfig` type, used for configuring subject references. It includes properties for `subject_description` and `subject_type`.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
SubjectReferenceConfig:
  subject_description
  subject_type
```

----------------------------------------

TITLE: Define StyleReferenceImageDict Type (APIDOC)
DESCRIPTION: Documents the `StyleReferenceImageDict` type, a dictionary representation of `StyleReferenceImage`, detailing its `config`, `reference_id`, `reference_image`, and `reference_type` properties.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
StyleReferenceImageDict:
  config
  reference_id
  reference_image
  reference_type
```

----------------------------------------

TITLE: SDK Conversion of 'types.Content' Instance for 'contents'
DESCRIPTION: Shows how the SDK internally converts a single 'types.Content' instance into a list containing that instance when used as the 'contents' argument.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
[
types.Content(
    role='user',
    parts=[types.Part.from_text(text='Why is the sky blue?')]
)
]
```

----------------------------------------

TITLE: Define StyleReferenceImage Type (APIDOC)
DESCRIPTION: Documents the `StyleReferenceImage` type, which specifies how to reference an image for style. It includes properties for `config`, `reference_id`, `reference_image`, `reference_type`, and `style_image_config`.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
StyleReferenceImage:
  config
  reference_id
  reference_image
  reference_type
  style_image_config
```

----------------------------------------

TITLE: Generate Images with Google GenAI Python Client
DESCRIPTION: Demonstrates how to generate an image using the `client.models.generate_images` method. It specifies the model, a descriptive prompt, and configuration options like the number of images and output MIME type. The generated image is then displayed.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
response1 = client.models.generate_images(
    model='imagen-3.0-generate-002',
    prompt='An umbrella in the foreground, and a rainy night sky in the background',
    config=types.GenerateImagesConfig(
        number_of_images=1,
        include_rai_reason=True,
        output_mime_type='image/jpeg',
    ),
)
response1.generated_images[0].image.show()
```

----------------------------------------

TITLE: Generate Content with Uploaded File using Gemini API
DESCRIPTION: Demonstrates the process of uploading a local file using 'client.files.upload' and then incorporating the uploaded file into the 'contents' argument for 'client.models.generate_content' to summarize its content.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: Python
CODE:
```
file = client.files.upload(file='a11.txt')
response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=['Could you summarize this file?', file]
)
print(response.text)
```

----------------------------------------

TITLE: Invoke Declared Function and Pass Response to Model (Python)
DESCRIPTION: Details the process of receiving a function call part from the model, extracting its arguments, invoking the corresponding Python function, and then passing the function's result back to the model. This allows for a multi-turn conversation where the model can use the function's output to generate a more informed response.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: python
CODE:
```
from google.genai import types

user_prompt_content = types.Content(
    role='user',
    parts=[types.Part.from_text(text='What is the weather like in Boston?')],
)
function_call_part = response.function_calls[0]
function_call_content = response.candidates[0].content

try:
    function_result = get_current_weather(
        **function_call_part.function_call.args
    )
    function_response = {'result': function_result}
except (
    Exception
) as e:  # instead of raising the exception, you can let the model handle it
    function_response = {'error': str(e)}

function_response_part = types.Part.from_function_response(
    name=function_call_part.name,
    response=function_response,
)
function_response_content = types.Content(
    role='tool', parts=[function_response_part]
)

response = client.models.generate_content(
    model='gemini-2.0-flash-001',
    contents=[
        user_prompt_content,
        function_call_content,
        function_response_content,
    ],
    config=types.GenerateContentConfig(
        tools=[tool],
    ),
)

print(response.text)
```

----------------------------------------

TITLE: API Reference for MediaModality Enum
DESCRIPTION: Defines the enumeration for various media modalities supported, including audio, document, image, text, and video.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
MediaModality:
  AUDIO
  DOCUMENT
  IMAGE
  MODALITY_UNSPECIFIED
  TEXT
  VIDEO
```

----------------------------------------

TITLE: API Reference for genai.types.PartnerModelTuningSpecDict
DESCRIPTION: Documents the structure and members of the `PartnerModelTuningSpecDict` type within the `genai.types` module, likely a dictionary representation of `PartnerModelTuningSpec`.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
PartnerModelTuningSpecDict:
  hyper_parameters
  training_dataset_uri
  validation_dataset_uri
```

----------------------------------------

TITLE: Define SlidingWindowDict Type (APIDOC)
DESCRIPTION: Documents the `SlidingWindowDict` type, which is likely a dictionary representation of the `SlidingWindow` configuration, including its `target_tokens` property.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
SlidingWindowDict:
  target_tokens
```

----------------------------------------

TITLE: API Reference for genai.types.ProactivityConfig
DESCRIPTION: Documents the structure and members of the `ProactivityConfig` type within the `genai.types` module, configuring proactivity settings.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
ProactivityConfig:
  proactive_audio
```

----------------------------------------

TITLE: API Reference for MediaResolution Enum
DESCRIPTION: Defines the enumeration for different media resolutions, such as high, low, and medium.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
MediaResolution:
  MEDIA_RESOLUTION_HIGH
  MEDIA_RESOLUTION_LOW
  MEDIA_RESOLUTION_MEDIUM
  MEDIA_RESOLUTION_UNSPECIFIED
```

----------------------------------------

TITLE: API Reference for ListBatchJobsResponse Type
DESCRIPTION: The response object returned when listing batch jobs. It contains a list of the batch jobs that match the query criteria.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
ListBatchJobsResponse:
  batch_jobs
```

----------------------------------------

TITLE: LiveMusicClientMessage API Reference
DESCRIPTION: Defines a client message structure for LiveMusic, encompassing client content, music generation configuration, playback controls, and setup information.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
LiveMusicClientMessage:
  client_content
  music_generation_config
  playback_control
  setup
```

----------------------------------------

TITLE: API Reference for SubjectReferenceType
DESCRIPTION: Defines the SubjectReferenceType enum or class, specifying different categories of subjects that can be referenced.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
SubjectReferenceType:
  SUBJECT_TYPE_ANIMAL
  SUBJECT_TYPE_DEFAULT
  SUBJECT_TYPE_PERSON
  SUBJECT_TYPE_PRODUCT
```

----------------------------------------

TITLE: API Reference for genai.types.PrebuiltVoiceConfig
DESCRIPTION: Documents the structure and members of the `PrebuiltVoiceConfig` type within the `genai.types` module, configuring options for prebuilt voices.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
PrebuiltVoiceConfig:
  voice_name
```

----------------------------------------

TITLE: API Definition for SafetySettingDict
DESCRIPTION: Defines the dictionary representation of `SafetySetting`. This type mirrors the `SafetySetting` class, providing a dictionary-based structure for configuring safety preferences, including `category`, `method`, and `threshold`.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
SafetySettingDict:
  category
  method
  threshold
```

----------------------------------------

TITLE: API Reference for MaskReferenceConfig Type
DESCRIPTION: Defines configuration parameters for mask references, including mask dilation, mode, and segmentation classes.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
MaskReferenceConfig:
  mask_dilation
  mask_mode
  segmentation_classes
```

----------------------------------------

TITLE: LiveMusicConnectParameters API Reference
DESCRIPTION: Defines parameters for connecting to the LiveMusic service, primarily specifying the model.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
LiveMusicConnectParameters:
  model
```

----------------------------------------

TITLE: API Reference for MaskReferenceImage Type
DESCRIPTION: Defines the structure for an image used as a mask reference, including its configuration, image-specific mask config, reference ID, image data, and type.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
MaskReferenceImage:
  config
  mask_image_config
  reference_id
  reference_image
  reference_type
```

----------------------------------------

TITLE: Define SlidingWindow Type (APIDOC)
DESCRIPTION: Documents the `SlidingWindow` type, which likely represents a configuration for a sliding window mechanism, specifically detailing its `target_tokens` property.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
SlidingWindow:
  target_tokens
```

----------------------------------------

TITLE: API Reference for genai.types.ProactivityConfigDict
DESCRIPTION: Documents the structure and members of the `ProactivityConfigDict` type within the `genai.types` module, likely a dictionary representation of `ProactivityConfig`.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
ProactivityConfigDict:
  proactive_audio
```

----------------------------------------

TITLE: AudioTranscriptionConfig Type Definition
DESCRIPTION: Represents the configuration settings for audio transcription processes.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
AudioTranscriptionConfig:
```

----------------------------------------

TITLE: API Reference for LiveMusicSetConfigParameters
DESCRIPTION: A type used to set configuration parameters for live music, likely without specific members detailed in this snippet.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
LiveMusicSetConfigParameters:
```

----------------------------------------

TITLE: API Reference for LiveMusicServerMessageDict
DESCRIPTION: Defines the dictionary-like structure for `LiveMusicServerMessage`, providing a mutable or serializable representation of server messages.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
LiveMusicServerMessageDict:
  - filtered_prompt
  - server_content
  - setup_complete
```

----------------------------------------

TITLE: FileStatus Type Definition
DESCRIPTION: Defines the structure for `FileStatus` within the `genai.types` module, typically used to convey status information including a code, details, and a message.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
FileStatus:
  code
  details
  message
```

----------------------------------------

TITLE: API Reference for LiveMusicPlaybackControl
DESCRIPTION: Defines an enumeration of control commands for live music playback, such as pause, play, stop, and reset context.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
LiveMusicPlaybackControl:
  - PAUSE
  - PLAY
  - PLAYBACK_CONTROL_UNSPECIFIED
  - RESET_CONTEXT
  - STOP
```

----------------------------------------

TITLE: API Documentation for CachedContentUsageMetadata
DESCRIPTION: Defines the structure and members of the `CachedContentUsageMetadata` type within the `genai` library. This type captures usage statistics for cached content.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
CachedContentUsageMetadata:
  audio_duration_seconds
  image_count
  text_count
  total_token_count
  video_duration_seconds
```

----------------------------------------

TITLE: AudioChunkDict Type Definition
DESCRIPTION: Represents the dictionary definition for the `AudioChunkDict` type, a dictionary representation of `AudioChunk`.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
AudioChunkDict:
  data
  mime_type
  source_metadata
```

----------------------------------------

TITLE: LiveConnectConfigDict API Reference
DESCRIPTION: Defines a dictionary of configuration options for the LiveConnect feature, including settings for audio transcription, proactivity, real-time input, response modalities, and model parameters like temperature and top-k/top-p sampling.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
LiveConnectConfigDict:
  output_audio_transcription
  proactivity
  realtime_input_config
  response_modalities
  seed
  session_resumption
  speech_config
  system_instruction
  temperature
  tools
  top_k
  top_p
```

----------------------------------------

TITLE: API Reference for MaskReferenceConfigDict Type
DESCRIPTION: Defines the dictionary representation of mask reference configuration, including mask dilation, mode, and segmentation classes.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
MaskReferenceConfigDict:
  mask_dilation
  mask_mode
  segmentation_classes
```

----------------------------------------

TITLE: GenAI Python Live Music and Real-time Input API Types
DESCRIPTION: This section details the various Python types (classes and their corresponding dictionary representations) used for configuring live music generation, setting weighted prompts, managing source metadata, sending real-time input, and handling server content within the `genai` library. Each type lists its available attributes.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
LiveMusicSetConfigParameters:
  music_generation_config
LiveMusicSetConfigParametersDict:
  music_generation_config
LiveMusicSetWeightedPromptsParameters:
  weighted_prompts
LiveMusicSetWeightedPromptsParametersDict:
  weighted_prompts
LiveMusicSourceMetadata:
  client_content
  music_generation_config
LiveMusicSourceMetadataDict:
  client_content
  music_generation_config
LiveSendRealtimeInputParameters:
  activity_end
  activity_start
  audio
  audio_stream_end
  media
  text
  video
LiveSendRealtimeInputParametersDict:
  activity_end
  activity_start
  audio
  audio_stream_end
  media
  text
  video
LiveServerContent:
  generation_complete
  grounding_metadata
  input_transcription
  interrupted
  model_turn
  output_transcription
  turn_complete
  url_context_metadata
LiveServerContentDict:
  generation_complete
  grounding_metadata
  input_transcription
  interrupted
```

----------------------------------------

TITLE: API Reference for DeleteModelConfigDict Type
DESCRIPTION: Defines the dictionary-based configuration options for deleting a model, including HTTP options, within the Google Cloud Generative AI Python library.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
DeleteModelConfigDict:
  - http_options
```

----------------------------------------

TITLE: API Reference for DeleteModelResponseDict Type
DESCRIPTION: Defines the dictionary-based response structure for a delete model operation within the Google Cloud Generative AI Python library.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
DeleteModelResponseDict:
```

----------------------------------------

TITLE: API Reference for LogprobsResultTopCandidates Type
DESCRIPTION: Defines the structure for a collection of top log probability candidates.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
LogprobsResultTopCandidates:
  candidates
```

----------------------------------------

TITLE: FileDataDict Type Definition
DESCRIPTION: Defines the structure and attributes for the `FileDataDict` type within the `genai.types` module, typically used for representing file metadata.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
FileDataDict:
  display_name
  file_uri
  mime_type
```

----------------------------------------

TITLE: API Documentation for CandidateDict
DESCRIPTION: Defines the structure and members of the `CandidateDict` type within the `genai` library. This dictionary-like type represents a generated candidate response from a model.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
CandidateDict:
  avg_logprobs
  citation_metadata
  content
  finish_message
  finish_reason
  grounding_metadata
  index
  logprobs_result
  safety_ratings
  token_count
  url_context_metadata
```

----------------------------------------

TITLE: DistillationDataStatsDict API Reference
DESCRIPTION: API documentation for the `DistillationDataStatsDict` type, detailing its attributes related to distillation data statistics within the Google GenAI library.
SOURCE: https://googleapis.github.io/python-genai/index

LANGUAGE: APIDOC
CODE:
```
DistillationDataStatsDict:
  training_dataset_stats
```