@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"

set SUPERBMD="%~dp0SuperBMD_2.4.2.1_RC\SuperBMD.exe"
set PYTHON=py -3

:: 処理対象のBMDファイルを順番に処理
for %%F in (*.bmd) do (
    call :process_bmd "%%~nF"
)

echo.
echo ==========================================
echo 全BMDファイルの差分生成が完了しました。
echo 出力先: variants フォルダ
echo ==========================================
pause
exit /b 0


:process_bmd
set BASE=%~1
echo.
echo ------------------------------------------
echo 処理中: %BASE%.bmd
echo ------------------------------------------

:: 作業ディレクトリ
set WORKDIR=%~dp0work_%BASE%
set VARDIR=%~dp0variants\%BASE%

if exist "%WORKDIR%" rmdir /s /q "%WORKDIR%"
mkdir "%WORKDIR%"
mkdir "%VARDIR%" 2>nul

:: BMD → DAE 変換
echo [1] BMD を DAE に変換中...
copy "%~dp0%BASE%.bmd" "%WORKDIR%\%BASE%.bmd" >nul
%SUPERBMD% "%WORKDIR%\%BASE%.bmd"
if errorlevel 1 (
    echo エラー: DAE変換に失敗しました
    goto :cleanup
)

:: DAE が生成されたか確認
if not exist "%WORKDIR%\%BASE%.dae" (
    echo エラー: %WORKDIR%\%BASE%.dae が見つかりません
    goto :cleanup
)

:: Python スクリプトで DAE 差分を生成
echo [2] DAE 差分を生成中 (10バリアント)...
%PYTHON% "%~dp0make_variants.py" ^
    "%WORKDIR%\%BASE%.dae" ^
    "%WORKDIR%\variants" ^
    "%BASE%" ^
    10 ^
    42

if errorlevel 1 (
    echo エラー: Python スクリプトの実行に失敗しました
    goto :cleanup
)

:: 各差分 DAE → BMD 変換
echo [3] 差分 DAE を BMD に変換中...
for /L %%V in (1,1,10) do (
    set VARNUM=0%%V
    set VARNUM=!VARNUM:~-2!
    set VARDAE=%WORKDIR%\variants\%BASE%_var!VARNUM!.dae
    set VARBMD=%VARDIR%\%BASE%_var!VARNUM!.bmd

    if exist "!VARDAE!" (
        :: テクスチャをvariantsディレクトリにコピー
        for %%T in ("%WORKDIR%\*.png") do (
            copy "%%T" "%WORKDIR%\variants\" >nul 2>nul
        )

        echo   バリアント !VARNUM!: DAE → BMD 変換中...
        %SUPERBMD% "!VARDAE!" "!VARBMD!" ^
            --mat "%WORKDIR%\%BASE%_materials.json" ^
            --texheader "%WORKDIR%\%BASE%_tex_headers.json"

        if errorlevel 1 (
            echo   警告: バリアント !VARNUM! の変換に失敗しました
        ) else (
            echo   完了: !VARBMD!
        )
    )
)

:cleanup
if exist "%WORKDIR%" rmdir /s /q "%WORKDIR%"
exit /b 0
