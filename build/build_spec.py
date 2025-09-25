import PyInstaller.__main__
import os

# Get the current directory and project root
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = current_dir  # Assuming this script is in the project root

# Path to logo file
logo_path = os.path.join(project_root, 'utils', 'logo.png')

# Build arguments
build_args = [
    '--name=SalesApp',
    '--onefile',
    '--windowed',
    '--clean',
    '--noconfirm',
    f'--add-data={logo_path};utils',  # Note the semicolon for Windows
    '--hidden-import=customtkinter',
    '--hidden-import=tkinter',
    '--hidden-import=reportlab.lib',
    '--hidden-import=reportlab.pdfbase',
    '--hidden-import=reportlab.pdfgen',
    '--hidden-import=reportlab.platypus',
    '--hidden-import=reportlab.lib.pagesizes',
    '--hidden-import=reportlab.lib.styles',
    '--hidden-import=reportlab.lib.units',
    '--hidden-import=reportlab.lib.colors',
    '--hidden-import=reportlab.lib.enums',
    '--hidden-import=bcrypt',
    '--hidden-import=sqlite3',
    '--hidden-import=datetime',
    '--collect-all=customtkinter',
    '--collect-all=reportlab',
    os.path.join(project_root, 'main.py')
]

print("Building executable with PyInstaller...")
print(f"Project root: {project_root}")
print(f"Logo path: {logo_path}")
print(f"Logo exists: {os.path.exists(logo_path)}")

try:
    PyInstaller.__main__.run(build_args)
    print("Build completed successfully!")
    print("Executable should be in the 'dist' folder")
except Exception as e:
    print(f"Build failed: {e}")