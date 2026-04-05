# Mind Kernel Template

このリポジトリは、**primary_user** の思考、価値観、判断基準、そしてキャリアの方向性をコード化・構造化した「Mind Kernel」のテンプレートです。

AIエージェントや他者が **primary_user** という人物を深く理解し、適切なコミュニケーションや意思決定のサポートを行うための「カーネル（核）」として機能することを目的としています。

## Modular Structure (v4.0.0)

モデルを役割と更新頻度に基づいて以下の4つのモジュールに分割し、`kernel/` ディレクトリ配下で管理しています。

*   [**kernel/identity.json**](./kernel/identity.json)
    *   あなたのアイデンティティと認知の基盤。プロフィール、不変の価値観、CliftonStrengthsなどの「不変の核（Nature）」。
*   [**kernel/backlog.json**](./kernel/backlog.json)
    *   現在進行形の課題、Issue、実験、および健康や収支のモニタリング項目。高頻度で更新される動的な状態。
*   [**kernel/patterns.json**](./kernel/patterns.json)
    *   獲得・定着した思考・言動のライブラリ。経験から得られた「再現性のある知恵（Learn）」。
*   [**kernel/meta.json**](./kernel/meta.json)
    *   モデルの設計思想、公開ポリシー、AIへの指示、各モジュールの定義。

詳細な各モジュールの役割については、[kernel/README.md](./kernel/README.md) を参照してください。

## Usage for AI Agents

このリポジトリを参照するAIエージェントは、`kernel/` 配下の各JSONを参照し、以下のスタンスで振る舞うことが期待されています。

*   一般的なアドバイスではなく、本リポジトリに定義された「primary_user固有のコンテキスト」に基づいた対話を行うこと。
*   仕事からプライベートまで相談できる「戦友」としてのポジションを意識すること。
*   AIの推測と事実を明確に分け、根拠がある場合はそれをセットで提示すること。
*   **Issueベースの成長**: 対話を通じて新たな課題を発見した場合は `backlog.json` への登録を、解決策が定着した場合は `patterns.json` への昇華を提案すること。

## Policies

*   **公開ポリシー**: 固有名詞や機密情報を排除し、抽象化された「パターン」として記述することを徹底しています。
*   **バージョニング**: Gitタグでバージョン管理します。

詳細な定義や最新のステータスについては、常に [kernel/meta.json](./kernel/meta.json) を参照してください。

## Security & Privacy (Safety first)

> [!CAUTION]
> **本リポジトリは「テンプレート」です。実際に自分の思考やバックログを記録して運用する際は、必ず「Private（非公開）リポジトリ」として運用することを強くおすすめします。**

このリポジトリをテンプレートとして利用（Fork）する際は、以下の点に十分注意してください。

1.  **個人情報の混入**: `kernel/` 内の JSON を更新する際は、氏名、住所、電話番号、具体的な所属先などの「個人が特定できる情報」を直接書かないようにしてください。
2.  **Git履歴**: 誤って個人情報をコミットしてしまった場合、単に削除するだけでは履歴が残ります。履歴ごと抹消するか、新しいリポジトリとして作り直すことを推奨します。
3.  **Secrets**: APIトークンなどは、決してファイルに直接書かず、GitHub Secrets 等の安全な管理方法を利用してください。
4.  **`.gitignore`**: 本リポジトリには標準的な `.gitignore` が含まれています。これを削除したり、重要なファイルが管理対象に含まれたりしないよう確認してください。

## Automation

### Monthly Growth Report
毎月1日のJST 09:00に、過去1ヶ月の Mind Kernel の差分（成長記録）を解析し、Slackに通知するワークフローが稼働しています。

*   **Script**: `scripts/analyze_growth.py --since "1 month ago"`
*   **Trigger**: Monthly Schedule & Manual Dispatch (`workflow_dispatch`)
*   **Secrets**: GitHub Repository Secret に以下の2つを設定してください。
    *   `SLACK_BOT_TOKEN`: Slack AppのBot User OAuth Token (scope: `files:write` が必要)
    *   `SLACK_CHANNEL_ID`: 通知先のチャンネルID
