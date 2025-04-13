# AI Agent Currency Converter

This agent is equipped with advanced reasoning, reflection, and tool usage capabilities.

## 🧠 How It Works

### Step-by-Step Planning
- For every user query, the agent generates a detailed plan to address the request.

### Response Logic
- **Non-Currency Queries**:  
  The agent responds directly with a natural, conversational answer.
  
- **Currency Conversion Queries**:  
  - Retrieves the latest exchange rates using real-time data.  
  - Performs accurate currency conversion based on the retrieved information.

### 🔍 Reflection Module
- After the initial plan is generated, a reflection module:
  - Reviews the reasoning and proposed steps.
  - Identifies any errors or inconsistencies.
  - Revises the plan to ensure the final response is both accurate and coherent.
---

## 🔄 Changes from First Version
In this version, we introduce a reflection module that enables the agent to detect and revise incorrect or suboptimal execution plans.

The agent now performs a self-evaluation step after generating an initial plan.

If flaws or inconsistencies are identified, the agent reflects on the previous reasoning and produces a revised version of the plan.

This enhancement builds on the foundation of the original implementation by enabling iterative improvement through feedback and self-correction.
---

## 🛠️ Installation

Ensure you have Python 3.10 or higher installed.

```bash
git clone https://github.com/JiangXue0820/ai_agent-currency_converter.git
cd ai_agent-currency_converter
pip install -r requirements.txt
```

---

## 🔑 Environment Variables

Before running the script, set your API key in the terminal using the export command:

```bash
export DEEPSEEK_API_KEY=your_deepseek_api_key
```

Replace `your_deepseek_api_key` with your actual OpenAI API key.

---

## 🧪 Usage

Run the main script to start the currency converter agent:

```bash
python run_agent.py
```

You'll be prompted to enter a query directly in the terminal. For example:

```
$ python3 run_agent.py
🧐 AI Agent Currency Converter is ready!
Type your query below (or type 'exit' to quit):

>>> Your query: convert 100 EURO to Malaysian Ringgit
>>> Query processing ...  
>>> Response:  
Thought: I need to convert 100 Euros to Malaysian Ringgit using the currency conversion tool  
Plan: Use convert_currency tool to convert 100 EUR to MYR. Return the conversion result  
Results: 100 EUR = 502.16 MYR  
--------------------------------------------------
```

---

## 🧩 Project Structure

```
ai_agent-currency_converter/
├── run_agent.py          # Entry point to run the agent
├── tools.py              # Tool definitions for conversion
├── modules.py            # Class of modules, including Tool and Interaction (working memory)
├── utils.py              # Utility functions
├── README.md             # Project documentation
```

---

## 📦 Dependencies

- openai  
- requests  
- python-dotenv

Install all dependencies with:

```bash
pip install -r requirements.txt
```

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests. Feedback and suggestions are welcome!

---

## 📄 License

This project is licensed under the MIT License.

---

Built with ❤️ by [JiangXue0820](https://github.com/JiangXue0820)
