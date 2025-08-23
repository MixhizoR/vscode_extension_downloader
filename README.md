# VS Code Extension Downloader

A Python script to download VS Code extensions (.vsix files) directly from the Visual Studio Marketplace.

## Features

- Download any VS Code extension by its unique identifier (e.g., `ms-vscode.cpptools`)
- Automatically detect and suggest the latest version
- Support for multiple platforms (Windows, macOS, Linux)
- Auto-detects your system platform
- Simple command-line interface

## Prerequisites

- Python 3.6 or higher
- `requests` library

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/vscode-extension-downloader.git
   cd vscode-extension-downloader
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or
   source .venv/bin/activate  # Linux/Mac
   ```

3. Install the required package:
   ```bash
   pip install requests
   ```

## Usage

Run the script:
```bash
python vscode_extension_downloader.py
```

### Example Workflow

1. Run the script
2. Enter the extension identifier when prompted (e.g., `ms-vscode.cpptools`)
3. The script will fetch available versions (or you can enter a specific version)
4. Choose whether to use the auto-detected platform or specify one
5. Confirm the download

The downloaded `.vsix` file will be saved in the same directory as the script.

## Platform Support

The script supports the following platforms:
- Windows (x64, x86)
- macOS (Intel, Apple Silicon)
- Linux (x64, x86)

## Common Extension Identifiers

| Extension | Identifier |
|-----------|------------|
| C/C++ | ms-vscode.cpptools |
| Python | ms-python.python |
| JavaScript | ms-vscode.vscode-typescript-next |
| Java | vscjava.vscode-java-pack |
| C# | ms-dotnettools.csharp |

## Troubleshooting

- If you get a 404 error, check that:
  - The extension identifier is correct
  - The version number exists
  - The platform is supported by the extension

## License

This project is open source and available under the [MIT License](LICENSE).

