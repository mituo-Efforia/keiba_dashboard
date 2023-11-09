# keiba_dashboard
2012年から2021年の10年分の中央競馬重賞レースのに関するデータについて、データの収集からダッシュボードの作成までをまとめたリポジトリです。  

## 🐴: 概要  
* 中央競馬各重賞レース(G1,G2,G3)の記録を可視化したDashboardです。
* Setting欄のドロップダウンよりレースのランク(G1,G2,G3)、レース名、表示するデータを選択し、applyボタンを押してください。
* 各グラフより以下の内容が確認できます。
* Time Transition 優勝馬、二着馬、三着馬、入着馬(三着馬と同じ)、平均走破タイムの推移
* SexRatio 優勝馬、二着馬、三着馬、入着馬の性別比率、表示データより平均が選ばれた場合は性別出走数比率を表示します。
* Jockey Results 優勝馬、二着馬、三着馬、入着馬の騎手の比率、表示データより平均が選ばれた場合は各騎手の出場回数を表示します。
* AgeRatio 優勝馬、二着馬、三着馬、入着馬の年齢比率、表示データより平均が選ばれた場合は年齢別出走数比率を表示します。

## 📚: リポジトリの構成  

* 'main.ipynb'
  * Dashを用いたダッシュボードの構築を行うnotebook。
   
* 'data'
  * csvではデータ量が多くgithubにpushできなかったため、parguetファイルを使用
  * scrapeで収集したデータをdata整形で加工後parquetファイルにて保存した。
  * 各データについての説明
    * dashboard_data.parquet : main.ipynbに読み込ませるデータ。　下記の二つのデータを結合し、該当するレースのみを抽出、加工したデータ。
    (20115 rows × 39 columns)
    * horse_data_2012_2021.parquet : horse_data_2012_2021.zip内のデータを結合し、加工を施したデータ。(加工内容に関してはdata整形を参照。)
    (1390261 rows × 25 columns)
    * race_data_2012_2021.parquet : race_data_2012_2021.zip内のデータを結合し、加工を施したデータ。(加工内容に関してはdata整形を参照。)
    (488126 rows × 19 columns)
      
* 'data整形用'
  * scrapeで収集してきたデータを適切な形に変換したnotebook
  * 下記に各notebookでの加工内容概要を記載
    * race_data_concat.ipynb : 分割して取得したrace_dataを結合し、以下の加工をした。
      *  カラムの半角スペースを削除し、扱いやすさを改善。
      *  可視化様に走破タイムを秒単位に変換。
      *  馬体重、性齢などの2つの要素が入っているカラムの情報分割。
    * horse_data_concat.ipynb : 分割して取得したhorse_dataを結合し、以下の加工をした。
      *  カラムの半角スペースを削除し、扱いやすさを改善。
      *  映像列など欠損値しかないカラムの削除
      *  芝2000の様な距離と馬場素材が入っているカラムを
         と2000の様にsurfaceと距離で情報分割。
    * dashboard_data_reshape.ipynb : 上記2データを加工して結合し、dashborard様に更に加工をしたデータ。
      * horse_dataから両方に重複するカラムの削除
      * horse_dataの方のrace_idに海外レースのidがstr型のためintに変換
      * horse_idとrace_idをkeyに結合
      * ソートに必要な開催年、レースレベル列の作成。
    * parquet_convert : 各データがcsvだと大きすぎてアップロードができなかったため、変換した。

* 'scrape'
  *  Webサイトスクレイピング実行用のnotebook、およびその処理を関数化したpythonファイルを格納
  *  主に2つのurl群をスクレイピング
  *  下記のrace_dataスクレイピングurlからテーブルデータ部分を取得。
     horse_dataスクレイピングurlからテーブルデータを取得。
     スクレイピング先サンプルurl
     * race_data : https://db.netkeiba.com/race/202106050811/
     * horse_data : https://db.netkeiba.com/horse/2018105027/

