#!/usr/bin/env python3
"""
从热门GitHub仓库自动爬取和整合AI代理规则
Auto-fetch and merge AI proxy rules from popular GitHub repositories
"""

import re
import json
import requests
from typing import List, Dict, Set
from datetime import datetime
from pathlib import Path

# 热门GitHub规则源列表
# 热门GitHub规则源列表
RULE_SOURCES = [
    {
        "name": "ACL4SSR",
        "urls": [
            "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/OpenAi.list",
            # 移除 Google.list，因为它包含太多非AI服务
            # "https://raw.githubusercontent.com/ACL4SSR/ACL4SSR/master/Clash/Ruleset/Google.list",
        ],
        "type": "clash"
    },
    {
        "name": "blackmatrix7",
        "urls": [
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/OpenAI/OpenAI.list",
            # 移除 Google.list
            # "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Google/Google.list",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Copilot/Copilot.list",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Claude/Claude.list",
            "https://raw.githubusercontent.com/blackmatrix7/ios_rule_script/master/rule/Clash/Gemini/Gemini.list",
        ],
        "type": "clash"
    },
    {
        "name": "Loyalsoldier",
        "urls": [
            "https://raw.githubusercontent.com/Loyalsoldier/clash-rules/release/proxy.txt",
        ],
        "type": "clash"
    }
]

# 需要过滤的宽泛域名（不作为后缀规则添加）
IGNORED_DOMAINS = {
    "google.com",
    "google.cn",
    "google.com.hk",
    "bing.com",
    "microsoft.com",
    "apple.com",
    "amazon.com",
    "baidu.com",
}

class RuleParser:
    """规则解析器"""
    
    def __init__(self):
        self.domains = set()
        self.domain_keywords = set()
        self.domain_suffixes = set()
        self.ip_cidrs = set()
        self.ip_asns = set()
        
    def parse_line(self, line: str, rule_type: str = "clash"):
        """解析单行规则"""
        line = line.strip()
        
        # 跳过注释和空行
        if not line or line.startswith('#') or line.startswith('//'):
            return
            
        # 移除行内注释
        if '#' in line:
            line = line.split('#')[0].strip()
        if '//' in line:
            line = line.split('//')[0].strip()
            
        # 移除payload标记
        if line.lower() in ['payload:', 'payload']:
            return
            
        # 移除前导的 - 和空格
        line = re.sub(r'^\s*-\s*', '', line)
        
        # 解析不同类型的规则
        patterns = [
            # DOMAIN-SUFFIX
            (r'^DOMAIN-SUFFIX\s*,\s*([^,]+)', 'suffix'),
            # DOMAIN
            (r'^DOMAIN\s*,\s*([^,]+)', 'domain'),
            # DOMAIN-KEYWORD
            (r'^DOMAIN-KEYWORD\s*,\s*([^,]+)', 'keyword'),
            # HOST-SUFFIX (Quantumult X)
            (r'^HOST-SUFFIX\s*,\s*([^,]+)', 'suffix'),
            # HOST (Quantumult X)
            (r'^HOST\s*,\s*([^,]+)', 'domain'),
            # HOST-KEYWORD (Quantumult X)
            (r'^HOST-KEYWORD\s*,\s*([^,]+)', 'keyword'),
            # IP-CIDR
            (r'^IP-CIDR\s*,\s*([^,]+)', 'ip-cidr'),
            # IP-ASN
            (r'^IP-ASN\s*,\s*([^,]+)', 'ip-asn'),
            # 纯域名（无前缀）
            (r'^([a-zA-Z0-9][-a-zA-Z0-9]*\.)+[a-zA-Z]{2,}$', 'suffix'),
        ]
        
        for pattern, rule_kind in patterns:
            match = re.match(pattern, line, re.IGNORECASE)
            if match:
                value = match.group(1).strip().lower()
                
                if rule_kind == 'suffix':
                    # 清理域名
                    value = value.replace('*.', '')
                    if value and self._is_valid_domain(value):
                        # 过滤宽泛域名
                        if value in IGNORED_DOMAINS:
                            continue
                        self.domain_suffixes.add(value)
                elif rule_kind == 'domain':
                    if value and self._is_valid_domain(value):
                        self.domains.add(value)
                elif rule_kind == 'keyword':
                    if value:
                        self.domain_keywords.add(value)
                elif rule_kind == 'ip-cidr':
                    if value:
                        self.ip_cidrs.add(value)
                elif rule_kind == 'ip-asn':
                    if value:
                        self.ip_asns.add(value)
                break
    
    def _is_valid_domain(self, domain: str) -> bool:
        """验证域名格式"""
        if not domain or len(domain) > 253:
            return False
        # 基本域名格式检查
        pattern = r'^([a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?\.)*[a-zA-Z0-9]([a-zA-Z0-9\-]{0,61}[a-zA-Z0-9])?$'
        return bool(re.match(pattern, domain))
    
    def get_all_rules(self) -> Dict:
        """获取所有规则"""
        return {
            'domains': sorted(list(self.domains)),
            'domain_suffixes': sorted(list(self.domain_suffixes)),
            'domain_keywords': sorted(list(self.domain_keywords)),
            'ip_cidrs': sorted(list(self.ip_cidrs)),
            'ip_asns': sorted(list(self.ip_asns)),
        }

def fetch_rules_from_url(url: str) -> str:
    """从URL获取规则内容"""
    try:
        print(f"  📥 Fetching: {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        print(f"  ✅ Success: {len(response.text)} bytes")
        return response.text
    except Exception as e:
        print(f"  ❌ Failed: {e}")
        return ""

def fetch_all_rules() -> RuleParser:
    """从所有源获取规则"""
    parser = RuleParser()
    
    print("🌐 Fetching rules from GitHub repositories...\n")
    
    for source in RULE_SOURCES:
        print(f"📦 Source: {source['name']}")
        for url in source['urls']:
            content = fetch_rules_from_url(url)
            if content:
                for line in content.split('\n'):
                    parser.parse_line(line, source['type'])
        print()
    
    return parser

def load_custom_rules(custom_file: str) -> RuleParser:
    """加载自定义规则"""
    parser = RuleParser()
    
    custom_path = Path(custom_file)
    if custom_path.exists():
        print(f"📄 Loading custom rules from {custom_file}")
        with open(custom_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for line in content.split('\n'):
                parser.parse_line(line, 'clash')
    else:
        print(f"ℹ️  Custom rules file not found: {custom_file}, skipping...")
    
    return parser

def merge_parsers(parsers: List[RuleParser]) -> RuleParser:
    """合并多个解析器"""
    merged = RuleParser()
    
    for parser in parsers:
        merged.domains.update(parser.domains)
        merged.domain_suffixes.update(parser.domain_suffixes)
        merged.domain_keywords.update(parser.domain_keywords)
        merged.ip_cidrs.update(parser.ip_cidrs)
        merged.ip_asns.update(parser.ip_asns)
    
    return merged

def save_rules(parser: RuleParser, output_file: str):
    """保存规则到JSON文件"""
    rules = parser.get_all_rules()
    
    # 确保输出目录存在
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    output_data = {
        "name": "AI Projects Proxy Rules",
        "description": "Auto-generated AI proxy rules from multiple sources",
        "updated": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "total_rules": sum(len(v) for v in rules.values()),
        "sources": [s['name'] for s in RULE_SOURCES],
        "rules": rules
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)
    
    print(f"💾 Rules saved to {output_file}")
    print(f"📊 Statistics:")
    print(f"   - Exact domains: {len(rules['domains'])}")
    print(f"   - Domain suffixes: {len(rules['domain_suffixes'])}")
    print(f"   - Domain keywords: {len(rules['domain_keywords'])}")
    print(f"   - IP CIDRs: {len(rules['ip_cidrs'])}")
    print(f"   - IP ASNs: {len(rules['ip_asns'])}")
    print(f"   - Total rules: {output_data['total_rules']}")

def fetch_v2fly_rules() -> RuleParser:
    """从 v2fly/domain-list-community 获取 AI 相关规则"""
    base_url = "https://raw.githubusercontent.com/v2fly/domain-list-community/master/data/"
    services = [
        'openai',
        'anthropic',
        'google-deepmind',
        'huggingface',
        'perplexity',
        'xai',
        'groq'
    ]
    
    parser = RuleParser()
    
    for service in services:
        url = base_url + service
        print(f"📥 Fetching v2fly rules for {service}...")
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 404:
                print(f"⚠️ v2fly rule file not found for {service}, skipping.")
                continue
            response.raise_for_status()
            
            count = 0
            for line in response.text.splitlines():
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                
                # v2fly 格式: domain 或 include:other-file
                parts = line.split()
                domain = parts[0]
                
                # 处理属性 (e.g., full:example.com)
                if ':' in domain:
                    type_, value = domain.split(':', 1)
                    if type_ == 'full':
                        parser.domains.add(value)
                    elif type_ == 'keyword':
                        parser.domain_keywords.add(value)
                    # 忽略 regex 和其他类型
                else:
                    parser.domain_suffixes.add(domain)
                count += 1
                
            print(f"✅ Fetched {count} domains for {service}")
            
        except Exception as e:
            print(f"❌ Failed to fetch v2fly rules for {service}: {e}")
            
    return parser

def main():
    print("🚀 AI Proxy Rules Fetcher")
    print("=" * 60)
    print()
    
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 获取GitHub规则
    github_parser = fetch_all_rules()
    
    # 获取 v2fly AI 规则
    v2fly_parser = fetch_v2fly_rules()
    
    # 加载自定义规则
    custom_file = project_root / 'data' / 'custom_rules.txt'
    custom_parser = load_custom_rules(str(custom_file))
    
    # 加载采集的项目规则
    collected_file = project_root / 'data' / 'collected_projects.json'
    collected_parser = RuleParser()
    if collected_file.exists():
        print(f"📄 Loading collected projects from {collected_file}")
        with open(collected_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for domain in data.get('domains', []):
                collected_parser.domain_suffixes.add(domain)
            for keyword in data.get('keywords', []):
                collected_parser.domain_keywords.add(keyword)
            for cidr in data.get('ip_cidrs', []):
                collected_parser.ip_cidrs.add(cidr)
            for asn in data.get('ip_asns', []):
                collected_parser.ip_asns.add(asn)
    
    # 合并所有规则
    print("🔄 Merging all rules...")
    final_parser = merge_parsers([github_parser, v2fly_parser, custom_parser, collected_parser])
    
    # 保存结果
    print()
    output_file = project_root / 'data' / 'ai_projects.json'
    save_rules(final_parser, str(output_file))
    
    print()
    print("✨ Rule fetching completed!")

if __name__ == '__main__':
    main()
