[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/SO1PVZ3b)
# Neurosynth Backend

A lightweight Flask backend that exposes **functional dissociation** endpoints on top of a Neurosynth-backed PostgreSQL database.

The service provides two APIs that return studies mentioning one concept/coordinate **but not** the other (A \ B). You can also query the opposite direction (B \ A).


## Table of Contents

- [Endpoints](#endpoints)
  - [Dissociate by terms](#dissociate-by-terms)
  - [Dissociate by MNI coordinates](#dissociate-by-mni-coordinates)
- [Quick Start](#quick-start)
  - [2) Verify the connection](#2-verify-the-connection)
  - [3) Populate the database](#3-populate-the-database)
  - [4) Run the Flask service](#4-run-the-flask-service)
  - [5) Smoke tests](#5-smoke-tests)
- [Environment Variables](#environment-variables)
- [Notes](#notes)
- [License](#license)


## Endpoints


```
GET /dissociate/terms/<term_a>/<term_b>

Returns studies that mention **`term_a`** but **not** `term_b`.


```
/dissociate/terms/posterior_cingulate/ventromedial_prefrontal
```

---
### Dissociate by MNI coordinates

```
```

Coordinates are passed as `x_y_z` (underscores, not commas).  
Returns studies that mention **`[x1, y1, z1]`** but **not** `[x2, y2, z2]`.
**Default Mode Network test case**

```
/dissociate/locations/0_-52_26/-2_50_-6
/dissociate/locations/-2_50_-6/0_-52_26
```

> Tip: You may design a single endpoint that returns **both directions** in one response (A–B **and** B–A) if that better suits your client.

---

## Quick Start

### 1) Provision PostgreSQL

Create a PostgreSQL database (e.g., on Render).

### 2) Verify the connection

```bash
python check_db.py --url "postgresql://<USER>:<PASSWORD>@<HOST>:5432/<DBNAME>"
```

### 3) Populate the database

```bash
python check_db.py --url "postgresql://shih_yun:f6jUpbNz3ZVrhjsddNkcXpCzrj5FEPaC@dpg-d3jp1u49c44c73c27npg-a.oregon-postgres.render.com/neurosynthbackend"
```

### 4) Run the Flask service

Deploy `app.py` as a Web Service (e.g., on Render) and set the environment variable:

- `DB_URL=postgresql://shih_yun:f6jUpbNz3ZVrhjsddNkcXpCzrj5FEPaC@dpg-d3jp1u49c44c73c27npg-a.oregon-postgres.render.com/neurosynthbackend`

用 Gunicorn 啟動：

```bash
gunicorn app:app --bind 0.0.0.0:$PORT
```

#### 本地測試

1. 安裝 Flask：
   ```bash
   pip install flask
   ```

2. 在專案根目錄建立 `.env` 檔案，內容如下（請填入你的 DB_URL）：
   ```
   DB_URL=postgresql://shih_yun:f6jUpbNz3ZVrhjsddNkcXpCzrj5FEPaC@dpg-d3jp1u49c44c73c27npg-a.oregon-postgres.render.com/neurosynthbackend
   ```

3. 啟動 Flask 伺服器（選擇一種）：
   ```bash
   sudo flask --app ns-mini.py run --port 80 --debug
   # 或
   flask --app ns-mini.py run --port 5001 --debug
   ```

**說明：**  
請將 `app.py` 裡 dotenv 的註解移除，改成：
```python
from dotenv import load_dotenv
load_dotenv()  # 在本地執行，請將你的 database URL 放在 .env 裡
```
這樣 Flask 會自動讀取 `.env` 檔案裡的 `DB_URL`，本地執行就能連線資料庫。

SQL 測試（不透過 API）：你可以直接用 `sql.py` 測試 dissociate 查詢

### 5) Smoke tests

After deployment, check the basic endpoints:

- Images: `https://<your-app>.onrender.com/img`
- DB connectivity: `https://<your-app>.onrender.com/test_db`

---

## Environment Variables

- **`DB_URL`** – Full PostgreSQL connection string used by the app.  
  Example:  
  `postgresql://shih_yun:f6jUpbNz3ZVrhjsddNkcXpCzrj5FEPaC@dpg-d3jp1u49c44c73c27npg-a.oregon-postgres.render.com/neurosynthbackend`

> **Security note:** Never commit real credentials to version control. Use environment variables or your hosting provider’s secret manager.

---

## Example Requests

**By terms**

```bash
curl https://zero5-shih-yunlin.onrender.com/dissociate/terms/posterior_cingulate/ventromedial_prefrontal
curl https://zero5-shih-yunlin.onrender.com/dissociate/terms/ventromedial_prefrontal/posterior_cingulate
```

**By coordinates**

```bash
curl https://zero5-shih-yunlin.onrender.com/dissociate/locations/0_-52_26/-2_50_-6
curl https://zero5-shih-yunlin.onrender.com/dissociate/locations/-2_50_-6/0_-52_26
```

---

## Requirements

- Python 3.10+
- PostgreSQL 12+
- Python dependencies (typical):
  - `Flask`
  - `SQLAlchemy`
  - PostgreSQL driver (e.g., `psycopg2-binary`)
  - Production WSGI server (e.g., `gunicorn`)

---

## Notes

- Path parameters use underscores (`_`) between coordinates: `x_y_z`.
- Term strings should be URL-safe (e.g., `posterior_cingulate`, `ventromedial_prefrontal`). Replace spaces with underscores on the client if needed.
- The term/coordinate pairs above illustrate a **Default Mode Network** dissociation example. Adjust for your analysis.
- `GPT-4.1.json`：作業用的 JSON 檔案，可用於模型測試或資料記錄。
---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
