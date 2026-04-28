#!/usr/bin/env python3
"""
stats.py — 跨天统计分析

分析指定日期范围内的对话日志，输出场景分布趋势、对话量趋势、
经验增长曲线、完成率统计等。

用法:
  python stats.py PROJECT_ROOT
  python stats.py PROJECT_ROOT --from 2026-04-21 --to 2026-04-28
"""

import sys
import os
import json
import argparse
from datetime import datetime, timedelta
from collections import Counter

# 复用 report.py 的解析能力
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from report import parse_log_file, parse_report_file, CATEGORIES


def collect_range_data(project_root: str, start_date: str, end_date: str) -> dict:
    """收集日期范围内的所有数据。"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    daily_records = []
    all_conversations = []
    total_experience = 0

    current = start
    while current <= end:
        day_str = current.strftime("%Y-%m-%d")
        log_path = os.path.join(project_root, "conversation-logs", f"{day_str}.md")
        convs = parse_log_file(log_path)

        # 经验卡片统计
        report_path = os.path.join(
            project_root, "conversation-logs", "reports", f"{day_str}-report.md"
        )
        report_data = parse_report_file(report_path)
        exp_count = len(report_data.get("experience_cards", []))
        total_experience += exp_count

        # 场景分布
        cat_counter = Counter(c["category"] for c in convs if c["category"])
        status_counter = Counter(c["status"] for c in convs)

        # 时段分布
        hour_counter = Counter()
        for c in convs:
            try:
                hour = int(c["time"].split(":")[0])
                hour_counter[hour] += 1
            except (ValueError, IndexError):
                pass

        daily_records.append({
            "date": day_str,
            "total": len(convs),
            "categories": dict(cat_counter),
            "statuses": dict(status_counter),
            "hours": dict(hour_counter),
            "experience_count": exp_count,
        })

        all_conversations.extend(convs)
        current += timedelta(days=1)

    return {
        "daily_records": daily_records,
        "all_conversations": all_conversations,
        "total_experience": total_experience,
    }


def compute_statistics(project_root: str, start_date: str, end_date: str) -> dict:
    """计算完整统计数据。"""
    data = collect_range_data(project_root, start_date, end_date)
    daily_records = data["daily_records"]
    all_convs = data["all_conversations"]
    total = len(all_convs)

    # === 基础统计 ===
    active_days = sum(1 for d in daily_records if d["total"] > 0)
    total_days = len(daily_records)

    # === 场景分布 ===
    cat_counter = Counter(c["category"] for c in all_convs if c["category"])
    category_stats = []
    for cat in CATEGORIES:
        count = cat_counter.get(cat, 0)
        pct = round(count / total * 100, 1) if total > 0 else 0
        category_stats.append({"category": cat, "count": count, "percentage": pct})

    # === 对话量趋势（每日） ===
    volume_trend = [
        {"date": d["date"], "count": d["total"]}
        for d in daily_records
    ]

    # === 场景分布趋势（每日各分类占比） ===
    category_trend = []
    for d in daily_records:
        day_total = d["total"]
        day_cats = {}
        for cat in CATEGORIES:
            count = d["categories"].get(cat, 0)
            day_cats[cat] = count
        category_trend.append({"date": d["date"], "total": day_total, **day_cats})

    # === 完成率统计 ===
    status_counter = Counter(c["status"] for c in all_convs)
    normal = status_counter.get("normal", 0)
    terminated = status_counter.get("terminated", 0)
    interrupted = status_counter.get("interrupted", 0)

    # === 时段分布 ===
    hour_counter = Counter()
    for d in daily_records:
        for hour_str, count in d["hours"].items():
            hour_counter[int(hour_str)] += count

    peak_hours = hour_counter.most_common(3)
    time_distribution = {
        "morning_6_12": sum(hour_counter.get(h, 0) for h in range(6, 12)),
        "afternoon_12_18": sum(hour_counter.get(h, 0) for h in range(12, 18)),
        "evening_18_24": sum(hour_counter.get(h, 0) for h in range(18, 24)),
        "night_0_6": sum(hour_counter.get(h, 0) for h in range(0, 6)),
        "peak_hours": [{"hour": h, "count": c} for h, c in peak_hours],
    }

    # === 经验增长曲线 ===
    exp_cumulative = 0
    experience_trend = []
    for d in daily_records:
        exp_cumulative += d["experience_count"]
        experience_trend.append({
            "date": d["date"],
            "daily_new": d["experience_count"],
            "cumulative": exp_cumulative,
        })

    return {
        "period": {"from": start_date, "to": end_date},
        "summary": {
            "total_conversations": total,
            "total_days": total_days,
            "active_days": active_days,
            "avg_per_active_day": round(total / active_days, 1) if active_days > 0 else 0,
            "total_experience": data["total_experience"],
            "completion_rate": round(normal / total * 100, 1) if total > 0 else 100,
            "termination_rate": round(terminated / total * 100, 1) if total > 0 else 0,
            "interruption_rate": round(interrupted / total * 100, 1) if total > 0 else 0,
        },
        "category_stats": category_stats,
        "volume_trend": volume_trend,
        "category_trend": category_trend,
        "time_distribution": time_distribution,
        "experience_trend": experience_trend,
    }


def main():
    parser = argparse.ArgumentParser(description="跨天统计分析")
    parser.add_argument("project_root", help="项目根目录")
    parser.add_argument("--from", dest="from_date", default=None, help="起始日期 YYYY-MM-DD")
    parser.add_argument("--to", dest="to_date", default=None, help="结束日期 YYYY-MM-DD")
    args = parser.parse_args()

    today = datetime.now().strftime("%Y-%m-%d")
    end_date = args.to_date or today

    if args.from_date:
        start_date = args.from_date
    else:
        # 默认最近 7 天
        start = datetime.strptime(end_date, "%Y-%m-%d") - timedelta(days=6)
        start_date = start.strftime("%Y-%m-%d")

    result = compute_statistics(args.project_root, start_date, end_date)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
