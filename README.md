# Talk to your data

This repository contains sample code in different notebooks covering the theme of querying local data in SQL databases or JSON files. 

The corresponding sample data and test cases can be found in the `data` folder.

Simple AI Agents to query your data in natural language:

* **single_js.ipynb**: Jupyter notebook showing a Langchain Agent talking to your JSON Data using JavaScript as query language.

* **single_sql.ipynb**: Jupyter notebook showing a Langchain Agent talking to your SQL database using SQL as query language.


Benchmarks of the AI Agents:

* **benchmark_js.ipynb**: Jupyter notebook running 100 test cases for JavaScript Agent.

* **benchmark_sql.ipynb**: Jupyter notebook running 100 test cases for SQL Agent.

* **compare_sql_js.ipynb**: Jupyter notebook with plots evaluating SQL Agent and JavaScript Agent.

The notebooks are written for python LangChain using Mistral AI models. To use the notebooks as they are you need an API Key from Mistral AI.

It is also possible to modify the notebooks so that they can be used with other models. Partially tested are:

* OpenAI: gpt-5.4-mini.
* Ollama: gpt-oss:20b.

For Ollama: gpt-oss:20b you will find:

* **single_js_oss20.ipynb**: Jupyter notebook showing a Langchain Agent talking to your local JSON Data using JavaScript as query language and the OpenAI model gpt-oss:20b for local inference.


