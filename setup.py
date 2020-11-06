from cx_Freeze import setup,Executable

setup(
    name='generate_datamatrix',
    version='0.0.0.5',
    description='generate_datamatrix',
    executables = [Executable('main.py')]
)
