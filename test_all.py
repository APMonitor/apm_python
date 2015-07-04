import os

os.chdir('example_hs71')
os.system('python main.py')

os.chdir('../example_cstr')
os.system('python main.py')

os.chdir('../example_diabetic')
os.system('python control.py')

os.chdir('../example_nlc')
os.system('python nlc.py')

os.chdir('../example_tank_mhe')
os.system('python test.py')

os.chdir('../example_tank_nlc')
os.system('python main.py')

os.chdir('../example_distillation')
os.system('python test.py')

