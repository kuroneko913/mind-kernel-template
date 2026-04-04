# Mind Kernel Modules

このディレクトリは、個人の認知モデルを「更新頻度」と「役割」で分割したモジュール群です。

- **`identity.json`**: あなたのアイデンティティと認知の基盤（不変の核）。
- **`backlog.json`**: 現在進行形の課題、Issue、実験。
- **`patterns.json`**: 獲得・定着した思考・言動のライブラリ（パターン）。
- **`meta.json`**: モデルの設計思想、公開ポリシー、各モジュールの定義（システム）。

※各モジュールの詳細な役割と使い分けの基準は `meta.json` の `governance.module_definitions` に定義されています。AIはそちらを参照してください。

## 成長のライフサイクル
1. 新たな課題や気づきを `backlog.json` に **Issue** として登録する。
2. 試行錯誤を経て、再現性のある解決策が見えたら、それを **Pattern** として抽出し `patterns.json` へ昇華させる。
3. 対応する `backlog.json` の項目をクローズ（削除）する。
