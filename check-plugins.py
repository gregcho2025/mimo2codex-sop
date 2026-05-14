"""
Codex 插件配置檢查腳本
用法: python check-plugins.py
"""
import os
import sys

CONFIG_PATH = os.path.expanduser(r"~\.codex\config.toml")

REQUIRED_PLUGINS = {
    'browser-use@openai-bundled',
    'chrome@openai-bundled',
    'computer-use@openai-bundled',
    'hyperframes@openai-curated',
    'documents@openai-primary-runtime',
    'spreadsheets@openai-primary-runtime',
    'presentations@openai-primary-runtime',
}

def check_plugins():
    if not os.path.exists(CONFIG_PATH):
        print(f"Error: Config file not found: {CONFIG_PATH}")
        sys.exit(1)

    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    print("Checking Codex plugins configuration...\n")

    found = set()
    missing = set()

    for plugin in REQUIRED_PLUGINS:
        if f'plugins."{plugin}"' in content and "enabled = true" in content:
            found.add(plugin)
            print(f"  [OK] {plugin}")
        else:
            missing.add(plugin)
            print(f"  [MISSING] {plugin}")

    print(f"\n{'='*40}")
    print(f"Found: {len(found)}/{len(REQUIRED_PLUGINS)}")

    if missing:
        print(f"\nMissing plugins. Add to {CONFIG_PATH}:")
        print()
        for plugin in missing:
            print(f'[plugins."{plugin}"]')
            print("enabled = true")
            print()
    else:
        print("\nAll plugins configured!")

    if "mimo2codex" in content and "8788" in content:
        print("\n[OK] mimo2codex provider configured")
    else:
        print("\n[MISSING] mimo2codex provider not configured")
        print("Add to config.toml:")
        print()
        print('[model_providers.mimo2codex]')
        print('name = "mimo2codex"')
        print('wire_api = "responses"')
        print('requires_openai_auth = true')
        print('base_url = "http://127.0.0.1:8788/v1"')

if __name__ == "__main__":
    check_plugins()
