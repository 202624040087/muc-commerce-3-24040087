from pathlib import Path
import pandas as pd

def answer_question(base_dir: Path, question: str) -> str:
    data_dir = base_dir / "data"
    
    # 加载数据
    metrics_df = pd.read_csv(data_dir / "overall_metrics.csv", encoding="utf-8-sig")
    metrics = dict(zip(metrics_df["指标"], metrics_df["数值"]))
    
    category_df = pd.read_csv(data_dir / "category_analysis.csv", encoding="utf-8-sig")
    segment_df = pd.read_csv(data_dir / "segment_analysis.csv", encoding="utf-8-sig")
    
    normalized = question.replace(" ", "").lower()

    # 1. 总体规模 - 用户数
    if any(word in normalized for word in ["多少用户", "用户数", "总用户"]):
        return f"数据集中共有 {int(metrics['用户数']):,} 名用户。"
    
    # 2. 流失情况 - 流失率
    if any(word in normalized for word in ["流失率", "流失人数", "流失情况", "流失多少"]):
        return f"总体流失率为 {metrics['流失率']:.1%}，共有 {int(metrics['流失人数']):,} 名流失用户。"
    
    # 3. 偏好品类 - 用户最多的品类
    if any(word in normalized for word in ["哪个品类", "最多用户", "品类最多", "偏好品类"]):
        max_category = category_df.loc[category_df['用户数'].idxmax()]
        return f"用户最多的品类是 '{max_category['PreferedOrderCat']}'，共有 {int(max_category['用户数']):,} 名用户。"
    
    # 4. 生命周期风险 - 流失率最高的阶段
    if any(word in normalized for word in ["哪个阶段", "风险最高", "生命周期", "阶段流失"]):
        max_segment = segment_df.loc[segment_df['流失率'].idxmax()]
        return f"流失率最高的生命周期阶段是 '{max_segment['TenureGroup']}'，流失率达到 {max_segment['流失率']:.1%}。"
    
    # 5. 订单情况 - 平均订单数
    if any(word in normalized for word in ["平均订单", "订单数", "订单多少"]):
        return f"用户的平均订单数为 {metrics['平均订单数']:.2f} 单。"
    
    # 6. 不支持的问题 - 友好提示
    return (
        "抱歉，我暂时只能回答以下类型的问题：\\n"
        "1. 系统中有多少用户？\\n"
        "2. 总体流失率是多少？\\n"
        "3. 哪个品类用户最多？\\n"
        "4. 哪个生命周期阶段风险最高？\\n"
        "5. 平均订单数是多少？\\n"
        "请换一种更具体的问法。"
    )