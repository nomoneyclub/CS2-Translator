# CS2 Translator - by Sl0w

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)](https://www.microsoft.com/windows)

## Real-Time Chat Translator for Counter-Strike 2

A powerful, real-time chat translator for Counter-Strike 2 that automatically detects and translates chat messages without affecting gameplay.

## Features

- **Live Translation** - Real-time translation of CS2 chat messages
- **20 Languages** - Support for the world's most spoken languages
- **Configurable Syntax** - Works with [ALL], [ALLE], [TODOS], etc.
- **Custom Syntax** - Add your own chat prefixes
- **Duplicate Protection** - Ultra-strong 5-layer duplicate detection
- **In-Game Hotkeys** - Works in fullscreen mode
- **Transparent Overlay** - Non-intrusive display over the game
- **Auto-Save Config** - Settings are automatically saved
- **No Console** - Runs completely in the background

## Supported Languages

| Language | Code | Language | Code |
|----------|------|----------|------|
| English | `en` | Japanese | `ja` |
| Chinese | `zh-CN` | German | `de` |
| Hindi | `hi` | Korean | `ko` |
| Spanish | `es` | Turkish | `tr` |
| French | `fr` | Vietnamese | `vi` |
| Arabic | `ar` | Italian | `it` |
| Bengali | `bn` | Polish | `pl` |
| Portuguese | `pt` | Ukrainian | `uk` |
| Russian | `ru` | Dutch | `nl` |
| Thai | `th` | Indonesian | `id` |

## Installation

### Option 1: Download EXE (Recommended)

1. **Download** the latest release from [Releases](../../releases)
2. **Install** Tesseract OCR from: https://github.com/UB-Mannheim/tesseract/wiki
3. **Run** `CS2_Translator_by_Sl0w.exe`

### Option 2: Run from Source

1. **Clone the repository**
   ```bash
   git clone https://github.com/nomoneyclub/CS2-Translator.git
   cd CS2-Translator
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to: `C:\Program Files\Tesseract-OCR\`

4. **Run the translator**
   ```bash
   python cs2_translator.pyw
   ```

## Usage

1. **Start CS2**
2. **Launch CS2 Translator**
3. **Select Chat Syntax** (e.g., [ALL] for English, [ALLE] for German)
4. **Select Target Language** (language you want translations in)
5. **Press F7** for auto-region detection (CS2 chat area)
6. **Press F10** to start translation

## Hotkeys

| Key | Function |
|-----|----------|
| **F7** / **Num2** | Auto-detect CS2 chat region |
| **F9** / **Num1** | Manual region selection |
| **F10** / **Num0** | Start/Stop translation |
| **F11** | Hide/Show overlay |
| **F12** | Quit application |

## Chat Syntax Options

The translator supports multiple chat prefixes based on game language:

| Prefix | Game Language |
|--------|---------------|
| `[ALL]` | English |
| `[ALLE]` | German |
| `[TODOS]` | Spanish |
| `[TOUS]` | French |
| `[TUTTI]` | Italian |
| `[ВСЕМ]` | Russian |
| `[TÜME]` | Turkish |
| `[全部]` | Chinese |

**Custom Syntax:** Click the `+` button to add your own prefix!

## Configuration

Settings are automatically saved to `cs2_translator_config.json`:
- Chat syntax preferences
- Target language
- Screen region
- Custom syntax entries

## Troubleshooting

### Tesseract not found
- Install Tesseract OCR from the official source
- Ensure it's installed in `C:\Program Files\Tesseract-OCR\`

### No translations appearing
- Check if CS2 is running
- Verify the correct chat syntax is selected
- Use F7 for automatic region detection

### Duplicate translations
- The built-in 5-layer duplicate protection prevents this
- If issues persist, restart the application

## Notes

- Only translates public chat messages (with selected prefix)
- Team chat is not translated
- System messages are filtered out
- Works with all CS2 resolutions

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

- **Tesseract OCR** for text recognition
- **Google Translate API** for translations
- **CS2 Community** for feedback and testing

## Support

For issues or questions:
- Open an [Issue](../../issues)
- Contact [@Sl0w](https://github.com/nomoneyclub)

---

**Created by Sl0w** | Version 1.0.0

⭐ **Like this project? Give it a star!** ⭐