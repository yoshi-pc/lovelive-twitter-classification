# このrepoの目的
このlovelive-twitter-classificationは、ラブライブ！公式Twitterがプロジェクトを横断的に交々と投稿するのが不便だと感じているユーザに向けて開発されているものです。

つまり、以下のような感情を抱えながら過ごしているユーザにピッタリです。

- ラブライブ！の一部のプロジェクトに興味があるけど、それが埋もれて確認しにくくて困っている。
- ラブライブ！の全てのプロジェクトに興味があるけれども、それぞれ情報が錯綜しすぎていて情報の整理をしかねている。

ここにあるPythonとHTMLファイルを元に動かすと、ツイートをプロジェクトごとに(大まかに)分類してくれて、それをWebページ上で簡単に閲覧することができるようになります。

TwitterのAPIに自身で登録した上でベアラートークンを環境変数にセットしさえすれば、自身の環境でも動かすことができます。

# 動かす方法
まずは、`retrieve.py`でツイートを公式から取得します。この時、APIを利用するためのベアラートークンが必要になるので、別途`.env`というファイルを作成し、そこに`twitter_baerer`という環境変数を定義してください。スクリプトではこの環境変数を真っ先に読み込みに行き、これが未定義だと例外を出して停止します。

通常は長い時間はかからず2〜3秒程度で取得が完了しますが、APIのレート制限などで取得が遅れる場合もありますので、エラーや例外が出ていない限りは気長に待つつもりで実行してください。

この時に取得したツイートデータは、外部ファイルに`joblib.dump()`で保存されます。次は、この外部ファイルを読み込んで実際にHTMLファイルを出力します。

このHTMLファイルを出力する部分は`make_html.py`がその役割を担っており、`./server/index_template.html`を読み込み、それを元に最終的な`./server/index.html`を作成します。
原理的には非常に簡単で、`index.html`内に記述した`{% aqours_content %}`といった記述をツイートを表示させるためのコンテンツに置換することで最終的なHTMLファイルを生成しています。

もしこの部分を改変するとなるとある程度のHTMLやbootstrap5の知識が要求されますが、自由に見た目等を編集できます。

# その他
まだ制作途中で細かい仕様も決めていないので、決まり次第色々と更新していこうと思います。
