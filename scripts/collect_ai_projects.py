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

# 内置热门AI服务域名列表
BUILT_IN_AI_DOMAINS = [
    # AI聊天和对话
    "openai.com",
    "chat.openai.com",
    "platform.openai.com",
    "anthropic.com",
    "claude.ai",
    "gemini.google.com",
    "bard.google.com",
    "poe.com",
    "character.ai",
    "perplexity.ai",
    "you.com",
    
    # AI图像生成
    "midjourney.com",
    "stability.ai",
    "stablediffusionweb.com",
    "dall-e.com",
    "firefly.adobe.com",
    "leonardo.ai",
    "playground.ai",
    "craiyon.com",
    
    # AI开发平台
    "huggingface.co",
    "replicate.com",
    "runpod.io",
    "together.ai",
    "cohere.com",
    "ai21.com",
    
    # AI工具和应用
    "jasper.ai",
    "copy.ai",
    "writesonic.com",
    "notion.ai",
    "gamma.app",
    "tome.app",
    "beautiful.ai",
    "canva.com",
    
    # AI视频和音频
    "runway.ml",
    "synthesia.io",
    "descript.com",
    "elevenlabs.io",
    "murf.ai",
    
    # AI研究和模型
    "paperswithcode.com",
    "arxiv.org",
    "kaggle.com",
    "civitai.com",
    
    # AI搜索
    "phind.com",
    "bing.com",  # Copilot
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
    
    # 保存数据
    output_file = 'data/ai_projects.json'
    save_data(projects, domains, output_file)
    
    print("✨ Collection completed!")

if __name__ == '__main__':
    main()
