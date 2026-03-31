# IOE Project (Fulfillment Centers)

## Status

- [x] IP formulation complete
- [ ] Simulated Dataset
- [ ] Code
- [ ] Real dataset

---

## Input File Format

```
n k1 k2 C1 C2 L
0 x0 y0 r0
1 x1 y1 r1
...
```

**Line 1 — parameters:**
- `n`  : number of cities
- `k1` : max number of local FCs
- `k2` : max number of regional FCs
- `C1` : local FC capacity (items/day)
- `C2` : regional FC capacity (items/day)
- `L`  : regional to local link cost factor

**Lines 2 to n+1 — cities:**
- city index, x coordinate, y coordinate, demand rate `ri` (items/day)

---