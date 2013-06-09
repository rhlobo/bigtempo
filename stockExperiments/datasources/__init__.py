import os


for module in os.listdir(os.path.dirname(__file__)):
    basename, extension = os.path.splitext(module)
    if module == '__init__.py' or extension.lower() not in ['.py']:
        continue
    __import__(basename, locals(), globals())
del module
