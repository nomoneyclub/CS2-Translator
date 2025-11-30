# Contributing to CS2 Translator

Thank you for your interest in contributing to CS2 Translator! 🎉

## 🚀 How Can I Contribute?

### 🐛 Bug Reports
- Use the [Issue Templates](../../issues/new/choose)
- Describe the problem in detail
- Add screenshots/logs if possible
- Provide your system information (Windows version, Python version, etc.)

### 💡 Feature Requests
- Check if the feature has already been suggested
- Describe the use case and expected benefit
- Be specific in your description

### 🔧 Code Contributions

#### Setup Development Environment

1. **Fork & Clone**
   ```bash
   git clone https://github.com/YourUsername/cs2-translator.git
   cd cs2-translator
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Tesseract OCR**
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Install to: `C:\Program Files\Tesseract-OCR\`

4. **Test Setup**
   ```bash
   python cs2_translator.pyw
   ```

#### Development Guidelines

**Code Style:**
- Use Python 3.8+ features
- Follow PEP 8 style guide
- Use type hints where possible
- Comment complex logic

**Commit Messages:**
```
feat: add custom chat syntax support
fix: resolve duplicate translation issue
docs: update installation instructions
refactor: optimize OCR image preprocessing
```

**Branch Naming:**
```
feature/custom-syntax
bugfix/duplicate-translations
docs/readme-update
```

#### Pull Request Process

1. **Create Feature Branch**
   ```bash
   git checkout -b feature/amazing-feature
   ```

2. **Develop & Test**
   - Implement your changes
   - Test thoroughly with CS2
   - Ensure no regression occurs

3. **Commit & Push**
   ```bash
   git add .
   git commit -m "feat: add amazing feature"
   git push origin feature/amazing-feature
   ```

4. **Open Pull Request**
   - Use a descriptive title
   - Reference relevant issues
   - Add screenshots for UI changes

## 🧪 Testing

### Manual Testing Checklist
- [ ] Tesseract OCR works
- [ ] CS2 process detection
- [ ] Region selection (Auto & Manual)
- [ ] Chat message recognition
- [ ] Translation accuracy
- [ ] Duplicate prevention
- [ ] Hotkeys (F7, F9, F10, F11, F12)
- [ ] Config persistence
- [ ] UI responsiveness

### Test Cases
1. **Different CS2 Resolutions**: 1920x1080, 2560x1440, 3840x2160
2. **Various Languages**: English, German, Russian, Spanish, French
3. **Chat Scenarios**: Public chat, mixed languages, special characters
4. **Edge Cases**: No CS2 running, no region selected, Tesseract missing

## 📝 Documentation

### Code Documentation
- Docstrings for all public functions
- Inline comments for complex logic
- Type hints for better IDE support

### User Documentation
- Update README.md for new features
- Update CHANGELOG.md for all changes
- Add screenshots for UI changes

## 🎯 Priority Areas

### High Priority
- **Performance Optimization** - OCR speed, memory usage
- **Accuracy Improvement** - Better chat detection, translation quality
- **User Experience** - Easier setup, better error messages

### Medium Priority
- **Platform Support** - Linux/Mac compatibility
- **Additional APIs** - DeepL, Azure Translator
- **Advanced Features** - Chat history, export functions

### Low Priority
- **UI Themes** - Customizable appearance
- **Plugin System** - Extensibility
- **Advanced Hotkeys** - More customization

## 🤝 Community

### Communication
- **Issues**: For bugs and feature requests
- **Discussions**: For general questions and ideas

### Code of Conduct
- Be respectful and constructive
- Help other developers
- Focus on the problem, not the person
- Keep discussions professional

## 🏆 Recognition

All contributors will be mentioned in the README.md. Significant contributions will be highlighted.

---

**Thank you for making CS2 Translator better!** 🚀
