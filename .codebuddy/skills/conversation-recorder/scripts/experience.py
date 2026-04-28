#!/usr/bin/env python3
"""
experience.py — 经验手册管理工具

搜索、统计、去重检查经验手册中的条目。

用法:
  python experience.py PROJECT_ROOT search --keyword "关键词"
  python experience.py PROJECT_ROOT stats
  python experience.py PROJECT_ROOT dedup
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from collections import Counter


HANDBOOK_FILENAME = "experience-handbook.md"


def get_handbook_path(project_root: str) -> str:
    return os.path.join(project_root, "conversation-logs", HANDBOOK_FILENAME)


def parse_handbook(filepath: str) -> list[dict]:
    """解析经验手册，返回所有经验条目。"""
    if not os.path.exists(filepath):
        return []

    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    entries = []
    # 匹配 **EXP-NNN**：标题 [★...] 格式
    pattern = r"\*\*(EXP-\d{3,})\*\*：(.+?)(?:\[([★☆]+)\])?\s*(?:\[来源: ([^\]]+)\])?\s*\n\s*(.+?)(?=\n- \*\*EXP-|\n### |\n## |\Z)"
    matches = re.findall(pattern, content, re.DOTALL)

    for exp_id, title, stars, source, body in matches:
        entries.append({
            "id": exp_id,
            "title": title.strip(),
            "stars": stars.strip() if stars else "",
            "source": source.strip() if source else "",
            "content": body.strip(),
        })

    # 也尝试匹配 ### EXP-YYYYMMDD-NN 格式（日报卡片格式）
    pattern2 = r"### (EXP-\d{8}-\d{2})：(.+?)\n(.*?)(?=\n### EXP-|\n## |\Z)"
    matches2 = re.findall(pattern2, content, re.DOTALL)

    for exp_id, title, body in matches2:
        # 避免重复
        if not any(e["id"] == exp_id for e in entries):
            stars_match = re.search(r"\*\*可复用度\*\*：([★☆]+)", body)
            type_match = re.search(r"\*\*类型\*\*：`([^`]+)`", body)
            entries.append({
                "id": exp_id,
                "title": title.strip(),
                "stars": stars_match.group(1) if stars_match else "",
                "type": type_match.group(1) if type_match else "",
                "content": body.strip(),
            })

    return entries


def search_entries(entries: list[dict], keyword: str) -> list[dict]:
    """按关键词搜索经验条目。"""
    keyword_lower = keyword.lower()
    results = []
    for entry in entries:
        searchable = f"{entry['title']} {entry['content']}".lower()
        if keyword_lower in searchable:
            results.append(entry)
    return results


def compute_stats(entries: list[dict]) -> dict:
    """统计经验手册概览。"""
    if not entries:
        return {"total": 0, "message": "经验手册尚无条目"}

    type_counter = Counter(e.get("type", "未分类") for e in entries)
    star_counts = {"★★★★★": 0, "★★★★☆": 0, "★★★☆☆": 0, "其他": 0}
    for e in entries:
        stars = e.get("stars", "")
        if "★★★★★" in stars:
            star_counts["★★★★★"] += 1
        elif "★★★★" in stars:
            star_counts["★★★★☆"] += 1
        elif "★★★" in stars:
            star_counts["★★★☆☆"] += 1
        else:
            star_counts["其他"] += 1

    return {
        "total": len(entries),
        "by_type": dict(type_counter),
        "by_stars": star_counts,
    }


def find_duplicates(entries: list[dict]) -> list[tuple]:
    """检查潜在重复条目（基于 bigram 词级 Jaccard 相似度）。"""
    duplicates = []
    
    def to_bigrams(text: str) -> set:
        """将文本转为 bigram 集合，用于中文相似度计算。"""
        # 清理文本，去除标点和空格
        clean = re.sub(r'[^\w]', '', text.lower())
        if len(clean) < 2:
            return {clean} if clean else set()
        return {clean[i:i+2] for i in range(len(clean) - 1)}

    for i in range(len(entries)):
        for j in range(i + 1, len(entries)):
            bigrams_a = to_bigrams(entries[i]["title"])
            bigrams_b = to_bigrams(entries[j]["title"])
            if not bigrams_a or not bigrams_b:
                continue
            intersection = len(bigrams_a & bigrams_b)
            union = len(bigrams_a | bigrams_b)
            similarity = intersection / union if union > 0 else 0
            if similarity > 0.5:
                duplicates.append({
                    "entry_a": entries[i]["id"],
                    "title_a": entries[i]["title"],
                    "entry_b": entries[j]["id"],
                    "title_b": entries[j]["title"],
                    "similarity": round(similarity, 2),
                })

    return duplicates


def main():
    parser = argparse.ArgumentParser(description="经验手册管理工具")
    parser.add_argument("project_root", help="项目根目录")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # search
    search_parser = subparsers.add_parser("search", help="搜索经验")
    search_parser.add_argument("--keyword", required=True, help="搜索关键词")

    # stats
    subparsers.add_parser("stats", help="统计概览")

    # dedup
    subparsers.add_parser("dedup", help="去重检查")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    handbook_path = get_handbook_path(args.project_root)
    entries = parse_handbook(handbook_path)

    if args.command == "search":
        results = search_entries(entries, args.keyword)
        if results:
            output = {
                "keyword": args.keyword,
                "matches": len(results),
                "results": [
                    {"id": r["id"], "title": r["title"], "stars": r.get("stars", "")}
                    for r in results
                ],
            }
        else:
            output = {
                "keyword": args.keyword,
                "matches": 0,
                "message": f"未找到包含 '{args.keyword}' 的经验条目",
            }
        print(json.dumps(output, ensure_ascii=False, indent=2))

    elif args.command == "stats":
        stats = compute_stats(entries)
        print(json.dumps(stats, ensure_ascii=False, indent=2))

    elif args.command == "dedup":
        dupes = find_duplicates(entries)
        if dupes:
            output = {"potential_duplicates": len(dupes), "pairs": dupes}
        else:
            output = {"potential_duplicates": 0, "message": "未发现潜在重复条目"}
        print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
