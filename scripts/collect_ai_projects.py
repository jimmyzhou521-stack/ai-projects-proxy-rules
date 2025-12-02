#!/usr/bin/env python3
"""
采集热门AI网站和项目
Collect popular AI websites and projects
"""

import json
import re
import requests
from datetime import datetime
from typing import List, Dict, Set
from pathlib import Path

# 内置热门AI服务域名列表
# 内置热门AI服务域名列表
BUILT_IN_AI_DOMAINS = [
    # OpenAI / ChatGPT
    "openai.com",
    "chatgpt.com",
    "ai.com",
    "chat.com",
    "searchgpt.com",
    "oaistatic.com",
    "oaiusercontent.com",
    "auth0.openai.com",
    "chatgpt.livekit.cloud",
    "host.livekit.cloud",
    "turn.livekit.cloud",
    "featuregates.org",
    "featureassets.org",
    "statsig.com",
    "statsigapi.net",
    "events.statsigapi.net",
    "api.statsig.com",
    "intercom.io",
    "intercomcdn.com",
    "sentry.io",
    "browser-intake-datadoghq.com",
    "workos.com",
    "workoscdn.com",
    "auth0.com",
    "identrust.com",
    "launchdarkly.com",
    "observeit.net",
    "segment.io",
    "stripe.com",
    "algolia.net",
    "openai-api.arkoselabs.com",
    "client-api.arkoselabs.com",
    "chat.openai.com.cdn.cloudflare.net",
    "openai.com.cdn.cloudflare.net",
    "openaicom-api-bdcpf8c6d2e9atf6.z01.azurefd.net",
    "openaicomproductionae4b.blob.core.windows.net",
    "production-openaicom-storage.azureedge.net",
    "openaiapi-site.azureedge.net",
    "openaicom.imgix.net",
    "static.cloudflareinsights.com",
    "challenges.cloudflare.com",
    "sora.com",

    # Google / Gemini / Colab
    "gemini.google.com",
    "bard.google.com",
    "ai.google.dev",
    "aistudio.google.com",
    "makersuite.google.com",
    "deepmind.com",
    "deepmind.google",
    "generativeai.google",
    "generativelanguage.googleapis.com",
    "proactivebackend-pa.googleapis.com",
    "geller-pa.googleapis.com",
    "alkalicore-pa.clients6.google.com",
    "alkalimakersuite-pa.clients6.google.com",
    "notebooklm.google",
    "notebooklm.google.com",
    "colab.research.google.com",
    "colab.google",
    "developerprofiles.google.com",
    "apis.google.com",
    "www.googleapis.com",
    "ssl.gstatic.com",
    
    # Microsoft / Copilot / Bing
    "copilot.microsoft.com",
    "bing.com",
    "www.bing.com",
    "r.bing.com",
    "sydney.bing.com",
    "edgeservices.bing.com",
    "services.bingapis.com",
    "gateway.bingviz.microsoft.net",
    "gateway.bingviz.microsoftapp.net",
    "bing-shopping.microsoft-falcon.io",
    "api.msn.com",
    "assets.msn.com",
    "location.microsoft.com",
    "self.events.data.microsoft.com",
    "in.appcenter.ms",
    "odc.officeapps.live.com",
    "api.microsoftapp.net",

    # Anthropic / Claude
    "anthropic.com",
    "claude.ai",
    "claudeusercontent.com",
    "servd-anthropic-website.b-cdn.net",

    # Notion AI
    "notion.ai",
    "notion.com",
    "notion.so",
    "notion.new",
    "notion.site",
    "notion-static.com",
    "http-inputs-notion.splunkcloud.com",

    # Perplexity
    "perplexity.ai",
    "pplx.ai",
    "pplx-res.cloudinary.com",

    # Others (Cursor, Grok, etc.)
    "cursor.com",
    "cursor.sh",
    "cursorapi.com",
    "cursor-cdn.com",
    "grok.com",
    "groq.com",
    "x.ai",
    "poe.com",
    "poecdn.net",
    "character.ai",
    "you.com",
    "midjourney.com",
    "stability.ai",
    "stablediffusionweb.com",
    "dall-e.com",
    "firefly.adobe.com",
    "leonardo.ai",
    "playground.ai",
    "craiyon.com",
    "openart.ai",
    "clipdrop.co",
    "huggingface.co",
    "replicate.com",
    "runpod.io",
    "together.ai",
    "cohere.com",
    "ai21.com",
    "jasper.ai",
    "copy.ai",
    "writesonic.com",
    "gamma.app",
    "tome.app",
    "beautiful.ai",
    "canva.com",
    "runway.ml",
    "synthesia.io",
    "descript.com",
    "elevenlabs.io",
    "murf.ai",
    "paperswithcode.com",
    "arxiv.org",
    "kaggle.com",
    "civitai.com",
    "phind.com",
    "dify.ai",
    "grazie.ai",
    "grazie.aws.intellij.net",
    "jetbrains.ai",
    "meta.ai",
    "gateway.ai.cloudflare.com",
    "cdn.usefathom.com",
] + [f"clients{i}.google.com" for i in range(1, 11)]

# 内置关键字
BUILT_IN_KEYWORDS = [
    "openai",
    "openaicom-api",
    "colab",
    "developerprofiles",
    "generativelanguage",
]

# 内置IP CIDR
BUILT_IN_CIDRS = [
    "24.199.123.28/32",
    "64.23.132.171/32",
]

# 内置IP ASN
BUILT_IN_ASNS = [
    "14061",
    "20473",
]

def extract_domain_from_url(url: str) -> str:
    """从URL提取主域名"""
    if not url:
        return ""
    
    # 移除协议
    url = re.sub(r'^https?://', '', url)
    # 移除路径
    url = url.split('/')[0]
    # 移除端口
    url = url.split(':')[0]
    
    # 提取主域名（去掉www等前缀）
    parts = url.split('.')
    if len(parts) >= 2:
        # 保留最后两部分作为主域名
        return '.'.join(parts[-2:])
    
    return url

def search_github_ai_projects(max_results: int = 100) -> List[Dict]:
    """搜索GitHub上的热门AI项目"""
    projects = []
    
    # 多个搜索关键词
    keywords = [
        "ChatGPT stars:>10000",
        "AI stars:>10000",
        "LLM stars:>10000",
        "stable-diffusion stars:>5000",
        "machine-learning stars:>10000",
        "deep-learning stars:>10000",
    ]
    
    headers = {
        'Accept': 'application/vnd.github.v3+json',
        'User-Agent': 'AI-Projects-Collector'
    }
    
    seen_repos = set()
    
    for keyword in keywords:
        try:
            url = f"https://api.github.com/search/repositories?q={keyword}&sort=stars&order=desc&per_page=30"
            response = requests.get(url, headers=headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                items = data.get('items', [])
                
                for item in items:
                    repo_name = item.get('full_name', '')
                    if repo_name in seen_repos:
                        continue
                    
                    seen_repos.add(repo_name)
                    
                    project = {
                        'name': item.get('name', ''),
                        'full_name': repo_name,
                        'description': item.get('description', ''),
                        'stars': item.get('stargazers_count', 0),
                        'homepage': item.get('homepage', ''),
                        'url': item.get('html_url', ''),
                    }
                    projects.append(project)
                    
                    if len(projects) >= max_results:
                        break
            
            if len(projects) >= max_results:
                break
                
        except Exception as e:
            print(f"Error searching GitHub for '{keyword}': {e}")
            continue
    
    # 按star数排序
    projects.sort(key=lambda x: x['stars'], reverse=True)
    return projects[:max_results]

def collect_domains(projects: List[Dict]) -> Set[str]:
    """从项目中收集域名"""
    domains = set(BUILT_IN_AI_DOMAINS)
    
    for project in projects:
        homepage = project.get('homepage', '')
        if homepage:
            domain = extract_domain_from_url(homepage)
            if domain and '.' in domain:
                # 过滤掉无效域名
                if domain not in ['github.com', 'github.io', 'localhost']:
                    domains.add(domain)
    
    return domains

def save_data(projects: List[Dict], domains: Set[str], output_file: str):
    """保存数据到JSON文件"""
    data = {
        'updated_at': datetime.now().isoformat(),
        'total_projects': len(projects),
        'total_domains': len(domains),
        'domains': sorted(list(domains)),
        'keywords': BUILT_IN_KEYWORDS,
        'ip_cidrs': BUILT_IN_CIDRS,
        'ip_asns': BUILT_IN_ASNS,
        'projects': projects[:50],  # 只保存前50个项目信息
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Data saved to {output_file}")
    print(f"📊 Total domains: {len(domains)}")
    print(f"📦 Total projects: {len(projects)}")

def main():
    print("🚀 Starting AI projects collection...")
    
    # 搜索GitHub项目
    print("🔍 Searching GitHub projects...")
    projects = search_github_ai_projects(max_results=100)
    
    # 收集域名
    print("🌐 Collecting domains...")
    domains = collect_domains(projects)
    
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 保存数据
    output_file = project_root / 'data' / 'collected_projects.json'
    # 确保目录存在
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    save_data(projects, domains, str(output_file))
    
    print("✨ Collection completed!")

if __name__ == '__main__':
    main()
