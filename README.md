# Milvaneth
FF14マーケット原価計算ソフト「Milvaneth」のリポジトリです。
![image](https://github.com/nunmo1st/Milvaneth/blob/master/screenshot.png)
## Overview
Universalis.appを用いた、FF14の原価計算を行うwebアプリです。

## USage
1. まずは「Universalis.app」にて初期設定を行ってください。

 ![image](https://github.com/nunmo1st/Milvaneth/blob/master/static/UVS_config2.png)

3. 次に、このWebアプリの設定画面にて設定を行ってください。

![image](https://github.com/nunmo1st/Milvaneth/blob/master/static/UVS_config3.png)
   
    ※キャラクター名のファーストネームとファミリーネームの間は半角スペースを空けてください。(履歴検索の絞り込みに用います。)

    ※「購入を行ったワールド」は、ワールドテレポを用いて材料の購入を行っている場合はALLがおススメです。(履歴検索のワールドの範囲を指定します。)

    ※「販売を行うワールド」は、キャラクターのホームDC・ワールドを設定してください。(利益率の計算を行う為に使用します。)


4. 確認を押して確定してください。(登録すると、情報がクッキーに保存されます。(有効期限4週間)

## Features

1.ノーマルモード

  最新の購入履歴を各ワールドから20件ずつ引き出し、値段で昇順にソートし上位20件の平均値で計算を行います。
  正確性では個別検索モードには劣りますが、ほぼ全てのアイテムで原価計算が可能です。
  履歴は計算に用いた履歴が表示されます。
  
2.個別検索モード

  設定で指定されたワールド・DCから設定されたキャラクター名の購入履歴だけを抽出し、最後の履歴から遡って3時間以内の履歴で計算を行います。
  正確な計算が可能ですが、購入履歴の無いアイテム・もしくは古い履歴である場合は履歴の読み出しができず、不完全な計算になる可能性があります。
  履歴は、計算に用いられた履歴は文字色がブラック。計算に用いられなかった古い記録はグレーで表示されます。
