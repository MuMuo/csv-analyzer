import pandas as pd
import streamlit as st
from utils import dataframe_agent

st.title("csv数据分析智能工具")

with st.sidebar:
    api_key =  st.text_input("请输入OPENAI_API秘钥", type="password")

def gen_chart(input_data, chart_type):
    df_data = pd.DataFrame(input_data["data"], columns=input_data["columns"])
    df_data.set_index(input_data["columns"][0], inplace=True)
    if chart_type == "bar":
        st.bar_chart(df_data)
    elif chart_type == "line":
        st.line_chart(df_data)
    elif chart_type == "scatter":
        st.scatter_chart(df_data)

upload_file = st.file_uploader("请上传需要分析的csv文件", type=["csv"])
if upload_file :
    if "df" not in st.session_state or st.session_state["file_name"] != upload_file.name:
        st.session_state["file_name"] = upload_file.name
        st.session_state["df"] = pd.read_csv(upload_file)

if "df" in st.session_state:
    with st.expander("原始数据"):
        st.dataframe(st.session_state["df"])

    query = st.text_area("请输入你的问题，如数据提取请求，可视化要求（支持散点图、折线图、条形图）")
    button = st.button("生成回答")
    if button:
        if not api_key:
            st.info("请输入你的OPENAI API秘钥")
            st.stop()
        if not query :
            st.info("请输入你的问题")
            st.stop()
        with st.spinner("AI正在思考中，请稍等 ..."):
            res = dataframe_agent(openai_api_key=api_key, df = st.session_state["df"], query=query)

        output_type=list(res.keys())[0]
        if output_type == "answer":
            st.write(res[output_type])
        elif output_type == "table":
            st.dataframe(pd.DataFrame(res[output_type]["data"], columns=res[output_type]["columns"]))
        elif output_type == "bar" or output_type == "line" or output_type == "scatter":
            gen_chart(res[output_type],output_type)
