# VS Code Setup Guide for Google Colab Project

## Prerequisites
1. **Visual Studio Code**:
   - Download and install [Visual Studio Code](https://code.visualstudio.com/).

2. **Python**:
   - Install Python from [the official Python website](https://www.python.org/downloads/) (ensure that the checkbox "Add Python to PATH" is selected).

3. **Git**:
   - Install Git from [the official Git website](https://git-scm.com/downloads).

4. **GitHub Account**:
   - Ensure you have a GitHub account. Sign up [here](https://github.com/join) if you don’t.

## Step-by-Step Setup
### Step 1: Clone Your GitHub Repository
Open a terminal in VS Code (View > Terminal) and run:
```bash
git clone https://github.com/Hungthang1234/DO-AN-TOT-NGHIEP.git
cd DO-AN-TOT-NGHIEP
```

### Step 2: Create a Python Virtual Environment
To create a virtual environment, run:
```bash
python -m venv venv
```

### Step 3: Activate the Virtual Environment
**On Windows:**  
```bash
venv\Scripts\activate
```
**On macOS/Linux:**  
```bash
source venv/bin/activate
```

### Step 4: Install Dependencies
Ensure you have a `requirements.txt` file in your project. If so, run:
```bash
pip install -r requirements.txt
```

If there is no requirements file, manually install the packages you need:
```bash
pip install package_name
```

### Step 5: Install GitHub Copilot
1. Open the Extensions view by clicking on the Extensions icon in the Activity Bar on the side of the window or pressing `Ctrl+Shift+X`.
2. Search for "GitHub Copilot" and click on "Install".

### Step 6: Activate GitHub Copilot
1. After installation, you may need to sign in to your GitHub account.
2. Follow the prompts to activate GitHub Copilot.

## Troubleshooting
- **Problems with Virtual Environment Activation:**
  - Ensure that you have navigated to the correct directory where the virtual environment is located.
  - Ensure that execution policies for scripts are set properly if you’re on Windows.

- **Issues with Dependency Installation:**
  - Ensure that you are connected to the internet.
  - Check for typos in the package names in the `requirements.txt` or during manual installation.

- **GitHub Copilot Not Working:**
  - Ensure that you are signed in to GitHub in VS Code.
  - Restart VS Code if Copilot is not responding.
  - Check the GitHub status page to see if there are any outages.

## Conclusion
Following this guide will enable you to successfully move your Google Colab project to VS Code with full GitHub Copilot integration. Happy Coding!