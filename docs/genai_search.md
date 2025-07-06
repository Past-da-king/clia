Skip to main content
Google AI for Developers
Models

Solutions
Code assistance
More
Search
/


English

Ayanda
Gemini API docs
API Reference
Cookbook
Community

Introducing updates to our 2.5 family of thinking models. Learn more
Home
Gemini API
Models
Was this helpful?

Send feedbackURL context

Experimental: The URL context tool is an experimental feature.
Using the URL context tool, you can provide Gemini with URLs as additional context for your prompt. The model can then retrieve content from the URLs and use that content to inform and shape its response.

This tool is useful for tasks like the following:

Extracting key data points or talking points from articles
Comparing information across multiple links
Synthesizing data from several sources
Answering questions based on the content of a specific page or pages
Analyzing content for specific purposes (like writing a job description or creating test questions)
This guide explains how to use the URL context tool in the Gemini API.

Use URL context
You can use the URL context tool in two main ways, by itself or in conjunction with Grounding with Google Search.

URL Context Only

You provide specific URLs that you want the model to analyze directly in your prompt.

Example prompts:

Summarize this document: YOUR_URLs

Extract the key features from the product description on this page: YOUR_URLs
Grounding with Google Search + URL Context

You can also enable both URL context and Grounding with Google Search together. You can enter a prompt with or without URLs. The model may first search for relevant information and then use the URL context tool to read the content of the search results for a more in-depth understanding.

Example prompts:

Give me three day events schedule based on YOUR_URL. Also let me know what needs to taken care of considering weather and commute.

Recommend 3 books for beginners to read to learn more about the latest YOUR_subject.
Code examples with URL context only
Python
Javascript
REST
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

client = genai.Client()
model_id = "gemini-2.5-flash"

url_context_tool = Tool(
    url_context = types.UrlContext
)

response = client.models.generate_content(
    model=model_id,
    contents="Compare recipes from YOUR_URL1 and YOUR_URL2",
    config=GenerateContentConfig(
        tools=[url_context_tool],
        response_modalities=["TEXT"],
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)
# get URLs retrieved for context
print(response.candidates[0].url_context_metadata)

Code examples with Grounding with Google Search
Python
Javascript
REST
from google import genai
from google.genai.types import Tool, GenerateContentConfig, GoogleSearch

client = genai.Client()
model_id = "gemini-2.5-flash"

tools = []
tools.append(Tool(url_context=types.UrlContext))
tools.append(Tool(google_search=types.GoogleSearch))

response = client.models.generate_content(
    model=model_id,
    contents="Give me three day events schedule based on YOUR_URL. Also let me know what needs to taken care of considering weather and commute.",
    config=GenerateContentConfig(
        tools=tools,
        response_modalities=["TEXT"],
    )
)

for each in response.candidates[0].content.parts:
    print(each.text)
# get URLs retrieved for context
print(response.candidates[0].url_context_metadata)

For more details about Grounding with Google Search, see the overview page.

Contextual response
The model's response will be based on the content it retrieved from the URLs. If the model retrieved content from URLs, the response will include url_context_metadata. Such a response might look something like the following (parts of the response have been omitted for brevity):

{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "... \n"
          }
        ],
        "role": "model"
      },
      ...
      "url_context_metadata":
      {
          "url_metadata":
          [
            {
              "retrieved_url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/1234567890abcdef",
              "url_retrieval_status": <UrlRetrievalStatus.URL_RETRIEVAL_STATUS_SUCCESS: "URL_RETRIEVAL_STATUS_SUCCESS">
            },
            {
              "retrieved_url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/abcdef1234567890",
              "url_retrieval_status": <UrlRetrievalStatus.URL_RETRIEVAL_STATUS_SUCCESS: "URL_RETRIEVAL_STATUS_SUCCESS">
            },
            {
              "retrieved_url": "YOUR_URL",
              "url_retrieval_status": <UrlRetrievalStatus.URL_RETRIEVAL_STATUS_SUCCESS: "URL_RETRIEVAL_STATUS_SUCCESS">
            },
            {
              "retrieved_url": "https://vertexaisearch.cloud.google.com/grounding-api-redirect/fedcba0987654321",
              "url_retrieval_status": <UrlRetrievalStatus.URL_RETRIEVAL_STATUS_SUCCESS: "URL_RETRIEVAL_STATUS_SUCCESS">
            }
          ]
        }
    }
}
Supported models
gemini-2.5-pro
gemini-2.5-flash
gemini-2.5-flash-lite
gemini-2.0-flash
gemini-2.0-flash-live-001
Limitations
The tool will consume up to 20 URLs per request for analysis.
For best results during experimental phase, use the tool on standard web pages rather than multimedia content such as YouTube videos.
During experimental phase, the tool is free to use. Billing to come later.
The experimental release has the following quotas:

1500 queries per day per project for requests made through the Gemini API
100 queries per day per user in Google AI Studio


Grounding with Google Search

Grounding with Google Search connects the Gemini model to real-time web content and works with all available languages. This allows Gemini to provide more accurate answers and cite verifiable sources beyond its knowledge cutoff.

Grounding helps you build applications that can:

Increase factual accuracy: Reduce model hallucinations by basing responses on real-world information.
Access real-time information: Answer questions about recent events and topics.
Provide citations: Build user trust by showing the sources for the model's claims.

Python
JavaScript
REST

from google import genai
from google.genai import types

# Configure the client
client = genai.Client()

# Define the grounding tool
grounding_tool = types.Tool(
    google_search=types.GoogleSearch()
)

# Configure generation settings
config = types.GenerateContentConfig(
    tools=[grounding_tool]
)

# Make the request
response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Who won the euro 2024?",
    config=config,
)

# Print the grounded response
print(response.text)
You can learn more by trying the Search tool notebook.

How grounding with Google Search works
When you enable the google_search tool, the model handles the entire workflow of searching, processing, and citing information automatically.

grounding-overview

User Prompt: Your application sends a user's prompt to the Gemini API with the google_search tool enabled.
Prompt Analysis: The model analyzes the prompt and determines if a Google Search can improve the answer.
Google Search: If needed, the model automatically generates one or multiple search queries and executes them.
Search Results Processing: The model processes the search results, synthesizes the information, and formulates a response.
Grounded Response: The API returns a final, user-friendly response that is grounded in the search results. This response includes the model's text answer and groundingMetadata with the search queries, web results, and citations.
Understanding the Grounding Response
When a response is successfully grounded, the response includes a groundingMetadata field. This structured data is essential for verifying claims and building a rich citation experience in your application.


{
  "candidates": [
    {
      "content": {
        "parts": [
          {
            "text": "Spain won Euro 2024, defeating England 2-1 in the final. This victory marks Spain's record fourth European Championship title."
          }
        ],
        "role": "model"
      },
      "groundingMetadata": {
        "webSearchQueries": [
          "UEFA Euro 2024 winner",
          "who won euro 2024"
        ],
        "searchEntryPoint": {
          "renderedContent": "<!-- HTML and CSS for the search widget -->"
        },
        "groundingChunks": [
          {"web": {"uri": "https://vertexaisearch.cloud.google.com.....", "title": "aljazeera.com"}},
          {"web": {"uri": "https://vertexaisearch.cloud.google.com.....", "title": "uefa.com"}}
        ],
        "groundingSupports": [
          {
            "segment": {"startIndex": 0, "endIndex": 85, "text": "Spain won Euro 2024, defeatin..."},
            "groundingChunkIndices": [0]
          },
          {
            "segment": {"startIndex": 86, "endIndex": 210, "text": "This victory marks Spain's..."},
            "groundingChunkIndices": [0, 1]
          }
        ]
      }
    }
  ]
}
The Gemini API returns the following information with the groundingMetadata:

webSearchQueries : Array of the search queries used. This is useful for debugging and understanding the model's reasoning process.
searchEntryPoint : Contains the HTML and CSS to render the required Search Suggestions. Full usage requirements are detailed in the Terms of Service.
groundingChunks : Array of objects containing the web sources (uri and title).
groundingSupports : Array of chunks to connect model response text to the sources in groundingChunks. Each chunk links a text segment (defined by startIndex and endIndex) to one or more groundingChunkIndices. This is the key to building inline citations.
Grounding with Google Search can also be used in combination with the URL context tool to ground responses in both public web data and the specific URLs you provide.

Attributing Sources with inline Citations
The API returns structured citation data, giving you complete control over how you display sources in your user interface. You can use the groundingSupports and groundingChunks fields to link the model's statements directly to their sources. Here is a common pattern for processing the metadata to create a response with inline, clickable citations.

Python
JavaScript

def add_citations(response):
    text = response.text
    supports = response.candidates[0].grounding_metadata.grounding_supports
    chunks = response.candidates[0].grounding_metadata.grounding_chunks

    # Sort supports by end_index in descending order to avoid shifting issues when inserting.
    sorted_supports = sorted(supports, key=lambda s: s.segment.end_index, reverse=True)

    for support in sorted_supports:
        end_index = support.segment.end_index
        if support.grounding_chunk_indices:
            # Create citation string like [1](link1)[2](link2)
            citation_links = []
            for i in support.grounding_chunk_indices:
                if i < len(chunks):
                    uri = chunks[i].web.uri
                    citation_links.append(f"[{i + 1}]({uri})")

            citation_string = ", ".join(citation_links)
            text = text[:end_index] + citation_string + text[end_index:]

    return text

# Assuming response with grounding metadata
text_with_citations = add_citations(response)
print(text_with_citations)

Spain won Euro 2024, defeating England 2-1 in the final.[1](https:/...), [2](https:/...), [4](https:/...), [5](https:/...) This victory marks Spain's record-breaking fourth European Championship title.[5]((https:/...), [2](https:/...), [3](https:/...), [4](https:/...)
Pricing
When you use Grounding with Google Search, your project is billed per API request that includes the google_search tool. If the model decides to execute multiple search queries to answer a single prompt (for example, searching for "UEFA Euro 2024 winner" and "Spain vs England Euro 2024 final score" within the same API call), this counts as a single billable use of the tool for that request.

For detailed pricing information, see the Gemini API pricing page.

Supported Models
Experimental and Preview models are not included. You can find their capabilities on the model overview page.

Model	Grounding with Google Search
Gemini 2.5 Pro	✔️
Gemini 2.5 Flash	✔️
Gemini 2.0 Flash	✔️
Gemini 1.5 Pro	✔️
Gemini 1.5 Flash	✔️
Note: Older models use a google_search_retrieval tool. For all current models, use the google_search tool as shown in the examples.
Grounding with Gemini 1.5 Models (Legacy)
While the google_search tool is recommended for Gemini 2.0 and later, Gemini 1.5 support a legacy tool named google_search_retrieval. This tool provides a dynamic mode that allows the model to decide whether to perform a search based on its confidence that the prompt requires fresh information. If the model's confidence is above a dynamic_threshold you set (a value between 0.0 and 1.0), it will perform a search.

Python
JavaScript
REST

# Note: This is a legacy approach for Gemini 1.5 models.
# The 'google_search' tool is recommended for all new development.
import os
from google import genai
from google.genai import types

client = genai.Client()

retrieval_tool = types.Tool(
    google_search_retrieval=types.GoogleSearchRetrieval(
        dynamic_retrieval_config=types.DynamicRetrievalConfig(
            mode=types.DynamicRetrievalConfigMode.MODE_DYNAMIC,
            dynamic_threshold=0.7 # Only search if confidence > 70%
        )
    )
)

config = types.GenerateContentConfig(
    tools=[retrieval_tool]
)

response = client.models.generate_content(
    model='gemini-1.5-flash',
    contents="Who won the euro 2024?",
    config=config,
)
print(response.text)
if not response.candidates[0].grounding_metadata:
  print("\nModel answered from its own knowledge.")