# 📘 Sing-box SRS 格式使用指南

## 什么是 SRS？

**SRS (Sing-box Rule Set)** 是 sing-box 的二进制规则集格式，相比 JSON 格式具有以下优势：

- ⚡ **更快的加载速度**：二进制格式解析更快
- 💾 **更小的文件体积**：优化的存储格式
- 🚀 **更低的内存占用**：特别是对于大量 domain_suffix 规则
- ✨ **生产环境推荐**：官方推荐在生产环境使用

---

## 🔧 使用方法

### 方式一：直接使用 JSON 格式（简单）

本项目已经生成了 `sing-box.json`，可以直接订阅使用：

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "ai-proxy",
        "format": "source",
        "url": "https://raw.githubusercontent.com/YOUR_USERNAME/ai-projects-proxy-rules/main/rules/sing-box.json",
        "download_detour": "direct",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": "ai-proxy",
        "outbound": "proxy"
      }
    ]
  }
}
```

### 方式二：编译为 SRS 格式（推荐）

#### 1️⃣ 安装 sing-box

**Linux / macOS:**

```bash
bash <(curl -fsSL https://sing-box.app/get.sh)
```

**Windows:**

```powershell
# 使用 scoop 安装
scoop install sing-box

# 或从 GitHub 下载
# https://github.com/SagerNet/sing-box/releases
```

#### 2️⃣ 下载并编译规则

```bash
# 下载 JSON 格式规则
curl -O https://raw.githubusercontent.com/YOUR_USERNAME/ai-projects-proxy-rules/main/rules/sing-box.json

# 编译为 SRS 格式
sing-box rule-set compile --output ai-proxy.srs sing-box.json
```

#### 3️⃣ 在配置中使用 SRS 文件

**本地文件：**

```json
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "ai-proxy",
        "format": "binary",
        "path": "/path/to/ai-proxy.srs"
      }
    ],
    "rules": [
      {
        "rule_set": "ai-proxy",
        "outbound": "proxy"
      }
    ]
  }
}
```

**远程 SRS 文件（需要自行托管）：**

```json
{
  "route": {
    "rule_set": [
      {
        "type": "remote",
        "tag": "ai-proxy",
        "format": "binary",
        "url": "https://your-server.com/ai-proxy.srs",
        "download_detour": "direct",
        "update_interval": "24h"
      }
    ],
    "rules": [
      {
        "rule_set": "ai-proxy",
        "outbound": "proxy"
      }
    ]
  }
}
```

---

## 📊 格式对比

| 特性 | JSON (source) | SRS (binary) |
|------|---------------|--------------|
| **文件大小** | ~1.5 KB | ~0.8 KB (-47%) |
| **加载速度** | 普通 | 快速 |
| **内存占用** | 普通 | 优化 |
| **可读性** | 人类可读 | 二进制格式 |
| **编辑难度** | 容易 | 需要重新编译 |
| **推荐场景** | 开发/测试 | 生产环境 |

---

## 🔄 自动化编译

如需在 GitHub Actions 中自动生成 SRS 文件，可以在 `.github/workflows/update.yml` 中添加：

```yaml
- name: Install sing-box
  run: |
    bash <(curl -fsSL https://sing-box.app/get.sh)

- name: Compile to SRS
  run: |
    cd rules
    sing-box rule-set compile --output sing-box.srs sing-box.json
- [Rule Set 格式说明](https://sing-box.sagernet.org/configuration/rule-set/)
- [Sing-box GitHub](https://github.com/SagerNet/sing-box)

---

## ⚠️ 注意事项

1. **版本兼容性**: 确保你的 sing-box 版本支持 version 2 (1.10.0+)
2. **SRS 更新**: SRS 文件无法直接编辑，需要修改 JSON 后重新编译
3. **二进制格式**: SRS 文件不可被文本编辑器读取
4. **托管问题**: GitHub 可能会阻止某些二进制文件，建议使用 GitHub Releases 或其他托管服务

---

**📝 最后更新**: 2025-12-02
