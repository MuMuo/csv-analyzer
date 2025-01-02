from langchain.chains.flare.prompts import PROMPT_TEMPLATE
from langchain_openai import ChatOpenAI
from langchain_experimental.agents.agent_toolkits import create_pandas_dataframe_agent
import json

PROMPT_TEMPLATE = """
你是一位数据分析助手，你的回应内容取决于用户的请求内容。

1. 对于文字回答的问题，按照这样的格式回答：
   {"answer": "<你的答案写在这里>"}
例如：
   {"answer": "订单量最高的产品ID是'MNWC3-067'"}

2. 如果用户需要一个表格，按照这样的格式回答：
   {"table": {"columns": ["A", "B", "C" ...], "data": [[20, 30, 25 ...], [34, 21, 19 ...], ...]}}

3. 如果用户的请求适合返回条形图，按照这样的格式回答：
   {"bar": {"columns": ["A", "B", "C", ...], "data": [[20, 30, 25 ...], [34, 21, 19 ...], ...], "index":[0, 1, 2, ...]}}

4. 如果用户的请求适合返回折线图，按照这样的格式回答：
   {"line": {"columns": ["A", "B", "C", ...], "data": [[20, 30, 25 ...], [34, 21, 19 ...], ...], "index":[0, 1, 2, ...]}}

5. 如果用户的请求适合返回散点图，按照这样的格式回答：
   {"scatter": {"columns": ["A", "B", "C", ...], "data": [[20, 30, 25 ...], [34, 21, 19 ...], ...], "index":[0, 1, 2, ...]}}
注意：我们只支持三种类型的图表："bar", "line" 和 "scatter"。


请将所有输出作为JSON字符串返回。请注意要将"columns"列表、"data"列表、"index"列表中的所有字符串都用双引号包围。
例如：{"columns": ["Products", "Orders"], "data": [["32085Lip", 245], ["76439Eye", 178]], "index":["id1","id2"]}

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
