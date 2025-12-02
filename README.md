# 🌐 AI网站代理规则自动生成器

自动采集热门国外AI网站域名，生成多种代理工具规则，每天自动更新。

**AI Websites Proxy Rules Auto-Generator**

Automatically collect popular international AI website domains and generate proxy rules for multiple tools, updated daily.

---

## ✨ 特性 Features

- 🤖 **自动采集**：每天自动采集GitHub热门AI项目和知名AI服务网站
- 🔄 **每日更新**：通过GitHub Actions每天自动更新规则
- 🛠️ **多工具支持**：支持6种主流代理工具
  - Clash
  - Surge
  - Quantumult X
  - Shadowrocket
  - Sing-box
  - Loon
- 📋 **内置域名**：包含100+热门AI服务（OpenAI、Claude、Midjourney等）
- 🌍 **开源免费**：完全开源，免费使用

---

## 📥 使用方法 Usage

### 方式一：直接订阅（推荐）

将以下链接添加到你的代理工具中：

#### Clash

```
https://raw.githubusercontent.com/YOUR_USERNAME/ai-projects-proxy-rules/main/rules/clash.yaml
```

#### Surge

```
https://raw.githubusercontent.com/YOUR_USERNAME/ai-projects-proxy-rules/main/rules/surge.conf
```

#### Quantumult X

```
https://raw.githubusercontent.com/YOUR_USERNAME/ai-projects-proxy-rules/main/rules/quantumult-x.conf
```

#### Shadowrocket

```
https://raw.githubusercontent.com/YOUR_USERNAME/ai-projects-proxy-rules/main/rules/shadowrocket.conf
```

#### Sing-box

**JSON 格式（推荐新手）：**

```
https://raw.githubusercontent.com/YOUR_USERNAME/ai-projects-proxy-rules/main/rules/sing-box.json
```

**SRS 格式（推荐生产环境）：**

SRS 是 sing-box 的优化二进制格式，性能更好、体积更小。详见：[Sing-box SRS 使用指南](docs/SINGBOX_SRS.md)

#### Loon

```
https://raw.githubusercontent.com/YOUR_USERNAME/ai-projects-proxy-rules/main/rules/loon.conf
```

> 💡 **提示**：将 `YOUR_USERNAME` 替换为你的GitHub用户名

### 方式二：手动下载

1. 进入 `rules` 目录
2. 下载对应工具的规则文件
3. 手动添加到代理工具配置中

---

## 🚀 部署到你的GitHub

### 1. Fork或上传此项目

```bash
git clone https://github.com/YOUR_USERNAME/ai-projects-proxy-rules.git
cd ai-projects-proxy-rules
git remote set-url origin https://github.com/YOUR_USERNAME/ai-projects-proxy-rules.git
git push -u origin main
```

### 2. 启用GitHub Actions

1. 进入仓库 `Settings` → `Actions` → `General`
2. 选择 `Allow all actions and reusable workflows`
3. 保存设置

### 3. 手动触发首次更新（可选）

1. 进入仓库 `Actions` 标签
2. 选择 `Update AI Proxy Rules` 工作流
3. 点击 `Run workflow` → `Run workflow`

---

## 📊 包含的AI网站

项目自动采集以下类型的AI网站：

### AI聊天对话

- OpenAI (ChatGPT)
- Anthropic (Claude)
- Google (Gemini, Bard)
- Poe
- Character.AI
- Perplexity
- You.com

### AI图像生成

- Midjourney
- Stability AI
- DALL-E
- Adobe Firefly
- Leonardo.AI
- Playground AI

### AI开发平台

- Hugging Face
- Replicate
- RunPod
- Together AI
- Cohere
- AI21

### AI应用工具

- Jasper
- Copy.AI
- Writesonic
- Notion AI
- Gamma
- Tome

### AI视频音频

- Runway
- Synthesia
- Descript
- ElevenLabs
- Murf AI

### 更多

完整列表请查看 `data/ai_projects.json`

---

## 🔧 自定义配置

### 添加自定义域名

编辑 `scripts/collect_ai_projects.py` 中的 `BUILT_IN_AI_DOMAINS` 列表：

```python
BUILT_IN_AI_DOMAINS = [
    "openai.com",
    "claude.ai",
    "your-custom-domain.com",  # 添加你的域名
    # ...
]
```

### 修改更新频率

编辑 `.github/workflows/update.yml` 中的 cron 表达式：

```yaml
schedule:
  - cron: '0 0 * * *'  # 每天UTC 0点（北京时间8点）
  # 修改为: '0 */6 * * *'  # 每6小时更新一次
```

---

## 🛠️ 本地运行

```bash
# 安装依赖
pip install -r requirements.txt

# 采集AI项目
cd scripts
python collect_ai_projects.py

# 生成规则文件
python generate_rules.py
```

---

## 📝 文件结构

```
ai-projects-proxy-rules/
├── .github/
│   └── workflows/
│       └── update.yml         # GitHub Actions自动更新
├── scripts/
│   ├── collect_ai_projects.py # 采集脚本
│   └── generate_rules.py      # 规则生成脚本
├── data/
│   └── ai_projects.json       # 项目数据
├── rules/
│   ├── clash.yaml             # Clash规则
│   ├── surge.conf             # Surge规则
│   ├── quantumult-x.conf      # Quantumult X规则
│   ├── shadowrocket.conf      # Shadowrocket规则
│   ├── sing-box.json          # Sing-box规则
│   └── loon.conf              # Loon规则
├── requirements.txt
├── README.md
└── .gitignore
```

---

## ⚠️ 注意事项

1. **GitHub API限制**：未认证情况下每小时60次请求，足够日常使用
2. **代理配置**：确保代理工具已正确配置代理服务器
3. **规则优先级**：某些代理工具需要注意规则顺序
4. **定期检查**：建议定期检查规则是否正常工作

---

## 🤝 贡献

欢迎提交Issue和Pull Request！

如果你发现新的热门AI网站，请通过以下方式贡献：

1. Fork本项目
2. 添加域名到 `scripts/collect_ai_projects.py`
3. 提交Pull Request

---

## 📄 许可证

MIT License

---

## 🔗 相关链接

- [Clash](https://github.com/Dreamacro/clash)
- [Surge](https://nssurge.com/)
- [Quantumult X](https://quantumult.app/)
- [Shadowrocket](https://apps.apple.com/app/shadowrocket/id932747118)
- [Sing-box](https://sing-box.sagernet.org/)
- [Loon](https://nsloon.com/)

---

## 💬 问题反馈

如有问题，请提交[Issue](https://github.com/YOUR_USERNAME/ai-projects-proxy-rules/issues)

---

**⭐ 如果这个项目对你有帮助，请给个Star！**

---

## 📊 统计

![GitHub stars](https://img.shields.io/github/stars/YOUR_USERNAME/ai-projects-proxy-rules?style=social)
![GitHub forks](https://img.shields.io/github/forks/YOUR_USERNAME/ai-projects-proxy-rules?style=social)
![GitHub last commit](https://img.shields.io/github/last-commit/YOUR_USERNAME/ai-projects-proxy-rules)
![GitHub workflow status](https://img.shields.io/github/actions/workflow/status/YOUR_USERNAME/ai-projects-proxy-rules/update.yml)
