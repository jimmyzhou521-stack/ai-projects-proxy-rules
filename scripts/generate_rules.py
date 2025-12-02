#!/usr/bin/env python3
"""
生成多种代理工具的规则文件
Generate proxy rules for multiple proxy tools
"""

import json
from datetime import datetime
from typing import List, Dict

def load_rules(data_file: str) -> dict:
    """从数据文件加载所有规则"""
    with open(data_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 兼容旧格式
    if 'domains' in data and not 'rules' in data:
        return {
            'domain_suffixes': data.get('domains', []),
            'domains': [],
            'domain_keywords': [],
            'ip_cidrs': [],
            'ip_asns': []
        }
    
    return data.get('rules', {})

def generate_clash_rules(rules: dict, output_file: str):
    """生成Clash规则"""
    total_rules = sum(len(v) for v in rules.values())
    content = [
        "# AI网站代理规则 - Clash格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 规则总数: {total_rules}",
        "# 使用方法: 将以下规则添加到Clash配置文件的rules部分",
        "",
        "payload:",
    ]
    
    # 添加精确域名
    for domain in rules.get('domains', []):
        content.append(f"  - DOMAIN,{domain}")
    
    # 添加域名后缀
    for domain in rules.get('domain_suffixes', []):
        content.append(f"  - DOMAIN-SUFFIX,{domain}")
    
    # 添加域名关键词
    for keyword in rules.get('domain_keywords', []):
        content.append(f"  - DOMAIN-KEYWORD,{keyword}")
    
    # 添加IP CIDR
    for cidr in rules.get('ip_cidrs', []):
        content.append(f"  - IP-CIDR,{cidr}")
    
    # 添加IP ASN
    for asn in rules.get('ip_asns', []):
        content.append(f"  - IP-ASN,{asn}")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Clash rules saved to {output_file} ({total_rules} rules)")

def generate_surge_rules(rules: dict, output_file: str):
    """生成Surge规则"""
    total_rules = sum(len(v) for v in rules.values())
    content = [
        "# AI网站代理规则 - Surge格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 规则总数: {total_rules}",
        "# 使用方法: 将以下规则添加到Surge配置文件的[Rule]部分",
        "",
    ]
    
    # 添加精确域名
    for domain in rules.get('domains', []):
        content.append(f"DOMAIN,{domain},Proxy")
    
    # 添加域名后缀
    for domain in rules.get('domain_suffixes', []):
        content.append(f"DOMAIN-SUFFIX,{domain},Proxy")
    
    # 添加域名关键词
    for keyword in rules.get('domain_keywords', []):
        content.append(f"DOMAIN-KEYWORD,{keyword},Proxy")
    
    # 添加IP CIDR
    for cidr in rules.get('ip_cidrs', []):
        content.append(f"IP-CIDR,{cidr},Proxy")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Surge rules saved to {output_file} ({total_rules} rules)")

def generate_quantumult_x_rules(rules: dict, output_file: str):
    """生成Quantumult X规则"""
    total_rules = sum(len(v) for v in rules.values())
    content = [
        "# AI网站代理规则 - Quantumult X格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 规则总数: {total_rules}",
        "# 使用方法: 将以下规则添加到Quantumult X配置文件的[filter_remote]部分",
        "",
    ]
    
    # 添加精确域名
    for domain in rules.get('domains', []):
        content.append(f"HOST,{domain},proxy")
    
    # 添加域名后缀
    for domain in rules.get('domain_suffixes', []):
        content.append(f"HOST-SUFFIX,{domain},proxy")
    
    # 添加域名关键词
    for keyword in rules.get('domain_keywords', []):
        content.append(f"HOST-KEYWORD,{keyword},proxy")
    
    # 添加IP CIDR
    for cidr in rules.get('ip_cidrs', []):
        content.append(f"IP-CIDR,{cidr},proxy")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Quantumult X rules saved to {output_file} ({total_rules} rules)")

def generate_shadowrocket_rules(rules: dict, output_file: str):
    """生成Shadowrocket规则"""
    total_rules = sum(len(v) for v in rules.values())
    content = [
        "# AI网站代理规则 - Shadowrocket格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 规则总数: {total_rules}",
        "# 使用方法: 将以下规则添加到Shadowrocket配置文件的[Rule]部分",
        "",
    ]
    
    # 添加精确域名
    for domain in rules.get('domains', []):
        content.append(f"DOMAIN,{domain},PROXY")
    
    # 添加域名后缀
    for domain in rules.get('domain_suffixes', []):
        content.append(f"DOMAIN-SUFFIX,{domain},PROXY")
    
    # 添加域名关键词
    for keyword in rules.get('domain_keywords', []):
        content.append(f"DOMAIN-KEYWORD,{keyword},PROXY")
    
    # 添加IP CIDR
    for cidr in rules.get('ip_cidrs', []):
        content.append(f"IP-CIDR,{cidr},PROXY")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Shadowrocket rules saved to {output_file} ({total_rules} rules)")

def generate_singbox_rules(rules: dict, output_file: str):
    """生成Sing-box规则 (JSON格式)"""
    total_rules = sum(len(v) for v in rules.values())
    
    rule_set = {
        "version": 1,
        "rules": []
    }
    
    # 添加域名规则
    if rules.get('domains') or rules.get('domain_suffixes') or rules.get('domain_keywords'):
        domain_rule = {"outbound": "proxy"}
        if rules.get('domains'):
            domain_rule["domain"] = rules['domains']
        if rules.get('domain_suffixes'):
            domain_rule["domain_suffix"] = rules['domain_suffixes']
        if rules.get('domain_keywords'):
            domain_rule["domain_keyword"] = rules['domain_keywords']
        rule_set["rules"].append(domain_rule)
    
    # 添加IP规则
    if rules.get('ip_cidrs'):
        rule_set["rules"].append({
            "ip_cidr": rules['ip_cidrs'],
            "outbound": "proxy"
        })
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rule_set, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Sing-box rules saved to {output_file} ({total_rules} rules)")

def generate_loon_rules(rules: dict, output_file: str):
    """生成Loon规则"""
    total_rules = sum(len(v) for v in rules.values())
    content = [
        "# AI网站代理规则 - Loon格式",
        f"# 更新时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"# 规则总数: {total_rules}",
        "# 使用方法: 将以下规则添加到Loon配置文件的[Rule]部分",
        "",
    ]
    
    # 添加精确域名
    for domain in rules.get('domains', []):
        content.append(f"DOMAIN,{domain},PROXY")
    
    # 添加域名后缀
    for domain in rules.get('domain_suffixes', []):
        content.append(f"DOMAIN-SUFFIX,{domain},PROXY")
    
    # 添加域名关键词
    for keyword in rules.get('domain_keywords', []):
        content.append(f"DOMAIN-KEYWORD,{keyword},PROXY")
    
    # 添加IP CIDR
    for cidr in rules.get('ip_cidrs', []):
        content.append(f"IP-CIDR,{cidr},PROXY")
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))
    
    print(f"✅ Loon rules saved to {output_file} ({total_rules} rules)")

def main():
    print("🚀 Starting rule generation...")
    
    # 加载规则数据
    data_file = 'data/ai_projects.json'
    rules = load_rules(data_file)
    
    total_rules = sum(len(v) for v in rules.values())
    print(f"📊 Total rules: {total_rules}")
    print(f"   - Exact domains: {len(rules.get('domains', []))}")
    print(f"   - Domain suffixes: {len(rules.get('domain_suffixes', []))}")
    print(f"   - Domain keywords: {len(rules.get('domain_keywords', []))}")
    print(f"   - IP CIDRs: {len(rules.get('ip_cidrs', []))}")
    print(f"   - IP ASNs: {len(rules.get('ip_asns', []))}")
    print()
    
    # 生成各种格式的规则
    generate_clash_rules(rules, 'rules/clash.yaml')
    generate_surge_rules(rules, 'rules/surge.conf')
    generate_quantumult_x_rules(rules, 'rules/quantumult-x.conf')
    generate_shadowrocket_rules(rules, 'rules/shadowrocket.conf')
    generate_singbox_rules(rules, 'rules/sing-box.json')
    generate_loon_rules(rules, 'rules/loon.conf')
    
    print("\n✨ Rule generation completed!")

if __name__ == '__main__':
    main()
