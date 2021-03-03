#include "header.h"

int main()
{
    int i,j;
    FILE *pFile[6];
    for(i=0; i<6; i++)
        pFile[i] = readfile(i);

    mytype *prices;
    prices = (mytype*) malloc(sizeof(mytype)*6);
    memset(prices, 0, sizeof(mytype)*6);

    myavg *avg;
    avg = (myavg*) malloc(sizeof(myavg)*6);
    memset(avg, 0, sizeof(myavg)*6);

    for(i=0; i<6; i++)
    {
        fread(prices[i], sizeof(mytype), 1, pFile[i]);
        if( ( check(prices[i])+calculate(prices[i], avg[i], i) )<0 )
            return -1;
    }

    char* savefile = "avg.dat";
    printf("%s\n", savefile);
    FILE *pWFile = fopen(savefile,"wb");
    for(i=144; i<99840-144; i++)
        for(j=0;j<6;j++)
            fwrite(&avg[j], sizeof(double), 20, pWFile);

    for(i=0; i<6; i++)
        fclose(pFile[i]);
    fclose(pWFile);
    free(prices);
    free(avg);
    return(0);
}
