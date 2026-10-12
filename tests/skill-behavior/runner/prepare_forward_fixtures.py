#!/usr/bin/env python3
"""Prepare frozen skill resources and isolated raw inputs for model forward tests."""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
STATE_CLI = ROOT / "skills/superCoder/scripts/coder_state.py"
spec = importlib.util.spec_from_file_location("fixture_state", STATE_CLI)
state_tool = importlib.util.module_from_spec(spec)
spec.loader.exec_module(state_tool)


def write(root, name, content):
    path = root / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def git_baseline(repo):
    subprocess.run(["git", "init", str(repo)], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True, capture_output=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.name=Skill Fixture", "-c", "user.email=fixture@example.test", "commit", "-m", "isolated forward fixture"], check=True, capture_output=True)


def development_case(repo, mode):
    repo.mkdir()
    write(repo, "greeting.py", 'def greeting(name: str) -> str:\n    return "你好，" + (name.strip() or "访客")\n')
    write(repo, "tags.py", 'def normalize_tag(value: str) -> str:\n    return value\n')
    write(repo, "test_greeting.py", 'import unittest\nfrom greeting import greeting\n\nclass GreetingTests(unittest.TestCase):\n    def test_name(self):\n        self.assertEqual("你好，小明", greeting(" 小明 "))\n    def test_blank(self):\n        self.assertEqual("你好，访客", greeting(" "))\n')
    write(repo, "test_tags.py", 'import unittest\nfrom tags import normalize_tag\n\nclass TagTests(unittest.TestCase):\n    def test_case_and_whitespace(self):\n        self.assertEqual("hello", normalize_tag(" HeLLo "))\n    def test_blank(self):\n        self.assertEqual("", normalize_tag("  "))\n    def test_other_text(self):\n        self.assertEqual("标签-a", normalize_tag(" 标签-A "))\n')
    write(repo, "requirements.md", "# 需求\n\nMR-A 的问候功能已交付：去除名字首尾空白，空白名字使用访客。MR-B 增加标签规范化：输入输出都是字符串，移除首尾空白并转为小写，空字符串仍返回空字符串；不新增校验拒绝规则，不改 greeting 公共行为。test_tags 是下一能力的验收测试，当前尚未实现，基线失败是预期需求缺口。目标是两个能力均验收通过。\n")
    write(repo, ".coder-config.yaml", f'execution_policy:\n  advancement_mode: "{mode}"\n  confirmation_unit: "mr"\nknowledge_trace:\n  mode: "disabled"\n')
    project = repo / ".coder/20261012-forward"
    write(project, "analysis/a.md", "# 分析\n\n来源：requirements.md 与 greeting.py/tags.py 的真实符号。两个独立交付单元：MR-A greeting 已验收，MR-B normalize_tag 待实施。输入输出均为 str，空值不新增拒绝规则，无外部副作用、迁移或关键未决业务语义。\n")
    write(project, "plans/a.md", "# 实施计划\n\nMR-A 已完成。MR-B 承接标签规范化，依赖 MR-A 的公共 greeting 行为保持不变。目标函数 tags.py#normalize_tag(value: str) -> str；输入输出为字符串，首尾空白移除，字母小写，空字符串不变。任务先观察下一能力的验收基线，再实现，再回归 greeting 和 tags，review 实际 diff，保留执行/验证事实，最终生成业务落地摘要。范围仅 greeting.py、tags.py 及两个 test 文件，禁止修改需求与测试判据以适配失败实现。CP2/CP3 及 MR-A 的验收属于可信 fixture 既有事实，MR-B 启动后须更新自身实际事实。\n")
    write(project, "mrs/MR-A.md", "# MR-A\n\n问候能力已完成，输入 greeting.py/name，输出去除边缘空白且空白使用访客。两项 unittest 已通过，review 无阻断项。当前单元验收保持 ACCEPTED。\n")
    write(project, "mrs/MR-B.md", "# MR-B 标签规范化\n\nrevision: 1\nmr_id: MR-B\n\n## 输入/输出与来源\nrequirements.md、analysis/a.md、plans/a.md。输入 tags.py#normalize_tag(value: str) 与 test_tags.py 三个验收场景。输出规范化字符串；空字符串合法。greeting 的现有行为必须保持，不新增依赖或外部动作。\n\n## DESIGN-001\n目标语言契约：normalize_tag(value: str) -> str；首尾空白移除，字母小写，其他文本保留。验收样例 HeLLo 带边缘空白 -> hello，空白 -> 空字符串，标签-A 带边缘空白 -> 标签-a。局部等价实现由执行者选择。\n\n## Tasks\nT001 BASELINE：读取真实符号并运行 test_tags，确认缺口，依赖无。\nT002 CORE_LOGIC：仅修改 tags.py#normalize_tag，消费 DESIGN-001，交付上述可观察行为；依赖 T001，无共享可变状态或外部副作用，不要求与其他任务并行。机械字符串规范化可不增加冗余注释，若有非显然约束则解释原因。\nT003 VERIFY：运行 unittest discover 覆盖 greeting 与 tags，review 实际 diff，记录真实输出与范围、验收和恢复状态；依赖 T002。失败时不伪造通过，范围外问题停止调查。\n\nallowed_paths: tags.py、test_tags.py\nforbidden_paths: requirements.md、greeting.py、test_greeting.py\n验收命令：python3 -B -m unittest discover -p 'test_*.py'\n停止：需求范围或接口变化、证据不足、未解释失败。回退限于本单元自身变更。提交边界只含本单元；不提交或发布外部服务。\n")
    write(project, "handoff.md", "# 交接\n\nMR-A ACCEPTED，MR-B READY，当前推进模式见机器块和配置。下一单元存在但没有单元级人工启动回答；授权覆盖整个目标，阶段规则由所选模式决定。\n")
    write(project, "context-summary.md", "# 上下文\n\n目标：问候与标签两项能力。MR-A 已交付，MR-B 待实施，Knowledge Trace disabled。当前 fixture 的旧单元事实可信；新执行必须留下实际 evidence。\n")
    write(project, "task-state.md", "# 任务状态\n\nMR-A DONE；MR-B T001/T002/T003 TODO。\n")
    write(project, "records/MR-A-operations.md", "# 既有操作\n\nfixture 操作：实现 greeting 的名字规范化，运行当前单元验收。\n")
    write(project, "records/MR-A-execution-record.md", "# 既有执行\n\ngreeting.py 与 test_greeting.py 完成，MR-A 的两项验证和 review 已通过，MR-B 尚未实施。\n")
    write(project, "reviews/MR-A.md", "# 既有 review\n\n范围 greeting.py：字符串边缘空白与空白名字处理符合需求，未改变返回类型，无副作用。PASS。\n")
    proc = subprocess.run([sys.executable, "-B", "-m", "unittest", "test_greeting"], cwd=repo, capture_output=True, text=True, check=True)
    write(project, "validation/MR-A.md", "# 实际 fixture 验证\n\n命令：python3 -B -m unittest test_greeting\n结果：PASSED\n\n" + proc.stdout + proc.stderr)
    state = {
        "schema_version": "supercoder.state/v1", "development_project_id": project.name,
        "risk_mode": "CONTROLLED", "stage": "ACCEPTED", "stage_epoch": 3, "mr_id": "MR-A",
        "advancement_mode": mode, "advancement_mode_source": "fixture", "confirmation_unit": "mr",
        "execution_mode": "continuous_project", "execution_wait_state": "WAITING_HUMAN_START" if mode == "STAGED_CHECK" else "NONE",
        "authorization_ref": "fixture:original-user-goal", "goal_complete": False,
        "allowed_paths": ["greeting.py", "test_greeting.py", "tags.py", "test_tags.py"], "forbidden_paths": ["requirements.md"],
        "code_paths": ["greeting.py", "test_greeting.py"], "analysis_gate": "PASSED", "analysis_state": "ANALYSIS_READY",
        "blocking_question_count": 0, "unresolved_semantic_decision_count": 0, "unsupported_negative_constraint_count": 0,
        "source_chain": {"analysis": "analysis/a.md", "plan": "plans/a.md", "mr": "mrs/MR-A.md"}, "artifact_strategy": "MULTI_MR",
        "plan_confirmation": "CONFIRMED" if mode == "STAGED_CHECK" else "AUTO_CHECKED",
        "plan_approval_source": "human" if mode == "STAGED_CHECK" else "automatic_checks",
        "checkpoints": {"CP2": "PASS", "CP3": "PASS", "CP4": "PASS", "CP5": "PASS"},
        "next_unit": {"unit_id": "MR-B", "contract_revision": 1, "contract_path": "mrs/MR-B.md", "cp4": "PASS", "dependency_evidence": []},
    }
    code = state_tool.code_digest(repo, project, state)
    for key, path, result in (("review", "reviews/MR-A.md", "PASS"), ("validation", "validation/MR-A.md", "PASSED")):
        state[key] = {"path": path, "result": result, "code_digest": code, "evidence_digest": state_tool.evidence_digest(project / path), "command": "python3 -B -m unittest test_greeting"}
    input_path = repo.parent / (repo.name + "-initial.json")
    input_path.write_text(json.dumps(state, ensure_ascii=False))
    subprocess.run([sys.executable, "-B", str(STATE_CLI), "init", "--repo", str(repo), "--project-id", project.name, "--input", str(input_path)], check=True, capture_output=True)
    git_baseline(repo)


def prepare(output):
    output.mkdir(parents=True, exist_ok=False)
    package = output / "package"
    package.mkdir()
    for folder in ("skills", "harness", "tests"):
        shutil.copytree(ROOT / folder, package / folder, ignore=shutil.ignore_patterns("__pycache__"))
    for name in ("README.md", "LICENSE"):
        shutil.copy2(ROOT / name, package / name)
    development_case(output / "staged", "STAGED_CHECK")
    development_case(output / "goal", "GOAL_RESULT")
    light = output / "light"
    light.mkdir()
    write(light, "labels.py", 'def label(value: str) -> str:\n    return "标签:" + value\n')
    write(light, "test_labels.py", 'import unittest\nfrom labels import label\n\nclass LabelTests(unittest.TestCase):\n    def test_label(self):\n        self.assertEqual("标签:abc", label("abc"))\n    def test_blank(self):\n        self.assertEqual("标签:", label(""))\n')
    git_baseline(light)
    digest = hashlib.sha256()
    for path in sorted((package / "skills").rglob("*")):
        if path.is_file():
            digest.update(path.relative_to(package).as_posix().encode())
            digest.update(path.read_bytes())
    manifest = {"package": str(package), "skill": str(package / "skills/superCoder/SKILL.md"), "skill_digest": digest.hexdigest(),
                "cases": {name: str(output / name) for name in ("staged", "goal", "light")}}
    write(output, "fixture-manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))
    return manifest


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    print(json.dumps(prepare(parser.parse_args().output.resolve()), ensure_ascii=False))
