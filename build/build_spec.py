import PyInstaller.__main__

PyInstaller.__main__.run([
    '--name=SalesApp',
    '--onefile',
    '--windowed',
    '--add-data=../utils/logo.png:utils',
    '--hidden-import=customtkinter',
    '--hidden-import=CTkMessagebox',
    '--hidden-import=reportlab',
    '--hidden-import=bcrypt',
    '--hidden-import=sqlite3',
    '../main.py'
])