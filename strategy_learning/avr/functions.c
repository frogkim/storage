#include "header.h"
void check(mytype prices)
{
    int i,k;
    for(i=0; i<99840; i++)
    {
        for(k=0; k<4; k++)
        {
            if(prices[i][k] == 0)
            {
                stop = 1;
                printf("Checking error. cur : %d, ohlc :%d", i, k);
                return;
            }
        }

    }
    printf("Checking has no problem.\n");
}

void calculate(mytype prices, myavg avg, int cur)
{
    int j,k;
    int term[5] = {3, 8, 21, 55, 144};

    for(j=0; j<5; j++)
    {
        for(k=0; k<4; k++)
        {
            if(stop>0)
                return;
            calavg(prices, avg, 99840, cur, term[j], k);
        }
    }
    printf("Currency : %d, Term : %d\n", cur, j);

    return;
}

void calavg(mytype prices, myavg avg, int length, int cur, int term, int ohlc)
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
            stop = 1;
            printf("stop turned on. %d %d %d\n", cur, i, ohlc);
            return;
        }

    }
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

FILE *writefile(int index)
{
        char savefile[20] = "avg";
        char filename[14];

        switch(index)
        {
            case 0 : strcpy(filename, "eurusd.dat"); break;
            case 1 : strcpy(filename, "gbpusd.dat"); break;
            case 2 : strcpy(filename, "audusd.dat"); break;
            case 3 : strcpy(filename, "usdchf.dat"); break;
            case 4 : strcpy(filename, "usdcad.dat"); break;
            case 5 : strcpy(filename, "usdjpy.dat"); break;
            default : break;
        }

        strcat(savefile, filename);
        printf("%s\n", savefile);
        FILE *pFile = fopen(savefile,"wb");
        if( pFile == NULL )
        {
            printf("Can't open %s\n", filename);
            exit(EXIT_FAILURE);
        }
    return pFile;
}
