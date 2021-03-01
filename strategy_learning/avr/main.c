#include "header.h"

int main()
{
    stop = 0;
    int i;
    FILE *pFile[6];
    FILE *pWFile[6];
    for(i=0; i<6; i++)
    {
        pFile[i] = readfile(i);
        pWFile[i] = writefile(i);
    }

    mytype *prices;
    prices = (mytype*) malloc(sizeof(mytype)*6);
    memset(prices, 0, sizeof(mytype)*6);

    myavg *avg;
    avg = (myavg*) malloc(sizeof(myavg)*6);
    memset(avg, 0, sizeof(myavg)*6);

    for(i=0; i<6; i++)
    {
        fread(&prices[i], sizeof(mytype), 1, pFile[i]);
        check(&prices[i]);
        calculate(&prices[i], &avg[i], i);
        if(stop>0)
            return -1000;
        fwrite(&avg[i], sizeof(myavg), 1, pWFile[i]);

    }

    for(i=0; i<6; i++)
    {
        fclose(pFile[i]);
        fclose(pWFile[i]);
    }
    return(0);
}
