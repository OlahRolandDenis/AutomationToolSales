import PyInstaller.__main__
import os
from utils.resource_path import resource_path

# Get the project root (parent of build directory)
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)  # Go up one level from build folder

# Path to logo file
logo_path = resource_path("utils/logo.png")

# Path to main.py
main_path = os.path.join(project_root, "main.py")

# Build arguments with ALL dependencies
build_args = [
    '--name=SalesApp',
    '--onefile',
    '--console',
    '--clean',
    '--noconfirm',
    f'--add-data={logo_path};utils',  # Colon for Mac/Linux, semicolon for Windows
    '--add-data="database/connection.db;database"',

    
    # GUI Libraries
    '--hidden-import=customtkinter',

    '--hidden-import=tkinter',
    '--hidden-import=tkinter.ttk',
    '--hidden-import=tkinter.messagebox',
    '--hidden-import=tkinter.filedialog',
    
    # Database
    '--hidden-import=sqlite3',
    
    # Security
    '--hidden-import=bcrypt',
    '--hidden-import=bcrypt._bcrypt',
    
    # Date/Time
    '--hidden-import=datetime',
    
    # PDF Generation - ReportLab
    '--hidden-import=reportlab',
    '--hidden-import=reportlab.lib',
    '--hidden-import=reportlab.lib.pagesizes',
    '--hidden-import=reportlab.lib.styles',
    '--hidden-import=reportlab.lib.units',
    '--hidden-import=reportlab.lib.colors',
    '--hidden-import=reportlab.lib.enums',
    '--hidden-import=reportlab.pdfbase',
    '--hidden-import=reportlab.pdfgen',
    '--hidden-import=reportlab.pdfgen.canvas',
    '--hidden-import=reportlab.platypus',
    '--hidden-import=reportlab.platypus.doctemplate',
    '--hidden-import=reportlab.platypus.paragraph',
    '--hidden-import=reportlab.platypus.tables',
    '--hidden-import=reportlab.platypus.frames',
    '--hidden-import=reportlab.platypus.pagebreak',
    '--hidden-import=reportlab.rl_config',
    
    # Standard Library modules that might be missed
    '--hidden-import=os',
    '--hidden-import=sys',
    '--hidden-import=random',
    '--hidden-import=tempfile',
    '--hidden-import=subprocess',
    '--hidden-import=platform',
    
    # Your custom modules (to ensure they're included)
    '--hidden-import=database',
    '--hidden-import=database.connection',
    '--hidden-import=services',
    '--hidden-import=services.auth_service',
    '--hidden-import=services.sales_service', 
    '--hidden-import=services.offer_service',
    '--hidden-import=models',
    '--hidden-import=models.user',
    '--hidden-import=models.sale',
    '--hidden-import=models.offer',
    '--hidden-import=ui',
    '--hidden-import=ui.login_window',
    '--hidden-import=ui.dashboard_window',
    '--hidden-import=ui.offer_window',
    


    
    # Collect all files from these packages
    '--collect-all=customtkinter',
    '--collect-all=tkinter',
    '--collect-all=reportlab',
    '--collect-all=bcrypt',
    '--collect-submodules=database',
    '--collect-submodules=services',
    '--collect-submodules=ui',
    
    # Add the main script
    main_path
]

print("Building executable with PyInstaller...")
print(f"Project root: {project_root}")
print(f"Logo path: {logo_path}")
print(f"Logo exists: {os.path.exists(logo_path)}")
print(f"Main.py path: {main_path}")
print(f"Main.py exists: {os.path.exists(main_path)}")

try:
    # Change to project root directory
    os.chdir(project_root)
    print(f"Changed directory to: {os.getcwd()}")
    
    PyInstaller.__main__.run(build_args)
    print("Build completed successfully!")
    print("Executable should be in the 'dist' folder")
except Exception as e:
    print(f"Build failed: {e}")
    import traceback
    traceback.print_exc()