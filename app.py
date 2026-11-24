from itertools import groupby


def analyze(data):
    threading, lifts = data["threading"], data["lifts"]
    if not isinstance(threading, list) or not threading or not isinstance(lifts, list) or not lifts:
        raise ValueError("Supply at least one warp end and one pick")
    if any(not isinstance(row, list) for row in lifts):
        raise ValueError("Each lift must be a list")
    if any(type(shaft) is not int or shaft < 1 for row in [threading, *lifts] for shaft in row):
        raise ValueError("Shaft numbers start at one")
    draft = []
    for lift in lifts:
        raised = set(lift)
        draft.append("".join("#" if shaft in raised else "." for shaft in threading))
    def longest(lines, marker):
        return max((sum(1 for _ in run) for line in lines for value, run in groupby(line)
                    if value == marker), default=0)
    return dict(drawdown=draft, longest_weft_float=longest(draft, "."), longest_warp_float=longest(zip(*draft), "#"))

if __name__ == "__main__":
    import json
    from pathlib import Path
    import sys
    try:
        path, = sys.argv[1:]
        result = analyze(json.loads(Path(path).read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=True, allow_nan=False))
    except (OSError, ValueError, TypeError, KeyError, AttributeError, OverflowError) as error:
        print(f"Invalid input: {error}", file=sys.stderr)
        sys.exit(2)
