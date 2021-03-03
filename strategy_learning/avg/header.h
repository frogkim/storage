#ifndef HEADER_H_INCLUDED
#define HEADER_H_INCLUDED

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <windows.h>

FILE *readfile(int index);
typedef double mytype[99840][4];
typedef double myavg[99840][20];
int check(mytype prices);
int calculate(mytype prices, myavg avg, int cur);
int calavg(mytype prices, myavg avg, int length, int cur, int term, int ohlc);
#endif // HEADER_H_INCLUDED
