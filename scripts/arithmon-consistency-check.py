#!/usr/bin/env python3
"""
arithmon-consistency-check.py

Cross-repository consistency overseer for the Arithmon program.

Per-repo CI cannot see drift that only exists *between* repos: a stale count in
one README, a DOI cited nowhere else, a root module left a version behind.
This script clones the org's repos and checks the invariants that span them.

The deployed pages listed in SITES are fetched and flattened to text so that
the same checks reach them. Without this, the program's most-read claim
surface would be the only one nothing audits.

Source of truth: program/LEDGER.json (see EMBEDDED_LEDGER for the schema).
If that file is absent the embedded fallback is used and a warning is emitted.

Usage:
    python3 arithmon-consistency-check.py                  # clone fresh, full report
    python3 arithmon-consistency-check.py --local ./work   # reuse existing clones
    python3 arithmon-consistency-check.py --json out.json  # machine-readable
    python3 arithmon-consistency-check.py --no-network      # skip redirect checks

Exit codes: 0 = clean (warnings allowed), 1 = at least one ERROR, 2 = harness failure.
"""

from __future__ import annotations

import argparse
import html
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import urllib.request
from collections import defaultdict
from dataclasses import dataclass, field, asdict

ORG = "arithmon"
REPOS = [".github", "program", "atlas", "sieve", "lean", "k7", "k7-lean"]

# The program's front door is uploaded, not committed, so cloning cannot reach
# it. Each entry is fetched and flattened to text under a pseudo-repo, which
# lets every claim check below apply to the served page unchanged. Skipped
# under --no-network. The rendered filename is what LEDGER.claim_surfaces
# must list for the page to count as a claim surface.
SITES = {"site": ("https://arithmon.com/", "arithmon-com.md")}

# Paths whose content is historical by design and must never trigger drift errors.
HISTORICAL = re.compile(r"(^|/)(legacy|archive)/|CHANGELOG|/\.git/|/\.lake/|/build/")

TEXT_EXT = {".md", ".cff", ".yml", ".yaml", ".toml", ".json", ".bib", ".txt", ".lean", ".py", ".tex"}

EMBEDDED_LEDGER = {
    "_comment": "Single source of truth for numbers that appear in more than one repo.",
    "framework_version": "3.5",
    "counts": {
        "type_I_relations": 33,
        "type_II_relations": 19,
        "type_III_relations": 21,
        "type_IV_relations": 22,
        "total_observables": 95,
        "testable_observables": 66,
        "axioms": 15,
        "axioms_prediction_chain": 4,
        "axioms_k3": 11,
        "certificate_conjuncts": 213,
        "sorry": 0,
    },
    "frozen_predictions": {
        "delta_CP_deg": 197,
        "delta_CP_window_deg": [182, 212],
    },
    "external_citation": "Physics Letters B",
    "external_citation_full": r"Physics Letters B\*{0,2}\s*\*{0,2}878\*{0,2}\s*\(2026\)\s*140566",
    "known_dois": {
        "10.5281/zenodo.20666879": "Sieve (frozen inputs, pre-registration)",
        "10.5281/zenodo.16891489": "K7 Framework (concept DOI)",
    },
    "lean_version": "3.5",
    "root_modules": {
        "k7-lean": "GIFT.lean",
    },
    # Files where a number is a *headline claim* rather than a local subsection
    # count. Drift checks run here only: this is what keeps the report readable.
    "claim_surfaces": [
        "README.md", "arithmon-com.md", "profile/README.md", "CITATION.md", "CITATION.cff",
        "STRUCTURE.md", "INDEX.md", "CONFRONTATIONS.md",
        "docs/wiki/Home.md", "docs/wiki/Home.fr.md",
        "docs/GIFT_EXEC_SUMMARY.md", "docs/GIFT_EXEC_SUMMARY.fr.md",
        "docs/wiki/Citation-Guide.md", "docs/wiki/Citation-Guide.fr.md",
        "publications/papers/README.md", "publications/validation/README.md",
    ],
    # Lines quoting a measurement rather than asserting a prediction.
    "experimental_markers": [
        "nufit", "pdg", "best fit", "best-fit", "measured", "measurement",
        "experimental", "t2k", "nova", "if dune", "would be refuted",
        "is falsified", "falsifi", "hypothetical", "e.g.",
    ],
    "require_citation_cff": [
        ".github", "program", "atlas", "sieve", "lean", "k7", "k7-lean",
    ],
    "readme_must_cite_external": ["k7", "program", ".github"],
    "old_org_prefixes": ["github.com/gift-framework/"],
}


# ----------------------------------------------------------------------------- findings

@dataclass
class Finding:
    level: str          # ERROR | WARN | INFO
    check: str
    repo: str
    message: str
    locations: list = field(default_factory=list)


class Report:
    def __init__(self):
        self.findings: list[Finding] = []

    def add(self, level, check, repo, message, locations=None):
        self.findings.append(Finding(level, check, repo, message, locations or []))

    def error(self, *a, **k): self.add("ERROR", *a, **k)
    def warn(self, *a, **k):  self.add("WARN", *a, **k)
    def info(self, *a, **k):  self.add("INFO", *a, **k)

    @property
    def n_errors(self):
        return sum(1 for f in self.findings if f.level == "ERROR")

    @property
    def n_warns(self):
        return sum(1 for f in self.findings if f.level == "WARN")


# ----------------------------------------------------------------------------- helpers

def run(cmd, cwd=None, timeout=600):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout)


def clone_all(workdir, quiet=True):
    """Shallow-clone every repo. Returns {repo_name: path}."""
    paths = {}
    for repo in REPOS:
        dest = os.path.join(workdir, repo.lstrip("."))
        if os.path.isdir(os.path.join(dest, ".git")):
            paths[repo] = dest
            continue
        url = f"https://github.com/{ORG}/{repo}.git"
        r = run(["git", "clone", "--depth", "1", "-q", url, dest])
        if r.returncode != 0:
            print(f"  ! clone failed for {repo}: {r.stderr.strip()[:200]}", file=sys.stderr)
            continue
        paths[repo] = dest
        if not quiet:
            print(f"  cloned {repo}")
    return paths


BLOCK_TAGS = "p|div|li|tr|h[1-6]|section|article|dt|dd|blockquote|br"


def render_page_text(src):
    """Flatten a served HTML page to one line per block element.

    Link targets are kept inline so that the link checks see them; everything
    else becomes plain text, because the claim checks are line-based and a
    number wrapped in markup would otherwise never match.
    """
    src = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", src)
    src = re.sub(r'(?i)<a\b[^>]*href="([^"]+)"[^>]*>', r" \1 ", src)
    src = re.sub(r"(?i)<(%s)\b[^>]*>" % BLOCK_TAGS, "\n", src)
    src = re.sub(r"(?i)</(%s)>" % BLOCK_TAGS, "\n", src)
    src = re.sub(r"<[^>]+>", " ", src)
    src = html.unescape(src)
    lines = (re.sub(r"[ \t ]+", " ", ln).strip() for ln in src.splitlines())
    return "\n".join(ln for ln in lines if ln)


def materialize_sites(workdir, quiet=True):
    """Fetch each deployed page into a pseudo-repo. Returns {key: path}."""
    paths = {}
    for key, (url, fname) in SITES.items():
        dest = os.path.join(workdir, key)
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "arithmon-consistency-check"})
            with urllib.request.urlopen(req, timeout=30) as r:
                raw = r.read().decode("utf-8", errors="replace")
        except Exception as exc:
            print(f"  ! could not fetch {url}: {exc}", file=sys.stderr)
            continue
        os.makedirs(dest, exist_ok=True)
        with open(os.path.join(dest, fname), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_page_text(raw))
        paths[key] = dest
        if not quiet:
            print(f"  fetched {url}")
    return paths


def resolve_local(workdir):
    """Map repo names onto an existing directory of clones."""
    paths = {}
    for repo in REPOS:
        for cand in (repo, repo.lstrip("."), repo.replace(".", "")):
            p = os.path.join(workdir, cand)
            if os.path.isdir(p):
                paths[repo] = p
                break
    return paths


def walk_files(root, exts=TEXT_EXT, skip_historical=True):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in (".git", ".lake", "build", "node_modules")]
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, root)
            if exts and os.path.splitext(fn)[1] not in exts:
                continue
            if skip_historical and HISTORICAL.search("/" + rel.replace(os.sep, "/")):
                continue
            yield full, rel


def read(path):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def strip_lean_comments(src: str) -> str:
    """Remove Lean 4 block comments /- ... -/ and line comments -- ... .

    Needed so that a docstring saying "machine-checked, no sorry" does not
    register as an unproven goal.
    """
    out, i, n = [], 0, len(src)
    depth = 0
    while i < n:
        if src.startswith("/-", i):
            depth += 1
            i += 2
            continue
        if depth and src.startswith("-/", i):
            depth -= 1
            i += 2
            continue
        if depth:
            i += 1
            continue
        if src.startswith("--", i):
            j = src.find("\n", i)
            if j == -1:
                break
            out.append("\n")
            i = j + 1
            continue
        out.append(src[i])
        i += 1
    return "".join(out)


def is_claim_surface(rel, ledger):
    rel = rel.replace(os.sep, "/")
    return rel in set(ledger.get("claim_surfaces", []))


VERSION_ROW = re.compile(r"^\s*\|\s*v?\d+\.\d+")          # changelog table row
# Directory-tree glyphs only: a bare mention of a .lean file must NOT exempt a
# line from drift checks ("140 conjuncts ... 143 .lean files" is a live claim).
TREE_LINE = re.compile(r"[├│└]")


def claim_lines(text):
    """Yield (lineno, line) for lines that carry a live headline claim.

    Skips fence markers, directory-tree listings and version-history table rows:
    these legitimately contain historical or per-module numbers that must not be
    compared against the current ledger. BibTeX blocks are NOT skipped, since a
    note field is a headline claim.
    """
    for ln, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            continue
        if VERSION_ROW.match(line) or TREE_LINE.search(line):
            continue
        yield ln, line


def is_experimental_line(line, ledger):
    low = line.lower()
    return any(mark in low for mark in ledger.get("experimental_markers", []))


def load_ledger(paths, report):
    p = paths.get("program")
    if p:
        f = os.path.join(p, "LEDGER.json")
        if os.path.isfile(f):
            try:
                return json.loads(read(f)), True
            except json.JSONDecodeError as e:
                report.error("ledger", "program", f"LEDGER.json is not valid JSON: {e}")
    report.warn(
        "ledger", "program",
        "program/LEDGER.json absent: falling back to embedded values. Commit the "
        "ledger so the canonical numbers live in exactly one place.",
    )
    return EMBEDDED_LEDGER, False


# ----------------------------------------------------------------------------- checks

def check_type_arithmetic(ledger, report):
    c = ledger["counts"]
    parts = ["type_I_relations", "type_II_relations", "type_III_relations", "type_IV_relations"]
    s = sum(c[k] for k in parts)
    if s != c["total_observables"]:
        report.error("ledger-arithmetic", "-",
                     f"ledger is internally inconsistent: {' + '.join(str(c[k]) for k in parts)}"
                     f" = {s}, but total_observables = {c['total_observables']}")
    ax = c.get("axioms")
    split = c.get("axioms_prediction_chain", 0) + c.get("axioms_k3", 0)
    if ax is not None and split and split != ax:
        report.error("ledger-arithmetic", "-",
                     f"axiom split {split} does not equal declared axioms {ax}")


def check_lean_sorry(paths, ledger, report):
    allowed = ledger["counts"].get("sorry", 0)
    pattern = re.compile(r"\bsorry\b")
    for repo in ("lean", "k7-lean"):
        root = paths.get(repo)
        if not root:
            continue
        hits = []
        for full, rel in walk_files(root, exts={".lean"}, skip_historical=True):
            code = strip_lean_comments(read(full))
            for ln, line in enumerate(code.splitlines(), 1):
                if pattern.search(line):
                    hits.append(f"{rel}:{ln}")
        if len(hits) > allowed:
            report.error("lean-sorry", repo,
                         f"{len(hits)} real `sorry` in code (ledger allows {allowed})", hits[:20])
        else:
            report.info("lean-sorry", repo,
                        f"{len(hits)} real `sorry` (comments excluded, ledger allows {allowed})")


def check_axiom_count(paths, ledger, report):
    expected = ledger["counts"].get("axioms")
    if expected is None:
        return
    root = paths.get("k7-lean")
    if not root:
        return
    decl = re.compile(r"^\s*(?:@\[[^\]]*\]\s*)?axiom\s+(\w+)", re.M)
    names = []
    for full, rel in walk_files(root, exts={".lean"}, skip_historical=True):
        code = strip_lean_comments(read(full))
        names += [m.group(1) for m in decl.finditer(code)]
    if len(names) != expected:
        report.error("axiom-count", "k7-lean",
                     f"{len(names)} `axiom` declarations found, ledger says {expected}",
                     sorted(names)[:30])
    else:
        report.info("axiom-count", "k7-lean", f"{len(names)} axioms, matches ledger")


def check_root_module_version(paths, ledger, report):
    want = str(ledger["framework_version"])
    for repo, module in ledger.get("root_modules", {}).items():
        root = paths.get(repo)
        if not root:
            continue
        f = os.path.join(root, module)
        if not os.path.isfile(f):
            report.warn("root-version", repo, f"declared root module {module} not found")
            continue
        head = "\n".join(read(f).splitlines()[:15])
        m = re.search(r"[Vv]ersion:?\s*v?(\d+\.\d+(?:\.\d+)?)", head)
        if not m:
            report.warn("root-version", repo, f"{module}: no version string in first 15 lines")
            continue
        found = m.group(1)
        if not found.startswith(want):
            lineno = head[: m.start()].count("\n") + 1
            report.error("root-version", repo,
                         f"{module} declares version {found} but the ledger says {want}. "
                         f"This is the first line a reader of the formal core sees.",
                         [f"{module}:{lineno}"])
        else:
            report.info("root-version", repo, f"{module} at {found}, matches ledger")


def check_citation_cff(paths, ledger, report):
    for repo in ledger.get("require_citation_cff", []):
        root = paths.get(repo)
        if not root:
            continue
        if not os.path.isfile(os.path.join(root, "CITATION.cff")):
            report.warn("citation-cff", repo,
                        "no CITATION.cff: GitHub will not show a 'Cite this repository' button")


def check_external_citation(paths, ledger, report):
    needle = ledger.get("external_citation", "")
    full_re = re.compile(ledger.get("external_citation_full", re.escape(needle)), re.I)
    for repo in ledger.get("readme_must_cite_external", []):
        root = paths.get(repo)
        if not root:
            continue
        candidates = ["README.md", os.path.join("profile", "README.md")]
        texts = [(c, read(os.path.join(root, c))) for c in candidates
                 if os.path.isfile(os.path.join(root, c))]
        if not texts:
            report.warn("external-citation", repo, "no README found to check")
            continue
        if not any(full_re.search(t) for _, t in texts):
            where = [c for c, t in texts if needle.lower() in t.lower()]
            msg = (f"README does not carry the indexed {needle} citation in full form"
                   + (f" (partial mention present in {where})" if where else ""))
            report.warn("external-citation", repo, msg)


def check_doi_crossrefs(paths, ledger, report):
    doi_re = re.compile(r"10\.5281/zenodo\.\d+")
    where = defaultdict(set)
    in_prose = defaultdict(bool)
    detail = defaultdict(list)
    for repo, root in paths.items():
        for full, rel in walk_files(root, skip_historical=True):
            ext = os.path.splitext(rel)[1]
            for d in set(doi_re.findall(read(full))):
                where[d].add(repo)
                detail[d].append(f"{repo}/{rel}")
                if ext in {".md", ".cff", ".bib", ".txt", ".tex"}:
                    in_prose[d] = True
    known = ledger.get("known_dois", {})
    for d, repos in sorted(where.items()):
        if not in_prose[d]:
            report.warn("doi-undocumented", sorted(repos)[0],
                        f"{d} is cited only inside source code, never in any README, .cff or "
                        f".bib: it is invisible to a reader and unverifiable by CI",
                        detail[d][:5])
    for d, label in known.items():
        if d not in where:
            report.warn("doi-missing", "-", f"ledger lists {d} ({label}) but no repo cites it")


def check_frozen_predictions(paths, ledger, report):
    fp = ledger.get("frozen_predictions", {})
    val = fp.get("delta_CP_deg")
    win = fp.get("delta_CP_window_deg")
    if val is None:
        return
    # any three-digit degree value attached to delta_CP that is not the frozen one
    bad_val = re.compile(r"(?:δ|delta)[_\s]?CP\s*[=:]\s*(\d{2,3})\s*(?:°|deg)", re.I)
    win_re = re.compile(r"\[\s*(\d{2,3})\s*(?:°|deg)?\s*,\s*(\d{2,3})\s*(?:°|deg)?\s*\]")
    seen_surfaces = 0
    for repo, root in paths.items():
        for full, rel in walk_files(root, exts={".md", ".json", ".cff"}, skip_historical=True):
            if not is_claim_surface(rel, ledger):
                continue
            for ln, line in claim_lines(read(full)):
                if is_experimental_line(line, ledger):
                    continue
                for m in bad_val.finditer(line):
                    seen_surfaces += 1
                    if int(m.group(1)) != int(val):
                        report.error("frozen-prediction", repo,
                                     f"δ_CP asserted as {m.group(1)}° on a claim surface, "
                                     f"ledger freezes {val}°", [f"{rel}:{ln}"])
                if win and re.search(r"δ_?CP|delta_?CP", line, re.I):
                    for m in win_re.finditer(line):
                        lo, hi = int(m.group(1)), int(m.group(2))
                        if 100 < lo < 400 and 100 < hi < 400 and [lo, hi] != list(win):
                            report.error("frozen-prediction", repo,
                                         f"falsification window [{lo}, {hi}] contradicts the "
                                         f"frozen window {win}", [f"{rel}:{ln}"])
    if seen_surfaces:
        report.info("frozen-prediction", "-",
                    f"δ_CP = {val}° consistent across {seen_surfaces} claim-surface assertion(s)")


def check_count_drift(paths, ledger, report):
    """Flag count-shaped claims whose number is not in the ledger."""
    c = ledger["counts"]
    valid = {c["type_I_relations"], c["total_observables"], c["type_II_relations"],
             c["type_III_relations"], c["type_IV_relations"], c["testable_observables"]}
    pat = re.compile(r"\b(\d{1,3})\s+(?:exact\s+)?(observables|relations)\b", re.I)
    ax_pat = re.compile(
        r"(?<!Lean )\b(\d{1,3})\s+(?:Lean 4 |stated |classified |published )?axioms?\b", re.I)
    conj_pat = re.compile(r"\b(\d{1,4})\s+(?:certificate\s+)?conjuncts?\b", re.I)
    for repo, root in paths.items():
        for full, rel in walk_files(root, exts={".md", ".cff", ".json"}, skip_historical=True):
            if not is_claim_surface(rel, ledger):
                continue
            for ln, line in claim_lines(read(full)):
                loc = [f"{rel}:{ln}"]
                for m in pat.finditer(line):
                    if int(m.group(1)) not in valid:
                        report.error("count-drift", repo,
                                     f"claim surface says '{m.group(0)}', not a ledger count "
                                     f"{sorted(valid)}", loc)
                for m in ax_pat.finditer(line):
                    if int(m.group(1)) != c.get("axioms"):
                        report.error("count-drift", repo,
                                     f"claim surface says '{m.group(0)}' vs ledger axioms "
                                     f"{c.get('axioms')}", loc)
                for m in conj_pat.finditer(line):
                    if int(m.group(1)) != c.get("certificate_conjuncts"):
                        report.error("count-drift", repo,
                                     f"claim surface says '{m.group(0)}' vs ledger conjuncts "
                                     f"{c.get('certificate_conjuncts')}", loc)


def check_version_pins(paths, ledger, report):
    """Claim surfaces pinning an older formal-core version than the ledger."""
    want = str(ledger.get("lean_version", ledger["framework_version"]))
    pin = re.compile(r"(?:K7-?Lean|GIFT)\s*v?(\d+\.\d+(?:\.\d+)?)", re.I)
    for repo, root in paths.items():
        for full, rel in walk_files(root, exts={".md", ".cff"}, skip_historical=True):
            if not is_claim_surface(rel, ledger):
                continue
            for ln, line in claim_lines(read(full)):
                for m in pin.finditer(line):
                    if not m.group(1).startswith(want):
                        report.error("version-pin", repo,
                                     f"claim surface pins the formal core at v{m.group(1)} "
                                     f"while the ledger is at {want}", [f"{rel}:{ln}"])


def check_axiom_taxonomy(paths, ledger, report):
    """The 15 axioms must be described the same way everywhere, not just counted."""
    desc = re.compile(r"15\s+(?:Lean 4 |classified |stated |published )?axiom(?:s|es)?\s*[,(]\s*([^)|.]{5,90})",
                      re.I)
    variants = defaultdict(list)
    for repo, root in paths.items():
        for full, rel in walk_files(root, exts={".md", ".cff", ".lean"}, skip_historical=True):
            for ln, line in claim_lines(read(full)):
                for m in desc.finditer(line):
                    key = re.sub(r"\s+", " ", m.group(1).strip().lower()).rstrip(",;")
                    variants[key].append(f"{repo}/{rel}:{ln}")
    families = defaultdict(list)
    for key, locs in variants.items():
        fam = "chain" if ("chain" in key or "main" in key or "principaux" in key) else \
              "taxonomy" if "taxonom" in key else "other"
        families[fam] += locs
    if len(families) > 1:
        report.warn("axiom-taxonomy", "-",
                    f"the 15 axioms are characterised in {len(families)} incompatible ways "
                    f"({', '.join(sorted(families))}): the count agrees but the description "
                    f"of what the 4 non-K3 axioms *are* does not",
                    [f"{fam}: {locs[0]}" for fam, locs in sorted(families.items())])


def check_old_org_links(paths, ledger, report, network=True):
    prefixes = ledger.get("old_org_prefixes", [])
    if not prefixes:
        return
    link_re = re.compile(r"github\.com/(?:" +
                         "|".join(re.escape(p.split("/")[1]) for p in prefixes) +
                         r")/[A-Za-z0-9._-]+")
    found = defaultdict(list)
    for repo, root in paths.items():
        for full, rel in walk_files(root, skip_historical=True):
            for m in set(link_re.findall(read(full))):
                found[m].append(f"{repo}/{rel}")
    for url, locs in sorted(found.items()):
        status = ""
        if network and shutil.which("curl"):
            r = run(["curl", "-sL", "-o", os.devnull, "-w", "%{http_code} %{url_effective}",
                     f"https://{url}"], timeout=60)
            status = r.stdout.strip()
        if status and not status.startswith("200"):
            report.error("stale-link", "-",
                         f"{url} no longer resolves ({status}) but is referenced in "
                         f"{len(locs)} file(s)", locs[:10])
        else:
            report.warn("stale-link", "-",
                        f"{url} still referenced in {len(locs)} file(s); currently redirects "
                        f"({status or 'not checked'}). The redirect dies if that name is reused.",
                        locs[:10])


def check_line_endings(paths, report):
    for repo, root in paths.items():
        crlf = []
        for full, rel in walk_files(root, exts={".lean", ".md", ".py"}, skip_historical=True):
            try:
                with open(full, "rb") as fh:
                    if b"\r\n" in fh.read():
                        crlf.append(rel)
            except OSError:
                pass
        if crlf:
            report.warn("line-endings", repo,
                        f"{len(crlf)} file(s) with CRLF endings: grep-based CI rules can "
                        f"diverge between machines", crlf[:10])


# ----------------------------------------------------------------------------- output

def render(report, ledger_from_file):
    order = {"ERROR": 0, "WARN": 1, "INFO": 2}
    icons = {"ERROR": "FAIL", "WARN": "WARN", "INFO": "ok  "}
    lines = ["", "=" * 74, "  ARITHMON CROSS-REPO CONSISTENCY REPORT", "=" * 74, ""]
    lines.append(f"  ledger source : {'program/LEDGER.json' if ledger_from_file else 'embedded fallback'}")
    lines.append(f"  errors        : {report.n_errors}")
    lines.append(f"  warnings      : {report.n_warns}")
    lines.append("")
    by_check = defaultdict(list)
    for f in report.findings:
        by_check[f.check].append(f)
    for check in sorted(by_check, key=lambda c: min(order[f.level] for f in by_check[c])):
        lines.append(f"-- {check} " + "-" * max(0, 68 - len(check)))
        for f in sorted(by_check[check], key=lambda f: order[f.level]):
            lines.append(f"  [{icons[f.level]}] {f.repo:9s} {f.message}")
            for loc in f.locations:
                lines.append(f"           . {loc}")
        lines.append("")
    if report.n_errors == 0:
        lines.append("  No blocking inconsistency across repos.")
    lines.append("")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="Arithmon cross-repo consistency checker")
    ap.add_argument("--local", metavar="DIR", help="reuse existing clones in DIR")
    ap.add_argument("--json", metavar="FILE", help="also write findings as JSON")
    ap.add_argument("--no-network", action="store_true", help="skip redirect resolution")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    report = Report()
    tmp = None
    try:
        if args.local:
            workdir = args.local
            paths = resolve_local(workdir)
            if not paths:
                print(f"no clones found under {workdir}", file=sys.stderr)
                return 2
        else:
            tmp = tempfile.mkdtemp(prefix="arithmon-audit-")
            workdir = tmp
            if not args.quiet:
                print("cloning org repos...")
            paths = clone_all(tmp, quiet=args.quiet)

        if args.no_network:
            report.warn("coverage", "-",
                        "deployed pages not audited (--no-network): "
                        + ", ".join(url for url, _ in SITES.values()))
        else:
            paths.update(materialize_sites(workdir, quiet=args.quiet))

        missing = [r for r in REPOS if r not in paths]
        if missing:
            report.warn("coverage", "-", f"repos not available for audit: {', '.join(missing)}")

        ledger, from_file = load_ledger(paths, report)

        check_type_arithmetic(ledger, report)
        check_lean_sorry(paths, ledger, report)
        check_axiom_count(paths, ledger, report)
        check_root_module_version(paths, ledger, report)
        check_citation_cff(paths, ledger, report)
        check_external_citation(paths, ledger, report)
        check_doi_crossrefs(paths, ledger, report)
        check_frozen_predictions(paths, ledger, report)
        check_count_drift(paths, ledger, report)
        check_version_pins(paths, ledger, report)
        check_axiom_taxonomy(paths, ledger, report)
        check_old_org_links(paths, ledger, report, network=not args.no_network)
        check_line_endings(paths, report)

        print(render(report, from_file))

        if args.json:
            with open(args.json, "w", encoding="utf-8") as fh:
                json.dump({"errors": report.n_errors, "warnings": report.n_warns,
                           "findings": [asdict(f) for f in report.findings]}, fh, indent=2)

        return 1 if report.n_errors else 0
    finally:
        if tmp and os.path.isdir(tmp):
            shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
