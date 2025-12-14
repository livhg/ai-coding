# Demo Project Setup Guide

This guide will walk you through setting up the Google Agent Development Kit (ADK) on Windows, macOS, and Linux.

## Step 1: Verify Installation

Before starting, ensure you have the required tools installed on your system.

### To verify installation:

```bash
python3 --version
uv --version     # Optional but recommended
```

If not installed, please refer to the official pages:

- **Python:** https://www.python.org/downloads/
- **uv (⚡ Recommended - Fast Python package manager):**

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
git clone git@github.com:livhg/demo-ai-agents.git
```

Or download from https://github.com/livhg/demo-ai-agents.git

---

## Step 3: Create a Virtual Environment

Virtual environments help isolate project dependencies and prevent conflicts.

### Setup with uv

1. **Navigate to Your Project Directory:**

   ```bash
   cd demo-ai-agents
   ```

2. **Create Virtual Environment and Install Packages (One Command!):**

   ```bash
   uv venv adk_env --python 3.14
   ```

3. **Activate Virtual Environment:**

   - **Windows (Command Prompt):** `adk_env\Scripts\activate`
   - **macOS/Linux:** `source adk_env/bin/activate`

### Alternative: Using Standard Python (Without uv)

If you prefer not to install uv, you can use the traditional Python approach:

<details>
<summary>Windows (using Command Prompt)</summary>

1. **Navigate to Your Project Directory:**

   ```cmd
   cd demo-ai-agents
   ```

2. **Create Virtual Environment:**

   ```cmd
   python -m venv adk_env
   ```

3. **Activate Virtual Environment:**

   ```cmd
   adk_env\Scripts\activate.bat
   ```

4. **Verify Activation:**
   - You should see `(adk_env)` at the beginning of your command prompt

</details>

<details>
<summary>macOS/Linux</summary>

1. **Navigate to Your Project Directory:**

   ```bash
   cd demo-ai-agents
   ```

2. **Create Virtual Environment:**

   ```bash
   python3 -m venv adk_env
   ```

3. **Activate Virtual Environment:**

   ```bash
   source adk_env/bin/activate
   ```

4. **Verify Activation:**
   - You should see `(adk_env)` at the beginning of your terminal prompt

</details>

---

## Step 4: Install Google ADK

With your virtual environment activated:

**Install Google ADK:**

```
pip install google-adk
```

---

## After Practice: Deactivating Virtual Environment

When you're done working, you can deactivate the virtual environment:

```
deactivate
```

Remove the virtual env

```
rm -rf adk_env    # macOS/Linux
rd /s adk_env     # Windows (Command Prompt)
```

---

## Troubleshooting

### Windows Issues

**Problem:** `python` command not recognized

- **Solution:** Close and reopen Command Prompt after installation. If still not working, try restarting your computer or reinstalling using `winget install 9NQ7512CXL7T`.

**Problem:** Cannot activate virtual environment

- **Solution:** Make sure you're using Command Prompt (cmd), not PowerShell. Open Command Prompt by searching for "cmd" in the Start menu.

### macOS/Linux Issues

**Problem:** `python` vs `python3` command

- **Solution:** On macOS/Linux, use `python3` instead of `python` for Python 3.x installations.

**Problem:** Permission denied errors

- **Solution:** Use `pip install --user google-adk` or ensure you have proper permissions.

**Problem:** venv module not found

- **Solution:** Install it explicitly:
  ```bash
  # Ubuntu/Debian
  sudo apt install python3-venv
  ```

### General Issues

**Problem:** Package installation fails

- **Solution:**
  1. Check your internet connection
  2. Try upgrading pip: `pip install --upgrade pip`
  3. Check for firewall or proxy issues

**Problem:** Import errors after installation

- **Solution:** Make sure your virtual environment is activated before installing and running code.

---

## Next Steps

After completing this setup:

1. Start developing with Google ADK
2. Check the [official documentation](https://cloud.google.com/adk) for API references and tutorials
3. Remember to activate your virtual environment each time you work on your project

---

**Happy coding! 🚀**
