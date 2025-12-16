#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数当てゲーム
コンピュータが1〜100までの数字をランダムに選び、ユーザーがその数字を当てるゲームです。
スコア表機能付き：参加者ごとの平均、最低点、最高点を算出します。
"""

import random
import csv
import os
from datetime import datetime


# スコア管理用の辞書（参加者名: [試行回数のリスト]）
scores = {}


def play_game(player_name):
    """
    数当てゲームをプレイする関数
    
    Args:
        player_name: 参加者名
    
    Returns:
        int: 試行回数（ゲームが中断された場合はNone）
    """
    print("=" * 50)
    print(f"{player_name}さんの番です！")
    print("=" * 50)
    print("コンピュータが1から100までの数を選びました。")
    print("その数を当ててください！")
    print("-" * 50)
    
    # 1〜100のランダムな数を生成
    target_number = random.randint(1, 100)
    attempts = 0
    
    # ゲームループ
    while True:
        try:
            # ユーザーからの入力を受け取る
            guess = input("\n数を入力してください (1-100): ")
            guess = int(guess.strip())
            
            # 入力値の範囲チェック
            if guess < 1 or guess > 100:
                print("1から100までの数を入力してください。")
                continue
            
            attempts += 1
            
            # 推測値と正解を比較
            if guess == target_number:
                print(f"\n🎉 正解です！")
                print(f"答えは {target_number} でした。")
                print(f"試行回数: {attempts} 回")
                return attempts
            elif guess > target_number:
                print("もっと小さい")
            else:
                print("もっと大きい")
                
        except ValueError:
            print("有効な数値を入力してください。")
        except KeyboardInterrupt:
            print("\n\nゲームを中断しました。")
            return None


def calculate_statistics(attempts_list):
    """
    試行回数のリストから統計情報を計算する関数
    
    Args:
        attempts_list: 試行回数のリスト
    
    Returns:
        dict: 統計情報（平均、最低点、最高点、プレイ回数）
    """
    if not attempts_list:
        return None
    
    return {
        'average': sum(attempts_list) / len(attempts_list),
        'min': min(attempts_list),
        'max': max(attempts_list),
        'count': len(attempts_list),
        'total': sum(attempts_list)
    }


def display_scoreboard():
    """
    スコア表を表示する関数
    各参加者の平均、最低点、最高点を表示します。
    """
    if not scores:
        print("\n" + "=" * 50)
        print("スコア表")
        print("=" * 50)
        print("まだスコアが記録されていません。")
        print("=" * 50)
        return
    
    print("\n" + "=" * 90)
    print("スコア表".center(90))
    print("=" * 90)
    print(f"{'参加者名':<20} {'平均試行回数':<18} {'最低試行回数':<18} {'最高試行回数':<18} {'プレイ回数':<12}")
    print("-" * 90)
    
    # 各参加者のスコアを計算して表示
    for player_name, attempts_list in sorted(scores.items()):
        stats = calculate_statistics(attempts_list)
        if stats:
            print(f"{player_name:<20} {stats['average']:<18.2f} {stats['min']:<18} {stats['max']:<18} {stats['count']:<12}")
    
    print("=" * 90)


def save_scoreboard_to_csv(filename=None):
    """
    スコア表をCSVファイルに保存する関数
    
    Args:
        filename: 保存するファイル名（指定しない場合は自動生成）
    
    Returns:
        str: 保存したファイル名
    """
    if not scores:
        print("\nスコアが記録されていないため、ファイルに保存できません。")
        return None
    
    # ファイル名が指定されていない場合は自動生成
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"scoreboard_{timestamp}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['参加者名', '平均試行回数', '最低試行回数', '最高試行回数', 'プレイ回数', '合計試行回数']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            
            # 各参加者のスコアを書き込む
            for player_name, attempts_list in sorted(scores.items()):
                stats = calculate_statistics(attempts_list)
                if stats:
                    writer.writerow({
                        '参加者名': player_name,
                        '平均試行回数': f"{stats['average']:.2f}",
                        '最低試行回数': stats['min'],
                        '最高試行回数': stats['max'],
                        'プレイ回数': stats['count'],
                        '合計試行回数': stats['total']
                    })
        
        print(f"\nスコア表を '{filename}' に保存しました。")
        return filename
        
    except Exception as e:
        print(f"\nファイルの保存中にエラーが発生しました: {e}")
        return None


def main():
    """メイン関数"""
    print("=" * 50)
    print("数当てゲームへようこそ！")
    print("=" * 50)
    
    while True:
        print("\nメニュー:")
        print("1. ゲームをプレイ")
        print("2. スコア表を表示")
        print("3. スコア表をCSVファイルに保存")
        print("4. 終了")
        
        try:
            choice = input("\n選択してください (1-4): ").strip()
            
            if choice == "1":
                # 参加者名を入力
                player_name = input("\n参加者名を入力してください: ").strip()
                if not player_name:
                    print("参加者名を入力してください。")
                    continue
                
                # ゲームをプレイ
                attempts = play_game(player_name)
                
                # スコアを記録（ゲームが完了した場合のみ）
                if attempts is not None:
                    if player_name not in scores:
                        scores[player_name] = []
                    scores[player_name].append(attempts)
                    print(f"\n{player_name}さんのスコアを記録しました。")
                
            elif choice == "2":
                display_scoreboard()
                
            elif choice == "3":
                # CSVファイルに保存するか確認
                custom_filename = input("\nファイル名を入力してください（Enterで自動生成）: ").strip()
                if custom_filename:
                    if not custom_filename.endswith('.csv'):
                        custom_filename += '.csv'
                    save_scoreboard_to_csv(custom_filename)
                else:
                    save_scoreboard_to_csv()
                
            elif choice == "4":
                print("\nゲームを終了します。お疲れ様でした！")
                break
                
            else:
                print("1から4の数字を入力してください。")
                
        except KeyboardInterrupt:
            print("\n\nゲームを終了します。")
            break
        except Exception as e:
            print(f"\nエラーが発生しました: {e}")


if __name__ == "__main__":
    main()
