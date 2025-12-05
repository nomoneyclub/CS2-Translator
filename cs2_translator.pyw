#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
CS2 Translator - by Sl0w
Real-time chat translation for Counter-Strike 2
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import messagebox, ttk, simpledialog
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import pytesseract
import mss
import psutil
from deep_translator import GoogleTranslator
from dataclasses import dataclass
from typing import List, Optional
import keyboard
import numpy as np
import json

# ============== CONFIGURATION ==============

TESSERACT_PATH = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Languages
SOURCE_LANGUAGE = "auto"
DEFAULT_TARGET_LANGUAGE = "en"  # Default: English

# Top 20 World Languages
TARGET_LANGUAGES = {
    "en": "English",
    "zh-CN": "中文 (Chinese)",
    "hi": "हिन्दी (Hindi)",
    "es": "Español (Spanish)",
    "fr": "Français (French)",
    "ar": "العربية (Arabic)",
    "bn": "বাংলা (Bengali)",
    "pt": "Português (Portuguese)",
    "ru": "Русский (Russian)",
    "ja": "日本語 (Japanese)",
    "de": "Deutsch (German)",
    "ko": "한국어 (Korean)",
    "tr": "Türkçe (Turkish)",
    "vi": "Tiếng Việt (Vietnamese)",
    "it": "Italiano (Italian)",
    "pl": "Polski (Polish)",
    "uk": "Українська (Ukrainian)",
    "nl": "Nederlands (Dutch)",
    "th": "ไทย (Thai)",
    "id": "Indonesia (Indonesian)"
}

# Chat Syntax (depends on game language)
DEFAULT_PREFIXES = ["[ALL]", "[ALLE]", "[TODOS]", "[TOUS]", "[TUTTI]", "[ВСЕМ]", "[TÜME]", "[全部]"]
CURRENT_PREFIX = "[ALL]"

# Scan Interval (seconds)
SCAN_INTERVAL = 1.0

# Overlay
OVERLAY_WIDTH = 550
OVERLAY_HEIGHT = 350
OVERLAY_OPACITY = 0.7

# CS2 Process
CS2_PROCESS_NAME = "cs2.exe"

# Config File
CONFIG_FILE = "cs2_translator_config.json"

# ============================================

@dataclass
class TranslatedText:
    original: str
    translated: str
    timestamp: float


class CS2Translator:
    def __init__(self):
        self.root = None
        self.capture_region = None
        self.is_running = False
        self.should_stop = False
        self.scan_thread = None
        self.last_texts = []
        self.translated_hashes = set()
        self.translations: List[TranslatedText] = []
        self.tesseract_ok = False
        self.scan_count = 0
        
        # Config
        self.config = self.load_config()
        self.chat_prefixes = self.config.get('chat_prefixes', DEFAULT_PREFIXES.copy())
        self.current_prefix = self.config.get('current_prefix', CURRENT_PREFIX)
        self.target_language = self.config.get('target_language', DEFAULT_TARGET_LANGUAGE)
        
        # Translator
        self.translator = GoogleTranslator(source=SOURCE_LANGUAGE, target=self.target_language)
        self.cache = {}
        
        # UI
        self.status_label = None
        self.text_widget = None
        self.region_label = None
        self.debug_label = None
        self.prefix_var = None
        self.lang_var = None
        
        # Check Tesseract
        self.check_tesseract()
    
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            if os.path.exists(CONFIG_FILE):
                with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except:
            pass
        return {}
    
    def save_config(self):
        """Save configuration to JSON file"""
        try:
            config = {
                'chat_prefixes': self.chat_prefixes,
                'current_prefix': self.current_prefix,
                'target_language': self.target_language,
                'capture_region': self.capture_region
            }
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2, ensure_ascii=False)
        except:
            pass
    
    def check_tesseract(self):
        """Check if Tesseract is installed"""
        try:
            if os.path.exists(TESSERACT_PATH):
                pytesseract.pytesseract.tesseract_cmd = TESSERACT_PATH
                pytesseract.get_tesseract_version()
                self.tesseract_ok = True
            else:
                self.tesseract_ok = False
        except Exception as e:
            self.tesseract_ok = False
    
    def is_cs2_running(self) -> bool:
        """Check if CS2 is running"""
        try:
            for proc in psutil.process_iter(['name']):
                if proc.info['name'] and CS2_PROCESS_NAME in proc.info['name'].lower():
                    return True
            return False
        except:
            return False
    
    def capture_screen(self) -> Optional[Image.Image]:
        if not self.capture_region:
            return None
        try:
            with mss.mss() as sct:
                screenshot = sct.grab(self.capture_region)
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                return img
        except Exception as e:
            return None
    
    def preprocess_for_ocr(self, img: Image.Image) -> List[Image.Image]:
        """Optimized for CS2 Chat"""
        versions = []
        
        try:
            img_large = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
            arr = np.array(img_large)
            
            # Extract bright pixels
            gray = np.mean(arr, axis=2)
            bright_mask = gray > 150
            v1 = np.zeros_like(gray, dtype=np.uint8)
            v1[bright_mask] = 255
            versions.append(Image.fromarray(v1))
            
            # Colored pixels
            max_rgb = np.max(arr, axis=2)
            min_rgb = np.min(arr, axis=2)
            saturation = max_rgb - min_rgb
            color_mask = (saturation > 50) | (gray > 180)
            v2 = np.zeros_like(gray, dtype=np.uint8)
            v2[color_mask] = 255
            versions.append(Image.fromarray(v2))
            
            # Classic inverted
            v3 = Image.fromarray(gray.astype(np.uint8))
            v3 = ImageOps.invert(v3)
            v3 = ImageEnhance.Contrast(v3).enhance(2.5)
            versions.append(v3)
            
        except Exception as e:
            img_large = img.resize((img.width * 2, img.height * 2), Image.LANCZOS)
            v1 = img_large.convert('L')
            v1 = ImageOps.invert(v1)
            v1 = ImageEnhance.Contrast(v1).enhance(2.5)
            versions.append(v1)
        
        return versions
    
    def extract_text(self, img: Image.Image) -> str:
        """Extract text with OCR"""
        if not self.tesseract_ok:
            return ""
        
        try:
            versions = self.preprocess_for_ocr(img)
            all_texts = []
            
            lang_combo = 'eng+rus+tur+pol+ukr+hun+ces+ron+bul+srp+hrv+ara+fra+spa+ita+por'
            
            for i, processed_img in enumerate(versions[:2]):
                try:
                    config = f'--psm 6 --oem 3 -l {lang_combo}'
                    text = pytesseract.image_to_string(processed_img, config=config)
                    text = self._clean_text(text)
                    if text and len(text) > 2:
                        all_texts.append(text)
                except Exception as e:
                    try:
                        text = pytesseract.image_to_string(processed_img, config='--psm 6 -l eng')
                        text = self._clean_text(text)
                        if text and len(text) > 2:
                            all_texts.append(text)
                    except:
                        pass
            
            if all_texts:
                best = max(all_texts, key=lambda t: len(t))
                return best
            
            return ""
            
        except Exception as e:
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Filter only chat messages with current prefix"""
        if not text:
            return ""
        
        text = text.strip()
        valid_lines = []
        
        for line in text.split('\n'):
            line = line.strip()
            
            if len(line) < 8 or ':' not in line:
                continue
            
            parts = line.split(':', 1)
            if len(parts) != 2:
                continue
            
            username_part = parts[0].strip()
            message_part = parts[1].strip()
            
            if not message_part or len(message_part) < 3:
                continue
            
            # Check current prefix
            if not username_part.startswith(self.current_prefix):
                continue
            
            # Extract username
            clean_username = username_part.replace(self.current_prefix, '').strip()
            if not clean_username or len(clean_username) < 2:
                continue
            
            # Filter system messages
            system_words = ['hat einen', 'wurde', 'killed', 'eliminated', 'died', 'exploded', 
                           'Blendgranate', 'Granate', 'Bombe', 'defused', 'planted', 'grenade',
                           'flashbang', 'smoke', 'molotov', 'incendiary']
            
            if any(word in message_part.lower() for word in system_words):
                continue
            
            # Quality check
            alnum_count = sum(1 for c in message_part if c.isalnum())
            if alnum_count < len(message_part) * 0.5:
                continue
            
            valid_lines.append(line)
        
        return '\n'.join(valid_lines)
    
    def translate_text(self, text: str) -> str:
        """Translate only message, keep username"""
        if not text or len(text) < 2:
            return ""
        
        if text in self.cache:
            return self.cache[text]
        
        try:
            result_lines = []
            for line in text.split('\n'):
                line = line.strip()
                if not line:
                    continue
                
                if ':' in line:
                    parts = line.split(':', 1)
                    username_part = parts[0]
                    message_part = parts[1].strip() if len(parts) > 1 else ""
                    
                    if message_part and len(message_part) > 1:
                        try:
                            # Recreate translator if needed
                            translated_msg = self.translator.translate(message_part)
                            if translated_msg:
                                result_lines.append(f"{username_part}: {translated_msg}")
                            else:
                                result_lines.append(line)
                        except Exception as te:
                            self._debug(f"Translate error: {te}")
                            # Try to recreate translator
                            try:
                                self.translator = GoogleTranslator(source=SOURCE_LANGUAGE, target=self.target_language)
                                translated_msg = self.translator.translate(message_part)
                                result_lines.append(f"{username_part}: {translated_msg}")
                            except:
                                result_lines.append(line)
                    else:
                        result_lines.append(line)
                else:
                    try:
                        translated = self.translator.translate(line)
                        result_lines.append(translated if translated else line)
                    except:
                        result_lines.append(line)
            
            result = '\n'.join(result_lines)
            if result:
                self.cache[text] = result
            return result
        except Exception as e:
            self._debug(f"Translation failed: {e}")
            return text
    
    def auto_region_cs2_chat(self):
        """Set automatic CS2 chat region for primary monitor"""
        # Use mss to get accurate monitor info
        try:
            with mss.mss() as sct:
                # Monitor 1 is the primary monitor (index 1, index 0 is all monitors combined)
                if len(sct.monitors) > 1:
                    monitor = sct.monitors[1]  # Primary monitor
                    screen_width = monitor['width']
                    screen_height = monitor['height']
                    left_offset = monitor['left']
                else:
                    screen_width = self.root.winfo_screenwidth()
                    screen_height = self.root.winfo_screenheight()
                    left_offset = 0
        except:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            left_offset = 0
        
        self.capture_region = {
            "left": left_offset,
            "top": int(screen_height * 0.75),
            "width": int(screen_width * 0.30),
            "height": int(screen_height * 0.15)
        }
        self._update_region_label()
        self.save_config()
    
    def select_region(self):
        """Manual region selection"""
        selector = tk.Toplevel()
        selector.attributes('-fullscreen', True)
        selector.attributes('-alpha', 0.3)
        selector.configure(bg='gray')
        selector.attributes('-topmost', True)
        
        canvas = tk.Canvas(selector, highlightthickness=0)
        canvas.pack(fill=tk.BOTH, expand=True)
        
        result = {"region": None}
        
        def on_click(event):
            result["start_x"] = event.x
            result["start_y"] = event.y
        
        def on_drag(event):
            canvas.delete("selection")
            canvas.create_rectangle(
                result["start_x"], result["start_y"], event.x, event.y,
                outline="red", width=3, tags="selection"
            )
        
        def on_release(event):
            x1, y1 = result["start_x"], result["start_y"]
            x2, y2 = event.x, event.y
            
            left = min(x1, x2)
            top = min(y1, y2)
            width = abs(x2 - x1)
            height = abs(y2 - y1)
            
            if width > 10 and height > 10:
                result["region"] = {
                    "left": left,
                    "top": top,
                    "width": width,
                    "height": height
                }
            
            selector.destroy()
        
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)
        
        selector.wait_window()
        
        if result["region"]:
            self.capture_region = result["region"]
            self._update_region_label()
            self.save_config()
    
    def _update_region_label(self):
        if self.region_label and self.capture_region:
            r = self.capture_region
            self.region_label.config(
                text=f"[REGION: {r['width']}x{r['height']}]",
                fg='#00ff00'
            )
    
    def _update_status(self, text: str, color: str = '#888888'):
        if self.status_label:
            self.status_label.config(text=text, fg=color)
    
    def _debug(self, msg: str):
        if self.debug_label:
            try:
                self.debug_label.config(text=msg[:50])
            except:
                pass
    
    def _text_similarity(self, text1: str, text2: str) -> float:
        """Calculate text similarity"""
        if not text1 or not text2:
            return 0.0
        
        def normalize(text):
            import re
            text = re.sub(r'[^\w\s]', '', text.lower())
            text = ' '.join(text.split())
            return text
        
        norm1 = normalize(text1)
        norm2 = normalize(text2)
        
        if norm1 == norm2:
            return 1.0
        
        words1 = set(norm1.split())
        words2 = set(norm2.split())
        
        if not words1 and not words2:
            return 1.0
        if not words1 or not words2:
            return 0.0
        
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        
        return len(intersection) / len(union) if union else 0.0
    
    def add_translation(self, original: str, translated: str):
        t = TranslatedText(original, translated, time.time())
        self.translations.append(t)
        if len(self.translations) > 25:
            self.translations = self.translations[-25:]
        self._update_display()
    
    def _update_display(self):
        if not self.text_widget or not self.root:
            return
        
        def do_update():
            try:
                self.text_widget.config(state='normal')
                self.text_widget.delete('1.0', 'end')
                
                for t in self.translations[-20:]:
                    self.text_widget.insert('end', f"{t.translated}\n", 'translated')
                
                self.text_widget.config(state='disabled')
                self.text_widget.see('end')
                self.root.update_idletasks()
            except Exception as e:
                pass
        
        self.root.after(0, do_update)
    
    def toggle_translation(self):
        if self.is_running:
            self.stop_translation()
        else:
            self.start_translation()
    
    def start_translation(self):
        if not self.tesseract_ok:
            messagebox.showerror("Error", "Tesseract OCR not found!\nPlease install Tesseract-OCR.")
            return
        
        if not self.capture_region:
            messagebox.showwarning("Warning", "No region selected!\nPress AUTO or REGION.")
            return
        
        if self.is_running:
            return
        
        self.is_running = True
        self.should_stop = False
        self.scan_thread = threading.Thread(target=self._scan_loop, daemon=True)
        self.scan_thread.start()
    
    def stop_translation(self):
        self.is_running = False
        self.should_stop = True
    
    def _scan_loop(self):
        while not self.should_stop:
            try:
                cs2_running = self.is_cs2_running()
                
                if self.root:
                    if cs2_running:
                        self.root.after(0, lambda: self._update_status("[LIVE]", '#00ff00'))
                    else:
                        self.root.after(0, lambda: self._update_status("[WAITING FOR CS2]", '#ffaa00'))
                
                if cs2_running and self.capture_region:
                    img = self.capture_screen()
                    
                    if img:
                        text = self.extract_text(img)
                        
                        if text and len(text) > 3:
                            import re
                            import hashlib
                            
                            clean_text = re.sub(r'[^\w\s]', '', text.lower())
                            clean_text = ' '.join(clean_text.split())
                            
                            text_hash = hashlib.md5(clean_text.encode()).hexdigest()
                            
                            message_only = ""
                            if ':' in text:
                                parts = text.split(':', 1)
                                if len(parts) > 1:
                                    message_only = re.sub(r'[^\w\s]', '', parts[1].lower().strip())
                                    message_only = ' '.join(message_only.split())
                            
                            # Ultra-Strong Duplicate Check
                            is_duplicate = (
                                text_hash in self.translated_hashes or
                                clean_text in self.last_texts or
                                (message_only and len(message_only) > 3 and 
                                 any(message_only in existing for existing in self.last_texts)) or
                                any(self._text_similarity(clean_text, existing) > 0.75 
                                    for existing in self.last_texts)
                            )
                            
                            if not is_duplicate:
                                self.last_texts.append(clean_text)
                                self.translated_hashes.add(text_hash)
                                
                                if len(self.last_texts) > 25:
                                    self.last_texts = self.last_texts[-25:]
                                if len(self.translated_hashes) > 50:
                                    self.translated_hashes = set(list(self.translated_hashes)[-35:])
                                
                                self._debug(f"NEW: {text[:30]}...")
                                
                                translated = self.translate_text(text)
                                if translated and translated != text:
                                    if self.root:
                                        self.root.after(0, lambda t=text, tr=translated:
                                            self.add_translation(t, tr))
                            else:
                                self._debug(f"DUPLICATE: {text[:25]}...")
                        else:
                            self._debug(f"No {self.current_prefix} text")
                
                time.sleep(SCAN_INTERVAL)
                
            except Exception as e:
                self._debug(f"Error: {e}")
                time.sleep(1)
    
    def toggle_visibility(self):
        if self.root:
            if self.root.state() == 'withdrawn':
                self.root.deiconify()
            else:
                self.root.withdraw()
    
    def on_prefix_change(self, event=None):
        """Callback for syntax change"""
        if self.prefix_var:
            new_prefix = self.prefix_var.get()
            if new_prefix and new_prefix != self.current_prefix:
                self.current_prefix = new_prefix
                self.last_texts.clear()
                self.translated_hashes.clear()
                self.cache.clear()
                self._debug(f"Syntax: {new_prefix}")
                self.save_config()
    
    def on_language_change(self, event=None):
        """Callback for target language change"""
        if self.lang_var:
            selected = self.lang_var.get()
            lang_code = selected.split(" - ")[0] if " - " in selected else selected
            
            if lang_code and lang_code != self.target_language:
                self.target_language = lang_code
                self.translator = GoogleTranslator(source=SOURCE_LANGUAGE, target=lang_code)
                self.cache.clear()
                self._debug(f"Language: {TARGET_LANGUAGES.get(lang_code, lang_code)}")
                self.save_config()
    
    def add_custom_prefix(self):
        """Add custom prefix"""
        custom = simpledialog.askstring(
            "Custom Syntax", 
            "Enter custom chat syntax:\n(e.g. [TEAM], [GLOBAL], etc.)",
            initialvalue="[CUSTOM]"
        )
        
        if custom and custom.strip():
            custom = custom.strip()
            if custom not in self.chat_prefixes:
                self.chat_prefixes.append(custom)
                self.save_config()
                if hasattr(self, 'prefix_combo'):
                    self.prefix_combo['values'] = self.chat_prefixes
                    self.prefix_var.set(custom)
                    self.on_prefix_change()
    
    def quit_app(self):
        self.should_stop = True
        self.save_config()
        if self.root:
            self.root.quit()
        sys.exit(0)
    
    def setup_hotkeys(self):
        keyboard.on_press_key('F7', lambda e: self.root.after(0, self.auto_region_cs2_chat) if self.root else None, suppress=False)
        keyboard.on_press_key('F9', lambda e: self.root.after(0, self.select_region) if self.root else None, suppress=False)
        keyboard.on_press_key('F10', lambda e: self.root.after(0, self.toggle_translation) if self.root else None, suppress=False)
        keyboard.on_press_key('F11', lambda e: self.toggle_visibility(), suppress=False)
        keyboard.on_press_key('F12', lambda e: self.quit_app(), suppress=False)
        
        keyboard.on_press_key('num 0', lambda e: self.root.after(0, self.toggle_translation) if self.root else None, suppress=False)
        keyboard.on_press_key('num 1', lambda e: self.root.after(0, self.select_region) if self.root else None, suppress=False)
        keyboard.on_press_key('num 2', lambda e: self.root.after(0, self.auto_region_cs2_chat) if self.root else None, suppress=False)
    
    def create_ui(self):
        self.root = tk.Tk()
        self.root.title("CS2 Translator - by Sl0w")
        self.root.geometry(f"{OVERLAY_WIDTH}x{OVERLAY_HEIGHT}+50+50")
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', OVERLAY_OPACITY)
        self.root.configure(bg='#0a0a0a')
        
        # Header
        header = tk.Frame(self.root, bg='#0d0d0d', pady=3)
        header.pack(fill=tk.X)
        
        tk.Label(header, text="CS2 TRANSLATOR - by Sl0w",
                font=('Consolas', 10, 'bold'), fg='#00ff88', bg='#0d0d0d').pack(side=tk.LEFT, padx=8)
        
        self.status_label = tk.Label(header, text="[IDLE]",
                                     font=('Consolas', 9), fg='#666', bg='#0d0d0d')
        self.status_label.pack(side=tk.RIGHT, padx=8)
        
        # Syntax Selection
        syntax_frame = tk.Frame(self.root, bg='#0a0a0a')
        syntax_frame.pack(pady=2)
        
        tk.Label(syntax_frame, text="SYNTAX:", font=('Consolas', 8), 
                fg='#666', bg='#0a0a0a').pack(side=tk.LEFT, padx=2)
        
        self.prefix_var = tk.StringVar(value=self.current_prefix)
        self.prefix_combo = ttk.Combobox(syntax_frame, textvariable=self.prefix_var,
                                        values=self.chat_prefixes, width=10, font=('Consolas', 8),
                                        state='readonly')
        self.prefix_combo.pack(side=tk.LEFT, padx=2)
        self.prefix_combo.bind('<<ComboboxSelected>>', self.on_prefix_change)
        
        tk.Button(syntax_frame, text="+", command=self.add_custom_prefix,
                 font=('Consolas', 8), bg='#2a2a2a', fg='#00ff00',
                 relief='flat', padx=4, pady=1).pack(side=tk.LEFT, padx=2)
        
        # Language Selection
        lang_frame = tk.Frame(self.root, bg='#0a0a0a')
        lang_frame.pack(pady=2)
        
        tk.Label(lang_frame, text="TRANSLATE TO:", font=('Consolas', 8), 
                fg='#666', bg='#0a0a0a').pack(side=tk.LEFT, padx=2)
        
        lang_options = [f"{code} - {name}" for code, name in TARGET_LANGUAGES.items()]
        current_lang_display = f"{self.target_language} - {TARGET_LANGUAGES.get(self.target_language, self.target_language)}"
        
        self.lang_var = tk.StringVar(value=current_lang_display)
        self.lang_combo = ttk.Combobox(lang_frame, textvariable=self.lang_var,
                                       values=lang_options, width=18, font=('Consolas', 8),
                                       state='readonly')
        self.lang_combo.pack(side=tk.LEFT, padx=2)
        self.lang_combo.bind('<<ComboboxSelected>>', self.on_language_change)
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg='#0a0a0a')
        btn_frame.pack(pady=2)
        
        tk.Button(btn_frame, text="AUTO", command=self.auto_region_cs2_chat,
                 font=('Consolas', 8), bg='#1a3a1a', fg='#00ff00', 
                 relief='flat', padx=8, pady=1).pack(side=tk.LEFT, padx=2)
        
        tk.Button(btn_frame, text="REGION", command=self.select_region,
                 font=('Consolas', 8), bg='#2a2a2a', fg='#aaa',
                 relief='flat', padx=8, pady=1).pack(side=tk.LEFT, padx=2)
        
        tk.Button(btn_frame, text="START", command=self.toggle_translation,
                 font=('Consolas', 8), bg='#1a1a3a', fg='#00aaff',
                 relief='flat', padx=8, pady=1).pack(side=tk.LEFT, padx=2)
        
        # Region
        self.region_label = tk.Label(self.root, text="[NO REGION - Press AUTO]",
                                     font=('Consolas', 8), fg='#ff4444', bg='#0a0a0a')
        self.region_label.pack(pady=1)
        
        # Text Area
        text_frame = tk.Frame(self.root, bg='#000000')
        text_frame.pack(fill=tk.BOTH, expand=True, padx=4, pady=2)
        
        self.text_widget = tk.Text(text_frame, font=('Consolas', 9),
                                   fg='#00ff88', bg='#000000',
                                   wrap=tk.WORD, state=tk.DISABLED,
                                   borderwidth=1, relief='solid')
        
        scroll = ttk.Scrollbar(text_frame, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=scroll.set)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        self.text_widget.tag_configure('translated', foreground='#00ff88', font=('Consolas', 9))
        
        # Debug
        self.debug_label = tk.Label(self.root, text="[READY - F7=Auto, F9=Region, F10=Start]",
                                    font=('Consolas', 7), fg='#444', bg='#0a0a0a')
        self.debug_label.pack(pady=1)
        
        if not self.tesseract_ok:
            tk.Label(self.root, text="[ERROR: Install Tesseract-OCR]",
                    font=('Consolas', 8), fg='#ff0000', bg='#0a0a0a').pack(pady=2)
        
        # Load config
        if self.config.get('capture_region'):
            self.capture_region = self.config['capture_region']
            self._update_region_label()
    
    def run(self):
        self.setup_hotkeys()
        self.create_ui()
        self.root.mainloop()


if __name__ == "__main__":
    app = CS2Translator()
    app.run()
