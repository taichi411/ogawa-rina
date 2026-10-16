# Gemini TTS接続テスト

Python標準ライブラリからGemini REST APIを呼びます。Python 3.11以上が必要で、pipでの追加インストールは不要です。最初は既製声 `Kore` で接続と音声取得を確認し、その後に莉奈のカスタム声IDへ切り替えます。

## 初回の操作

1. この変更をmainへマージします。新しい手動実行workflowはデフォルトブランチへの追加後に利用できます。
2. リポジトリの **Settings → Secrets and variables → Actions → New repository secret** を開きます。
3. 名前を **GEMINI_API_KEY** にして、値にGoogle AI Studioで発行したAPIキーを入力します。台本やチャット、コードにはキーを貼りません。
4. **Actions → Gemini TTS → Run workflow** を開き、ブランチmainを選択します。
5. 最初は既定の台本・Kore・gemini-3.8-flash-ttsのままで実行します。
6. 完了した実行の **Artifacts → gemini-tts-…** をダウンロードします。ZIP内の `output.wav` を再生して確認します。

生成物にはWAVと `output.json`（モデル、声、MIME、バイト数、APIが返した使用量）が含まれます。生成音声は自動でGitへコミットせず、Actionsのartifactとして7日間保存します。必要な音声は期限前に保存してください。

API呼び出しは手動実行時のみです。PRではキーを使わないオフラインテストだけを実行します。生成API側の利用枠・課金は別途適用されます。失敗時の自動再試行は行いません。

リポジトリは現在publicです。キーはSecretsで管理しますが、台本などのworkflow入力・実行情報は機密情報の保存先として扱わないでください。初回は上記の公開可能なテスト文を使います。

## 台本と声の変更

Run workflowの **text** が読み上げ台本、**style** が演技指示です。`<laugh>` や `<short pause>` などはtextにそのまま入力できます。台本はシェルのコードへ埋め込まず、環境変数から読み込みます。

**voice** はKore等の既製声名、またはAPIで利用できる `voice_...` などのIDです。AI Studio上の表示名 `ogawa-rena 3` が一意なAPI用IDであるとは仮定しません。既製声で成功後、カスタム声IDを確認して設定します。

## 失敗した場合

このチャットへ **失敗したActions実行のURL** を送ってください。接続されたGitHubツールで取得可能な範囲のログ・ジョブ・artifactを確認し、コード修正を行えます。APIキー自体は送る必要がありません。

| 表示 | 確認するもの |
|---|---|
| GEMINI_API_KEY is missing | Repository secretの名前・登録先 |
| HTTP 400 / 401 | 入力・声ID・APIキーの有効性 |
| HTTP 403 | APIキーの制限・プロジェクトのAPI/モデル利用権限 |
| HTTP 404 | モデル名・声ID・利用可能なモデル |
| HTTP 429 | レート制限・クォータ・課金設定 |
| タイムアウト / HTTP 5xx | ネットワーク・Google側の障害。状況確認後に手動再実行 |
| 音声が返らない / WAVが不正 | 該当実行URLを共有し、応答形式を調査 |

キー・リクエストヘッダー・APIエラー本文はログへ出しません。HTTPステータスと確認先を表示します。

## ローカル実行と検証

GEMINI_API_KEYを実行環境の環境変数に設定してから実行します。

```bash
python scripts/gemini_tts.py --text "こんにちは。音声生成の接続テストです。" --voice Kore
python scripts/gemini_tts.py --text-file transcript.txt --style "Warm, relaxed Japanese." --output out/gemini-tts/output.wav
python -m unittest discover -s scripts -p test_gemini_tts.py -v
```

既存のRemotion用 `out` 除外設定を利用するため、ローカル生成物はGitへ入りません。

## 仕様の参照

- [Google公式TTSドキュメント](https://ai.google.dev/gemini-api/docs/generate-content/speech-generation)
- [GitHub Actions Secrets](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/use-secrets)

この段階ではチャットからworkflowを新規起動する接続は追加していません。まず手動でAPI接続を確認します。

## 莉奈のカスタム声IDを調べる

1. 声一覧機能の変更をmainへマージします。
2. **Actions → Gemini Voice IDs → Run workflow** を開きます。
3. ブランチmain、検索語 `ogawa` のまま実行します。既存の `GEMINI_API_KEY` をそのまま利用します。
4. 実行ページのSummaryに表示名とVoice IDの表が出ます。artifactにも `voices.json` と `voices.md` が保存されます。
5. 実行ページのURLをこのチャットへ送ってください。取得可能な結果から候補を確認します。

この処理は `GET /v1beta/voices` で保存済みのカスタム声を検索するだけで、声の作成・削除・音声生成は行いません。APIキー、voice replication key、音声データは出力しません。声名とIDの表はpublicリポジトリのActions Summaryに表示されます。

同じ `ogawa-rena 3` が複数ある場合も、異なるIDを全件残します。並び順だけでお気に入りの声を決めません。各候補のIDを **Gemini TTS → Run workflow → voice** に入力して同じ短い台本で試し、AI Studioのお気に入りの声と聴き比べて選びます。APIのIDは表示名ではなく `voice_...` 等の値です。

0件なら検索を空欄にして再実行し、それでも見つからなければAI Studioで使ったアカウント・プロジェクトとAPIキー側の利用権限・声の保存状態を確認します。APIが列挙するのは呼び出し元がアクセスできる保存済みの声で、AI Studioに見えている声がこのキーで必ず取得できるとは限りません。

```bash
python scripts/gemini_voices.py --search ogawa
python scripts/gemini_voices.py --search ""
```

仕様：[Google Voices API](https://ai.google.dev/api/voices)。APIはBetaです。
