#include "sl_emlib_gpio_simple_init.h"
#include "sl_emlib_gpio_init_BTN_config.h"
#include "sl_emlib_gpio_init_LED_config.h"
#include "em_gpio.h"
#include "em_cmu.h"

void sl_emlib_gpio_simple_init(void)
{
  CMU_ClockEnable(cmuClock_GPIO, true);
  GPIO_PinModeSet(SL_EMLIB_GPIO_INIT_BTN_PORT,
                  SL_EMLIB_GPIO_INIT_BTN_PIN,
                  SL_EMLIB_GPIO_INIT_BTN_MODE,
                  SL_EMLIB_GPIO_INIT_BTN_DOUT);

  GPIO_PinModeSet(SL_EMLIB_GPIO_INIT_LED_PORT,
                  SL_EMLIB_GPIO_INIT_LED_PIN,
                  SL_EMLIB_GPIO_INIT_LED_MODE,
                  SL_EMLIB_GPIO_INIT_LED_DOUT);
}
