import ast
from pathlib import Path

TARGET_FILES = [
    Path("importldraw.py"),
    Path("loadldraw") / "loadldraw.py",
]


def _parse(path: Path) -> ast.AST:
    return ast.parse(path.read_text(encoding="utf-8"))


def test_no_bare_except() -> None:
    for path in TARGET_FILES:
        tree = _parse(path)
        for node in ast.walk(tree):
            if isinstance(node, ast.ExceptHandler) and node.type is None:
                raise AssertionError(f"Bare except found in {path}:{node.lineno}")


def test_no_none_equality_checks() -> None:
    for path in TARGET_FILES:
        tree = _parse(path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare):
                continue

            left_is_none = isinstance(node.left, ast.Constant) and node.left.value is None
            if left_is_none and any(isinstance(op, (ast.Eq, ast.NotEq)) for op in node.ops):
                raise AssertionError(f"Use 'is' for None comparison in {path}:{node.lineno}")

            for op, comparator in zip(node.ops, node.comparators):
                right_is_none = isinstance(comparator, ast.Constant) and comparator.value is None
                if right_is_none and isinstance(op, (ast.Eq, ast.NotEq)):
                    raise AssertionError(f"Use 'is' for None comparison in {path}:{node.lineno}")


def test_no_type_is_comparisons() -> None:
    for path in TARGET_FILES:
        tree = _parse(path)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Compare):
                continue

            if not node.ops or not isinstance(node.ops[0], (ast.Is, ast.IsNot)):
                continue

            if isinstance(node.left, ast.Call) and isinstance(node.left.func, ast.Name) and node.left.func.id == "type":
                raise AssertionError(f"Use isinstance instead of type(...) is ... in {path}:{node.lineno}")
