a = Analysis(
    ['wechat.py'],
    pathex=[],
    binaries=[],
    datas=[],  # 移除配置文件
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='wechat',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
)