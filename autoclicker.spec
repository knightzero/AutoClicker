# -*- mode: python -*-
a = Analysis(['autoclicker.py'],
             pathex=['C:\\Users\\knightZeRo\\Dropbox\\GitHub\\AutoClicker'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='autoclicker.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )
