from flask import Flask, render_template, request
from openai import OpenAI
import os

app = Flask(__name__)

# 配置API密钥和基础URL
OPENAI_API_KEY = "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"
OPENAI_BASE_URL = "https://integrate.api.nvidia.com/v1"

client = OpenAI(
    base_url=OPENAI_BASE_URL,
    api_key=OPENAI_API_KEY
)

@app.route('/', methods=['GET', 'POST'])
def index():
    response_text = ""
    if request.method == 'POST':
        user_input = request.form.get('user_input')

        # 定义AI的提示词
        prompt = f"我要你扮演一个会调情的渣男，你来回复对方。风格如下：渣男、撩妹高手、海王、调戏、暧昧用户输入: {user_input}"

        # 调用AI API
        completion = client.chat.completions.create(
            model="meta/llama-3.1-405b-instruct",
            messages=[{"role":"user","content":prompt}],
            temperature=0.2,
            top_p=0.7,
            max_tokens=1024,
            stream=True
        )

        # 收集AI的回复
        for chunk in completion:
            if chunk.choices[0].delta.content is not None:
                response_text += chunk.choices[0].delta.content

    return render_template('index.html', response=response_text)

if __name__ == '__main__':
    # 为了安全，建议使用环境变量来存储API密钥
    # OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    app.run(host='0.0.0.0', port=5000, debug=True)
