# 🏛️ 四人 AI 战略智囊团

GPT（架构）· Muse（创意）· Grok（质检）· Gemini（统筹），四家大模型轮流对同一个问题出方案、发散、挑刺、定案。

## 本地运行

```bash
pip install -r requirements.txt
# 在项目根目录建 .env，填入四个 API Key（参考 secrets.toml.example 的变量名）
streamlit run app.py
```

## 部署到 Streamlit Cloud（免费，拿到可分享链接）

1. 把本项目推到一个 GitHub 仓库
2. 打开 https://share.streamlit.io ，用 GitHub 登录，New app → 选这个仓库 → 主文件选 `app.py`
3. 在 Advanced settings / Secrets 里粘贴四个 API Key（格式见 `secrets.toml.example`）
4. Deploy，完成后会得到一个 `https://xxx.streamlit.app` 链接，发给朋友即可打开使用

## 注意

- 朋友使用时消耗的是你 Secrets 里密钥的额度，留意用量
- 想换模型：改 `app.py` 顶部的模型配置区即可
