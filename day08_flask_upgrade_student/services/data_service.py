import pandas as pd
from pathlib import Path
from typing import List, Dict, Any

# ✅ 自动定位 data 目录
BASE_DIR = Path(__file__).resolve().parent.parent / "data"

def load_metric_api_data() -> List[Dict[str, Any]]:
    file_path = BASE_DIR / "overall_metrics.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"找不到文件: {file_path}")

    df = pd.read_csv(file_path)
    return df.to_dict(orient="records")

def load_category_api_data(selected_category: str = "全部") -> List[Dict[str, Any]]:
    file_path = BASE_DIR / "category_analysis.csv"
    if not file_path.exists():
        raise FileNotFoundError(f"找不到文件: {file_path}")

    df = pd.read_csv(file_path)

    # ✅ 统一列名为中文（防止 CSV 是英文列名）
    df = df.rename(columns={
        "PreferedOrderCat": "偏好品类",
        "用户数": "用户数",
        "流失率": "流失率",
        "平均订单数": "平均订单数"
    })

    if selected_category != "全部":
        df = df[df["偏好品类"] == selected_category]

    return df.to_dict(orient="records")