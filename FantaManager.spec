# -*- mode: python -*-

block_cipher = None


a = Analysis(['FantaManager.py'],
             pathex=['/home/paolo/Documenti/FM'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None,
             excludes=None,
             cipher=block_cipher)
pyz = PYZ(a.pure,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='FantaManager',
          debug=False,
          strip=None,
          upx=True,
          console=True )
