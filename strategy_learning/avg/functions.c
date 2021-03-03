#include "header.h"
int check(mytype prices)
{
    int i,k;
    for(i=0; i<99840; i++)
    {
        for(k=0; k<4; k++)
        {
            if(prices[i][k] == 0)
            {
                printf("Checking error. cur : %d, ohlc :%d", i, k);
                return -1;
            }
        }

    }
    printf("Checking has no problem.\n");
    return 0;
}

int calculate(mytype prices, myavg avg, int cur)
{
    int j,k;
    int term[5] = {3, 8, 21, 55, 144};

    for(j=0; j<5; j++)
        for(k=0; k<4; k++)
            if(calavg(prices, avg, 99840, cur, term[j], k) < 0)
                return -1;
    printf("Currency : %d, Term : %d\n", cur, j);
    return 0;
}

int calavg(mytype prices, myavg avg, int length, int cur, int term, int ohlc)
{
    int i;
    double temp=0;
    // calculate summation until length
    for(i=0; i<term; i++)
        temp += prices[i][ohlc];

    // calculate first ratio
    avg[i][ohlc] = temp / ohlc;
    avg[i][ohlc] = (avg[i][ohlc] - prices[i][0])/ avg[i][ohlc];

    // calculate ratio and assign
    for(i=term; i<length; i++)
    {
        temp -= prices[i-term][ohlc];
        temp += prices[i][ohlc];
        avg[i][ohlc] = temp / term;
        avg[i][ohlc] = (avg[i][ohlc] - prices[i][0])/ avg[i][ohlc];

        if( temp == 0 )
        {
            printf("stop turned on. %d %d %d\n", cur, i, ohlc);
            return -1;
        }
    }
    return 0;
}


FILE *readfile(int index)
{
        char filename[16];
        switch(index)
        {
            case 0 : strcpy(filename, "eurusd.dat"); printf("%s\n", filename); break;
            case 1 : strcpy(filename, "gbpusd.dat"); printf("%s\n", filename); break;
            case 2 : strcpy(filename, "audusd.dat"); printf("%s\n", filename); break;
            case 3 : strcpy(filename, "usdchf.dat"); printf("%s\n", filename); break;
            case 4 : strcpy(filename, "usdcad.dat"); printf("%s\n", filename); break;
            case 5 : strcpy(filename, "usdjpy.dat"); printf("%s\n", filename); break;
            default : break;
        }
        FILE *pFile = fopen(filename,"rb");
        if( pFile == NULL )
        {
            printf("Can't open %s\n", filename);
            exit(EXIT_FAILURE);
        }
    return pFile;
}
