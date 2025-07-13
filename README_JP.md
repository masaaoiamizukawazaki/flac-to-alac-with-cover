# FLAC to ALAC Converter & Cover Embedding Fix Tool

---

## ■はじめに

開発経験が乏しく、AIに作成させたため、機能や品質について至らない点があるかもしれません。  
ご理解のほどよろしくお願いいたします。

---

## ■起動方法

「`flac-to-alac-with-cover.exe`」を実行してください。

---

## ■機能

主に3つの機能があります：

- FLAC形式の音声ファイルをALAC（Apple Lossless Audio Codec）形式に変換する
- FLAC FolderとOutput Folderのファイルを比較し、ALACにのみジャケットがない場合は修正を試みる
- FLAC Folderで指定したフォルダ内の`.flac`以外のファイルをリスト化する

---

## ■使い方

本ツールは、以下のようなフォルダ構成を想定しています：

```
FLAC/
└── アーティスト名/
    └── アルバム名/
        └── *.flac
```

この場合、**FLAC Folderには「FLAC」フォルダ自体を指定**してください。  
出力先のALACフォルダも、以下のような構造で自動生成されます：

```
ALAC/
└── アーティスト名/
    └── アルバム名/
        └── *.m4a
```

---

### UI操作の説明

| ボタン | 機能 |
|--------|------|
| FLAC Folder | `.flac` ファイルが入っているフォルダを選択 |
| Output Folder | `.m4a` ファイルの出力先フォルダを指定（空欄なら `ALAC/` が自動生成） |
| Start Conversion | 変換処理の開始 |
| Stop | 処理の中断（途中終了） |
| Check Non-FLAC Files | `.flac` 以外のファイルをリスト表示 |
| Fix ALAC Cover Embedding | `.m4a` にカバーアートが無ければ `.flac` から補完する |

補足：
- すでに変換済みで、`ALAC` 側の更新日時が新しければ処理はスキップされます。
- ジャケットが埋め込まれている `.m4a` には再埋め込みしません。

---

## ■ライセンスと使用しているライブラリ

本ツールは以下のオープンソースコンポーネントを利用しています：

- [FFmpeg](https://ffmpeg.org/) （LGPL/GPLライセンスのマルチメディア処理フレームワーク）
- [Mutagen](https://mutagen.readthedocs.io/) （GPLv2 or later）

同梱しているFFmpegバイナリは LGPLv3 および GPLv3 ライセンスのもとで配布されています。

---

## ■ソースコードについて

本ツールのソースコードは以下のGitHubリポジトリにて公開しています：  
🔗 [https://github.com/masaaoiamizukawazaki/flac-to-alac-with-cover](https://github.com/masaaoiamizukawazaki/flac-to-alac-with-cover)

ご自由にダウンロード、検査、改変が可能です。

---

## ■免責事項

本ツールは現状のまま提供されており、いかなる保証もありません。  
ご利用は自己責任でお願いいたします。

---

## ■お問い合わせ

不具合報告やご質問は、上記GitHubリポジトリの**Issue**機能をご利用ください。  
対応が遅れる場合や、対応しない可能性もありますことをあらかじめご了承ください。