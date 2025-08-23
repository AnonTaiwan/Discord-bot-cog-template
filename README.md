# Anon Taiwan Discord Bot Cog Example

一個範例 Bot repo  
任何希望實作功能並整合進 Anon Taiwan Discord 機器人的開發者  
須以此為模板進行開發，並不得更動 `bot.py`  
僅能提交 `cog/` 資料夾內的檔案供管理員審核  
管理員審核並同意後始得將該功能整合進 Anon Taiwan 的 Discord 機器人  
若有需要可以在 `JSON/bot.json` 儲存隱密資料，並於提交申請時一併告知

### Requirements

- Python: 3.8~3.12

若有任何特殊需求請在申請時一併提出

### Tutorial

#### 1. Install Python

#### 2. Install Prerequisites

```bash
$ pip install -r requirements.txt
```

#### 3. Config environment

```bash
$ cp JSON/bot.json.sample JSON/bot.json
```

Edit the values in `JSON/bot.json`

#### 4. Run

```bash
$ python3 bot.py
```