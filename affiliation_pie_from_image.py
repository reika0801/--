"""
Pie chart for affiliation counts derived from 課題3 image.
No CSV needed; counts are hard-coded based on the provided table.
日本語フォントを指定して、日本語ラベルが正しく表示されるようにします。
"""

from matplotlib import pyplot as plt
from matplotlib import font_manager, rcParams

# Counts read from the provided 課題3 table image
counts = {
    "営業": 10,
    "開発": 10,
    "管理": 8,
    "人事": 7,
}


def set_japanese_font():
    """
    Mac向けに日本語フォントを設定します。
    環境に応じて使えるものから順に選択します。
    """
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
            # 実際にフォントが解決できるかチェック
            font_manager.findfont(font)
            rcParams["font.family"] = name
            # マイナス記号が豆腐にならないようにする
            rcParams["axes.unicode_minus"] = False
            return
        except Exception:
            continue


if __name__ == "__main__":
    set_japanese_font()

    plt.figure(figsize=(6, 6))
    plt.title("所属ごとの参加者数（課題3画像より）")
    plt.pie(
        counts.values(),
        labels=counts.keys(),
        autopct="%1.1f%%",
        startangle=90,
        counterclock=False,
    )
    plt.tight_layout()
    out_path = "affiliation_pie_from_image.png"
    plt.savefig(out_path, dpi=150)
    print(f"saved: {out_path}")

