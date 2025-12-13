#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
数当てゲーム
コンピュータが1〜100までの数字をランダムに選び、ユーザーがその数字を当てるゲームです。
"""

import random


def main():
    """メイン関数"""
    print("=" * 50)
    print("数当てゲームへようこそ！")
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
                break
            elif guess > target_number:
                print("もっと小さい")
            else:
                print("もっと大きい")
                
        except ValueError:
            print("有効な数値を入力してください。")
        except KeyboardInterrupt:
            print("\n\nゲームを終了します。")
            break


if __name__ == "__main__":
    main()
