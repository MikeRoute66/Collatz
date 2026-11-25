# Collatz

Small toolkit and HTML explorer for finite experiments around the Collatz
conjecture.

The conjecture says that repeatedly applying this rule eventually reaches `1`
for every positive integer:

- even `n`: `n / 2`
- odd `n`: `3n + 1`

This repository does not prove the conjecture. The browser front end focuses on
the odd-only trajectory graph, collapsing even values out of the displayed
sequence.

## Usage

Open the HTML front end:

```bash
./collatz
```

The launcher prints a local URL, opens it in your browser when possible, and
keeps serving the page until you press `Ctrl+C`.

In the Inverse Collatz view, set a depth and select **Draw** to watch the
tree grow one layer at a time. **Draw** reuses the layers built in the
current tab, even after you view a shallower depth. **Stop** pauses
generation. Select **Draw** again to continue from where you stopped.
Drag, scroll, or use the arrow keys to pan. Use **Horizontal position**
and **Top depth** to jump directly across wide or deep trees. Doubling
chains run vertically. Horizontal forks widen as layers are added,
leaving room for shorter descendant forks within their span.
Select **Fit Tree** to see the full layout, then zoom in to read the
fixed-size labels. Hover over a node to see its exact integer value.

Run the command-line tools:

```bash
python3 collatz.py sequence 27
python3 collatz.py stats 27
python3 collatz.py verify 100000
python3 collatz.py records 100000
```

## Tests

```bash
python3 -m unittest
```
