#!/usr/bin/env python3
"""
report.py — 对话日志解析与报告数据生成

解析 conversation-logs/ 下的 Markdown 日志文件，提取结构化数据，
输出 JSON 供 AI 填充报告模板。

用法:
  python report.py PROJECT_ROOT --type daily [--date YYYY-MM-DD]
  python report.py PROJECT_ROOT --type weekly [--date YYYY-MM-DD]
  python report.py PROJECT_ROOT --type monthly [--date YYYY-MM-DD]
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter


CATEGORIES = [
    "快速代码生成与复用",
    "代码纠错与实时调试排障",
    "代码优化与规范整改",
    "学习赋能与技术落地",
    "辅助文档与注释产出",
]


def parse_log_file(filepath: str) -> list[dict]:
    """解析单个日志 Markdown 文件，返回对话记录列表。"""
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    conversations = []
    # 匹配对话块: ## [HH:MM] 对话 #N 或含 ⚠️ 标记
    pattern = r"## \[(\d{2}:\d{2})\] 对话 #(\d+)(.*?)(?=\n## \[|\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    for time_str, num, body in matches:
        conv = {
            "number": int(num),
            "time": time_str,
            "status": "normal",
            "category": "",
            "user_input": "",
            "ai_summary": [],
        }

        # 检查状态标记
        if "⚠️ 用户终止" in body:
            conv["status"] = "terminated"
        elif "⚠️ 异常中断" in body:
            conv["status"] = "interrupted"

        # 提取场景分类
        cat_match = re.search(r"### 场景分类\s*\n`([^`]+)`", body)
        if cat_match:
            conv["category"] = cat_match.group(1)

        # 提取用户输入
        input_match = re.search(r"### 用户输入\s*\n((?:>.*\n?)+)", body)
        if input_match:
            lines = input_match.group(1).strip().split("\n")
            conv["user_input"] = "\n".join(
                line.lstrip("> ").rstrip() for line in lines
            )

        # 提取 AI 摘要
        summary_match = re.search(r"### AI 反馈摘要[^\n]*\n((?:- .*\n?)+)", body)
        if summary_match:
            conv["ai_summary"] = [
                line.lstrip("- ").strip()
                for line in summary_match.group(1).strip().split("\n")
                if line.strip().startswith("-")
            ]

        conversations.append(conv)

    return conversations


def parse_report_file(filepath: str) -> dict:
    """解析日报文件，提取经验卡片。"""
    if not os.path.exists(filepath):
        return {"experience_cards": []}

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    cards = []
    pattern = r"### (EXP-\d{8}-\d{2})：(.+?)\n(.*?)(?=\n### EXP-|\n## |\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    for exp_id, title, body in matches:
        card = {"id": exp_id, "title": title.strip(), "body": body.strip()}

        type_match = re.search(r"\*\*类型\*\*：`([^`]+)`", body)
        if type_match:
            card["type"] = type_match.group(1)

        cat_match = re.search(r"\*\*场景分类\*\*：(.+)", body)
        if cat_match:
            card["category"] = cat_match.group(1).strip()

        cards.append(card)

    return {"experience_cards": cards}


def generate_daily_data(project_root: str, date_str: str) -> dict:
    """生成日报所需的结构化数据。"""
    log_path = os.path.join(project_root, "conversation-logs", f"{date_str}.md")
    conversations = parse_log_file(log_path)

    if not conversations:
        return {"error": f"No conversations found for {date_str}"}

    # 场景分布统计
    cat_counter = Counter(c["category"] for c in conversations if c["category"])
    total = len(conversations)

    category_stats = []
    for cat in CATEGORIES:
        count = cat_counter.get(cat, 0)
        pct = round(count / total * 100) if total > 0 else 0
        category_stats.append({"category": cat, "count": count, "percentage": pct})

    # 状态统计
    status_counter = Counter(c["status"] for c in conversations)

    return {
        "date": date_str,
        "total_conversations": total,
        "category_stats": category_stats,
        "status_stats": {
            "normal": status_counter.get("normal", 0),
            "terminated": status_counter.get("terminated", 0),
            "interrupted": status_counter.get("interrupted", 0),
        },
        "conversations": [
            {
                "number": c["number"],
                "time": c["time"],
                "category": c["category"],
                "status": c["status"],
                "user_input_preview": c["user_input"][:50] + ("..." if len(c["user_input"]) > 50 else ""),
                "ai_summary_count": len(c["ai_summary"]),
            }
            for c in conversations
        ],
    }


def generate_weekly_data(project_root: str, date_str: str) -> dict:
    """生成周报所需的结构化数据。"""
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    # 找到本周一
    monday = target_date - timedelta(days=target_date.weekday())

    daily_data = []
    all_conversations = []
    total_experience = 0

    for i in range(7):
        day = monday + timedelta(days=i)
        if day > target_date:
            break
        day_str = day.strftime("%Y-%m-%d")
        log_path = os.path.join(project_root, "conversation-logs", f"{day_str}.md")
        convs = parse_log_file(log_path)

        # 检查日报经验卡片
        report_path = os.path.join(
            project_root, "conversation-logs", "reports", f"{day_str}-report.md"
        )
        report_data = parse_report_file(report_path)
        exp_count = len(report_data.get("experience_cards", []))
        total_experience += exp_count

        daily_data.append({
            "date": day_str,
            "conversation_count": len(convs),
            "experience_count": exp_count,
        })
        all_conversations.extend(convs)

    # 汇总场景分布
    cat_counter = Counter(c["category"] for c in all_conversations if c["category"])
    total = len(all_conversations)
    active_days = sum(1 for d in daily_data if d["conversation_count"] > 0)

    category_stats = []
    for cat in CATEGORIES:
        count = cat_counter.get(cat, 0)
        pct = round(count / total * 100) if total > 0 else 0
        category_stats.append({"category": cat, "count": count, "percentage": pct})

    # 状态统计
    status_counter = Counter(c["status"] for c in all_conversations)
    normal = status_counter.get("normal", 0)
    terminated = status_counter.get("terminated", 0)
    interrupted = status_counter.get("interrupted", 0)

    iso_cal = target_date.isocalendar()

    return {
        "year": iso_cal[0],
        "week_number": iso_cal[1],
        "start_date": monday.strftime("%Y-%m-%d"),
        "end_date": target_date.strftime("%Y-%m-%d"),
        "total_conversations": total,
        "active_days": active_days,
        "avg_per_day": round(total / active_days, 1) if active_days > 0 else 0,
        "total_experience": total_experience,
        "category_stats": category_stats,
        "daily_data": daily_data,
        "status_stats": {
            "normal": normal,
            "terminated": terminated,
            "interrupted": interrupted,
        },
        "completion_rate": round(normal / total * 100, 1) if total > 0 else 100,
    }


def generate_monthly_data(project_root: str, date_str: str) -> dict:
    """生成月报所需的结构化数据。"""
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    year, month = target_date.year, target_date.month
    first_day = datetime(year, month, 1)

    # 遍历当月每一天
    weekly_buckets = {}
    all_conversations = []
    total_experience = 0

    day = first_day
    while day.month == month and day <= target_date:
        day_str = day.strftime("%Y-%m-%d")
        log_path = os.path.join(project_root, "conversation-logs", f"{day_str}.md")
        convs = parse_log_file(log_path)
        all_conversations.extend(convs)

        # 按周分桶
        week_key = f"W{day.isocalendar()[1]}"
        if week_key not in weekly_buckets:
            weekly_buckets[week_key] = {"conversations": 0, "experience": 0}
        weekly_buckets[week_key]["conversations"] += len(convs)

        # 检查日报经验
        report_path = os.path.join(
            project_root, "conversation-logs", "reports", f"{day_str}-report.md"
        )
        report_data = parse_report_file(report_path)
        exp_count = len(report_data.get("experience_cards", []))
        weekly_buckets[week_key]["experience"] += exp_count
        total_experience += exp_count

        day += timedelta(days=1)

    total = len(all_conversations)
    cat_counter = Counter(c["category"] for c in all_conversations if c["category"])

    category_stats = []
    for cat in CATEGORIES:
        count = cat_counter.get(cat, 0)
        pct = round(count / total * 100) if total > 0 else 0
        category_stats.append({"category": cat, "count": count, "percentage": pct})

    return {
        "year": year,
        "month": month,
        "total_conversations": total,
        "total_experience": total_experience,
        "category_stats": category_stats,
        "weekly_breakdown": weekly_buckets,
    }


def main():
    parser = argparse.ArgumentParser(description="对话日志报告数据生成")
    parser.add_argument("project_root", help="项目根目录")
    parser.add_argument("--type", choices=["daily", "weekly", "monthly"], default="daily")
    parser.add_argument("--date", default=None, help="目标日期 YYYY-MM-DD，默认今天")
    args = parser.parse_args()

    date_str = args.date or datetime.now().strftime("%Y-%m-%d")

    if args.type == "daily":
        result = generate_daily_data(args.project_root, date_str)
    elif args.type == "weekly":
        result = generate_weekly_data(args.project_root, date_str)
    elif args.type == "monthly":
        result = generate_monthly_data(args.project_root, date_str)

    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
