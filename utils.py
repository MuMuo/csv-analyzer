from langchain.chains.flare.prompts import PROMPT_TEMPLATE
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import json

PROMPT_TEMPLATE = """
你是一位数据分析助手，你的回应内容取决于用户的请求内容。

1、对于文字回答得问题，按照这样的格式回答：
    {"answer":"<你的答案写在这里>"}
例如：
    {"answer":"数学最高分是98"}
2、如果用户需要一个表格，按照这样的格式回答：
    {"table":{"columns":["column1", "column2", ...], "data":[[value11, value12, ...],[value21, value22, ...],...]}}
3、如果用户的请求适合返回条形图，按照这样的格式回答：
    {"bar":{"columns":["column1", "column2", ...], "data":[value1, value2, ...]}}
4、如果用户的请求适合返回曲线图， 按照这样的格式回答：
    {"line":{"columns":["column1", "column2", ...], "data":[value1, value2, ...]}}
5、如果用户的请求适合返回散点图， 按照这样的格式回答：
    {"scatter":{"columns":["column1", "column2", ...], "data":[value1, value2, ...]}}
请注意我们只支持三种图表："bar","line","scatter"。

请将所有结果以JSON字符串格式输出，请注意要将"columns"列表和"data"列表中的所有字符串用双引号包围。
例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]]}

你要处理的用户请求如下：
"""

def dataframe_agent(openai_api_key, df, query):
    model = ChatOpenAI(model="gpt-3.5-turbo",
                       openai_api_key=openai_api_key,
                       openai_api_base="https://api.aigc369.com/v1",
                       temperature=0)

    agent = create_pandas_dataframe_agent(llm=model,
                                  df=df,
                                  agent_executor_kwargs={"handle_parsing_errors":True},
                                  allow_dangerous_code=True,
                                  verbose=True)

    prompt = PROMPT_TEMPLATE + query
    response = agent.invoke({"input":prompt})
    response_dict = json.loads(response["output"])

    return response_dict

#import pandas as pd
#import os
#data_df = pd.read_csv("./house_price.csv")
#res = dataframe_agent(os.getenv("OPENAI_API_KEY"), df=df, query="请过滤出price大于12000000的记录")
