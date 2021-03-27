#include "em_common.h"
#include "sl_app_assert.h"
#include "sl_bluetooth.h"
#include "gatt_db.h"
#include "app.h"

#include "sl_emlib_gpio_init_BTN_config.h"
#include "sl_emlib_gpio_init_LED_config.h"
#include "em_cmu.h"
#include "em_gpio.h"
#include "em_letimer.h"
#include "em_prs.h"
#include "em_iadc.h"
#include "stdio.h"
#include "stdlib.h"
#include "math.h"
//#include "printf.h"

// Set CLK_ADC to 10kHz (this corresponds to a sample rate of 1ksps)
#define CLK_SRC_ADC_FREQ         5000000  // CLK_SRC_ADC; largest division is by 4
#define CLK_ADC_FREQ             1000000  // CLK_ADC; IADC_SCHEDx PRESCALE has 10 valid bits
#define ADC_DONE_SIGNAL             1

// When changing GPIO port/pins above, make sure to change xBUSALLOC macro's
// accordingly.
#define IADC_INPUT_0_BUS          CDBUSALLOC
#define IADC_INPUT_0_BUSALLOC     GPIO_CDBUSALLOC_CDEVEN0_ADC0
#define IADC_INPUT_1_BUS          CDBUSALLOC
#define IADC_INPUT_1_BUSALLOC     GPIO_CDBUSALLOC_CDODD0_ADC0

// IADC input GPIO port/pin configuration
#define SAMPLING_FREQ_HZ        1
#define PRS_CHANNEL_LETIMER_IADC 1

// System Setting
static void LETIMER_init(void);
static void PRS_init(void);
static void ADC_init(void);
void LETIMER0_IRQHandler(void);

static uint8_t advertising_set_handle = 0xff;
static uint8_t connection_handle;
static volatile uint32_t scanResult[3];

// custom function prototype
static void ResistCalc(void);
static float GetTemp(void);
static float GetEthanol(float tmp);
static void SetAdvData(void);
static void SetScanData(void);
// custom global variable
typedef struct{
    uint16_t year;
    uint8_t month;
    uint8_t day;
    uint8_t hour;
    uint8_t minute;
} datetime;

uint16_t cnt;
float tempArr[10];
float ethnArr[10];
float tempResist;
float ethnResist;
float temparature;
float ethanol;
uint8_t letsw;
uint8_t sampleCollect;
datetime TIME;
uint16_t curTime;
float tempRecord[1008]; // 6 weeks = 6 * 7 * 24 hours (1008 hours)
float ethnRecord[1008];
/**************************************************************************//**
 * Application Init.
 *****************************************************************************/
SL_WEAK void app_init(void)
{
  LETIMER_init();
  PRS_init();
  ADC_init();
  cnt = 0;
  tempResist = 0.0;
  ethnResist = 0.0;
  temparature = 0.0;
  ethanol = 0.0;
  memset(tempArr, 0, sizeof(float)*10);
  memset(ethnArr, 0, sizeof(float)*10);
  memset(tempRecord, 0, sizeof(float)*1008);
  memset(ethnRecord, 0, sizeof(float)*1008);

  TIME.year = 0;
  TIME.month = 0;
  TIME.day = 0;
  TIME.hour = 0;
  TIME.minute = 0;
  curTime = 0;
  letsw = 0;
  sampleCollect = 0;

  LETIMER_Enable(LETIMER0, true);
  IADC_command(IADC0, iadcCmdStartScan);

  printf("\napp_init finished\n");
  printf("collecting sensor data samples [----------]\b\b\b\b\b\b\b\b\b\b\b");
}

/**************************************************************************//**
 * Application Process Action.
 *****************************************************************************/
SL_WEAK void app_process_action(void)
{
    IADC_command(IADC0, iadcCmdStartSingle);              // start AC conversion
    while (!(IADC0->IF & IADC_IF_SINGLEDONE)){}           // wait for conversion end

    if(!letsw){
            return;
    }
    letsw = 0;
    ResistCalc();
    cnt++;
    if(!sampleCollect){
            if(cnt<10){
                    printf("O");
            } else{
                    printf("O");
                    sampleCollect = 1;
            }
    } else {
            printf("\nADC0: %0.4f C,  ADC1: %0.4f", temparature, ethanol);
    }


}
// GPIO_PinOutSet(SL_EMLIB_GPIO_INIT_LED_PORT, SL_EMLIB_GPIO_INIT_LED_PIN);
// GPIO_PinOutClear(SL_EMLIB_GPIO_INIT_LED_PORT, SL_EMLIB_GPIO_INIT_LED_PIN);

/**************************************************************************//**
 * Bluetooth stack event handler.
 * @param[in] evt Event coming from the Bluetooth stack.
 *****************************************************************************/
void sl_bt_on_event(sl_bt_msg_t *evt)
{
    switch (SL_BT_MSG_ID(evt->header)) {
        case sl_bt_evt_system_boot_id:
            sl_bt_advertiser_create_set(&advertising_set_handle);
            SetAdvData();
            SetScanData();
            sl_bt_advertiser_set_timing(advertising_set_handle, 1600, 1600, 0, 0);
            //sl_bt_advertiser_start(advertising_set_handle, advertiser_general_discoverable, advertiser_connectable_scannable);
            sl_bt_advertiser_start(advertising_set_handle, sl_bt_advertiser_general_discoverable, sl_bt_advertiser_connectable_scannable);

        break;

        case sl_bt_evt_connection_opened_id:                                    // a new connection was opened
            connection_handle = evt->data.evt_connection_opened.connection;
        break;

        case sl_bt_evt_connection_closed_id:                                                // connection was closed
            //sl_bt_advertiser_start(advertising_set_handle, advertiser_general_discoverable, advertiser_connectable_scannable);
            sl_bt_advertiser_start(advertising_set_handle, sl_bt_advertiser_general_discoverable, sl_bt_advertiser_connectable_scannable);
        break;

        case sl_bt_evt_system_external_signal_id:

        break;

        default:
        break;
    }
}

static void SetAdvData(void)
{
    typedef struct {
        uint8_t length;
        uint8_t flags;
        uint8_t data;
    } advdataSTR;
    advdataSTR advdata = {0x02, 0x01, 0x06};
    sl_bt_advertiser_set_data(advertising_set_handle, 0, sizeof(advdataSTR), (uint8_t*)&advdata);
}

static void SetScanData(void){
    typedef struct {
        uint8_t name_len;
        uint8_t name_type;
        char    name[15];
    } scandataSTR;
    scandataSTR scandata;
    scandata.name_len = 15;
    scandata.name_type = 0x09;
    strncpy(scandata.name, "Highway start!", 14);
    sl_bt_advertiser_set_data(advertising_set_handle, 1, sizeof(scandataSTR), (uint8_t*)&scandata);
}

static void LETIMER_init(void)
{
    LETIMER_Init_TypeDef init = LETIMER_INIT_DEFAULT;
    CMU_ClockSelectSet(cmuClock_EM23GRPACLK, cmuSelect_LFXO);
    CMU_ClockEnable(cmuClock_LETIMER0, true);
    init.ufoa0 = letimerUFOAPulse;
    init.enable = true;
    init.comp0Top = true;
    init.topValue = CMU_ClockFreqGet(cmuClock_LETIMER0) / SAMPLING_FREQ_HZ;
    init.debugRun = false;
    init.repMode = letimerRepeatFree;
    LETIMER_Init(LETIMER0, &init);
    LETIMER_IntEnable(LETIMER0, LETIMER_IEN_UF); // for interuption
    NVIC_EnableIRQ(LETIMER0_IRQn);
}

static void PRS_init(void)
{
    CMU_ClockEnable(cmuClock_PRS, true);
    PRS_SourceAsyncSignalSet(0, PRS_ASYNC_CH_CTRL_SOURCESEL_LETIMER0, prsSignalLETIMER0_CH0);
    PRS_Combine(0, 0, prsLogic_A);
    PRS_ConnectConsumer(0, prsTypeAsync, prsConsumerIADC0_SCANTRIGGER);
}

static void ADC_init(void)
{
    IADC_Init_t init = IADC_INIT_DEFAULT;
    IADC_AllConfigs_t initAllConfigs = IADC_ALLCONFIGS_DEFAULT;
    IADC_InitScan_t initScan = IADC_INITSCAN_DEFAULT;
    IADC_ScanTable_t initScanTable = IADC_SCANTABLE_DEFAULT;

    CMU_ClockSelectSet(cmuClock_IADCCLK, cmuSelect_FSRCO);  // FSRCO - 20MHz
    CMU_ClockEnable(cmuClock_IADC0, true);
    CMU_ClockEnable(cmuClock_GPIO, true);

    IADC_reset(IADC0);
    init.warmup = iadcWarmupNormal;
    init.srcClkPrescale = IADC_calcSrcClkPrescale(IADC0, CLK_SRC_ADC_FREQ, 0);
    initAllConfigs.configs[0].reference = iadcCfgReferenceVddx;
    initAllConfigs.configs[0].adcClkPrescale = IADC_calcAdcClkPrescale(IADC0, CLK_ADC_FREQ, 0, iadcCfgModeNormal, init.srcClkPrescale);
    initScan.triggerAction = iadcTriggerActionOnce;
    initScan.triggerSelect = iadcTriggerSelPrs0PosEdge;
    initScan.showId = true;

    // === Pin Input Config ============
    // Configure Input sources for single ended conversion
    initScanTable.entries[0].posInput = iadcPosInputPortCPin0;
    initScanTable.entries[0].negInput = iadcNegInputGnd;
    initScanTable.entries[0].includeInScan = true;

    initScanTable.entries[1].posInput = iadcPosInputPortDPin3;
    initScanTable.entries[1].negInput = iadcNegInputGnd;
    initScanTable.entries[1].includeInScan = true;

    // Allocate the analog bus for IADC0 input
    GPIO->CDBUSALLOC |= GPIO_CDBUSALLOC_CDEVEN0_ADC0;
    GPIO->CDBUSALLOC |= GPIO_CDBUSALLOC_CDODD0_ADC0;

    IADC_init(IADC0, &init, &initAllConfigs);
    IADC_initScan(IADC0, &initScan, &initScanTable);

    IADC_clearInt(IADC0, _IADC_IF_MASK);
    IADC_enableInt(IADC0, IADC_IEN_SCANTABLEDONE);
    NVIC_ClearPendingIRQ(IADC_IRQn);
    NVIC_EnableIRQ(IADC_IRQn);
}

void LETIMER0_IRQHandler(void)
{
  LETIMER_IntClear(LETIMER0, LETIMER_IEN_UF);
  letsw = 1;
}

void IADC_IRQHandler(void)
{
    IADC_Result_t result = {0, 0};
    IADC_clearInt(IADC0, IADC_IF_SCANTABLEDONE);
    while(IADC_getScanFifoCnt(IADC0)) {                                             // read Data from ADC FIFO
        result = IADC_pullScanFifoResult(IADC0);
        scanResult[result.id] = result.data;
    }
    sl_bt_external_signal(ADC_DONE_SIGNAL);
}


/**************************************************************************//**
 * Custom Functions
 *****************************************************************************/
static void ResistCalc(void)
{
    float tempCurrent = (float) scanResult[0];
    float ethnCurrent = (float) scanResult[1];

    if(!sampleCollect)
        {
            tempArr[cnt] = tempCurrent;
            ethnArr[cnt] = ethnCurrent;
            return;
        }
    int i, k, total;
    total = 10;
    k = total - 1;
    tempArr[k] = tempCurrent;
    ethnArr[k] = ethnCurrent;

    tempResist = 0;
    ethnResist = 0;
    for(i=0; i<total; i++)
        {
            tempResist += tempArr[i];
            ethnResist += ethnArr[i];
        }
    tempResist = tempResist / total;
    ethnResist = ethnResist / total;

    for(i=total-1; i>0; i--)
        {
            k = i - 1;
            tempArr[k] = tempArr[i];
            ethnArr[k] = ethnArr[i];
        }
    temparature = GetTemp();
    ethanol = GetEthanol(temparature);
}

static float GetTemp(void)
{
    float ADCMAX = 4095.0;

    float TEMPARATURENOMINAL = 25.0;
    float Beta = 1.0 / 3950.0;
    float KELVIN = 273.15;


    float tmp = ADCMAX / tempResist - 1;
    tmp = Beta * log(1.0 / tmp);
    tmp += 1.0 / (TEMPARATURENOMINAL + KELVIN);
    tmp = 1.0 / tmp;
    tmp -= KELVIN;
    return tmp;
}

static float GetEthanol(float tmp)
{
    float ADCMAX = 4095.0;
    float v = ADCMAX / ethnResist - 1;
    return v;
}

