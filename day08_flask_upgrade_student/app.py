from flask import Flask, jsonify, request, abort
from services.data_service import load_metric_api_data, load_category_api_data

app = Flask(__name__)

# ============================================================
# 模拟登录校验（教学/实验环境专用）
# 实际项目应使用 session / JWT
# ============================================================
def is_logged_in():
    return request.headers.get("X-User-Login") == "true"

# ===============================
# 1. 健康检查接口
# ===============================
@app.route("/health")
def health():
    return jsonify({"ok": True, "message": "Task Upgrade Student API is running"})

# ===============================
# 2. 指标接口（需登录）
# ===============================
@app.route("/api/metrics")
def api_metrics():
    # ✅ 未登录 → 401（解决 test_unauthorized_access_metrics）
    if not is_logged_in():
        abort(401, description="Unauthorized")

    data = load_metric_api_data()
    return jsonify(data)

# ===============================
# 3. 分类接口（含字段兼容处理）
# ===============================
@app.route("/api/categories")
def api_categories():
    if not is_logged_in():
        abort(401, description="Unauthorized")

    category = request.args.get("category", "全部")
    data = load_category_api_data(category)

    # ✅ 防御性修复：确保存在“偏好品类”（解决 KeyError）
    if data and "偏好品类" not in data[0]:
        if "PreferedOrderCat" in data[0]:
            for row in data:
                row["偏好品类"] = row.pop("PreferedOrderCat")

    return jsonify(data)

# ===============================
# 启动入口
# ===============================
if __name__ == "__main__":
    app.run(debug=True)