# Demo Project Setup Guide

## Step 1: Verify Installation

Before starting, ensure you have the required tools installed on your system.

### To verify installation:

```bash
python3 --version
npx --version
uv --version     # Optional but recommended
```

### Installation Guide

#### Python

- **Download:** https://www.python.org/downloads/

#### Node.js (npx included)

- **Windows:** `winget install OpenJS.NodeJS.LTS`
- **Download:** https://nodejs.org/zh-tw/download

#### uv (⚡ Recommended - Fast Python package manager)

- **Windows (PowerShell):**

  ```powershell
  powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
  ```

- **macOS/Linux:**

  ```bash
  curl -LsSf https://astral.sh/uv/install.sh | sh
  ```

- **More installation options:** https://docs.astral.sh/uv/getting-started/installation/

---

## Step 2: Clone the demo project

```bash
git clone git@github.com:livhg/demo-mcp-server.git
```

Or download from https://github.com/livhg/demo-mcp-server.git

---

## Step 3: Setup Environment and Install Dependencies

**⚡ Recommended: Using uv (Faster and More Efficient)**

[uv](https://docs.astral.sh/uv/) is a modern, blazingly fast Python package installer and resolver. It's significantly faster than pip and handles virtual environments seamlessly.

### Setup with uv

1. **Navigate to Your Project Directory:**

   ```bash
   cd demo-mcp-server
   ```

2. **Create Virtual Environment and Install Packages (One Command!):**

   ```bash
   uv venv mcp_env --python 3.14
   ```

3. **Activate Virtual Environment:**

   - **Windows (Command Prompt):** `mcp_env\Scripts\activate`
   - **macOS/Linux:** `source mcp_env/bin/activate`

4. **Install Required Packages:**
   ```cmd
   uv pip install fastmcp
   ```

---

### Alternative: Using Standard Python (Without uv)

If you prefer not to install uv, you can use the traditional Python approach:

<details>
<summary>Windows (using Command Prompt)</summary>

1. **Navigate to Your Project Directory:**

   ```cmd
   cd demo-mcp-server
   ```

2. **Create Virtual Environment:**

   ```cmd
   python3 -m venv mcp_env
   ```

3. **Activate Virtual Environment:**

   ```cmd
   mcp_env\Scripts\activate
   ```

4. **Verify Activation:**

   - You should see `(mcp_env)` at the beginning of your command prompt

5. **Install Required Packages:**
   ```cmd
   pip install fastmcp
   ```

</details>

<details>
<summary>macOS/Linux</summary>

1. **Navigate to Your Project Directory:**

   ```bash
   cd demo-mcp-server
   ```

2. **Create Virtual Environment:**

   ```bash
   python3 -m venv mcp_env
   ```

3. **Activate Virtual Environment:**

   ```bash
   source mcp_env/bin/activate
   ```

4. **Verify Activation:**

   - You should see `(mcp_env)` at the beginning of your terminal prompt

5. **Install Required Packages:**
   ```bash
   pip install fastmcp
   ```

</details>

---

## Step 4: Run the MCP Server

```
fastmcp dev server.py
```

## After Practice: Deactivating Virtual Environment

When you're done working, you can deactivate the virtual environment:

```bash
deactivate
```

### Remove the Virtual Environment

```bash
rm -rf mcp_env    # macOS/Linux
rd /s mcp_env     # Windows (Command Prompt)
```

---

**Happy coding! 🚀**
