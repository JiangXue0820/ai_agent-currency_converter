# 🧠 AI Agent Currency Converter

A multi-turn conversational currency converter powered by LangGraph and OpenAI agents. This project demonstrates how to build a conversational AI system that can plan, convert, and validate currency conversion queries step-by-step using tool-augmented reasoning.

---

## 🚀 Features

- **Real-time currency conversion** using [exchangerate.host](https://exchangerate.host)
- **Integrated with DeepSeek Function Calling**
- **Agent from scratch**: with reasoning, planning, tool-using capabilities
- **Tool decorator**: flexible for adding new tools

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

Create a `.env` file in the root directory with the following content:

```env
DEEPSEEK_API_KEY=your_deepseek_api_key
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
├── agent.py              # Agent class and behavior
├── tool_bank.py          # Tool definitions for conversion
├── tool_decorator.py     # Decorators for tools
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

## 🧠 Future Improvements

- Add support for natural language queries like "How much is 50 euros in yen?"
- Integrate logging and error tracking
- Improve currency name normalization

---

## 🤝 Contributing

Feel free to fork this repository and submit pull requests. Feedback and suggestions are welcome!

---

## 📄 License

This project is licensed under the MIT License.

---

Built with ❤️ by [JiangXue0820](https://github.com/JiangXue0820)