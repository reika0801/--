"""
所属ごとの平均スコアを棒グラフで表示するスクリプト。

前提:
- 同じフォルダに「課題3.csv」があり、列構成が「名前,所属,スコア」
- このスクリプトを /Users/reika/Desktop/課題/ に置いて実行する
"""

import csv
import sys
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


def load_department_scores(csv_path: Path):
    """CSVから所属ごとの合計・件数・最高点・最低点を集計する。"""
    dept_sum = {}
    dept_count = {}
    dept_max = {}
    dept_min = {}

    with csv_path.open(encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f)
        header = next(reader, None)  # ヘッダー行: 名前,所属,スコア
        for row in reader:
            if not row or len(row) < 3:
                continue
            dept = row[1].strip()
            try:
                score = float(row[2])
            except ValueError:
                continue
            dept_sum[dept] = dept_sum.get(dept, 0.0) + score
            dept_count[dept] = dept_count.get(dept, 0) + 1
            dept_max[dept] = max(dept_max.get(dept, score), score)
            dept_min[dept] = min(dept_min.get(dept, score), score)

    departments = sorted(dept_sum.keys())
    averages = [dept_sum[d] / dept_count[d] for d in departments]
    max_scores = [dept_max[d] for d in departments]
    min_scores = [dept_min[d] for d in departments]
    return departments, averages, max_scores, min_scores


def main():
    set_japanese_font()

    # 引数でCSVパスを指定できるようにし、なければ課題3.csvを使う
    if len(sys.argv) > 1:
        csv_name = sys.argv[1]
    else:
        csv_name = "課題3.csv"

    csv_path = Path(csv_name)
    if not csv_path.is_absolute():
        csv_path = Path(__file__).resolve().parent / csv_path

    departments, averages, max_scores, min_scores = load_department_scores(csv_path)

    plt.figure(figsize=(6, 4))
    bars = plt.bar(departments, averages, color="skyblue")
    plt.xlabel("所属")
    plt.ylabel("平均スコア")
    plt.title("所属ごとの平均スコア（課題3）")
    plt.ylim(0, 100)

    # 棒の上に平均・最高・最低スコアを表示
    for bar, avg, max_s, min_s in zip(bars, averages, max_scores, min_scores):
        height = bar.get_height()
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height + 1,  # 少し上に表示
            f"{avg:.1f}\n(最:{max_s:.0f} 最低:{min_s:.0f})",
            ha="center",
            va="bottom",
        )

    plt.tight_layout()

    out_path = Path(__file__).resolve().parent / "affiliation_bar_from_csv.png"
    plt.savefig(out_path, dpi=150)
    print(f"saved: {out_path}")


if __name__ == "__main__":
    main()


