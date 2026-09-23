# TikTok #001 — サーブ練習

ステータス：企画採用済み。衣装・人物の参考画像を生成済み。最初の動画試作にはRunwayを使う方針で、接続完了は未確認。実写風の動作映像は未生成。完成動画ではない。

## 制作工程

[共通制作フロー](../../docs/production-workflow.md)に従う。ChatGPT Imagesで正面・横顔・全身のマスター画像を整備し、サーブ用の開始フレームへ展開する。Codexが生成指示と素材確認を担当し、まずRunwayでGen-4.5の利用可否を確認してサーブ1球を試作する。Veo 3.1 / Seedanceも共通フローの選択肢とし、切り替える場合は使用モデルと結果を記録する。採用したMP4をRemotionでつなぎ、字幕・音量を調整する。BGM・SE・ロゴは必要に応じて追加し、TikTok / Shorts向けに書き出す。

参考画像：`public/assets/rina/tennis/look-reference-v1.png`。画像生成ツールで制作。人物と衣装の検討用。コートのライン配置とネットまでの距離に不整合があるため、サーブの開始フレームとしては未採用。生成プロンプトは `image-prompt.txt` に保存。

## 採用した内容

莉奈が自分でベンチにスマホを立て、サーブを練習する。ネット、少しアウト、成功が混じる。テニス経験者が自然にアドバイスしたくなる、普通の練習記録。大げさな失敗や演技はしない。

9:16、1080×1920、30fps、目標20秒。顔は `public/assets/reference/rina-base.jpg` 左下のボブを主基準とする。

白いスポーツTシャツ、ネイビーのスコート、白いテニスシューズを今回の衣装案とする。右利きは今回の映像上の仮設定で、キャラクター正史には追加しない。声質未確定のため台詞音声は必須にせず、字幕と自然な環境音で構成できる。

## 編集構成

| 秒 | 映像 | 字幕 |
|---|---|---|
| 0–2.5 | スマホの角度を直し、コートへ戻る。調整後は固定画角 | 今日はサーブ練習🎾 |
| 2.5–7 | トスから着地まで連続した1球。ネットに当たる。小さく肩を落として次へ | なし |
| 7–11.5 | 2球目。対角のサービスボックスのサービスラインを少し越える。着地点を見て首をかしげる | なし |
| 11.5–16 | 3球目。対角のサービスボックスに入る。小さくうなずく | なし |
| 16–20 | スマホを取りに戻り、少し照れた自然な表情 | 同じように打ってるつもりなんだけどな。 |

秒数は編集目安。生成は各サーブを余裕のある長さで別クリップにし、動作を早回しせず待機部分を削って調整する。打球前後の途中で切らない。

## 撮影・生成の共通指示

自然なスマホ縦撮影。ベンチは手前のベースライン後方、少し横に寄せた位置。選手の全身、足元、トスの頂点、ネット、対角のサービスボックスの着地点が見える。サーブ中はカメラを固定し、ズーム・追尾・スローモーションを入れない。顔、衣装、コート、光、ラケット、利き手、撮影位置を全カットで維持する。顔の同一性は基準画像左下を優先する。

フォームは趣味でテニスをしている人の自然な動き。トスが少し安定しない程度で、危険な動作や誇張した初心者演技を入れない。球は1球、ラケットは1本。手・腕・ラケットを増やさない。ボールが途中で消える、増える、曲がる、ラケットをすり抜ける映像は採用しない。

## 動画生成用プロンプト

各クリップに同じ採用マスター画像とコート開始フレームを使用する。以下は未実行の下書きで、共通文と各クリップ文を組み合わせる。マスター整備後に人物参照の記述を採用画像へ合わせ、接続先モデルの入力形式・音声対応・最大尺に合わせて調整する。

### Common

Photorealistic casual smartphone tennis practice footage, vertical 9:16, real time. The same adult Japanese woman Rina, age 27, matching the lower-left bob portrait in the identity reference. Preserve her face and small mole near her mouth. Same plain white athletic T-shirt, navy tennis skort, white tennis shoes, dark brown bob, court and daylight throughout. Smartphone propped on a bench behind and slightly to one side of the near baseline. Fixed wide view showing the player's entire body, feet, the full ball toss, net and opposite service box. She serves right-handed from behind the baseline into the diagonally opposite service box. A recreational player's natural serve, mild toss inconsistency, no exaggerated incompetence. Exactly one ball in play and one racket. Continuous physically plausible motion from preparation through toss, racket contact, follow-through and landing. No camera movement during the serve, no cuts during ball flight, no slow motion, no text or logos. Natural court ambience and synchronized racket/ball sounds if audio is supported; no speech or music.

### Opening — source duration about 5 seconds

She finishes adjusting the phone at close range, checks the framing briefly, then walks back to the near baseline holding her racket. The phone settles and remains completely stationary. Natural unposed expression. No extra phone visible in the scene.

### Serve 1 — source duration about 6 seconds

She prepares, tosses and serves one ball. The ball travels from the strings toward the correct diagonal service box but strikes the net and drops back on her side. She exhales and briefly lowers her shoulders, then calmly resets. Show the entire serve and the visible net contact without cutting.

### Serve 2 — source duration about 6 seconds

She prepares, tosses and serves one ball. The ball clears the net and first bounces just beyond the opposite service line, still within the lateral width of the intended diagonal service box. She watches the bounce and slightly tilts her head. Show the full ball trajectory and first bounce without cutting.

### Serve 3 — source duration about 6 seconds

She prepares, tosses and serves one ball. The ball clears the net and first bounces clearly inside the diagonally opposite service box. She gives a small satisfied nod, a restrained pleased reaction. Show the entire serve and first bounce without cutting.

### Ending — source duration about 5 seconds

She walks back toward the bench-mounted phone with her racket, a slightly sheepish relaxed smile, then reaches to stop the recording. Keep the same camera position until her hand reaches it. No dialogue.

## 完成判定

- 人物の顔・ホクロ・衣装・利き手がカット間で一致。
- コートのライン配置とネット位置が正しい。
- トス・打点・着地が画面内に入り、途中で動作を切っていない。
- ネット、アウト、成功が実際の打球で判別できる。字幕で結果を偽装しない。
- アウトはベースラインではなくサービスラインとの位置関係で確認する。
- 球・ラケット・指・手足に生成破綻がない。
- 字幕は上下のUI領域を避け、全身や着地点を隠さない。
- 映像を通常速度で全編確認してから完成MP4として納品する。
