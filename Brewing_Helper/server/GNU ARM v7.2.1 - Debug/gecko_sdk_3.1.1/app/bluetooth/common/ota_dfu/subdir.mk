################################################################################
# Automatically-generated file. Do not edit!
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../gecko_sdk_3.1.1/app/bluetooth/common/ota_dfu/sl_ota_dfu.c 

OBJS += \
./gecko_sdk_3.1.1/app/bluetooth/common/ota_dfu/sl_ota_dfu.o 

C_DEPS += \
./gecko_sdk_3.1.1/app/bluetooth/common/ota_dfu/sl_ota_dfu.d 


# Each subdirectory must supply rules for building sources it contributes
gecko_sdk_3.1.1/app/bluetooth/common/ota_dfu/sl_ota_dfu.o: ../gecko_sdk_3.1.1/app/bluetooth/common/ota_dfu/sl_ota_dfu.c
	@echo 'Building file: $<'
	@echo 'Invoking: GNU ARM C Compiler'
	arm-none-eabi-gcc -g3 -gdwarf-2 -mcpu=cortex-m33 -mthumb -std=c99 '-DSL_RAIL_LIB_MULTIPROTOCOL_SUPPORT=0' '-DBGM220PC22HNA=1' '-DSL_COMPONENT_CATALOG_PRESENT=1' '-DSL_RAIL_UTIL_PA_CONFIG_HEADER=<sl_rail_util_pa_config.h>' '-DMBEDTLS_CONFIG_FILE=<mbedtls_config.h>' -I"D:\git\storage\Brewing_Helper\server" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\common\toolchain\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\service\iostream\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\emdrv\nvm3\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\service\device_init\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\sl_component\sl_protocol_crypto\src" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\common\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\mbedtls\include" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\emlib\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\protocol\bluetooth\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\sl_component\sl_cryptoacc_library\include" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\service\hfxo_manager\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\emdrv\common\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\emdrv\uartdrv\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\service\ram_interrupt_vector_init\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\sl_component\se_manager\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\sl_component\se_manager\src" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\common" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\protocol\ble" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\protocol\ieee802154" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\protocol\zwave" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\protocol\mfm" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\chip\efr32\efr32xg2x" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\sl_component\sl_alt\include" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\sl_component\sl_mbedtls_support\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\app\bluetooth\common\app_assert" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\service\sleeptimer\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\service\mpu\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\service\system\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\emdrv\dmadrv\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\emdrv\gpiointerrupt\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\plugin\rail_util_pti" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\sl_component\sl_psa_driver\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\Device\SiliconLabs\BGM22\Include" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\service\power_manager\inc" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\silicon_labs\silabs_core\memory_manager" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\emlib\init\gpio_simple" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\plugin\pa-conversions" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\radio\rail_lib\plugin\pa-conversions\efr32xg22" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\app\bluetooth\common\ota_dfu" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\sl_component\sl_mbedtls_support\config" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\util\third_party\crypto\mbedtls\library" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\bootloader" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\bootloader\api" -I"D:\git\storage\Brewing_Helper\server\gecko_sdk_3.1.1\platform\CMSIS\Include" -I"D:\git\storage\Brewing_Helper\server\config" -I"D:\git\storage\Brewing_Helper\server\autogen" -Os -Wall -Wextra -fno-builtin -ffunction-sections -fdata-sections -imacrossl_gcc_preinclude.h -mfpu=fpv5-sp-d16 -mfloat-abi=hard -c -fmessage-length=0 -MMD -MP -MF"gecko_sdk_3.1.1/app/bluetooth/common/ota_dfu/sl_ota_dfu.d" -MT"gecko_sdk_3.1.1/app/bluetooth/common/ota_dfu/sl_ota_dfu.o" -o "$@" "$<"
	@echo 'Finished building: $<'
	@echo ' '


