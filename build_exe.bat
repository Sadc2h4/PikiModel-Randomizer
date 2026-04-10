@echo off
setlocal
cd /d "%~dp0"

echo =====================================================
echo  PikiModel Randomizer - EXE ビルドスクリプト
echo =====================================================
echo.

:: ---- 仮想環境が既にあれば削除して再作成 ----
if exist minimam (
    echo 既存の仮想環境を削除中...
    rmdir /s /q minimam
)

echo [1] 仮想環境 minimam を作成中...
py -3 -m venv minimam
if errorlevel 1 (
    echo エラー: 仮想環境の作成に失敗しました
    pause & exit /b 1
)

echo [2] 仮想環境を有効化してパッケージをインストール中...
call minimam\Scripts\activate.bat

if errorlevel 1 (
    echo エラー: pip install に失敗しました
    pause & exit /b 1
)

echo.
echo [3] PyInstaller でビルド中...
echo.

pyinstaller PikiModel_Randomizer.spec --noconfirm --clean

if errorlevel 1 (
    echo エラー: PyInstaller ビルドに失敗しました
    call deactivate
    pause & exit /b 1
)

call deactivate

echo.
echo =====================================================
echo  ビルド完了！
echo  出力先: dist\PikiModel_Randomizer\
echo    PikiModel_Randomizer.exe  <- 実行ファイル
echo    _internal\                <- 必要ファイル一式
echo       SPERO_icon.ico
echo       numpy / Python ランタイム等
echo.
echo  ※ Hocotate_Toolkit.exe は外部ツールです。
echo    アプリ起動後に「参照...」ボタンで指定してください。
echo =====================================================
echo.
pause
