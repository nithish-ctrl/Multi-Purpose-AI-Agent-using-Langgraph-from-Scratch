from langchain_core.tools import tool
from model import load_model

@tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return "Sunny"

llm = load_model().bind_tools([get_weather])

response = llm.invoke(
    "What's the weather in Mumbai? Use the tool."
)

print(response)
print(response.tool_calls)
print(response.additional_kwargs)