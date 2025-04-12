import os
from openai import OpenAI
from pprint import pprint
from tool_bank import *
from tool_decorator import *
from utils import *

class Agent:
    def __init__(self):
        """Initialize Agent with empty tool registry."""
        self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.tools: dict[str, Tool] = {}
        self.model = 'deepseek-chat'

    def add_tools(self, tool: Tool) -> None:
        """Register a new tool with the agent."""
        self.tools[tool.name] = tool

    def use_tool(self, tool_name: str, **kwargs: Any) -> str:
        """Execute a specific tool with given arguments."""
        if tool_name not in self.tools:
            raise ValueError(f"Tool '{tool_name}' not found. Available tools: {list(self.tools.keys())}")
        
        tool = self.tools[tool_name]
        return tool.func(**kwargs)
    
    def create_system_prompt(self) -> str:
        """Create the system prompt for the LLM with available tools."""
        
        tools_json = {
            "role": "AI Assistant",
            "capabilities": [
                "Using provided tools to help users when necessary",
                "Responding directly without tools for questions that don't require tool usage",
                "Planning efficient tool usage sequences"
            ],
            "instructions": [
                "Use tools only when they are necessary for the task",
                "If a query can be answered directly, respond with a simple message instead of using tools",
                "When tools are needed, plan their usage efficiently to minimize tool calls"
            ],
            "tools": [
                {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": {
                        name: {
                            "type": info["type"],
                            "description": info["description"]
                        }
                        for name, info in tool.parameters.items()
                    }
                }
                for tool in self.tools.values()
            ],
            "response_format": {
                "type": "json",
                "schema": {
                    "requires_tools": {
                        "type": "boolean",
                        "description": "whether tools are needed for this query"
                    },
                    "direct_response": {
                        "type": "string",
                        "description": "response when no tools are needed",
                        "optional": True
                    },
                    "thought": {
                        "type": "string", 
                        "description": "reasoning about how to solve the task (when tools are needed)",
                        "optional": True
                    },
                    "plan": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "steps to solve the task (when tools are needed)",
                        "optional": True
                    },
                    "tool_calls": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "tool": {
                                    "type": "string",
                                    "description": "name of the tool"
                                },
                                "args": {
                                    "type": "object",
                                    "description": "parameters for the tool"
                                }
                            }
                        },
                        "description": "tools to call in sequence (when tools are needed)",
                        "optional": True
                    }
                },
                "examples": [
                    {
                        "query": "Convert 100 USD to EUR",
                        "response": {
                            "requires_tools": True,
                            "thought": "I need to use the currency conversion tool to convert USD to EUR",
                            "plan": [
                                "Use convert_currency tool to convert 100 USD to EUR",
                                "Return the conversion result"
                            ],
                            "tool_calls": [
                                {
                                    "tool": "convert_currency",
                                    "args": {
                                        "amount": 100,
                                        "from_currency": "USD", 
                                        "to_currency": "EUR"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "query": "What's 500 Japanese Yen in British Pounds?",
                        "response": {
                            "requires_tools": True,
                            "thought": "I need to convert JPY to GBP using the currency converter",
                            "plan": [
                                "Use convert_currency tool to convert 500 JPY to GBP",
                                "Return the conversion result"
                            ],
                            "tool_calls": [
                                {
                                    "tool": "convert_currency",
                                    "args": {
                                        "amount": 500,
                                        "from_currency": "JPY",
                                        "to_currency": "GBP"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "query": "What currency does Japan use?",
                        "response": {
                            "requires_tools": False,
                            "direct_response": "Japan uses the Japanese Yen (JPY) as its official currency. This is common knowledge that doesn't require using the currency conversion tool."
                        }
                    }
                ]
            }
        }
        
        return f"""You are an AI assistant that helps users by providing direct answers or using tools when necessary.
Configuration, instructions, and available tools are provided in JSON format below:

{json.dumps(tools_json, indent=2)}

Always respond with a JSON object following the response_format schema above. 
Remember to use tools only when they are actually needed for the task."""
    
    def get_agent_response(self, user_query: str) -> str:

        message = [
                {"role": "system", "content": self.create_system_prompt()},
                {"role": "user", "content": user_query}
                ]
        
        response = call_llm(self.client, message, model=self.model, temperature=0)
        return extract_json_block(response)

        
    def execute(self, user_query: str) -> str:
        """Execute the full pipeline: plan and execute tools."""
        
        response = self.get_agent_response(user_query)
        pprint("Response:")
        pprint(response)

        # If agent decide not to use tools, directly return response    
        if not response.get("requires_tools", True):
            return response["direct_response"]
        
        # Else, excetue tools in sequence:
        results = []
        for tool_call in response['tool_calls']:
            tool_name = tool_call['tool']
            tool_args = tool_call['args']
            result = self.use_tool(tool_name, **tool_args)
            results.append(result)

        # Combine results
        return f"""Thought: {response['thought']}\nPlan: {'. '.join(response['plan'])}\nResults: {'. '.join(results)}"""          

            
if __name__ == "__main__":
    agent = Agent()
    agent.add_tools(convert_currency)

    query_list = ["I am traveling to Japan from Serbia, I have 1500 of local currency, how much of Japanese currency will I be able to get?",
                    "How are you doing?"]

    for query in query_list:
        print(f"\nQuery: {query}")
        result = agent.execute(query)
        print(result)