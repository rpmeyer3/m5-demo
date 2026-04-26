"""Strip HTML, CSS, and JS comments from index.html in-place (safely)."""
import re
from pathlib import Path

SRC = Path(r"c:\Users\meyer\Documents\GitHub\m5-demo\m5-demo\index.html")


def strip_js(code: str) -> str:
    """Strip // and /* */ comments from JS, respecting strings/templates/regex."""
    out = []
    i = 0
    n = len(code)
    # naive regex-context tracking: a regex literal can follow these tokens
    prev_significant = ""
    regex_ok_after = {
        "", "(", ",", "=", ":", "[", "!", "&", "|", "?", "{", "}", ";",
        "+", "-", "*", "/", "%", "^", "~", "<", ">", "return", "typeof",
        "in", "of", "instanceof", "new", "delete", "void", "throw", "case",
        "do", "else", "&&", "||", "==", "!=", "===", "!==", "=>",
    }

    def last_token_is_regex_ok():
        # walk back through out to find last non-space char/word
        s = "".join(out)
        j = len(s) - 1
        while j >= 0 and s[j] in " \t\r\n":
            j -= 1
        if j < 0:
            return True
        ch = s[j]
        if ch.isalnum() or ch == "_" or ch == ")" or ch == "]":
            # could be identifier or end of expr -> not regex
            # but check keywords
            k = j
            while k >= 0 and (s[k].isalnum() or s[k] == "_"):
                k -= 1
            word = s[k + 1:j + 1]
            if word in {"return", "typeof", "in", "of", "instanceof", "new",
                        "delete", "void", "throw", "case", "do", "else"}:
                return True
            return False
        return ch in regex_ok_after

    while i < n:
        c = code[i]
        nxt = code[i + 1] if i + 1 < n else ""

        # line comment
        if c == "/" and nxt == "/":
            while i < n and code[i] != "\n":
                i += 1
            continue
        # block comment
        if c == "/" and nxt == "*":
            i += 2
            while i < n - 1 and not (code[i] == "*" and code[i + 1] == "/"):
                i += 1
            i += 2
            continue
        # string literals
        if c in ("'", '"'):
            quote = c
            out.append(c)
            i += 1
            while i < n:
                ch = code[i]
                out.append(ch)
                i += 1
                if ch == "\\" and i < n:
                    out.append(code[i])
                    i += 1
                    continue
                if ch == quote:
                    break
            continue
        # template literal
        if c == "`":
            out.append(c)
            i += 1
            depth = 0
            while i < n:
                ch = code[i]
                if ch == "\\" and i + 1 < n:
                    out.append(ch)
                    out.append(code[i + 1])
                    i += 2
                    continue
                if ch == "$" and i + 1 < n and code[i + 1] == "{":
                    out.append("${")
                    i += 2
                    depth += 1
                    # consume until matching }
                    brace = 1
                    while i < n and brace > 0:
                        ch2 = code[i]
                        out.append(ch2)
                        if ch2 == "{":
                            brace += 1
                        elif ch2 == "}":
                            brace -= 1
                        i += 1
                    continue
                out.append(ch)
                i += 1
                if ch == "`":
                    break
            continue
        # regex literal
        if c == "/" and last_token_is_regex_ok():
            out.append(c)
            i += 1
            in_class = False
            while i < n:
                ch = code[i]
                out.append(ch)
                i += 1
                if ch == "\\" and i < n:
                    out.append(code[i])
                    i += 1
                    continue
                if ch == "[":
                    in_class = True
                elif ch == "]":
                    in_class = False
                elif ch == "/" and not in_class:
                    break
                elif ch == "\n":
                    # not a regex; bail (shouldn't happen in valid code)
                    break
            # consume flags
            while i < n and code[i].isalpha():
                out.append(code[i])
                i += 1
            continue

        out.append(c)
        i += 1

    return "".join(out)


def strip_css(code: str) -> str:
    out = []
    i = 0
    n = len(code)
    while i < n:
        c = code[i]
        nxt = code[i + 1] if i + 1 < n else ""
        if c == "/" and nxt == "*":
            i += 2
            while i < n - 1 and not (code[i] == "*" and code[i + 1] == "/"):
                i += 1
            i += 2
            continue
        if c in ("'", '"'):
            quote = c
            out.append(c)
            i += 1
            while i < n:
                ch = code[i]
                out.append(ch)
                i += 1
                if ch == "\\" and i < n:
                    out.append(code[i])
                    i += 1
                    continue
                if ch == quote:
                    break
            continue
        out.append(c)
        i += 1
    return "".join(out)


def collapse_blank_lines(s: str) -> str:
    return re.sub(r"\n[ \t]*\n[ \t]*\n+", "\n\n", s)


def main():
    html = SRC.read_text(encoding="utf-8")

    # Process <script>...</script> blocks
    def script_repl(m):
        return m.group(1) + strip_js(m.group(2)) + m.group(3)

    html = re.sub(
        r"(<script\b[^>]*>)(.*?)(</script>)",
        script_repl,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Process <style>...</style> blocks
    def style_repl(m):
        return m.group(1) + strip_css(m.group(2)) + m.group(3)

    html = re.sub(
        r"(<style\b[^>]*>)(.*?)(</style>)",
        style_repl,
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )

    # Strip HTML comments (but not inside script/style which are already cleaned;
    # HTML comments inside those blocks would have been part of strings—rare).
    # We need to avoid stripping inside script/style. Easiest: split on those tags.
    parts = re.split(
        r"(<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>)",
        html,
        flags=re.DOTALL | re.IGNORECASE,
    )
    for idx, part in enumerate(parts):
        if idx % 2 == 0:  # outside script/style
            parts[idx] = re.sub(r"<!--.*?-->", "", part, flags=re.DOTALL)
    html = "".join(parts)

    html = collapse_blank_lines(html)

    SRC.write_text(html, encoding="utf-8")
    print(f"Done. New size: {SRC.stat().st_size} bytes")


if __name__ == "__main__":
    main()
