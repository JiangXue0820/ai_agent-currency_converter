import os
from openai import OpenAI
from pprint import pprint
from utils import *
from typing import List, Any
from modules import Interaction, Tool
from datetime import datetime
from tools import convert_currency

class Agent:
    def __init__(self):
        """Initialize Agent with empty tool registry."""
        self.client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"), base_url="https://api.deepseek.com")
        self.tools: dict[str, Tool] = {}
        self.model = 'deepseek-chat'
        self.interactions: list[Interaction] = [] # working memory, new feature

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
                "If asked by the user, reflecting on the plan and suggesting changes if needed"
            ],
            "instructions": [
                "Use tools only when they are necessary for the task",
                "If a query can be answered directly, respond with a simple message instead of using tools",
                "When tools are needed, plan their usage efficiently to minimize tool calls",
                "If asked by the user, reflect on the plan and suggest changes if needed"
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
    
    def plan(self, user_query: str) -> str:
        """Given user query, generate execution plans. """

        message = [
                {"role": "system", "content": self.create_system_prompt()},
                {"role": "user", "content": user_query}
                ]
        
        plan = extract_json_block(call_llm(self.client, message, model=self.model, temperature=0))  # get the original plan

        # Store the interaction immediately after planning
        self.interactions.append(Interaction(
                                    timestamp=datetime.now(),
                                    query=user_query,
                                    plan=plan
                                ))
        return plan
    
    def reflect_on_plan(self) -> dict[str, Any]:
        """Reflect on the most recent plan using interaction history."""
        if not self.interactions:
            return {"reflection": "No plan to reflect on", "requires_changes": False}
        
        reflection_prompt = {
            "task": "reflection",
            "context": {
                "user_query": self.interactions[-1].query,
                "generated_plan": self.interactions[-1].plan
            },
            "instructions": [
                "Review the generated plan for potential improvements",
                "Consider if the chosen tools are appropriate",
                "Verify tool parameters are correct",
                "Check if the plan is efficient",
                "Determine if tools are actually needed"
            ],
            "response_format": {
                "type": "json",
                "schema": {
                    "requires_changes": {
                        "type": "boolean",
                        "description": "whether the plan needs modifications"
                    },
                    "reflection": {
                        "type": "string",
                        "description": "explanation of what changes are needed or why no changes are needed"
                    },
                    "suggestions": {
                        "type": "array",
                        "items": {"type": "string"},
                        "description": "specific suggestions for improvements",
                        "optional": True
                    }
                }
            }
        }

        # create a message for querying LLM to reflect the plans
        message = [
                    {"role": "system", "content": self.create_system_prompt()},
                    {"role": "user", "content": json.dumps(reflection_prompt)}
                ]

        reflection = extract_json_block(call_llm(self.client, message, model=self.model, temperature=0))  # get reflection results

        return reflection
        
    def execute(self, user_query: str) -> str:
        """Execute the full pipeline: plan and execute tools."""
        
        # Create initial plan (this also stores it in memory)
        origin_plan = self.plan(user_query)

        # Reflect on the plan using memory
        reflection = self.reflect_on_plan()

        # Check if reflection suggests changes
        if reflection.get("requires_changes", False):
            # Generate new plan based on reflection
            messages = [
                {"role": "system", "content": self.create_system_prompt()},
                {"role": "user", "content": user_query},
                {"role": "assistant", "content": json.dumps(origin_plan)},
                {"role": "user", "content": f"Please revise the plan based on this feedback: {json.dumps(reflection)}"}
            ]
            
            final_plan = extract_json_block(call_llm(self.client, messages, model=self.model, temperature=0))  # get reflection results
        else:
            final_plan = origin_plan

        # Update the stored interaction with all information
        self.interactions[-1].plan = {
                "initial_plan": origin_plan,
                "reflection": reflection,
                "final_plan": final_plan
            }
        
        # If agent decide not to use tools, directly return response    
        if not final_plan.get("requires_tools", True):
            return f"""Response: {final_plan['direct_response']}
            Reflection: {reflection.get('reflection', 'No improvements suggested')}"""        
        
        # Else, excetue tools in sequence:
        results = []
        for tool_call in final_plan['tool_calls']:
            tool_name = tool_call['tool']
            tool_args = tool_call['args']
            result = self.use_tool(tool_name, **tool_args)
            results.append(result)

        # Combine results
        return f"""- Initial Thought: {origin_plan['thought']}
- Initial Plan: {'. '.join(origin_plan['plan'])}
- Reflection: {reflection.get('reflection', 'No improvements suggested')}
- Final Plan: {'. '.join(final_plan['plan'])}
- Results: {'. '.join(results)}"""

            
if __name__ == "__main__":
    agent = Agent()
    agent.add_tools(convert_currency)

    print("🧠 AI Agent Currency Converter is ready!")
    print("Type your query below (or type 'exit' to quit):\n")

    while True:
        query = input(">>> Input your query here: ").strip()
        
        if query.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        print(">>> Query processing ... ")
        result = agent.execute(query)
        print(">>> Response:")
        print(result)
        print("-" * 50)