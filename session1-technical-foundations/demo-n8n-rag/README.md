# RAG Foundation Lab - n8n

**視覺化、真實環境的 RAG 實作**

---

## 啟動 n8n

### 選項 1：本機環境（推薦）

```bash
# 1. 確認已安裝 Docker 和 Docker Compose
docker --version
docker compose version

# 2. 下載 docker-compose.yml
mkdir -p demo-n8n-rag
cd demo-n8n-rag/
curl -O https://raw.githubusercontent.com/livhg/ai-coding/main/session1-technical-foundations/demo-n8n-rag/docker-compose.yml

# 3. 啟動環境
docker compose up -d
```

### 選項 2：Play with Docker 線上環境

如果本機沒有安裝 Docker，可使用免費的線上環境：

1. 前往 https://labs.play-with-docker.com/
2. 登入（需要 Docker Hub 帳號）
3. 點擊 **+ ADD NEW INSTANCE**
4. 執行以下指令：

```bash
# 下載 docker-compose.yml
curl -O https://raw.githubusercontent.com/livhg/ai-coding/main/session1-technical-foundations/demo-n8n-rag/docker-compose.yml

# 啟動環境
docker compose up -d
```

> ⚠️ **注意**：Play with Docker 的 session 會在 2 小時後自動關閉，資料不會保存。

## 開啟 n8n

瀏覽器輸入：http://localhost:5678  
若使用 Play with Docker，點擊頁面上的 `OPEN PORT` 並輸入 **5678**，即可開啟 n8n

### Login Account
第一次登入會要求 sign up，所有資料都保存在該環境內，環境結束即刪除。

## 建立 RAG Workflow

1. Start from scratch
2. Open node -> RAG starter template
3. Modify your embedding model and chat model
4. Execute workflow
5. Upload knowledge base
6. Open chat

---

## 📊 5 個 CSV 知識庫

| 檔案 | 主題 | 文件數 | 測試問題範例 |
|------|------|--------|------------|
| `01_ai_ml_basics.csv` | AI/ML 基礎 | 8 | "什麼是 RAG？" |
| `02_python_basics.csv` | Python 語言 | 8 | "如何讀取檔案？" |
| `03_coffee_shop.csv` | 咖啡店產品 | 8 | "拿鐵多少錢？" |
| `04_remote_work.csv` | 遠端工作 | 8 | "如何申請休假？" |
| `05_ecommerce.csv` | 電商平台 | 8 | "如何退貨？" |

---

## 關閉與清理

### 停止容器

```bash
# 在 docker-compose.yml 所在目錄執行
docker compose down
```

### 完全移除（包含資料）

```bash
# 停止並移除容器、網路、volumes
docker compose down -v

# 移除 n8n 映像檔（可選）
docker rmi n8nio/n8n:latest
```

> 💡 **提示**：如果只是暫時停止，使用 `docker compose down` 即可，資料會保留在 volume 中。下次執行 `docker compose up -d` 時會恢復。

---