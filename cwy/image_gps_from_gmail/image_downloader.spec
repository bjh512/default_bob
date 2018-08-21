# -*- mode: python -*-

block_cipher = None


a = Analysis(['image_downloader.py'],
             pathex=['C:\\Develop\\default_bob\\cwy\\image_gps_from_gmail\\source'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='image_downloader',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
