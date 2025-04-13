# 🧠 AI Agent Currency Converter

This project implements a simple AI agent for currency-related questions. 

The agent is capable of reasoning, reflection and tool usage. 
Given a user query, the agent generates a step-by-step plan to address the request. If the query is unrelated to currency, it responds directly with a natural answer. If currency conversion is required, it retrieves the latest exchange rates and performs the conversion using real-time data. Additionally, a reflection module reviews the initial plan, identifies any errors or inconsistencies, and revises the plan to ensure the final response is accurate and coherent.

Given a user query, the agent determines whether it requires calling the currency conversion tool. If the query is unrelated to currency, the agent responds directly. If conversion is needed, it retrieves the latest exchange rate and calculates the amount from one currency to another using real-time data.
---

## 🚀 Features

- **Real-time currency conversion** using [exchangerate.host](https://exchangerate.host)
- **Agent from scratch**: with reasoning, planning, tool execution
- **Tool decorator** for seamless integration of new tools and functionality
- **Working memory** for reading and writing plan reflections (new feature)
---

🔄 Changes from First Version
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
