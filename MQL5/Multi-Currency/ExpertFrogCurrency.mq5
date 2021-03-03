//+------------------------------------------------------------------+
//|                                                   ExpertMACD.mq5 |
//|                   Copyright 2009-2017, MetaQuotes Software Corp. |
//|                                              http://www.mql5.com |
//+------------------------------------------------------------------+
#property copyright "2009-2017, MetaQuotes Software Corp."
#property link      "http://www.mql5.com"
#property version   "1.00"
//+------------------------------------------------------------------+
//| Include                                                          |
//+------------------------------------------------------------------+
#include <Expert\ExpertMultiCurrency.mqh>
#include <Expert\Signal\SignalMACD.mqh>
#include <Expert\Trailing\TrailingNone.mqh>
#include <Expert\Money\MoneyNone.mqh>
//+------------------------------------------------------------------+
//| Inputs                                                           |
//+------------------------------------------------------------------+
//--- inputs for expert
int          Expert_MagicNumber          =10986645;
bool         Expert_EveryTick            =false;
double       equity;
MqlDateTime  frtime;
bool         stop;

//+------------------------------------------------------------------+
//| Global expert object                                             |
//+------------------------------------------------------------------+
struct SYMBOLSTRURTURE
{
   string name;
   CExpert ExtExpert;
} SYMBOLSTR[6];

//CExpert ExtExpert[6];
//+------------------------------------------------------------------+
//| Initialization function of the expert                            |
//+------------------------------------------------------------------+
int OnInit(void)
  {

      TimeGMT(frtime);
      equity = AccountInfoDouble(ACCOUNT_EQUITY);
      stop = false;

      SYMBOLSTR[0].name = "EURUSD";
      SYMBOLSTR[1].name = "GBPUSD";
      SYMBOLSTR[2].name = "AUDUSD";
      SYMBOLSTR[3].name = "USDCHF";
      SYMBOLSTR[4].name = "USDCAD";
      SYMBOLSTR[5].name = "USDJPY";

      //--- Initializing expert
      for(int i=0; i<6; i++)
      {
            if(!SYMBOLSTR[i].ExtExpert.Init(SYMBOLSTR[i].name,PERIOD_H1,Expert_EveryTick,Expert_MagicNumber))
              {
               //--- failed
               printf(__FUNCTION__+": error initializing expert");
               return(-1);
              }
         //--- Signal setting
            int result = SignalSetting(i);
            if(result < 0)
               return(result);
         //--- Creation of trailing object
            CTrailingNone *trailing=new CTrailingNone;
            if(trailing==NULL)
              {
               //--- failed
               printf(__FUNCTION__+": error creating trailing");
               return(-5);
              }
         //--- Add trailing to expert (will be deleted automatically))
            if(!SYMBOLSTR[i].ExtExpert.InitTrailing(trailing))
              {
               //--- failed
               printf(__FUNCTION__+": error initializing trailing");
               return(-6);
              }
         //--- Set trailing parameters
         //--- Check trailing parameters
            if(!trailing.ValidationSettings())
              {
               //--- failed
               printf(__FUNCTION__+": error trailing parameters");
               return(-7);
              }
            CMoneyNone *money=new CMoneyNone;
            if(money==NULL)
              {
               //--- failed
               printf(__FUNCTION__+": error creating money");
               return(-8);
              }
         //--- Creation of money object
         //--- Add money to expert (will be deleted automatically))
            if(!SYMBOLSTR[i].ExtExpert.InitMoney(money))
              {
               //--- failed
               printf(__FUNCTION__+": error initializing money");
               return(-9);
              }
            //--- Set money parameters
            //--- Check money parameters
            if(!money.ValidationSettings())
                 {
                  //--- failed
                  printf(__FUNCTION__+": error money parameters");
                  return(-10);
                 }
         //--- Tuning of all necessary indicators
             if(!SYMBOLSTR[i].ExtExpert.InitIndicators())
                 {
                 //--- failed
                    printf(__FUNCTION__+": error initializing indicators");
                    return(-11);
                 }
      } // end for i
//multi experts    
   return(INIT_SUCCEEDED);
  }
//+------------------------------------------------------------------+
//| Deinitialization function of the expert                          |
//+------------------------------------------------------------------+
void OnDeinit(const int reason)
  {
   for(int i=0; i<6; i++)
      SYMBOLSTR[i].ExtExpert.Deinit();
  }
//+------------------------------------------------------------------+
//| Function-event handler "tick"                                    |
//+------------------------------------------------------------------+
void OnTick(void)
  {
   if(stop) return;
   equity = MathMax(AccountInfoDouble(ACCOUNT_EQUITY), equity);
   if(AccountInfoDouble(ACCOUNT_EQUITY) / equity < 0.5)
   {
         stop = true;
         SYMBOLSTR[0].ExtExpert.Close();
         return;
   }   
   
   // signal calculate
   double other_signals[6] = { 0 };
   other_signals[0] = SYMBOLSTR[0].ExtExpert.Processing(0);
   
   if(other_signals[0] < -1e+50)
      return;
   /* multi trading
   for(int i=0; i<6; i++)
      m_other_signals[i] = SYMBOLSTR[i].ExtExpert.Processing(i);
   */
   //Print(other_signals[0]);
   SYMBOLSTR[0].ExtExpert.PositionProcessing(0, other_signals);  // m_other_signal is useless in test1
   // Time controlled trading 
/* 
   TimeGMT(frtime);
   if(frtime.hour > 21)
   {
      equity = AccountInfoDouble(ACCOUNT_BALANCE);
      for(int i=0; i<6; i++)
      {
         if(ExtExpert[i].GetStop())
         {
            ExtExpert[i].SetStop(false);
            Print("EA is restart.");
         }
      }
   }
   if(frtime.hour < 21)
   {
      if(AccountInfoDouble(ACCOUNT_EQUITY) / equity < 0.8)
      {
         stop = true;
         ExtExpert[i].Close();
         return;
      }   
      double m_other_signals[6] = { 0 };
      for(int i=0; i<6; i++)
         m_other_signals[i] = SYMBOLSTR[i].ExtExpert.Processing(0);
         SYMBOLSTR[i].ExtExpert.PositionProcessing(i, m_other_signals);  // m_other_signal is useless in test1
*/      
  }
//+------------------------------------------------------------------+
//| Function-event handler "trade"                                   |
//+------------------------------------------------------------------+
void OnTrade(void)
  {
   for(int i=0; i<6; i++)
      SYMBOLSTR[i].ExtExpert.OnTrade();
  }
//+------------------------------------------------------------------+
//| Function-event handler "timer"                                   |
//+------------------------------------------------------------------+
void OnTimer(void)
  {
   for(int i=0; i<6; i++)
      SYMBOLSTR[i].ExtExpert.OnTimer();
  }
//+------------------------------------------------------------------+
double  OnTester(void)
{
//--- custom criterion optimization value (the higher, the better) 
   if(stop) return 0;
   
   double avg_p = 0;
   double deal_profit = 0.0;
   double deal_volume = 0.0;
   uint p_result = 0;
   uint t_result = HistoryDealsTotal();
   if(t_result == 0)
      return 0;
   ulong ticket_history_deal=0; 
   
   for(uint i=0;i<t_result;i++) 
   { 
      if((ticket_history_deal=HistoryDealGetTicket(i))>0) 
      { 
         deal_profit =HistoryDealGetDouble(ticket_history_deal,DEAL_PROFIT); 
         deal_volume =HistoryDealGetDouble(ticket_history_deal,DEAL_VOLUME);
      }
      else
         return -1;
      if(deal_volume < 0.01)
         continue;
      if(deal_profit > 0)
         p_result++;
      avg_p += deal_profit / deal_volume;
   }
   
   if(t_result < 3000)
      return 0.0;
   
   avg_p /= t_result;
   return avg_p * ((double)p_result/(double)t_result);
}
/*
   int    min_trade = 250;
   double ret=0.0; 
   double array[]; 
   double trades_volume; 
   GetTradeResultsToArray(array,trades_volume); 
   int trades=ArraySize(array); 
   if(trades < min_trade)
      return(0);
      
   double t_profit = 0; // total count
   double p_profit = 0; // profit position count only
   for(int i=0; i<trades; i++)
   {
      if(array[i] > 0)
      {
         t_profit += array[i];
         p_profit += array[i];
      }
      else
         t_profit -= array[i];
   }

   double pass_rate =p_profit / t_profit;

   // Test pass rate
   //   if(pass_rate < 0.6)
   //       return(0.0);

   ret = AccountInfoDouble(ACCOUNT_EQUITY) * pass_rate;
   return(ret);
*/


//--- By example
bool GetTradeResultsToArray(double &pl_results[],double &volume) 
  { 
//--- request the complete trading history 
   if(!HistorySelect(0,TimeCurrent())) 
      return (false); 
   uint total_deals=HistoryDealsTotal(); 
   volume=0; 
//--- set the initial size of the array with a margin - by the number of deals in history 
   ArrayResize(pl_results,total_deals); 
//--- counter of deals that fix the trading result - profit or loss 
   int counter=0; 
   ulong ticket_history_deal=0; 
//--- go through all deals 
   for(uint i=0;i<total_deals;i++) 
     { 
      //--- select a deal  
      if((ticket_history_deal=HistoryDealGetTicket(i))>0) 
        { 
         ENUM_DEAL_ENTRY deal_entry  =(ENUM_DEAL_ENTRY)HistoryDealGetInteger(ticket_history_deal,DEAL_ENTRY); 
         long            deal_type   =HistoryDealGetInteger(ticket_history_deal,DEAL_TYPE); 
         double          deal_profit =HistoryDealGetDouble(ticket_history_deal,DEAL_PROFIT); 
         double          deal_volume =HistoryDealGetDouble(ticket_history_deal,DEAL_VOLUME); 
         //--- we are only interested in trading operations         
         if((deal_type!=DEAL_TYPE_BUY) && (deal_type!=DEAL_TYPE_SELL)) 
            continue; 
         //--- only deals that fix profits/losses 
         if(deal_entry!=DEAL_ENTRY_IN) 
           { 
            //--- write the trading result to the array and increase the counter of deals 
            pl_results[counter]=deal_profit; 
            volume+=deal_volume; 
            counter++; 
           } 
        } 
     } 
//--- set the final size of the array 
   ArrayResize(pl_results,counter); 
   return (true); 
  } 
//+------------------------------------------------------------------+


//+------------------------------------------------------------------+
int SignalSetting(int symnum)
{
//--------------------------------------------------------------------+
      CExpertSignal *signal;
      for(int i=1; i<Signals; i++)
      {
         switch(i)
         {
            case 1: signal = new CSignalAC; break;
            case 2: signal = new CSignalAMA; break;
            case 3: signal = new CSignalAO; break;
            case 4: signal = new CSignalBearsPower; break;
            case 5: signal = new CSignalBullsPower; break;
            case 6: signal = new CSignalCCI; break;
            case 7: signal = new CSignalDEMA; break;
            case 8: signal = new CSignalDEMA; break;
            case 9: signal = new CSignalEnvelopes; break;
            case 10: signal = new CSignalFrAMA; break;
            case 11: signal = new CSignalITF; break;
            case 12: signal = new CSignalMA; break;
            case 13: signal = new CSignalMACD; break;
            case 14: signal = new CSignalRSI; break;
            case 15: signal = new CSignalRSI; break;
            case 16: signal = new CSignalSAR; break;
            case 17: signal = new CSignalStoch; break;
            case 18: signal = new CSignalTEMA; break;
            case 19: signal = new CSignalTriX; break;
            case 20: signal = new CSignalWPR; break;
            default: signal = NULL; break;
         }
         
         if(signal==NULL)
           {
            //--- failed
            printf(__FUNCTION__+": error creating signal");
            return(-2);
           }
      //--- Add signal to expert (will be deleted automatically))
         if(!SYMBOLSTR[symnum].ExtExpert.InitSignal(signal, i))
           {
            //--- failed
            printf(__FUNCTION__+": error initializing signal");
            
            return(-3 + i*100);
           }
         //--- Check signal parameters
         if(!signal.ValidationSettings())
           {
            //--- failed
            printf(__FUNCTION__+": error signal parameters");
            return(-4);
           }
   }
    return(0);
//--------------------------------------------------------------------+
}

