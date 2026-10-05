#ifndef COLLATZ_H
#define COLLATZ_H
#include <stdint.h>

#define COLLATZ_OVERFLOW UINT64_MAX

/* Numero de passos ate chegar a 1. Retorna COLLATZ_OVERFLOW se 3n+1 estourar 64 bits. */
uint64_t collatz_steps(uint64_t n);

/* Procura, em 1..limit, o numero inicial com a maior sequencia.
   Em caso de overflow, *best_n = 0. */
void collatz_longest(uint64_t limit, uint64_t *best_n, uint64_t *best_steps);

#endif
