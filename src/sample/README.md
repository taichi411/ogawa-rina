# sample.mp4 のRemotion再現版

コンポジション: `SampleRecreation`（1920×1080、30fps、897フレーム、29.9秒）。
参考動画の黒い余白を取り除き、映像部分を画面全体に拡大しています。

## プレビュー・書き出し

```powershell
npm run dev
npx remotion render SampleRecreation out/sample-recreated.mp4 --crf=18
```

納品版 `out/sample-recreated-final.mp4` は、Remotion出力の映像に元のAAC音声を
無再圧縮で結合し、映像と音声を29.9秒に揃えています。
Windowsでは `./scripts/render-sample.ps1` で書き出しから音声結合まで実行できます。

Chromeの自動取得ができない環境では、実行時に
`--browser-executable="C:/Program Files/Google/Chrome/Application/chrome.exe"`
を指定できます。

## 構造

| ファイル         | 開始フレーム | 内容                               |
| ---------------- | -----------: | ---------------------------------- |
| Intro.tsx        |            0 | リード獲得の悩み                   |
| Problems.tsx     |           98 | MA導入・コンテンツ不足・リード不足 |
| Solution.tsx     |          314 | ホワイトペーパー・街並み           |
| Benefits.tsx     |          468 | 資料フォルダー・リード獲得         |
| Question.tsx     |          619 | 企画と制作・疑問符・資料の山       |
| CallToAction.tsx |          758 | はじめかた・URL                    |

`Recreation.tsx` が尺、場面の開始フレーム、音声、拡大を管理します。
`shared.tsx` は文字の分割アニメーション、図形、星、モニターなどです。
人物の腕の角度、文字の出現順、拡大、揺れなどはフレーム数から決定します。
CSSアニメーションやランダムな実行時タイミングには依存しません。

## 参考由来の素材と精度

元の人物イラスト・網点・文字輪郭を保つため、参考動画から切り出した43点の
画像レイヤーを `public/sample-recreation/` に保存しています。
動画全体の貼り付けや、全フレーム画像の連番再生ではありません。
文字は輪郭を優先した画像素材のため、テキストを変更するには対応する画像を
差し替えるか、Reactのテキスト要素へ置き換えてください。

音声は参考動画から取り出したAACを使用しています。
ワイプの帯の位置・幅は参考フレームから実測し、`wipe.ts` に保存しています。
人物の腕・表情の微細な変化、文字の揺れ、星の点滅などはパーツ単位の再構成で、
全画素・全フレームが完全一致するものではありません。
元映像の有効な画素数は約486×274であり、1920×1080化しても素材自体の
解像感が新しく増えるものではありません。

## 解析の再現

`scripts/prepare-reference.py` がパーツの切り抜き、位置データ、ワイプ計測を行います。
入力は `analysis/frames/0001.png` ～ `0897.png` です。FFmpegでは次のように作れます。

```powershell
npx remotion ffmpeg -i "C:/Users/airfl/Downloads/sample.mp4" -vf "crop=486:274:652:446" -an analysis/frames/%04d.png
```

元の `MyComp` と既存の素材・READMEは保持しています。
