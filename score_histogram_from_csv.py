"""
課題3.csvのスコアからヒストグラム（度数分布）を作成するスクリプト。

区分:
- 90点以上
- 89〜80点
- 79〜70点
"""

import csv
from pathlib import Path

from matplotlib import pyplot as plt
from matplotlib import font_manager, rcParams


def set_japanese_font() -> None:
    """Mac向けに日本語フォントを設定します。"""
    candidates = [
        "Hiragino Sans",
        "Hiragino Kaku Gothic ProN",
        "YuGothic",
        "Yu Gothic",
        "Osaka",
    ]

    for name in candidates:
        try:
            font = font_manager.FontProperties(family=name)
            font_manager.findfont(font)
            rcParams["font.family"] = name
            rcParams["axes.unicode_minus"] = False
            return
        except Exception:
            continue


def load_scores(csv_path: Path):
    """CSVからスコアだけのリストを取得する。"""
    scores = []
    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # ヘッダー: 名前,所属,スコア
        for row in reader:
            if not row or len(row) < 3:
                continue
            try:
                score = float(row[2])
            except ValueError:
                continue
            scores.append(score)
    return scores


def main():
    set_japanese_font()

    base_dir = Path(__file__).resolve().parent
    csv_path = base_dir / "課題3.csv"
    scores = load_scores(csv_path)

    # 手動で3区分に分ける
    bins_labels = ["90点以上", "89〜80点", "79〜70点"]
    counts = [0, 0, 0]
    for s in scores:
        if s >= 90:
            counts[0] += 1
        elif 80 <= s <= 89:
            counts[1] += 1
        elif 70 <= s <= 79:
            counts[2] += 1

    plt.figure(figsize=(6, 4))
    bars = plt.bar(bins_labels, counts, color="lightgreen")
    plt.xlabel("スコア区分")
    plt.ylabel("人数")
    plt.title("スコアの度数分布（課題3）")

    # 棒の上に人数を表示
    for bar, c in zip(bars, counts):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 0.2,
            f"{c}人",
            ha="center",
            va="bottom",
        )

    plt.ylim(0, max(counts) + 2)
    plt.tight_layout()

    out_path = base_dir / "score_histogram_from_csv.png"
    plt.savefig(out_path, dpi=150)
    print(f"saved: {out_path}")


if __name__ == "__main__":
    main()


