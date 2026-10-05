#include "collatz.h"

uint64_t collatz_steps(uint64_t n) {
    uint64_t steps = 0;
    while (n != 1) {
        if (n & 1) {
            if (n > (UINT64_MAX - 1) / 3) return COLLATZ_OVERFLOW;
            n = 3 * n + 1;
        } else {
            n >>= 1;
        }
        steps++;
    }
    return steps;
}

void collatz_longest(uint64_t limit, uint64_t *best_n, uint64_t *best_steps) {
    *best_n = 1;
    *best_steps = 0;
    for (uint64_t n = 2; n <= limit; n++) {
        uint64_t s = collatz_steps(n);
        if (s == COLLATZ_OVERFLOW) { *best_n = 0; return; }
        if (s > *best_steps) { *best_steps = s; *best_n = n; }
    }
}
