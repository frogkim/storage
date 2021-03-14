//+------------------------------------------------------------------+
//|                                                  pricesender.mq5 |
//|                        Copyright 2021, MetaQuotes Software Corp. |
//|                                             https://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "Copyright 2021, MetaQuotes Software Corp."
#property link      "https://www.mql5.com"
#property version   "1.00"
#import "d:\\frozenfrog\\frozendll.dll"
void	   SetTrigger(int value);
int		GetTrigger();
void  	SetValues(double open, double high, double low, double close);
double	GetValues(int index);
#import
//+------------------------------------------------------------------+
//| Script program start function                                    |
//+------------------------------------------------------------------+
//int targetLength = 24*4*5*52*12;
//int targetLength = 24*4*5*52*4;
int targetLength = 99840;



class Symbolclass
{
   string   name;
   int      copied;
   
public:
   MqlRates rates[];
            Symbolclass(void);
            ~Symbolclass(void);
   void     set(int index);
   bool     test();
   string   GetSymbolName();
   int      GetCopied();
};
//constructor
void Symbolclass::Symbolclass(void)
{
}
//destructor
void Symbolclass::~Symbolclass(void)
{
}
//member function
void Symbolclass::set(int index)
{
      switch(index)
      {
         case 0: name = "EURUSD"; break;
         case 1: name = "GBPUSD"; break;
         case 2: name = "AUDUSD"; break;
         case 3: name = "USDCHF"; break;
         case 4: name = "USDCAD"; break;
         case 5: name = "USDJPY"; break;
         default: name = ""; return;
      }
      copied = CopyRates(name,PERIOD_H1,0,targetLength,rates);
}

bool Symbolclass::test(void)
{
   if(targetLength == copied)
      return true;
   
   return false;
}
string Symbolclass::GetSymbolName(void)
{
   return name;
}
int   Symbolclass::GetCopied(void)
{
   return copied;
}
// --- main function
void OnStart()
{
   // Let C wait
   SetTrigger(100);
   // Load Symbol data
   Symbolclass symbol[6];
   for(int i=0; i<6; i++)
   {
      symbol[i].set(i);
      if(!symbol[i].test())
      {
         printf("%s is failed in copying",symbol[i].GetSymbolName());
         printf("Target bars : %i", targetLength);
         printf("Terminal max bar : %i", TerminalInfoInteger(TERMINAL_MAXBARS));
         return;
      }
      printf("%s is copied : %d",symbol[i].GetSymbolName(), symbol[i].GetCopied());
   }
   // Confirm Synchronize
   for(int i=0; i<targetLength; i++)
   {
      if(!(symbol[0].rates[i].time & 
         symbol[1].rates[i].time &
         symbol[2].rates[i].time &
         symbol[3].rates[i].time &
         symbol[4].rates[i].time &
         symbol[5].rates[i].time))
         {
            Print("Synchronize error");
            return;
         }
   }
   Print("start to copy");
   // copy price1
   for(int i=0; i<targetLength; i++)
   {
      for(int j=0; j<6; j++)
      {
         SetValues(symbol[j].rates[i].open,
                  symbol[j].rates[i].high,
                  symbol[j].rates[i].low,
                  symbol[j].rates[i].close);
         SetTrigger(1);
         while( GetTrigger() == 1 )
         {
            continue;
            // waiting for Trigger 1
         }
      }
      if( i % 1000 == 0 )
         printf("%d lines were done.", i);
   }
   SetTrigger(-1);
   printf("%d lines were done.", targetLength);
   Print("end");
}
  
void fail(int error_code)
{
   printf("Failed to read, error : %i", error_code);
}
//+------------------------------------------------------------------+
/*
   
   MqlDateTime time;
   TimeGMT(time);
   Print(2^PERIOD_H1);
   
*/