# 第6回 解答

## 演習

<!-- [tool call] の行は、表示された行をそのまま貼り付けてください。終わらなかった STEP は、空欄のままでかまいません。 -->

- STEP 1 のツールの名前：glossary_search_glossary
- STEP 2 の [tool call]：[tool call]   glossary_search_glossary({'query': '3レベル'})
- STEP 3 の [tool call]：[tool call]   fetch_fetch({'url': 'https://modelcontextprotocol.io/'})
- STEP 4 の [tool call]：[tool call]   aws_aws___search_documentation({'topics': ['general'], 'search_phrase': 'Amazon S3 バージョニング 概要'}) / [tool call]   aws_aws___search_documentation({'topics': ['general'], 'search_phrase': '"Versioning" "Amazon S3" what is'})
- 気づき・疑問：glossary と fetch は起動時に [server] ...: コマンドで起動 と表示され、aws は [server] aws: URL に接続 と異なる表示がされた。

## 宿題

<!-- 基礎・実装・発展のどれか1つに取り組めば完了です。 -->

- 取り組んだレベル：基礎
- やったこと：
サーバー側のファイル（`app/mcp_server.py`）に `get_lecture_summary` を公開する処理を追加した（エージェント側の設定・コードは演習時点から変更していない）。
`git status` で変更対象を確認したのち、`uv run python -m app.mcp_agent --list-tools` でツール一覧の表示を確認した。
`uv run python -m app.mcp_agent --trace "第2回では何を学びますか？ "` を実行してツールの呼び出しを確認し、`uv run pytest -q` でテストを実行した。

- 結果：
`uv run python -m app.mcp_agent --list-tools` の出力で、モデルに見えているツールが 7 個から 8 個に増え、`[glossary_get_lecture_summary]` が追加されていることを確認した。
`--trace` 付きの質問実行では、`[tool call] glossary_get_lecture_summary({'lecture': 2})` が呼ばれ、返却された第2回の要点をもとに回答が生成された（モデル応答 2 回）。
`uv run pytest -q` の実行結果は `21 passed in 5.15s` となり、すべてのテストが通過した。

- 気づき・疑問：
エージェント側のファイル（`app/mcp_servers.json` や `app/mcp_agent.py`）を変更しなくても、`app/mcp_server.py` 側でツールを公開するだけで起動時にツール一覧へ `glossary_get_lecture_summary` が自動で追加され、モデルからも正しく選択・呼び出しが行われることがログから確認できた。
`get_lecture_summary` も他のツールと同様に `サーバー名_ツール名`（`glossary_get_lecture_summary`）の形式でモデルに公開され、ツールの説明文に従って質問中の「第2回」から `{'lecture': 2}` という整数引数が適切に抽出されていた。



