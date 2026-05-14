# mimo2codex 使用 SOP

> 適用環境：Windows 11 + Node.js 18+

## 目錄

1. [快速開始](#1-快速開始)
2. [本地安裝與設定](#2-本地安裝與設定)
3. [Hugging Face Space 使用](#3-hugging-face-space-使用)
4. [Codex CLI 設定](#4-codex-cli-設定)
5. [Codex 桌面端設定](#5-codex-桌面端設定)
6. [常用指令](#6-常用指令)
7. [故障排除](#7-故障排除)
8. [更新與部署](#8-更新與部署)

---

## 1. 快速開始

### 前置需求

- Node.js ≥ 18（[下載](https://nodejs.org/)）
- MiMo 或 DeepSeek API Key

### 取得 API Key

| Provider | 控制台 | Key 前綴 |
|---|---|---|
| MiMo | [platform.xiaomimimo.com](https://platform.xiaomimimo.com) | `sk-`（按量）/ `tp-`（Token 套餐） |
| DeepSeek | [api-docs.deepseek.com](https://api-docs.deepseek.com) | `sk-` |

---

## 2. 本地安裝與設定

### 方式一：npm 全域安裝（推薦）

```powershell
npm install -g mimo2codex
```

### 方式二：一鍵腳本

```powershell
irm https://raw.githubusercontent.com/7as0nch/mimo2codex/main/scripts/install.ps1 | iex
```

### 方式三：手動建置

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex
npm install
npm run web:install
npm run build:all
npm link
```

### 啟動代理

**MiMo：**
```powershell
$env:MIMO_API_KEY="sk-你的MiMo金鑰"
mimo2codex
```

**DeepSeek：**
```powershell
$env:DS_API_KEY="sk-你的DeepSeek金鑰"
mimo2codex --model ds
```

**雙 Provider 同時啟用：**
```powershell
$env:MIMO_API_KEY="sk-mimo-key"
$env:DS_API_KEY="sk-deepseek-key"
mimo2codex
```

啟動後會顯示：
- Admin UI 地址：`http://127.0.0.1:8788/admin/`
- auth.json 和 config.toml 的設定內容

---

## 3. Hugging Face Space 使用

### 線上聊天介面

直接訪問：**https://huggingface.co/spaces/gregcho/mimo2codex**

1. 在左側選擇 Provider（MiMo 或 DeepSeek）
2. 選擇模型
3. 輸入你的 API Key
4. 調整 Temperature 和 Max Tokens
5. 開始聊天

### Space 更新部署

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex-hf-space
python -c "
from huggingface_hub import HfApi
import os
api = HfApi(token='HF_TOKEN')
for fname in os.listdir('.'):
    if os.path.isfile(fname):
        api.upload_file(path_or_fileobj=fname, path_in_repo=fname, repo_id='gregcho/mimo2codex', repo_type='space')
print('Done!')
"
```

---

## 4. Codex CLI 設定

### 步驟 1：建立設定檔

建立 `%USERPROFILE%\.codex\auth.json`：
```json
{
  "OPENAI_API_KEY": "mimo2codex-local"
}
```

建立 `%USERPROFILE%\.codex\config.toml`：
```toml
model = "mimo-v2.5-pro"
wire_api = "responses"
```

> 或直接複製 mimo2codex 啟動時顯示的內容。

### 步驟 2：啟動 mimo2codex

```powershell
$env:MIMO_API_KEY="sk-你的金鑰"
mimo2codex
```

### 步驟 3：啟動 Codex CLI

```powershell
codex
```

---

## 5. Codex 桌面端設定

1. 完全退出 Codex 桌面端（托盤 → 退出）
2. 編輯 `auth.json` 和 `config.toml`（同上）
3. 重新啟動 Codex 桌面端
4. 在模型下拉選單中選擇 `mimo-v2.5-pro`

---

## 6. 常用指令

```powershell
# 查看版本
mimo2codex --version

# 輸出設定片段
mimo2codex print-config

# 輸出 cc-switch 設定
mimo2codex print-cc-switch

# 指定端口
mimo2codex --port 9999

# 關閉 Admin UI
mimo2codex --no-admin

# 不顯示思考過程
mimo2codex --no-reasoning

# 除錯模式
mimo2codex --verbose
```

---

## 7. 故障排除

### MiMo 報 400 "reasoning_content must be passed back"

升級到 mimo2codex ≥ 0.2.3：
```powershell
npm update -g mimo2codex
```

### Admin UI 顯示 503

重新建置前端：
```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex
npm run build:all
```

### Codex 桌面端沒讀到新設定

完全退出後重啟（托盤 → 退出，不只是關視窗）。

### DeepSeek 報 401

確認使用 `DS_API_KEY` 且金鑰正確。

---

## 8. 更新與部署

### 更新 mimo2codex

```powershell
npm update -g mimo2codex
mimo2codex --version
```

### 更新本地倉庫

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex
git pull
npm install
npm run build:all
```

### 重新部署 Hugging Face Space

```powershell
cd C:\Users\Greg\Desktop\AI\mimo2codex-hf-space
# 修改 app.py 後
python deploy.py
```

---

## 相關連結

- [mimo2codex GitHub](https://github.com/7as0nch/mimo2codex)
- [mimo2codex npm](https://www.npmjs.com/package/mimo2codex)
- [Hugging Face Space](https://huggingface.co/spaces/gregcho/mimo2codex)
- [MiMo 控制台](https://platform.xiaomimimo.com)
- [DeepSeek API](https://api-docs.deepseek.com)
