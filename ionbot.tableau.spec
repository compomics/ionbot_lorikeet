# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['ionbot.tableau.py'],
             pathex=['C:\\Work\\ionbot_lorikeet_windows'],
             binaries=[],
   datas=[('templates', 'templates'),('static', 'static'),('unimodptms.txt', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=['matplotlib', 'scipy', 'pandas'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          [],
          name='ionbot.tableau',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True )
