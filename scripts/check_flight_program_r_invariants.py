#!/usr/bin/env python3
"""Invariant checks for launch-critical Flight Program R logic."""

from __future__ import annotations

import argparse
import sys
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class CheckResult:
    name: str
    passed: bool
    details: str


def _variable_name(node: ET.Element) -> str | None:
    var = node.find("Variable")
    if var is None:
        return None
    return var.attrib.get("variableName")


def _constant_text(node: ET.Element) -> str | None:
    const = node.find("Constant")
    if const is None:
        return None
    return const.attrib.get("text")


def check_countdown_not_unconditionally_throttle_zero(root: ET.Element) -> CheckResult:
    guard_found = False

    for elseif in root.findall(".//ElseIf"):
        cond = elseif[0] if len(elseif) else None
        if cond is None or cond.tag != "Not":
            continue

        comparison = cond.find("Comparison")
        if comparison is None or comparison.attrib.get("op") != "=":
            continue

        lhs = comparison.find("Variable")
        rhs = comparison.findall("Variable")
        if lhs is None or len(rhs) < 2:
            continue

        lhs_name = rhs[0].attrib.get("variableName")
        rhs_name = rhs[1].attrib.get("variableName")
        if lhs_name != "fc_mode" or rhs_name != "fc_mode_countdown":
            continue

        set_inputs = elseif.findall("./Instructions/SetInput")
        for set_input in set_inputs:
            if set_input.attrib.get("input") != "throttle":
                continue
            value = set_input.find("Constant")
            if value is not None and value.attrib.get("number") == "0":
                guard_found = True

    if guard_found:
        return CheckResult(
            "countdown_not_unconditionally_throttle_zero",
            True,
            "Found throttle=0 path explicitly guarded by NOT(fc_mode == fc_mode_countdown).",
        )

    return CheckResult(
        "countdown_not_unconditionally_throttle_zero",
        False,
        "Did not find the expected throttle=0 guard excluding countdown mode.",
    )


def check_countdown_arm_and_abort_paths(root: ET.Element) -> CheckResult:
    arm_threshold_present = False
    ag1_abort_present = False
    timeout_abort_present = False

    for if_node in root.findall(".//If"):
        comparison = if_node.find("Comparison")
        if comparison is None:
            continue

        craft_prop = comparison.find("CraftProperty")
        var = comparison.find("Variable")
        if (
            comparison.attrib.get("op") == "g"
            and craft_prop is not None
            and craft_prop.attrib.get("property") == "Input.Throttle"
            and var is not None
            and var.attrib.get("variableName") == "countdown_arm_throttle"
        ):
            if if_node.find("./Instructions/Break") is not None:
                arm_threshold_present = True

        act_group = comparison.find("ActivationGroup")
        if (
            comparison.attrib.get("op") == "="
            and act_group is not None
            and act_group.find("Constant") is not None
            and act_group.find("Constant").attrib.get("number") == "1"
        ):
            assigns_abort = any(
                _variable_name(set_var) == "countdown_abort"
                and _constant_text(set_var) == "1"
                for set_var in if_node.findall("./Instructions/SetVariable")
            )
            if assigns_abort:
                ag1_abort_present = True

        if (
            comparison.attrib.get("op") == "ge"
            and len(comparison.findall("Variable")) >= 2
            and comparison.findall("Variable")[0].attrib.get("variableName") == "countdown_elapsed_s"
            and comparison.findall("Variable")[1].attrib.get("variableName") == "countdown_timeout_s"
        ):
            assigns_abort = any(
                _variable_name(set_var) == "countdown_abort"
                and _constant_text(set_var) == "1"
                for set_var in if_node.findall("./Instructions/SetVariable")
            )
            if assigns_abort:
                timeout_abort_present = True

    passed = arm_threshold_present and ag1_abort_present and timeout_abort_present
    details = (
        f"arm_threshold_present={arm_threshold_present}, "
        f"ag1_abort_present={ag1_abort_present}, "
        f"timeout_abort_present={timeout_abort_present}"
    )
    return CheckResult("countdown_arm_threshold_and_abort_paths", passed, details)


def check_autostage_canonical_input_usage(root: ET.Element) -> CheckResult:
    user_input_var = None
    for user_input in root.findall(".//UserInput"):
        constants = user_input.findall("Constant")
        prompt_text = " ".join(c.attrib.get("text", "") for c in constants)
        if "Autostage enabled?" in prompt_text:
            user_input_var = user_input.find("Variable")
            break

    if user_input_var is None:
        return CheckResult(
            "autostage_canonical_input_usage",
            False,
            "Could not locate autostage user-input prompt and its backing variable.",
        )

    canonical_var = user_input_var.attrib.get("variableName")
    canonical_candidates = {
        var.attrib.get("name")
        for var in root.findall(".//Variables/Variable")
        if var.attrib.get("name") == "init" or "autostage" in var.attrib.get("name", "")
    }

    has_normalized_one = False
    has_normalized_zero = False
    for set_var in root.findall(".//SetVariable"):
        if _variable_name(set_var) != canonical_var:
            continue
        ctext = _constant_text(set_var)
        if ctext == "1":
            has_normalized_one = True
        if ctext == "0":
            has_normalized_zero = True

    single_canonical = len(canonical_candidates) == 1
    passed = single_canonical and has_normalized_one and has_normalized_zero
    details = (
        f"canonical_var={canonical_var}, "
        f"canonical_candidates={sorted(canonical_candidates)}, "
        f"has_normalized_one={has_normalized_one}, "
        f"has_normalized_zero={has_normalized_zero}"
    )
    return CheckResult("autostage_canonical_input_usage", passed, details)


def run_checks(xml_path: Path) -> list[CheckResult]:
    tree = ET.parse(xml_path)
    root = tree.getroot()

    checks: list[Callable[[ET.Element], CheckResult]] = [
        check_countdown_not_unconditionally_throttle_zero,
        check_countdown_arm_and_abort_paths,
        check_autostage_canonical_input_usage,
    ]
    return [check(root) for check in checks]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--xml",
        default="Flight Program R V3.0.xml",
        help="Path to the Flight Program R XML file (default: %(default)s)",
    )
    args = parser.parse_args()

    xml_path = Path(args.xml)
    if not xml_path.exists():
        print(f"ERROR: XML file not found: {xml_path}")
        return 2

    results = run_checks(xml_path)

    failures = 0
    for result in results:
        status = "PASS" if result.passed else "FAIL"
        print(f"[{status}] {result.name}: {result.details}")
        if not result.passed:
            failures += 1

    if failures:
        print(f"\nInvariant check result: FAIL ({failures} invariant(s) failed)")
        return 1

    print("\nInvariant check result: PASS (all invariants satisfied)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
