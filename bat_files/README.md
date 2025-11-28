# Batch Files Directory

Windows batch scripts for launching and managing the House Price Prediction application.

## 🚀 Primary Launchers

### **MENU.bat** (Recommended - Main Launcher)
Interactive menu with 7 options:
```
[1] 🚀 Start Web Application    - Launch Flask server + open browser
[2] ⏹️  Stop Server              - Kill all Python processes  
[3] 🌐 Open Browser              - Open http://127.0.0.1:5000
[4] 📊 View Model Info           - Display model metadata & metrics
[5] 📁 Open Project Folder       - Open workspace in Explorer
[6] 📚 View Documentation        - Access guides & docs
[7] 🧪 Run Tests                 - Execute test suite
[0] ❌ Exit
```

### **START_WEB.bat**
Quick launcher - starts Flask server and opens browser automatically.
Use this for fast startup without menu.

## 🛠️ Utility Scripts

### **STOP_WEB.bat**
Stops all Python processes (kills Flask server).

### **VIEW_MODEL_INFO.bat**
Displays model metadata from `config/model_metadata.json` and `docs/MODEL_REFERENCE.txt`.
Shows active model, performance metrics, and training info.

## 📦 Archived Files

### **start.bat.old**
Old main launcher with complex multi-version menu system.
Preserved for reference. Use `MENU.bat` instead.

### **ARCHIVE_start.bat**
Documentation explaining why start.bat was archived.

## 🎯 Quick Start

**First Time Setup:**
1. Double-click `MENU.bat`
2. Choose option [1] to start application
3. Server starts automatically and browser opens

**Daily Use:**
- Just double-click `START_WEB.bat` for instant launch
- Or use `MENU.bat` for more options

## 📖 Documentation

For detailed guides, see `../docs/` folder:
- `QUICK_START.md` - Getting started guide
- `PROJECT_STRUCTURE.md` - Directory layout
- `ADVANCED_CHARTS_COMPLETE.md` - Charts documentation
- `EXTERNAL_API_COMPLETE.md` - API reference

## ⚙️ Technical Details

**Directory Navigation:**
All .bat files are designed to run from the `bat_files/` folder.
They use `%~dp0` to navigate to parent directory where needed.

**Python Environment:**
Scripts use `.venv\Scripts\python.exe` to run Python code.
Ensure virtual environment exists at workspace root.

**Port Configuration:**
Default server port: 5000
URL: http://127.0.0.1:5000

## 🔧 Troubleshooting

**Server won't start?**
- Check if port 5000 is already in use
- Verify `.venv` exists in parent directory
- Run `STOP_WEB.bat` to kill any hanging processes

**Browser doesn't open?**
- Manually navigate to http://127.0.0.1:5000
- Check if server started successfully (look for console output)

**Model info not displaying?**
- Ensure `config/model_metadata.json` exists
- Check `docs/MODEL_REFERENCE.txt` is present
- Try running from `MENU.bat` option [4]
