import PyInstaller.__main__
import os

# 获取图标文件的绝对路径
icon_path = os.path.join(os.path.dirname(__file__), 'src', 'icon.ico')

PyInstaller.__main__.run([
    'src/calculator.py',
    '--onefile',
    '--windowed',
    '--name=数字计算器',
    f'--icon={icon_path}',
    '--add-data=src/icon.ico;src',
    '--hidden-import=ttkbootstrap',
    '--distpath=dist',
    '--workpath=build',
    '--clean',
    '--noupx'
]) 