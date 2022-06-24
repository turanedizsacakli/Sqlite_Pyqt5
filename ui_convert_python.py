from PyQt5 import uic

with open("addProduct.py","w", encoding="utf-8") as fout:
    uic.compileUi("addProduct.ui", fout)