#!/usr/bin/env python3
import os
import sys
import subprocess

def main():
    print('Building CS2 Translator EXE...')
    cmd = ['pyinstaller', '--onefile', '--windowed', '--noconsole', '--name=CS2_Translator_by_Sl0w', 'cs2_translator.pyw']
    subprocess.check_call(cmd)
    print('Done! File: dist/CS2_Translator_by_Sl0w.exe')

if __name__ == '__main__':
    main()
