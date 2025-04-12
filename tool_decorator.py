from dataclasses import dataclass
from typing import Callable, Any, get_origin, get_args, Literal, get_type_hints
import inspect

@dataclass
class Tool:
    name: str
    description: str
    func: Callable[..., str]
    parameters: dict[str, dict[str, str]]

    def __repr__(self):
        return (f"Tool(name={self.name!r}, description={self.description!r},\n"
                f"func={self.func},\n"
                f"parameters={self.parameters})")
    
    def __call__(self, *args, **kwds):
        return self.func(*args, **kwds)


def parse_docstring_params(docstring: str) -> dict[str, str]:
    """
    Parses the docstring to extract parameter names and and parameters of tools.

    The docstring follows the following template by default: 
    ```
    Description of what the tool does.

    Parameters:
        - param1: Description of first parameter
        - param2: Description of second parameter
    ```
    Args:
        docstring (str): The docstring to parse.

    Returns:
        dict[str, str]: A dictionary mapping parameter names to their types.
    """
    if not docstring:
        return {}
    
    params = {}
    lines = [item.strip() for item in docstring.split('\n')]

    try:
        start_idx = lines.index('Parameters:')+1
    except:
        raise ValueError("Docstring format is incorrect! Please check!")

    for i in range(start_idx, len(lines)):
        line = lines[i].strip()
        if not line:
            continue
        line = line.lstrip('-').strip()  # Safer: only strip dash at start
        name, description = line.split(':', 1)  # Avoid unpacking error
        params[name.strip()] = description.strip()
    
    return params

def get_type_description(type_hint: Any) -> str:
    """
    Returns a human-readable description of a type hint.

    This function takes a Python type hint (e.g., int, List[str], Literal["A", "B"])
    and returns a readable string representation suitable for documentation or display.

    Special handling includes:
    - Literal types are formatted as "one of (option1, option2, ...)"
    - Generic types (like List[int], Dict[str, float]) are recursively parsed
    - Standard types (like int, str) return their type name

    Args:
        type_hint (Any): The type hint to describe.

    Returns:
        str: A human-readable description of the type hint.
    """
    origin = get_origin(type_hint)
    args = get_args(type_hint)

    if origin is Literal:
        return f"one of {args}"
    elif origin:
        origin_name = origin.__name__
        args_str = ", ".join(get_type_description(arg) for arg in args)
        return f"{origin_name}[{args_str}]"
    elif hasattr(type_hint, '__name__'):
        return type_hint.__name__
    else:
        return str(type_hint)
    

# Define a decorator called "tool", which convert each function into a Tool instance
def tool(name: str = None):
    def decorator(func: Callable[..., str]) -> Tool:
        # use function name or customized name as tool name
        tool_name = name or func.__name__   
        
        # get data type of input parameters
        type_hints = get_type_hints(func)   
        
        # get docstring of the function and parse into parameters
        description = inspect.getdoc(func) or "No description available"  
        param_docs  = parse_docstring_params(description) 
    
        # retrieve function signature
        sig = inspect.signature(func)

        # summarize function parameters
        # loop through sig.parameters.items() instead of type_hints() to avoid missing unannotated params
        params = {}
        for param_name in sig.parameters.keys():
            params[param_name] = {
                'type': get_type_description(type_hints.get(param_name, Any)),
                'description': param_docs.get(param_name, 'No description available')
            }

        return Tool(
            name=tool_name, 
            description=description.split('\n\n')[0],  # use the first paragraph in docstring
            func=func,
            parameters=params
        )
    return decorator