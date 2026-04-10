# PikiModel Randomizer
<!-- Python 3.10 / Windows -->
![Python](https://img.shields.io/badge/language-Python%203.10-3776AB?style=flat-square&logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white)

## Download

<a href="https://github.com/Sadc2h4/PikiModel-Randomizer/releases/tag/v1.1a">
  <img
    src="https://raw.githubusercontent.com/Sadc2h4/brand-assets/main/button/Download_Button_1.png"
    alt="Download .zip"
    height="48"
  />
</a>
<br>
<a href="https://uu.getuploader.com/freehack/download/200">
  <img
    src="https://raw.githubusercontent.com/Sadc2h4/brand-assets/main/button/Download_Button_3.png"
    alt="Download .zip"
    height="48"
  />
</a>
<br>

## Features

本アプリケーションはPikmin 2で使用されるキャラクターモデル（BMDファイル）のスケールをランダムに変化させた**バリアントを一括生成**するGUIツールです．  
頭・葉・体・脚・腕・目といった部位ごとにスケールの変動範囲を細かく設定でき，シード値を指定することで再現性のある結果を得ることができます．  
変換処理には外部ツール **Hocotate Toolkit** を使用します．
普段見慣れたキャラクターモデルもこのアプリケーションでランダマイズすると違った雰囲気を楽しめるかもしれません。

----------------------------------------------------------------------------------------------------

This application is a GUI tool for **batch-generating scale variants** of Pikmin 2 character models (BMD files).  
Scale ranges can be configured individually for each body part — head, leaf, body, legs, arms, and eyes.  
A fixed seed value produces reproducible results.  
Conversion relies on the external tool **Hocotate Toolkit**.
Even familiar character models might take on a different vibe when randomized using this app.

> [!WARNING]
> Ninjin.bmdなどを変換するとゲームがクラッシュする報告があります。通常のピクミンモデルのみを対象にしてください。
> 
> There have been reports that the game crashes when converting files such as Ninjin.bmd.
> Please limit your conversions to standard Pikmin models only.

## Requirements / 動作要件

| 項目 / Item | 内容 / Details |
|-------------|----------------|
| OS | Windows 10 / 11 (64-bit) |
| 外部ツール / External tool | [Hocotate Toolkit](https://github.com/Sadc2h4/Hocotate-Tool-Kit) |

>[!IMPORTANT]
>Hocotate Toolkit は別途ダウンロードして任意の場所に展開してください．  
>初回起動時にアプリ上部の「参照...」ボタンで `Hocotate_Toolkit.exe` のパスを指定してください．
>
>Download and extract Hocotate Toolkit separately to any location.  
>On first launch, click the **Browse...** button at the top of the window to specify the path to `Hocotate_Toolkit.exe`.


## Setup / セットアップ

```
PikiModel_Randomizer.exe
_internal\               ← Python ランタイム・依存ライブラリ（変更不要 / do not modify）
    SPERO_icon.ico
    numpy / tkinter 等
```

追加インストールは不要です。`PikiModel_Randomizer.exe` をダブルクリックして起動してください。  
No additional installation is required. Double-click `PikiModel_Randomizer.exe` to launch.

## Usage / 使い方

### 1. Hocotate_Toolkit.exe のパス指定 / Specify Hocotate_Toolkit.exe Path

アプリ起動後，ウィンドウ上部の「**Hocotate_Toolkit.exe:**」欄右の **参照...** をクリックし，  
Hocotate Toolkit フォルダ内の `Hocotate_Toolkit.exe` を選択してください．  
指定したパスは自動的に保存され，次回以降の起動時も引き継がれます．

----------------------------------------------------------------------------------------------------

After launching, click **Browse...** next to the **"Hocotate_Toolkit.exe:"** field at the top of the window  
and select `Hocotate_Toolkit.exe` inside the Hocotate Toolkit folder.  
The path is saved automatically and restored on subsequent launches.

---

### 2. BMDフォルダの選択 / Select BMD Folder

**「BMDフォルダ / BMD Folder」** 枠の **参照... / Browse...** ボタンをクリックして，  
バリアントを生成したい `.bmd` ファイルが入ったフォルダを選択してください．  
選択後，フォルダ内の `.bmd` ファイルが一覧に表示されます．

----------------------------------------------------------------------------------------------------

Click **Browse...** in the **"BMD Folder"** frame and select the folder containing the `.bmd` files  
you want to generate variants for. Detected files will appear in the list below.

---

### 3. 設定 / Settings

**「設定 / Settings」** 枠で変換のパラメーターを調整します．

| 設定項目 / Setting | 説明 / Description |
|-------------------|-------------------|
| バリアント数 / Variants | 各BMDファイルから生成するバリアントの数（1〜50） |
| シード値 / Seed | 乱数シード．同じ値を指定すると同じ結果が再現されます |
| CMDを非表示 / Hide CMD window | 変換中のコンソールウィンドウを非表示にします |
| 出力結果を一つずつ選択 / Select one output per type | 生成した複数バリアントの中からランダムに1つだけを `selected/` フォルダへ出力します |

---

### 4. スケール範囲の設定 / Scale Ranges

**「スケール範囲設定 / Scale Ranges」** タブで，部位ごとにスケールの最小値・最大値を設定します．  
数値が大きいほど元のサイズより大きくなり，小さいほど小さくなります（1.0 = 等倍）．

> [!WARNING]
> スケールを3.0以上にすると動作が遅くなる場合があります．負荷が高くなる組み合わせは避けるようにしてください．
> Setting the scale to 3.0 or higher may cause the system to slow down. Please avoid combinations that place a heavy load on the system.

| 部位 / Part | デフォルト範囲 / Default Range |
|-------------|-------------------------------|
| 頭 / Head | 0.75 〜 1.40 |
| 葉 / Leaf | 0.60 〜 1.60 |
| 体 / Body | 0.80 〜 1.25 |
| 脚 (左右) / Legs (L+R) | 0.70 〜 1.40 |
| 脚中心 / Leg Centre | 0.85 〜 1.15 |
| 腕 (左右) / Arms (L+R) | 0.70 〜 1.40 |
| 目 / Eye | 0.80 〜 1.30 |

---

### 5. 変換開始 / Start Conversion

**「変換開始 / Start Conversion」** ボタンをクリックすると変換が始まります．  
進捗はプログレスバーとログ欄でリアルタイムに確認できます．
変換が完了すると，選択したBMDフォルダ内に以下のフォルダが作成されます．

----------------------------------------------------------------------------------------------------

Click **"Start Conversion"** to begin processing.  
Progress can be monitored in real time via the progress bars and the log panel.
Upon completion, the following folders are created inside the selected BMD folder:

```
(Selected BMD folder)
├── variants\
│   ├── (BMD name)\
│   │   ├── (BMD name)_var01.bmd
│   │   ├── (BMD name)_var02.bmd
│   │   └── ...
│   └── ...
└── selected\               ← Created only when "Select one output per type" is enabled
    ├── (BMD name).bmd
    └── ...
```

## Language / 言語切り替え

ウィンドウ上部のドロップダウンから **日本語 / English** を切り替えられます．設定は次回起動時に引き継がれます．  
Switch between **日本語 / English** using the dropdown at the top of the window. The setting is saved automatically.

## Settings File / 設定ファイル

設定（言語・Hocotateパス・バリアント数・シード値・スケール範囲など）は  
`_internal\bmd_variant_settings.json` に自動保存されます．

----------------------------------------------------------------------------------------------------

Settings (language, Hocotate path, variants, seed, scale ranges, etc.) are saved automatically to  
`_internal\bmd_variant_settings.json`.

## Deletion Method / 削除方法

・`PikiModel_Randomizer.exe` と `_internal\` フォルダをまとめて削除してください．  
・Please delete `PikiModel_Randomizer.exe` and the `_internal\` folder.

## Disclaimer / 免責事項

・本ソフトウェアの使用によって生じたいかなる損害についても，作者は一切の責任を負いません．  
・I assume no responsibility whatsoever for any damages incurred through the use of this software.
