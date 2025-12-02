#!/usr/bin/env python3
"""
生成多种代理工具的规则文件
Generate proxy rules for multiple proxy tools
"""

import json
from datetime import datetime
from typing import List, Dict
from pathlib import Path

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
    """生成Sing-box规则 (JSON格式)
    
    此函数生成的是 source format (JSON)，可以被 sing-box 直接使用。
    如需更高性能，可以使用以下命令编译为 SRS 二进制格式：
    
    sing-box rule-set compile --output ai-proxy.srs sing-box.json
    
    SRS 格式说明：
    - SRS (Sing-box Rule Set) 是优化后的二进制格式
    - 相比 JSON 格式有更好的性能和更小的文件体积
    - 推荐在生产环境使用 SRS 格式
    """
    total_rules = sum(len(v) for v in rules.values())
    
    # 使用 version 2 以优化 domain_suffix 的内存使用
    # version 1: 初始版本 (sing-box 1.8.0+)
    # version 2: 优化 domain_suffix 内存使用 (sing-box 1.10.0+)
    rule_set = {
        "version": 2,
        "rules": []
    }
    
    # 添加域名规则
    if rules.get('domains') or rules.get('domain_suffixes') or rules.get('domain_keywords'):
        domain_rule = {}
        if rules.get('domains'):
            domain_rule["domain"] = rules['domains']
        if rules.get('domain_suffixes'):
            domain_rule["domain_suffix"] = rules['domain_suffixes']
        if rules.get('domain_keywords'):
            domain_rule["domain_keyword"] = rules['domain_keywords']
        rule_set["rules"].append(domain_rule)
    
    # 添加IP规则
    ip_rule = {}
    if rules.get('ip_cidrs'):
        ip_rule["ip_cidr"] = rules['ip_cidrs']
    
    if rules.get('ip_asns'):
        # 确保ASN是整数
        asns = []
        for asn in rules['ip_asns']:
            try:
                asns.append(int(asn))
            except ValueError:
                continue
        if asns:
            ip_rule["ip_asn"] = asns
            
    if ip_rule:
        rule_set["rules"].append(ip_rule)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(rule_set, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Sing-box rules saved to {output_file} ({total_rules} rules)")
    print(f"   💡 Tip: Compile to SRS for better performance:")
    print(f"   sing-box rule-set compile --output ai-proxy.srs {Path(output_file).name}")

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
    
    # 获取脚本所在目录的父目录（项目根目录）
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    
    # 加载规则数据
    data_file = project_root / 'data' / 'ai_projects.json'
    rules = load_rules(str(data_file))
    
    total_rules = sum(len(v) for v in rules.values())
    print(f"📊 Total rules: {total_rules}")
    print(f"   - Exact domains: {len(rules.get('domains', []))}")
    print(f"   - Domain suffixes: {len(rules.get('domain_suffixes', []))}")
    print(f"   - Domain keywords: {len(rules.get('domain_keywords', []))}")
    print(f"   - IP CIDRs: {len(rules.get('ip_cidrs', []))}")
    print(f"   - IP ASNs: {len(rules.get('ip_asns', []))}")
    print()
    
    # 确保输出目录存在
    rules_dir = project_root / 'rules'
    rules_dir.mkdir(parents=True, exist_ok=True)
    
    # 生成各种格式的规则
    generate_clash_rules(rules, str(rules_dir / 'clash.yaml'))
    generate_surge_rules(rules, str(rules_dir / 'surge.conf'))
    generate_quantumult_x_rules(rules, str(rules_dir / 'quantumult-x.conf'))
    generate_shadowrocket_rules(rules, str(rules_dir / 'shadowrocket.conf'))
    generate_singbox_rules(rules, str(rules_dir / 'sing-box.json'))
    generate_loon_rules(rules, str(rules_dir / 'loon.conf'))
    
    print("\n✨ Rule generation completed!")

if __name__ == '__main__':
    main()
