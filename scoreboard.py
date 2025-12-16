#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
5教科スコア表作成プログラム
参加者一人ひとりの5教科の平均点、最高点、最低点を算出して表形式で表示します。
"""

import csv
import os
from collections import defaultdict


def load_scores_from_csv(filename):
    """
    CSVファイルからスコアデータを読み込む関数
    
    Args:
        filename: CSVファイル名
    
    Returns:
        dict: {参加者名: [スコアのリスト]} の形式
    """
    scores = defaultdict(list)
    
    try:
        with open(filename, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            
            # ヘッダー行を取得
            headers = reader.fieldnames
            if not headers:
                print("エラー: CSVファイルにヘッダーが見つかりません。")
                return {}
            
            # 参加者名の列を特定（最初の列を参加者名と仮定）
            name_column = headers[0]
            
            # スコア列を特定（数値列を探す）
            score_columns = []
            for header in headers[1:]:
                score_columns.append(header)
            
            # データを読み込む
            for row in reader:
                player_name = row[name_column].strip()
                if not player_name:
                    continue
                
                # 各スコアを取得
                for column in score_columns:
                    try:
                        score = float(row[column].strip())
                        scores[player_name].append(score)
                    except (ValueError, KeyError):
                        # スコアが無効な場合はスキップ
                        continue
    
    except FileNotFoundError:
        print(f"エラー: ファイル '{filename}' が見つかりません。")
        return {}
    except Exception as e:
        print(f"エラー: ファイルの読み込み中に問題が発生しました: {e}")
        return {}
    
    return scores


def calculate_statistics(scores_list):
    """
    スコアのリストから統計情報を計算する関数
    
    Args:
        scores_list: スコアのリスト
    
    Returns:
        dict: 統計情報（平均、最低点、最高点、スコア数）
    """
    if not scores_list:
        return None
    
    return {
        'average': sum(scores_list) / len(scores_list),
        'min': min(scores_list),
        'max': max(scores_list),
        'count': len(scores_list),
        'total': sum(scores_list)
    }


def display_scoreboard(scores):
    """
    5教科スコア表を表示する関数
    各参加者の5教科の平均点、最高点、最低点を表形式で表示します。
    
    Args:
        scores: {参加者名: [スコアのリスト]} の形式の辞書
    """
    if not scores:
        print("\n" + "=" * 50)
        print("5教科スコア表")
        print("=" * 50)
        print("スコアデータがありません。")
        print("=" * 50)
        return
    
    print("\n" + "=" * 100)
    print("5教科スコア表".center(100))
    print("=" * 100)
    print(f"{'参加者名':<20} {'平均点':<20} {'最低点':<20} {'最高点':<20} {'科目数':<15}")
    print("-" * 100)
    
    # 各参加者のスコアを計算して表示
    for player_name, scores_list in sorted(scores.items()):
        stats = calculate_statistics(scores_list)
        if stats:
            print(f"{player_name:<20} {stats['average']:<20.2f} {stats['min']:<20.2f} {stats['max']:<20.2f} {stats['count']:<15}")
    
    print("=" * 100)


def save_scoreboard_to_csv(scores, output_filename):
    """
    スコア表をCSVファイルに保存する関数
    
    Args:
        scores: {参加者名: [スコアのリスト]} の形式の辞書
        output_filename: 保存するファイル名
    """
    if not scores:
        print("\nスコアデータがありません。")
        return False
    
    try:
        with open(output_filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['参加者名', '平均点', '最低点', '最高点', 'スコア数', '合計点']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            # 各参加者のスコアを書き込む
            for player_name, scores_list in sorted(scores.items()):
                stats = calculate_statistics(scores_list)
                if stats:
                    writer.writerow({
                        '参加者名': player_name,
                        '平均点': f"{stats['average']:.2f}",
                        '最低点': f"{stats['min']:.2f}",
                        '最高点': f"{stats['max']:.2f}",
                        'スコア数': stats['count'],
                        '合計点': f"{stats['total']:.2f}"
                    })
        
        print(f"\nスコア表を '{output_filename}' に保存しました。")
        return True
        
    except Exception as e:
        print(f"\nファイルの保存中にエラーが発生しました: {e}")
        return False


def main():
    """メイン関数"""
    print("=" * 50)
    print("5教科スコア表作成プログラム")
    print("=" * 50)
    print("参加者一人ひとりの5教科の平均点、最高点、最低点を算出します。")
    
    while True:
        print("\nメニュー:")
        print("1. CSVファイルからスコア表を表示")
        print("2. CSVファイルからスコア表を作成して保存")
        print("3. 終了")
        
        try:
            choice = input("\n選択してください (1-3): ").strip()
            
            # デバッグ用（入力値を確認）
            if choice and choice not in ["1", "2", "3"]:
                print(f"入力された値: '{choice}' (長さ: {len(choice)})")
            
            if choice == "1":
                filename = input("\nCSVファイル名を入力してください: ").strip()
                if not filename:
                    print("ファイル名を入力してください。")
                    continue
                
                scores = load_scores_from_csv(filename)
                if scores:
                    display_scoreboard(scores)
                
            elif choice == "2":
                input_filename = input("\n読み込むCSVファイル名を入力してください: ").strip()
                if not input_filename:
                    print("ファイル名を入力してください。")
                    continue
                
                output_filename = input("保存するCSVファイル名を入力してください（Enterで自動生成）: ").strip()
                if not output_filename:
                    output_filename = "scoreboard_result.csv"
                elif not output_filename.endswith('.csv'):
                    output_filename += '.csv'
                
                scores = load_scores_from_csv(input_filename)
                if scores:
                    display_scoreboard(scores)
                    save_scoreboard_to_csv(scores, output_filename)
                
            elif choice == "3":
                print("\nプログラムを終了します。")
                break
                
            else:
                print("1から3の数字を入力してください。")
                
        except KeyboardInterrupt:
            print("\n\nプログラムを終了します。")
            break
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")


if __name__ == "__main__":
    main()

