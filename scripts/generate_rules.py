#!/usr/bin/env python3
"""
生成多种代理工具的规则文件
Generate proxy rules for multiple proxy tools
"""

import json
from datetime import datetime
from typing import List

def load_domains(data_file: str) -> List[str]:
    """从数据文件加载域名列表"""
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('domains', [])

def generate_clash_rules(domains: List[str], output_file: str):
    """生成Clash规则"""
    content = [
        "# AI网站代理规则 - Clash格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "# 使用方法: 将以下规则添加到Clash配置文件的rules部分",
        "",
        "payload:",
    ]
    
    for domain in domains:
        content.append(f"  - DOMAIN-SUFFIX,{domain}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Clash rules saved to {output_file}")

def generate_surge_rules(domains: List[str], output_file: str):
    """生成Surge规则"""
    content = [
        "# AI网站代理规则 - Surge格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "# 使用方法: 将以下规则添加到Surge配置文件的[Rule]部分",
        "",
    ]
    
    for domain in domains:
        content.append(f"DOMAIN-SUFFIX,{domain},Proxy")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Surge rules saved to {output_file}")

def generate_quantumult_x_rules(domains: List[str], output_file: str):
    """生成Quantumult X规则"""
    content = [
        "# AI网站代理规则 - Quantumult X格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "# 使用方法: 将以下规则添加到Quantumult X配置文件的[filter_remote]部分",
        "",
    ]
    
    for domain in domains:
        content.append(f"HOST-SUFFIX,{domain},proxy")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Quantumult X rules saved to {output_file}")

def generate_shadowrocket_rules(domains: List[str], output_file: str):
    """生成Shadowrocket规则"""
    content = [
        "# AI网站代理规则 - Shadowrocket格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "# 使用方法: 将以下规则添加到Shadowrocket配置文件的[Rule]部分",
        "",
    ]
    
    for domain in domains:
        content.append(f"DOMAIN-SUFFIX,{domain},PROXY")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Shadowrocket rules saved to {output_file}")

def generate_singbox_rules(domains: List[str], output_file: str):
    """生成Sing-box规则 (JSON格式)"""
    rules = {
        "version": 1,
        "rules": [
            {
                "domain_suffix": domains,
                "outbound": "proxy"
            }
        ]
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rules, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Sing-box rules saved to {output_file}")

def generate_loon_rules(domains: List[str], output_file: str):
    """生成Loon规则"""
    content = [
        "# AI网站代理规则 - Loon格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        "# 使用方法: 将以下规则添加到Loon配置文件的[Rule]部分",
        "",
    ]
    
    for domain in domains:
        content.append(f"DOMAIN-SUFFIX,{domain},PROXY")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Loon rules saved to {output_file}")

def main():
    print("🚀 Starting rule generation...")
    
    # 加载域名数据
    data_file = 'data/ai_projects.json'
    domains = load_domains(data_file)
    
    print(f"📊 Total domains: {len(domains)}")
    
    # 生成各种格式的规则
    generate_clash_rules(domains, 'rules/clash.yaml')
    generate_surge_rules(domains, 'rules/surge.conf')
    generate_quantumult_x_rules(domains, 'rules/quantumult-x.conf')
    generate_shadowrocket_rules(domains, 'rules/shadowrocket.conf')
    generate_singbox_rules(domains, 'rules/sing-box.json')
    generate_loon_rules(domains, 'rules/loon.conf')
    
    print("✨ Rule generation completed!")

if __name__ == '__main__':
    main()
