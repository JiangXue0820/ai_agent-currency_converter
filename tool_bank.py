from tool_decorator import tool
import urllib.request
import json

@tool()
def convert_currency(amount: float, from_currency: str, to_currency: str) -> float:
    """
    Converts currency using latest exchange rates.

    Parameters:
        - amount: The amount of money in old currency
        - from_currency: Source currency code (e.g., USD)
        - to_currency: Target currency code (e.g., EUR)  
    """
    try:
        url = f"https://open.er-api.com/v6/latest/{from_currency.upper()}"
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read())

        if 'rates' not in data:
            return "Error: Could not fetch exchange rates"
        
        rate = data['rates'].get(to_currency.upper())
        if not rate:
            return f"Error: Could not find exchange rate for {from_currency.upper()} -> {to_currency.upper()}"
        
        converted_amount = amount * rate
        
        return f"{amount} {from_currency.upper()} = {converted_amount:.2f} {to_currency.upper()}"
    
    except Exception as e:
        return f"Error converting currency: {str(e)}"
    
if __name__ == "__main__":
    convert_currency(100, 'USD', 'EUR')