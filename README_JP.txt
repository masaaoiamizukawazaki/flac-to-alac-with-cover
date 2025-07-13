FLAC to ALAC Converter & Cover Embedding Fix Tool

■はじめに
開発経験が乏しく、AIに作成させたため、機能や品質について至らない点があるかもしれません。
ご理解のほどよろしくお願いいたします。

■起動方法
「flac-to-alac-with-cover.exe」を実行してください。

■機能
主に3つの機能があります。
・FLAC形式の音声ファイルをALAC（Apple Lossless Audio Codec）形式に変換する。
・FLAC FolderとOutput Folderのファイルを比較し、ALACにのみジャケットがない場合は修正を試みます。
・FLAC Folderで指定したフォルダ内の.flac以外のファイルをリスト化します。

■使い方
本ツールは、以下のようなフォルダ構成を想定しています。

FLAC/
└── アーティスト名/
    └── アルバム名/
        └── .flac ファイル

この場合、FLAC Folderには「FLAC」フォルダ自体を指定してください。  
出力先のALACフォルダも同様の構造で自動生成されます。

FLAC Folder	FLACファイルが入っているフォルダを選択してください。
Output Folder	ALACファイルの出力先フォルダを指定してください。
			デフォルトでは、FLAC Folderで指定した親フォルダと同階層にALACフォルダを作成します。

「Start Conversion」ボタンで変換処理を開始します。
「Stop」ボタンで処理を中断します。
　FLAC FolderとALAC Folderに同名のファイルがあり、
　FLACの更新日がALACよりも古い場合は、変換をスキップします。

「Check Non-FLAC Files」ボタンで、FLACフォルダ内にFLAC以外のファイルがあるか確認できます。

「Fix ALAC Cover Embedding」ボタンで、
　FLACフォルダとOutputフォルダを比較し、
　ALACファイルにのみジャケットが埋め込まれていない場合、修正を試みます。
　すでに画像が埋め込まれている場合、処理をスキップします。

■ライセンスと使用しているライブラリ
本ツールは以下のオープンソースコンポーネントを利用しています。

FFmpeg （LGPL/GPLライセンスのマルチメディア処理フレームワーク）

Mutagen （Python製オーディオメタデータライブラリ、LGPLライセンス）

FFmpegのライセンスについて
同梱しているFFmpegバイナリはLGPLv3およびGPLv3ライセンスのもと配布されています。
FFmpegのソースコードや詳細なライセンス情報は以下のページから入手できます。
https://ffmpeg.org/

Mutagenのライセンスについて
MutagenはGPL v2以降（GPL v2 or later）で提供されています。
詳細は以下をご参照ください。
https://mutagen.readthedocs.io/

■ソースコードについて
本ツールのソースコードは以下のGitHubリポジトリにて公開しています。
https://github.com/masaaoiamizukawazaki/flac-to-alac-with-cover

ご自由にダウンロード、検査、改変が可能です。

■免責事項
本ツールは現状のまま提供されており、いかなる保証もありません。
ご利用は自己責任でお願いいたします。

■お問い合わせ
不具合報告やご質問は、上記GitHubリポジトリのIssue機能をご利用ください。
不具合対応については、対応が遅れる場合や、対応しない場合がありますことをご了承ください。