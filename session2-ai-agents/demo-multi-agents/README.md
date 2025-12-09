# Demo Project Setup Guide

This guide will walk you through setting up the Google Agent Development Kit (ADK) on Windows, macOS, and Linux.

## Table of Contents
- [Step 1: Verify Python and Git Installation](#step-1-verify-python-and-git-installation)
- [Step 2: Create a Virtual Environment](#step-2-create-a-virtual-environment)
- [Step 3: Install Google ADK](#step-3-install-google-adk)
- [After Practice: Deactivating Virtual Environment](#after-practice-deactivating-virtual-environment)
- [Troubleshooting](#troubleshooting)

---

## Step 1: Verify Python and Git Installation

Before starting, ensure you have Python and Git installed on your system.

### To verify installation:

```bash
python3 --version
git --version
```

If not installed, please refer to the official pages:

- **Python:** https://www.python.org/downloads/
- **Git:** https://git-scm.com/downloads/win

---

## Step 2: Create a Virtual Environment

Virtual environments help isolate project dependencies and prevent conflicts.

### Windows (using Command Prompt)

1. **Navigate to Your Project Directory:**
   ```cmd
   git clone git@github.com:livhg/demo-ai-agents.git
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

### macOS/Linux

1. **Navigate to Your Project Directory:**
   ```bash
   git clone git@github.com:livhg/demo-ai-agents.git
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

---

## Step 3: Install Google ADK

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
rm -rf adk_env
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