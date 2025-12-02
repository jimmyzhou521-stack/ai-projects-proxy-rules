#!/usr/bin/env python3
"""
Sing-box SRS 编译辅助脚本
自动检测 sing-box 工具并编译 JSON 规则为 SRS 格式
"""

import os
import sys
import subprocess
from pathlib import Path

def check_singbox_installed():
    """检查 sing-box 是否已安装"""
    try:
        result = subprocess.run(['sing-box', 'version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        if result.returncode == 0:
            version_line = result.stdout.split('\n')[0]
            print(f"✅ Found {version_line}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass
    
    print("❌ sing-box not found!")
    print("\n📥 Installation instructions:")
    print("   Linux/macOS: bash <(curl -fsSL https://sing-box.app/get.sh)")
    print("   Windows:     scoop install sing-box")
    print("   Manual:      https://github.com/SagerNet/sing-box/releases")
    return False

def compile_to_srs(json_file: Path, output_file: Path = None):
    """编译 JSON 规则为 SRS 格式"""
    if not json_file.exists():
        print(f"❌ File not found: {json_file}")
        return False
    
    if output_file is None:
        output_file = json_file.with_suffix('.srs')
    
    print(f"\n🔨 Compiling {json_file.name} to {output_file.name}...")
    
    try:
        result = subprocess.run(
            ['sing-box', 'rule-set', 'compile', 
             '--output', str(output_file), 
             str(json_file)],
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            json_size = json_file.stat().st_size
            srs_size = output_file.stat().st_size
            reduction = ((json_size - srs_size) / json_size) * 100
            
            print(f"✅ Successfully compiled!")
            print(f"   📊 Size comparison:")
            print(f"      JSON: {json_size:,} bytes")
            print(f"      SRS:  {srs_size:,} bytes")
            print(f"      Reduction: {reduction:.1f}%")
            return True
        else:
            print(f"❌ Compilation failed!")
            print(f"   Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Compilation timeout!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 Sing-box SRS Compilation Tool")
    print("=" * 60)
    
    # 检查 sing-box 是否安装
    if not check_singbox_installed():
        sys.exit(1)
    
    # 获取项目根目录
    script_dir = Path(__file__).parent
    project_root = script_dir.parent
    rules_dir = project_root / 'rules'
    
    # 编译 sing-box.json
    json_file = rules_dir / 'sing-box.json'
    srs_file = rules_dir / 'sing-box.srs'
    
    if compile_to_srs(json_file, srs_file):
        print(f"\n✨ SRS file created: {srs_file}")
        print(f"\n📝 Usage in sing-box config:")
        print("""
{
  "route": {
    "rule_set": [
      {
        "type": "local",
        "tag": "ai-proxy",
        "format": "binary",
        "path": "path/to/sing-box.srs"
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
        """)
    else:
        sys.exit(1)

if __name__ == '__main__':
    main()
