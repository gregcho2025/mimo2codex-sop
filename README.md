# mimo2codex 完整使用 SOP

> 從零開始，到 Codex + MiMo 可正常使用。
> 適用環境：Windows 11 + Node.js 18+

---

## 目錄

1. [前置準備](#1-前置準備)
2. [安裝 mimo2codex](#2-安裝-mimo2codex)
3. [取得 API Key](#3-取得-api-key)
4. [建立桌面啟動捷徑](#4-建立桌面啟動捷徑)
5. [設定 Codex CLI](#5-設定-codex-cli)
6. [設定 Codex 桌面端](#6-設定-codex-桌面端)
7. [Codex 插件配置](#7-codex-插件配置)
8. [Hugging Face 線上聊天](#8-hugging-face-線上聊天)
9. [日常使用流程](#9-日常使用流程)
10. [常用指令速查](#10-常用指令速查)
11. [故障排除](#11-故障排除)
12. [更新維護](#12-更新維護)
13. [相關連結](#13-相關連結)

---

## 1. 前置準備

### 系統需求

| 項目 | 需求 |
|---|---|
| 作業系統 | Windows 11 |
| Node.js | ≥ 18（[下載](https://nodejs.org/)） |
| npm | 隨 Node.js 一起安裝 |

### 確認 Node.js 已安裝

開啟 PowerShell，執行：

```powershell
node --version
npm --version
```

如果顯示版本號（如 `v24.14.1`），表示已安裝。如果報錯，先到 [nodejs.org](https://nodejs.org/) 下載安裝。

---

## 2. 安裝 mimo2codex

### 方式一：npm 全域安裝（推薦）

```powershell
npm install -g mimo2codex
```

### 方式二：一鍵腳本

```powershell
irm https://raw.githubusercontent.com/7as0nch/mimo2codex/main/scripts/install.ps1 | iex
```

### 方式三：從原始碼建置

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex
npm install
npm run web:install
npm run build:all
npm link
```

### 確認安裝成功

```powershell
mimo2codex --version
```

應顯示 `0.2.4` 或更高版本。

---

## 3. 取得 API Key

### MiMo（小米米莫）

1. 前往 [platform.xiaomimimo.com](https://platform.xiaomimimo.com)
2. 註冊 / 登入
3. 控制台 → API Keys → 建立新 Key
4. 複製金鑰（`sk-` 開頭為按量計費，`tp-` 開頭為 Token 套餐）

### DeepSeek

1. 前往 [api-docs.deepseek.com](https://api-docs.deepseek.com)
2. 註冊 / 登入
3. 建立 API Key
4. 複製金鑰（`sk-` 開頭）

### Key 前綴說明

| 前綴 | 說明 |
|---|---|
| `sk-` | 按量計費（Pay-as-you-go） |
| `tp-` | Token 套餐（Token Plan） |

> `tp-` 開頭的 Key 會自動走 token-plan 主機，`sk-` 開頭走 pay-as-you-go 主機。

---

## 4. 建立桌面啟動捷徑

### 建立批次檔

在桌面建立 `啟動mimo2codex.bat`，內容如下：

```bat
@echo off
title mimo2codex Proxy
echo ========================================
echo   mimo2codex Proxy 啟動中...
echo ========================================
echo.

set MIMO_API_KEY=tp-你的MiMo金鑰

echo [MiMo V2.5 Pro - Token Plan]
echo 代理位址: http://127.0.0.1:8788
echo Admin UI: http://127.0.0.1:8788/admin/
echo.
echo 按 Ctrl+C 可停止代理
echo ========================================
echo.

mimo2codex

pause
```

> 把 `tp-你的MiMo金鑰` 換成你的實際 API Key。

### 使用方式

- **雙擊** `啟動mimo2codex.bat` 即可啟動代理
- 視窗會顯示代理狀態、Admin UI 網址
- 按 **Ctrl+C** 可停止代理

### 開機自動啟動（選用）

1. 按 `Win+R`，輸入 `shell:startup`，開啟啟動資料夾
2. 把 `啟動mimo2codex.bat` 的捷徑（右鍵 → 建立捷徑）拖進去
3. 以後開機就會自動啟動代理

---

## 5. 設定 Codex CLI

### 步驟 1：確認 mimo2codex 正在執行

雙擊桌面上的 `啟動mimo2codex.bat`，確認看到：

```
mimo2codex v0.2.4 listening on http://127.0.0.1:8788
```

### 步驟 2：設定 auth.json

編輯 `%USERPROFILE%\.codex\auth.json`（即 `C:\Users\Greg\.codex\auth.json`）：

```json
{
  "OPENAI_API_KEY": "mimo2codex-local"
}
```

> 任何非空值都可以，mimo2codex 不驗證此欄位。

### 步驟 3：設定 config.toml

編輯 `%USERPROFILE%\.codex\config.toml`（即 `C:\Users\Greg\.codex\config.toml`）：

找到 `model_provider` 和 `model` 那兩行，改成：

```toml
model_provider = "mimo2codex"
model = "mimo-v2.5-pro"
model_context_window = 128000
```

找到 `[model_providers]` 區塊，確認有：

```toml
[model_providers.mimo2codex]
name = "mimo2codex"
wire_api = "responses"
requires_openai_auth = true
base_url = "http://127.0.0.1:8788/v1"
```

### 步驟 4：啟動 Codex CLI

```powershell
codex
```

在 Codex 裡直接輸入指令，就會使用 MiMo V2.5 Pro 模型。

---

## 6. 設定 Codex 桌面端

### 步驟 1：完全退出 Codex

- 系統托盤（右下角）→ 找到 Codex 圖示 → 右鍵 → **退出**
- 不只是關視窗，必須完全退出

### 步驟 2：確認 mimo2codex 正在執行

雙擊 `啟動mimo2codex.bat`。

### 步驟 3：確認設定檔

- `auth.json` 和 `config.toml` 已按上方步驟設定好

### 步驟 4：重新啟動 Codex 桌面端

- 開啟 Codex App
- 在模型下拉選單中選擇 `mimo-v2.5-pro`

---

## 7. Codex 插件配置

以下插件如果已在 `config.toml` 中啟用，無需額外設定。

### 確認插件狀態

開啟 `%USERPROFILE%\.codex\config.toml`，確認以下區塊存在：

```toml
[plugins."browser-use@openai-bundled"]
enabled = true

[plugins."chrome@openai-bundled"]
enabled = true

[plugins."computer-use@openai-bundled"]
enabled = true

[plugins."hyperframes@openai-curated"]
enabled = true

[plugins."documents@openai-primary-runtime"]
enabled = true

[plugins."spreadsheets@openai-primary-runtime"]
enabled = true

[plugins."presentations@openai-primary-runtime"]
enabled = true
```

### 如果缺少插件配置

在 `config.toml` 的 `[model_providers]` 區塊之後，加入上述內容。

### 插件使用方式

| 插件 | 調用方式 | 用途 |
|---|---|---|
| Chrome | `@Chrome 打開 X，幫我讀這條帖子` | 需要登入態的網站操作 |
| Browser | `@Browser 打開 http://localhost:3000` | 本地網頁測試 |
| Computer | `@Computer 打開系統設定` | 桌面操作、權限檢查 |
| HyperFrames | `@HyperFrames 做一個 10 秒產品介紹視頻` | HTML 視頻、動效 |

### Chrome 插件額外需求

1. 安裝 Codex Chrome Extension：[Chrome Web Store](https://chromewebstore.google.com/detail/codex/hehggadaopoacecdllhhajmbjkdcmajg)
2. 確認 Codex native host 正常運作
3. 如果 `@Chrome` 連不上，檢查擴展狀態

### HyperFrames 注意事項

正確寫法：
```toml
[plugins."hyperframes@openai-curated"]
enabled = true
```

錯誤寫法（不要這樣寫）：
```toml
[plugins."hyperframes@plugins"]
enabled = true
```

> marketplace 名稱是 `openai-curated`，不是本地資料夾名。

---

## 8. Hugging Face 線上聊天

### 直接使用

訪問：**https://huggingface.co/spaces/gregcho/mimo2codex**

1. 左側 **Provider** 選 MiMo V2.5 Pro 或 DeepSeek V4 Pro
2. **Model** 選模型
3. **API Key** 輸入你的金鑰
4. 調整 Temperature 和 Max Tokens
5. 開始聊天

### 重新部署 Space

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex-hf-space
python -c "
from huggingface_hub import HfApi
import os
api = HfApi(token='你的HF_TOKEN')
for fname in os.listdir('.'):
    if os.path.isfile(fname):
        api.upload_file(path_or_fileobj=fname, path_in_repo=fname, repo_id='gregcho/mimo2codex', repo_type='space')
print('Done!')
"
```

---

## 9. 日常使用流程

### 每次使用 Codex 的步驟

1. **雙擊** 桌面上的 `啟動mimo2codex.bat`（啟動代理）
2. 開啟新的 PowerShell 視窗或 Codex 桌面端
3. 執行 `codex` 或在桌面端選擇模型
4. 開始使用

### 檢查代理狀態

瀏覽器開啟：http://127.0.0.1:8788/admin/

可以查看：
- 請求日誌
- Token 用量統計
- 模型映射記錄
- Provider 狀態

---

## 10. 常用指令速查

```powershell
# 查看版本
mimo2codex --version

# 輸出 Codex 設定內容
mimo2codex print-config

# 輸出 cc-switch 設定
mimo2codex print-cc-switch

# 指定端口（預設 8788）
mimo2codex --port 9999

# 關閉 Admin UI
mimo2codex --no-admin

# 不顯示思考過程（多輪工具調用仍回傳）
mimo2codex --no-reasoning

# 除錯模式（顯示每次翻譯的請求體）
mimo2codex --verbose

# 使用 DeepSeek
mimo2codex --model ds

# 同時啟用雙 Provider
$env:MIMO_API_KEY="sk-mimo-key"
$env:DS_API_KEY="sk-deepseek-key"
mimo2codex
```

---

## 11. 故障排除

### MiMo 報 400 "reasoning_content must be passed back"

```powershell
npm update -g mimo2codex
mimo2codex --version   # 確認 >= 0.2.3
```

### Admin UI 顯示 503 "Admin UI not built"

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex
npm run build:all
```

### Codex 桌面端沒讀到新設定

完全退出後重啟（托盤 → 退出，不只是關視窗）。

### DeepSeek 報 401 Unauthorized

確認使用 `DS_API_KEY` 且金鑰正確：

```powershell
mimo2codex --model ds --verbose
```

### 啟動時顯示 ⚠ key 前綴與主機不匹配

清除殘留的環境變數：

```powershell
# PowerShell
Remove-Item Env:MIMO_BASE_URL
[Environment]::SetEnvironmentVariable('MIMO_BASE_URL', $null, 'User')
```

### Codex 說"我馬上做"然後回合結束

通常是 `reasoning_content` 丟失，升級 mimo2codex ≥ 0.2.3。

### 報 "image_gen tool not available"

Codex 的 `/hatch` 想調 OpenAI 圖像 API，MiMo 沒有。用 mimoskill 替代：

```powershell
python mimoskill/scripts/generate_pet.py --description "chibi shiba 程序員" --out pet.png
```

### 插件入口是灰色的

1. 確認 `config.toml` 裡有插件配置（見第 7 節）
2. 完全退出 Codex 後重啟
3. 檢查 Chrome Extension 和 native host（如使用 Chrome 插件）

---

## 12. 更新維護

### 更新 mimo2codex

```powershell
npm update -g mimo2codex
mimo2codex --version
```

### 更新本地原始碼倉庫

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex
git pull
npm install
npm run build:all
```

### 更新 Hugging Face Space

修改 `C:\Users\Greg\Desktop\AI\mimo2codex-hf-space\app.py` 後，執行部署腳本。

### 更新 SOP 文件

修改 `C:\Users\Greg\Desktop\AI\mimo2codex-sop\README.md` 後：

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex-sop
git add README.md
git commit -m "Update SOP"
git push
```

---

## 13. 相關連結

| 項目 | 網址 |
|---|---|
| mimo2codex GitHub | https://github.com/7as0nch/mimo2codex |
| mimo2codex npm | https://www.npmjs.com/package/mimo2codex |
| Hugging Face Space | https://huggingface.co/spaces/gregcho/mimo2codex |
| SOP GitHub 倉庫 | https://github.com/gregcho2025/mimo2codex-sop |
| MiMo 控制台 | https://platform.xiaomimimo.com |
| DeepSeek API | https://api-docs.deepseek.com |
| Codex Chrome Extension | https://chromewebstore.google.com/detail/codex/hehggadaopoacecdllhhajmbjkdcmajg |

---

## 本地檔案結構

```
C:\Users\Greg\Desktop\AI\
├── mimo2codex\              # mimo2codex 原始碼
├── mimo2codex-hf-space\     # Hugging Face Space 部署檔案
│   ├── app.py               # Gradio 聊天介面
│   ├── requirements.txt     # Python 依賴
│   └── README.md            # Space 說明文件
└── mimo2codex-sop\          # SOP 文件（GitHub 倉庫）
    └── README.md            # 本文件

C:\Users\Greg\Desktop\
└── 啟動mimo2codex.bat        # 桌面啟動捷徑

C:\Users\Greg\.codex\
├── auth.json                # Codex 認證檔
└── config.toml              # Codex 設定檔（含插件配置）
```
