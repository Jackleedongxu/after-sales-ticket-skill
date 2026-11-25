#!/usr/bin/env python3
"""
售后工单结构化辅助脚本

本脚本提供 JSON 格式校验与基础规范化功能，可作为 Skill 的参考实现。
实际工单解析逻辑由 LLM 根据 SKILL.md 中的规则完成。
"""

import json
import sys
from typing import Dict, Any


REQUIRED_FIELDS = [
    "适用机型",
    "故障代码",
    "故障现象",
    "可能原因",
    "排查步骤",
    "所需配件",
    "解决方案",
    "注意事项",
    "客户/现场",
    "其他信息",
]


def validate_ticket(data: Dict[str, Any]) -> list[str]:
    """校验工单 JSON 是否包含所有必需字段。"""
    errors = []
    for field in REQUIRED_FIELDS:
        if field not in data:
            errors.append(f"缺少字段: {field}")
        elif not isinstance(data[field], str):
            errors.append(f"字段 '{field}' 应为字符串类型")
    return errors


def normalize_ticket(data: Dict[str, Any]) -> Dict[str, str]:
    """确保所有字段存在且为字符串，缺失则填充 [N/A]。"""
    result = {}
    for field in REQUIRED_FIELDS:
        value = data.get(field, "[N/A]")
        result[field] = str(value) if value is not None else "[N/A]"
    return result


def main():
    """从标准输入读取 JSON，校验并输出规范化结果。"""
    try:
        raw = sys.stdin.read()
        data = json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"JSON 解析失败: {e}", file=sys.stderr)
        sys.exit(1)

    if isinstance(data, list):
        results = []
        for i, item in enumerate(data):
            errors = validate_ticket(item)
            if errors:
                print(f"卡片 {i+1} 校验失败: {'; '.join(errors)}", file=sys.stderr)
            results.append(normalize_ticket(item))
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        errors = validate_ticket(data)
        if errors:
            print(f"校验失败: {'; '.join(errors)}", file=sys.stderr)
            sys.exit(1)
        normalized = normalize_ticket(data)
        print(json.dumps(normalized, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
