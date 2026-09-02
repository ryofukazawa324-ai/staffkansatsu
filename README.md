# staffkansatsu

スタッフの良い行動・改善期待行動を日々記録し、半年単位で振り返るためのスマホ対応Webアプリです。

## 主な機能

- Excelシフト表からスタッフ名を取得
- 抽出開始名 / 終了名で範囲指定
- 指定スタッフの除外、観察対象ON/OFF
- 良い点、改善期待行動、具体的な出来事、次回確認、現在グレードを記録
- 4〜9月を上期、10〜3月を下期として自動集計
- 半年まとめ・ChatGPT分析用テキストのコピー
- JSONバックアップ / 復元
- CSV出力

## データ保存について

観察記録やスタッフ情報はブラウザの localStorage に保存します。GitHubリポジトリには観察内容を保存しません。

端末変更やブラウザデータ削除に備えて、定期的にJSONバックアップを保存してください。

## GitHub Pages

`.github/workflows/pages.yml` を含めています。Pagesが未設定の場合は、Repository Settings → Pages → Build and deployment → Source を `GitHub Actions` に設定してください。
