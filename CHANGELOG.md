# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-30

### Added
- **Live Chat Translation** for Counter-Strike 2
- **20 Target Languages** - World's most spoken languages
- **Configurable Chat Syntax** ([ALL], [ALLE], [TODOS], etc.)
- **Custom Syntax Support** - Users can add their own chat prefixes
- **Ultra-Strong Duplicate Protection** - 5-layer check prevents duplicate translations
- **In-Game Hotkeys** - Work in fullscreen mode
- **Transparent Overlay** - Non-intrusive display over the game
- **Auto-Region Detection** - Automatic CS2 chat area detection
- **Manual Region Selection** - Precise customization possible
- **Multi-Language OCR** - Support for 15+ languages
- **Console-free EXE** - Runs completely in the background
- **Auto-Installer** - Automatic dependency installation
- **Config Persistence** - Settings are automatically saved

### Features
- **OCR Engine**: Tesseract with optimized image processing for CS2 chat
- **Translation**: Google Translate API with caching
- **UI**: Console-style transparent overlay
- **Hotkeys**: F7 (Auto-Region), F9 (Manual), F10 (Start/Stop), F11 (Hide), F12 (Quit)
- **Numpad Alternative**: 0-2 for better in-game compatibility
- **Process Detection**: Only activates when CS2 is running
- **Smart Filtering**: Filters system messages and keeps only real chat messages

### Technical
- **Python 3.8+** compatibility
- **Windows** platform-specific
- **Thread-safe** screen capture with MSS
- **Memory-efficient** caching and cleanup
- **Error-resilient** with comprehensive exception handling

## [Unreleased]

### Planned
- Linux/Mac support
- Additional translation APIs (DeepL, Azure)
- Chat history export
- Customizable UI themes
- Plugin system for extended features
