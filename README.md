# pov-ray_render_for_simutrans_vehicle

pov-rayを用いてsimutransの車両アドオンを自動レンダーするアプリケーションです。
本アプリケーションはwindows用ですが、ソースコードはLinux等でも使用可能なはずです。

### インストール方法

releaseより最新版をダウンロードして下さい。インストールは不要で、ダウンロード後simutrans_vehicle_addon_maker_with_pov-ray.exeをダブルクリックすれば起動します。

### 使い方

0. http://www.povray.org/ よりpov-rayをダウンロードします。
1. simutrans_vehicle_addon_maker_with_pov-ray.exeを起動します。または、pythonを使用している場合、ソースコードの全ファイルをダウンロードして ```python run_pov_vehicle.py``` で起動します。  
2. pov-rayシーンファイルを生成していない場合、起動したウィンドウの「.povファイルを作成」を押してシーンファイルのテンプレートを作成します。作成済みの場合は3.へ  
3. pov-rayシーンファイルを編集します。編集済みの場合は4.へ  
4. simutrans_vehicle_addon_maker_with_pov-ray.exe上で「選択」ボタンから編集済みのpov-rayシーンファイルを選択し(2.を経由した方は不要)、pakサイズを指定して「変換を実行」を押します。
5. 出力する画像名を指定すると、変換が実行されます。pov-rayのウィンドウが一瞬表示され、画像生成後にpov-rayのウィンドウが閉じたら完成です。

### こんなときは

- 起動しない、安定して動作しない  
アンチウイルスソフト等の設定により、起動しない、または起動後にクラッシュする場合があります。アンチウイルスソフト等の設定を修正してください。
- 「変換を実行」時にpov-rayのウィンドウが自動で閉じず、なんらかの警告文を表示している  
v1.0ではpov-rayシーンファイルと出力画像が同じディレクトリに存在しない場合エラーが起こることがあります。画像の出力先を同じディレクトリに変更してみてください。
それでも改善しない場合は、pov-rayシーンファイルに誤りがある可能性があります。括弧の数など構文を修正してください。  
- 出力画像の位置がおかしい
v1.0ではpak128.japan用以外オフセットの設定が完了しておらず、車両の位置がずれて出力される可能性があります。
また、シーンファイル内のpaksize及び画像位置を適切に設定する必要があります。

## 利用・改造・再配布についてと免責事項

本プログラムを使用した一切の作品、および本プログラム自体の改造・再配布について一切の制限はございません。ご自由にお使いください。

本プログラムのダウンロード、インストール、使用等に伴い生じた一切の損害・損失について当方は責任を負いかねます。

## release note

2025.01.05 : v1.0 公開 pak128.japan用のみ画像位置修正を反映
