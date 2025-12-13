"""Utility: SequentialThinking

A minimal pipeline helper to chain steps where each step receives
previous output as its input.
"""

from __future__ import annotations
from typing import Any, Callable, Dict, List, Optional


class SequentialThinking:
    def __init__(self, steps: Optional[List[Dict[str, Any]]] = None) -> None:
        self.steps: List[Dict[str, Any]] = steps or []

    def add_step(self, description: str, action: Callable[[Any], Any]) -> None:
        self.steps.append({"desc": description, "action": action})

    def run(self, context: Any) -> Any:
        results: List[Any] = []
        for i, step in enumerate(self.steps, start=1):
            print(f"Step {i}: {step['desc']}")
            result = step["action"](context)
            results.append(result)
            # output → input للخطوة اللي بعدها
            context = result
        return results[-1] if results else None


__all__ = ["SequentialThinking"]


if __name__ == "__main__":
    # مثال استخدام سريع
    st = SequentialThinking()
    st.add_step("تحضير البيانات", lambda ctx: ctx.lower())
    st.add_step("تجزئة", lambda ctx: ctx.split())
    st.add_step("عدّ الكلمات", lambda ctx: len(ctx))

    print(st.run("Hello Sequential Thinking"))  # يطبع 3
