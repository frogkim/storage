; Peripheral base addresses
PRS		EQU	0x400E6000	; Peripheral Reflex System
RMU		EQU	0x400E5000 	; Reset Management Unit
CMU		EQU	0x400E4000	; Clock Management Unit
EMU		EQU	0x400E3000	; Energy Management Unit
LDMA		EQU	0x400E2000 	; Linked Direct Memory Access 
FPUEH		EQU	0x400E1000	;
MSC		EQU	0x400E0000	; Memory System Controller
LESENSE		EQU	0x40055000 	; Low Enegry Sensor Interface
WDOG1		EQU	0x40052400 	; Watchdog Timer1
WDOG0		EQU	0x40052000	; Watchdog Timer0
PCNT2		EQU	0x4004E800	; Pulse Counter2
PCNT1		EQU	0x4004E400	; Pulse Counter1
PCNT0		EQU	0x4004E000	; Pulse Counter0
LEUART0		EQU	0x4004A000 	; Low Enegry UART
LETIMER0	EQU	0x40046000 	; Low Energy Timer
RTCC		EQU	0x40042000 	; Real Time Clock
SMU		EQU	0x40022000
CSEN		EQU	0x4001F000
CRYOTIMER	EQU	0x4001E000
TRNG0		EQU	0x4001D000	; True Random Number Generator	
GPCRC		EQU	0x4001C000	; CRC engine	
WTIMER1		EQU	0x4001A400 	; TIMER1 module
WTIMER0		EQU	0x4001A000 	; TIMER0 module
TIMER1		EQU	0x40018400	; TIMER1 module
TIMER0		EQU	0x40018000	; TIMER0 module
USART3		EQU	0x40010C00	; USART3 module
USART2		EQU	0x40010800	; USART2 module
USART1		EQU	0x40010400 	; USART1 module
USART0		EQU	0x40010000 	; USART0 module
I2C1		EQU	0x4000C400	; I2C1 module
I2C0		EQU	0x4000C000 	; I2C0 module
GPIO		EQU	0x4000A000 	; GPIO module
VDAC0		EQU	0x40008000 	; DAC0 module
IDAC0		EQU	0x40006000	; Current DAC0 module
ADC0		EQU	0x40002000 	; ADC0 module
ACMP1		EQU	0x40000400 	; Analog comparator 1
ACMP0		EQU	0x40000000 	; Analog Comparator 0


;-------- CMU registers --------------------------------------------------------------------
CMU_CTRL 	EQU	0x000 		; CMU Control Register
CMU_HFRCOCTRL 	EQU 	0x010 		; HFRCO Control Register
CMU_AUXHFRCOCTRL EQU	0x018		; RW AUXHFRCO Control Register
CMU_LFRCOCTRL 	EQU	0x020 		; LFRCO Control Register
CMU_HFXOCTRL 	EQU 	0x024 		; HFXO Control Register
CMU_HFXOSTARTUPCTRL EQU	0x02C 		; HFXO Startup Control
CMU_HFXOSTEADYSTATECTRL EQU 0x030 	; RW HFXO Steady State Control
CMU_HFXOTIMEOUTCTRL EQU	0x034 		; HFXO Timeout Control
CMU_LFXOCTRL 	EQU	0x038 		; LFXO Control Register
CMU_CALCTRL 	EQU	0x050 		; Calibration Control Register
CMU_CALCNT 	EQU	0x054 		; Calibration Counter Register
CMU_OSCENCMD 	EQU	0x060 		; Oscillator Enable/Disable Command Register
CMU_CMD 	EQU	0x064 		; Command Register
CMU_DBGCLKSEL 	EQU	0x070 		; Debug Trace Clock Select
CMU_HFCLKSEL 	EQU	0x074 		; High Frequency Clock Select Command Register
CMU_LFACLKSEL 	EQU	0x080 		; Low Frequency A Clock Select Register
CMU_LFBCLKSEL 	EQU	0x084 		; Low Frequency B Clock Select Register
CMU_LFECLKSEL 	EQU	0x088 		; Low Frequency E Clock Select Register
CMU_STATUS 	EQU	0x090 		; Status Register
CMU_HFCLKSTATUS EQU	0x094 		; HFCLK Status Register
CMU_HFXOTRIMSTATUS EQU	0x09C 		; HFXO Trim Status
CMU_IF 		EQU	0x0A0 		; Interrupt Flag Register
CMU_IFS 	EQU	0x0A4 		; Interrupt Flag Set Register
CMU_IFC 	EQU	0x0A8 		; Interrupt Flag Clear Register
CMU_IEN 	EQU	0x0AC 		; Interrupt Enable Register
CMU_HFBUSCLKEN0 EQU	0x0B0 		; High Frequency Bus Clock Enable Register 0
CMU_HFPERCLKEN0 EQU	0x0C0 		; High Frequency Peripheral Clock Enable Register 0
CMU_HFRADIOALTCLKEN0 EQU 0x0CC 		; High Frequency Alternate Radio Peripheral Clock Enable Register 0
CMU_LFACLKEN0 	EQU	0x0E0 		; Low Frequency a Clock Enable Register 0 (Async Reg)
CMU_LFBCLKEN0 	EQU	0x0E8 		; Low Frequency B Clock Enable Register 0 (Async Reg)
CMU_LFECLKEN0 	EQU	0x0F0 		; Low Frequency E Clock Enable Register 0 (Async Reg)
CMU_HFPRESC 	EQU	0x100 		; High Frequency Clock Prescaler Register
CMU_HFCOREPRESC EQU	0x108 		; High Frequency Core Clock Prescaler Register
CMU_HFPERPRESC 	EQU	0x10C 		; High Frequency Peripheral Clock Prescaler Register
CMU_HFRADIOPRESC EQU	0x110 		; High Frequency Radio Peripheral Clock Prescaler Register
CMU_HFEXPPRESC 	EQU	0x114 		; High Frequency Export Clock Prescaler Register
CMU_LFAPRESC0 	EQU	0x120 		; Low Frequency a Prescaler Register 0 (Async Reg)
CMU_LFBPRESC0 	EQU	0x128 		; Low Frequency B Prescaler Register 0 (Async Reg)
CMU_LFEPRESC0 	EQU	0x130 		; Low Frequency E Prescaler Register 0 (Async Reg)
CMU_HFRADIOALTPRESC EQU 0x138 		; High Frequency Alternate Radio Peripheral Clock Prescaler Register
CMU_SYNCBUSY 	EQU	0x140 		; Synchronization Busy Register
CMU_FREEZE 	EQU	0x144 		; Freeze Register
CMU_PCNTCTRL 	EQU	0x150 		; PCNT Control Register
CMU_ADCCTRL 	EQU	0x15C 		; ADC Control Register
CMU_ROUTEPEN 	EQU	0x170 		; I/O Routing Pin Enable Register
CMU_ROUTELOC0 	EQU	0x174 		; I/O Routing Location Register
CMU_ROUTELOC1 	EQU	0x178 		; I/O Routing Location Register
CMU_LOCK 	EQU	0x180 		; Configuration Lock Register

;-------- EMU registers --------------------------------------------------------------------
EMU_CTRL 	EQU	0x000 		; Control Register
EMU_STATUS 	EQU	0x004 		; Status Register
EMU_LOCK 	EQU	0x008 		; Configuration Lock Register
EMU_RAM0CTRL 	EQU	0x00C 		; Memory Control Register
EMU_CMD 	EQU	0x010 		; Command Register
EMU_EM4CTRL 	EQU	0x018 		; EM4 Control Register
EMU_TEMPLIMITS 	EQU	0x01C 		; Temperature Limits for Interrupt Generation
EMU_TEMP 	EQU	0x020 		; Value of Last Temperature Measurement
EMU_IF 		EQU	0x024 		; Interrupt Flag Register
EMU_IFS 	EQU	0x028 		; Interrupt Flag Set Register
EMU_IFC 	EQU	0x02C 		; Interrupt Flag Clear Register
EMU_IEN 	EQU	0x030 		; Interrupt Enable Register
EMU_PWRLOCK 	EQU	0x034 		; Regulator and Supply Lock Register
EMU_PWRCFG 	EQU	0x038 		; Power Configuration Register
EMU_PWRCTRL 	EQU	0x03C 		; Power Control Register
EMU_DCDCCTRL 	EQU	0x040 		; DCDC Control
EMU_DCDCMISCCTRL EQU	0x04C 		; DCDC Miscellaneous Control Register
EMU_DCDCZDETCTRL EQU	0x050 		; DCDC Power Train NFET Zero Current Detector Control Register
EMU_DCDCCLIMCTRL EQU	0x054 		; DCDC Power Train PFET Current Limiter Control Register
EMU_DCDCLNCOMPCTRL EQU	0x058 		; DCDC Low Noise Compensator Control Register
EMU_DCDCLNVCTRL EQU	0x05C 		; DCDC Low Noise Voltage Register
EMU_DCDCLPVCTRL EQU	0x064 		; DCDC Low Power Voltage Register
EMU_DCDCLPCTRL 	EQU	0x06C 		; DCDC Low Power Control Register
EMU_DCDCLNFREQCTRL EQU	0x070 		; DCDC Low Noise Controller Frequency Control
EMU_DCDCSYNC 	EQU	0x078 		; DCDC Read Status Register
EMU_VMONAVDDCTRL EQU	0x090 		; VMON AVDD Channel Control
EMU_VMONALTAVDDCTRL EQU	0x094 		; Alternate VMON AVDD Channel Control
EMU_VMONDVDDCTRL EQU	0x098 		; VMON DVDD Channel Control
EMU_VMONIO0CTRL EQU	0x09C 		; VMON IOVDD0 Channel Control
EMU_RAM1CTRL 	EQU	0x0B4 		; Memory Control Register
EMU_RAM2CTRL 	EQU	0x0B8 		; Memory Control Register
EMU_DCDCLPEM01CFG EQU	0x0EC 		; Configuration Bits for Low Power Mode to Be Applied During EM01
EMU_EM23PERNORETAINCMD EQU 0x100 	; Clears Corresponding Bits in EM23PERNORETAINSTATUS 
EMU_EM23PERNORETAINSTATUS EQU 0x104 	; Status Indicating If Peripherals Were Powered Down in EM23
EMU_EM23PERNORETAINCTRL equ 0x108 	; When Set Corresponding Peripherals May Get Powered Down in EM23

;-------- PRS registers -----------------------------------------------------------------
PRS_SWPULSE 	EQU	0x000 		; Software Pulse Register
PRS_SWLEVEL 	EQU	0x004 		; Software Level Register
PRS_ROUTEPEN 	EQU	0x008 		; I/O Routing Pin Enable Register
PRS_ROUTELOC0 	EQU	0x010 		; I/O Routing Location Register
PRS_ROUTELOC1 	EQU	0x014 		; I/O Routing Location Register
PRS_ROUTELOC2 	EQU	0x018 		; I/O Routing Location Register
PRS_CTRL 	EQU	0x020 		; Control Register
PRS_DMAREQ0 	EQU	0x024 		; DMA Request 0 Register
PRS_DMAREQ1 	EQU	0x028 		; DMA Request 1 Register
PRS_PEEK 	EQU	0x030 		; PRS Channel Values
PRS_CH0_CTRL 	EQU	0x040 		; Channel Control Register
PRS_CH1_CTRL 	EQU	0x044 		; Channel Control Register
PRS_CH2_CTRL 	EQU	0x048 		; Channel Control Register
PRS_CH3_CTRL 	EQU	0x04C 		; Channel Control Register
PRS_CH4_CTRL 	EQU	0x050 		; Channel Control Register
PRS_CH5_CTRL 	EQU	0x054 		; Channel Control Register
PRS_CH6_CTRL 	EQU	0x058 		; Channel Control Register
PRS_CH7_CTRL 	EQU	0x05C 		; Channel Control Register
PRS_CH8_CTRL 	EQU	0x060 		; Channel Control Register
PRS_CH9_CTRL 	EQU	0x064 		; Channel Control Register
PRS_CH10_CTRL 	EQU	0x068 		; Channel Control Register	
PRS_CH11_CTRL 	EQU	0x06C 		; Channel Control Register

;-------- TIMER registers   -----------------------------------------------------------------
TIMERn_CTRL 	EQU	0x000 		; Control Register
TIMERn_CMD 	EQU	0x004 		; Command Register
TIMERn_STATUS 	EQU	0x008 		; Status Register
TIMERn_IF 	EQU	0x00C 		; Interrupt Flag Register
TIMERn_IFS 	EQU	0x010 		; Interrupt Flag Set Register
TIMERn_IFC 	EQU	0x014 		; Interrupt Flag Clear Register
TIMERn_IEN 	EQU	0x018 		; Interrupt Enable Register
TIMERn_TOP 	EQU	0x01C 		; Counter Top Value Register
TIMERn_TOPB 	EQU	0x020 		; Counter Top Value Buffer Register
TIMERn_CNT 	EQU	0x024 		; Counter Value Register
TIMERn_LOCK 	EQU	0x02C 		; TIMER Configuration Lock Register
TIMERn_ROUTEPEN EQU	0x030 		; I/O Routing Pin Enable Register
TIMERn_ROUTELOC0 EQU	0x034 		; I/O Routing Location Register
TIMERn_ROUTELOC2 EQU	0x03C 		; I/O Routing Location Register
TIMERn_CC0_CTRL EQU	0x060 		; CC Channel Control Register
TIMERn_CC0_CCV 	EQU	0x064 		; CC Channel Value Register
TIMERn_CC0_CCVP EQU	0x068 		; CC Channel Value Peek Register
TIMERn_CC0_CCVB EQU	0x06C 		; CC Channel Buffer Register
TIMERn_CC1_CTRL EQU	0x070 		; CC Channel Control Register
TIMERn_CC1_CCV 	EQU 	0x074		; CC Channel Value Register
TIMERn_CC1_CCVP EQU	0x078		; CC Channel Value Peek Register
TIMERn_CC1_CCVB EQU	0x07C		; CC Channel Buffer Register
TIMERn_CC2_CTRL EQU	0x080 		; CC Channel Control Register
TIMERn_CC2_CCV 	EQU	0x084 		; CC Channel Value Register
TIMERn_CC2_CCVP EQU	0x088 		; CC Channel Value Peek Register
TIMERn_CC2_CCVB EQU	0x08C 		; CC Channel Buffer Register	
TIMERn_CC3_CTRL EQU	0x090 		; CC Channel Control Register
TIMERn_CC3_CCV 	EQU	0x094 		; CC Channel Value Register
TIMERn_CC3_CCVP EQU	0x098 		; CC Channel Value Peek Register
TIMERn_CC3_CCVB EQU	0x09C 		; CC Channel Buffer Register
TIMERn_DTCTRL 	EQU	0x0A0 		; DTI Control Register
TIMERn_DTTIME 	EQU	0x0A4 		; DTI Time Control Register
TIMERn_DTFC 	EQU	0x0A8 		; DTI Fault Configuration Register
TIMERn_DTOGEN 	EQU	0x0AC 		; DTI Output Generation Enable Register
TIMERn_DTFAULT 	EQU	0x0B0 		; DTI Fault Register
TIMERn_DTFAULTC EQU	0x0B4 		; DTI Fault Clear Register
TIMERn_DTLOCK 	EQU	0x0B8 		; DTI Configuration Lock Register

;-------- LETIMER registers -----------------------------------------------------------------
LETIMERn_CTRL	EQU	0x000		; Control Register
LETIMERn_CMD	EQU	0x004 		; Command Register
LETIMERn_STATUS	EQU	0x008  		; Status Register
LETIMERn_CNT	EQU	0x00C 		; Counter Value Register
LETIMERn_COMP0	EQU	0x010 		; Compare Value Register 0
LETIMERn_COMP1	EQU	0x014  		; Compare Value Register 1
LETIMERn_REP0	EQU	0x018  		; Repeat Counter Register 0
LETIMERn_REP1	EQU	0x01C  		; Repeat Counter Register 1
LETIMERn_IF	EQU	0x020  		; Interrupt Flag Register
LETIMERn_IFS	EQU	0x024  		; Interrupt Flag Set Register
LETIMERn_IFC	EQU	0x028  		; Interrupt Flag Clear Register
LETIMERn_IEN	EQU	0x02C  		; Interrupt Enable Register
LETIMERn_SYNCBUSY EQU	0x034  		; Synchronization Busy Register
LETIMERn_ROUTEPEN EQU	0x040  		; I/O Routing Register
LETIMERn_ROUTELOC0 EQU	0x044 		; I/O Routing Location Register
LETIMERn_PRSSEL EQU	0x050 		; PRS Input Select Register

;-------- CRYOTIMER registers ------------------------------------------------------------------
CRYOTIMER_CTRL 	EQU	0x000		; Control Register
CRYOTIMER_PERIODSEL EQU	0x004 		; Interrupt Duration
CRYOTIMER_CNT 	EQU	0x008 		; Counter Value
CRYOTIMER_EM4WUEN   EQU	0x00C 		; Wake Up Enable
CRYOTIMER_IF 	EQU	0x010 		; Interrupt Flag Register
CRYOTIMER_IFS 	EQU	0x014 		; Interrupt Flag Set Register
CRYOTIMER_IFC	EQU	0x018  		; Interrupt Flag Clear Register
CRYOTIMER_IEN 	EQU	0x01C 		; Interrupt Enable Register

;-------- I2C registers -----------------------------------------------------------------------
I2Cn_CTRL 	EQU	0x000  		; Control Register
I2Cn_CMD 	EQU	0x004   	; Command Register
I2Cn_STATE 	EQU	0x008  		; State Register
I2Cn_STATUS 	EQU	0x00C  		; Status Register
I2Cn_CLKDIV 	EQU	0x010  		; Clock Division Register
I2Cn_SADDR 	EQU	0x014  		; Slave Address Register
I2Cn_SADDRMASK	EQU	0x018  		; Slave Address Mask Register
I2Cn_RXDATA 	EQU	0x01C  		; Receive Buffer Data Register
I2Cn_RXDOUBLE 	EQU	0x020 		; Receive Buffer Double Data Register
I2Cn_RXDATAP 	EQU	0x024  		; Receive Buffer Data Peek Register
I2Cn_RXDOUBLEP 	EQU	0x028 		; Receive Buffer Double Data Peek Register
I2Cn_TXDATA 	EQU	0x02C  		; Transmit Buffer Data Register
I2Cn_TXDOUBLE 	EQU	0x030 		; Transmit Buffer Double Data Register
I2Cn_IF 	EQU	0x034  		; Interrupt Flag Register
I2Cn_IFS 	EQU	0x038  		; Interrupt Flag Set Register
I2Cn_IFC 	EQU	0x03C  		; Interrupt Flag Clear Register
I2Cn_IEN 	EQU	0x040  		; Interrupt Enable Register
I2Cn_ROUTEPEN 	EQU	0x044  		; I/O Routing Pin Enable Register
I2Cn_ROUTELOC0 	EQU	0x048 		; I/O Routing Location Register

;-------- USART REGISTERS ---------------------------------------------------------------------
USARTn_CTRL 	EQU	0x000   	; Control Register
USARTn_FRAME 	EQU	0x004   	; USART Frame Format Register
USARTn_TRIGCTRL EQU	0x008 		; USART Trigger Control register
USARTn_CMD 	EQU	0x00C 		; Command Register
USARTn_STATUS 	EQU	0x010  		; USART Status Register
USARTn_CLKDIV 	EQU	0x014   	; Clock Control Register
USARTn_RXDATAX 	EQU	0x018   	; RX Buffer Data Extended Register
USARTn_RXDATA 	EQU	0x01C   	; RX Buffer Data Register
USARTn_RXDOUBLEX EQU	0x020   	; RX Buffer Double Data Extended Register
USARTn_RXDOUBLE EQU	0x024   	; RX FIFO Double Data Register
USARTn_RXDATAXP EQU	0x028   	; RX Buffer Data Extended Peek Register
USARTn_RXDOUBLEXP EQU	0x02C   	; RX Buffer Double Data Extended Peek Register
USARTn_TXDATAX 	EQU	0x030   	; TX Buffer Data Extended Register
USARTn_TXDATA 	EQU	0x034   	; TX Buffer Data Register
USARTn_TXDOUBLEX EQU	0x038   	; TX Buffer Double Data Extended Register
USARTn_TXDOUBLE EQU	0x03C   	; TX Buffer Double Data Register
USARTn_IF 	EQU	0x040   	; Interrupt Flag Register
USARTn_IFS 	EQU	0x044   	; Interrupt Flag Set Register
USARTn_IFC 	EQU	0x048   	; Interrupt Flag Clear Register
USARTn_IEN 	EQU	0x04C   	; Interrupt Enable Register
USARTn_IRCTRL 	EQU	0x050   	; IrDA Control Register
USARTn_INPUT 	EQU	0x058   	; USART Input Register
USARTn_I2SCTRL 	EQU	0x05C   	; I2S Control Register
USARTn_TIMING 	EQU	0x060 		; Timing Register
USARTn_CTRLX 	EQU	0x064 		; Control Register Extended
USARTn_TIMECMP0 EQU	0x068 		; Used to Generate Interrupts and Various Delays
USARTn_TIMECMP1 EQU	0x06C 		; Used to Generate Interrupts and Various Delays
USARTn_TIMECMP2 EQU	0x070 		; Used to Generate Interrupts and Various Delays
USARTn_ROUTEPEN EQU	0x074 		; I/O Routing Pin Enable Register
USARTn_ROUTELOC0 EQU	0x078 		; I/O Routing Location Register
USARTn_ROUTELOC1 EQU	0x07C 		; I/O Routing Location Register

;-------- GPIO registers ---------------------------------------------------------------------
GPIO_PA_CTRL	EQU	0x000  		; Port Control Register
GPIO_PA_MODEL	EQU	0x004  		; Port Pin Mode Low Register
GPIO_PA_MODEH	EQU	0x008  		; Port Pin Mode High Register
GPIO_PA_DOUT	EQU	0x00C   	; Port Data Out Register
;GPIO_PA_DOUTSET	EQU	0x010  		; Port Data Out Set Register
;GPIO_PA_DOUTCLR	EQU	0x014   	; Port Data Out Clear Register
GPIO_PA_DOUTTGL	EQU	0x018   	; Port Data Out Toggle Register
GPIO_PA_DIN	EQU	0x01C   	; Port Data In Register
GPIO_PA_PINLOCKN EQU	0x020   	; Port Unlocked Pins Register
GPIO_PA_OVTDIS 	EQU	0x028 		; Over Voltage Disable for All Modes

GPIO_PB_CTRL	EQU	0x030  		; Port Control Register
GPIO_PB_MODEL	EQU	0x034  		; Port Pin Mode Low Register
GPIO_PB_MODEH	EQU	0x038  		; Port Pin Mode High Register
GPIO_PB_DOUT	EQU	0x03C   	; Port Data Out Register
GPIO_PB_DOUTTGL	EQU	0x048   	; Port Data Out Toggle Register
GPIO_PB_DIN	EQU	0x04C   	; Port Data In Register
GPIO_PB_PINLOCKN EQU	0x050   	; Port Unlocked Pins Register
GPIO_PB_OVTDIS 	EQU	0x058 		; Over Voltage Disable for All Modes

GPIO_PC_CTRL	EQU	0x060  		; Port Control Register
GPIO_PC_MODEL	EQU	0x064  		; Port Pin Mode Low Register
GPIO_PC_MODEH	EQU	0x068  		; Port Pin Mode High Register
GPIO_PC_DOUT	EQU	0x06C   	; Port Data Out Register
GPIO_PC_DOUTTGL	EQU	0x078   	; Port Data Out Toggle Register
GPIO_PC_DIN	EQU	0x07C   	; Port Data In Register
GPIO_PC_PINLOCKN EQU	0x080   	; Port Unlocked Pins Register
GPIO_PV_OVTDIS 	EQU	0x088 		; Over Voltage Disable for All Modes

GPIO_PD_CTRL	EQU	0x090  		; Port Control Register
GPIO_PD_MODEL	EQU	0x094  		; Port Pin Mode Low Register
GPIO_PD_MODEH	EQU	0x098  		; Port Pin Mode High Register
GPIO_PD_DOUT	EQU	0x09C   	; Port Data Out Register
GPIO_PD_DOUTTGL	EQU	0x0A8   	; Port Data Out Toggle Register
GPIO_PD_DIN	EQU	0x0AC   	; Port Data In Register
GPIO_PD_PINLOCKN EQU	0x0B0   	; Port Unlocked Pins Register
GPIO_PD_OVTDIS 	EQU	0x0B8 		; Over Voltage Disable for All Modes

GPIO_PF_CTRL	EQU	0x0F0  		; Port Control Register
GPIO_PF_MODEL	EQU	0x0F4  		; Port Pin Mode Low Register
GPIO_PF_MODEH	EQU	0x0F8  		; Port Pin Mode High Register
GPIO_PF_DOUT	EQU	0x0FC   	; Port Data Out Register
GPIO_PF_DOUTTGL	EQU	0x108   	; Port Data Out Toggle Register
GPIO_PF_DIN	EQU	0x10C   	; Port Data In Register
GPIO_PF_PINLOCKN EQU	0x110   	; Port Unlocked Pins Register
GPIO_PF_OVTDIS 	EQU	0x118 		; Over Voltage Disable for All Modes

GPIO_PI_CTRL	EQU	0x180  		; Port Control Register
GPIO_PI_MODEL	EQU	0x184  		; Port Pin Mode Low Register
GPIO_PI_MODEH	EQU	0x188  		; Port Pin Mode High Register
GPIO_PI_DOUT	EQU	0x18C   	; Port Data Out Register
GPIO_PI_DOUTTGL	EQU	0x198   	; Port Data Out Toggle Register
GPIO_PI_DIN	EQU	0x19C   	; Port Data In Register
GPIO_PI_PINLOCKN EQU	0x1A0   	; Port Unlocked Pins Register
GPIO_PI_OVTDIS 	EQU	0x1A8 		; Over Voltage Disable for All Modes

GPIO_PJ_CTRL	EQU	0x1B0  		; Port Control Register
GPIO_PJ_MODEL	EQU	0x1B4  		; Port Pin Mode Low Register
GPIO_PJ_MODEH	EQU	0x1B8  		; Port Pin Mode High Register
GPIO_PJ_DOUT	EQU	0x1BC   	; Port Data Out Register
GPIO_PJ_DOUTTGL	EQU	0x1B8   	; Port Data Out Toggle Register
GPIO_PJ_DIN	EQU	0x1CC   	; Port Data In Register
GPIO_PJ_PINLOCKN EQU	0x1D0   	; Port Unlocked Pins Register
GPIO_PJ_OVTDIS 	EQU	0x1D8 		; Over Voltage Disable for All Modes

GPIO_PK_CTRL	EQU	0x1E0  		; Port Control Register
GPIO_PK_MODEL	EQU	0x1E4  		; Port Pin Mode Low Register
GPIO_PK_MODEH	EQU	0x1E8  		; Port Pin Mode High Register
GPIO_PK_DOUT	EQU	0x1EC   	; Port Data Out Register
GPIO_PK_DOUTTGL	EQU	0x1F8   	; Port Data Out Toggle Register
GPIO_PK_DIN	EQU	0x1FC   	; Port Data In Register
GPIO_PK_PINLOCKN EQU	0x200   	; Port Unlocked Pins Register
GPIO_PK_OVTDIS 	EQU	0x208 		; Over Voltage Disable for All Modes

GPIO_EXTIPSELL	EQU	0x400   	; External Interrupt Port Select Low Register
GPIO_EXTIPSELH	EQU	0x404   	; External Interrupt Port Select High Register
GPIO_EXTIPINSELL EQU	0x408 		; External Interrupt Pin Select Low Register
GPIO_EXTIPINSELH EQU	0x40C 		; External Interrupt Pin Select High Register
GPIO_EXTIRISE	EQU	0x410   	; External Interrupt Rising Edge Trigger Register
GPIO_EXTIFALL	EQU	0x414   	; External Interrupt Falling Edge Trigger Register
GPIO_EXTILEVEL 	EQU	0x418 		; External Interrupt Level Register

GPIO_IF		EQU	0x41C   	; Interrupt Flag Register
GPIO_IFS	EQU	0x420   	; Interrupt Flag Set Register
GPIO_IFC	EQU	0x424   	; Interrupt Flag Clear Register
GPIO_IEN	EQU	0x428   	; Interrupt Enable Register
GPIO_EM4WUEN	EQU	0x42C   	; EM4 Wake-up Enable Register
GPIO_ROUTEPEN	EQU	0x440   	; I/O Routing Pin Enable Register
GPIO_ROUTELOC0 	EQU	0x444 		; I/O Routing Location Register
GPIO_ROUTELOC1 	EQU	0x448 		; I/O Routing Location Register 1
GPIO_INSENSE	EQU	0x450   	; Input Sense Register
GPIO_LOCK	EQU	0x454   	; Configuration Lock Register

;-------- LDMA registers ----------------------------------------------------------------------
LDMA_CTRL 	EQU	0x000 		; DMA Control Register
LDMA_STATUS 	EQU	0x004 		; DMA Status Register
LDMA_SYNC 	EQU	0x008 		; DMA Synchronization Trigger Register (Single-Cycle RMW)
LDMA_CHEN 	EQU	0x020 		; DMA Channel Enable Register (Single-Cycle RMW)
LDMA_CHBUSY 	EQU	0x024 		; DMA Channel Busy Register
LDMA_CHDONE 	EQU	0x028 		; DMA Channel Linking Done Register (Single-Cycle RMW)
LDMA_DBGHALT 	EQU	0x02C 		; DMA Channel Debug Halt Register
LDMA_SWREQ 	EQU	0x030 		; DMA Channel Software Transfer Request Register
LDMA_REQDIS 	EQU	0x034 		; DMA Channel Request Disable Register
LDMA_REQPEND 	EQU	0x038 		; DMA Channel Requests Pending Register
LDMA_LINKLOAD 	EQU	0x03C 		; DMA Channel Link Load Register
LDMA_REQCLEAR 	EQU	0x040 		; DMA Channel Request Clear Register
LDMA_IF 	EQU	0x060 		; Interrupt Flag Register
LDMA_IFS 	EQU	0x064 		; Interrupt Flag Set Register
LDMA_IFC 	EQU	0x068 		; Interrupt Flag Clear Register
LDMA_IEN 	EQU	0x06C 		; Interrupt Enable Register

LDMA_CH0_REQSEL EQU	0x080 		; Channel Peripheral Request Select Register
LDMA_CH0_CFG 	EQU	0x084 		; Channel Configuration Register
LDMA_CH0_LOOP 	EQU	0x088 		; Channel Loop Counter Register
LDMA_CH0_CTRL 	EQU	0x08C 		; Channel Descriptor Control Word Register
LDMA_CH0_SRC 	EQU	0x090 		; Channel Descriptor Source Data Address Register
LDMA_CH0_DST 	EQU	0x094 		; Channel Descriptor Destination Data Address Register
LDMA_CH0_LINK 	EQU	0x098 		; Channel Descriptor Link Structure Address Register

;-------- RTCC registers ----------------------------------------------------------------------
RTCC_CTRL 	EQU	0x000 		; Control Register
RTCC_PRECNT 	EQU	0x004 		; Pre-Counter Value Register
RTCC_CNT 	EQU	0x008 		; Counter Value Register
RTCC_COMBCNT 	EQU	0x00C 		; Combined Pre-Counter and Counter Value Register
RTCC_TIME 	EQU	0x010 		; Time of Day Register
RTCC_DATE 	EQU	0x014 		; Date Register
RTCC_IF 	EQU	0x018 		; RTCC Interrupt Flags
RTCC_IFS 	EQU	0x01C 		; Interrupt Flag Set Register
RTCC_IFC 	EQU	0x020 		; Interrupt Flag Clear Register
RTCC_IEN 	EQU	0x024 		; Interrupt Enable Register
RTCC_STATUS 	EQU	0x028 		; Status Register
RTCC_CMD 	EQU	0x02C 		; Command Register
RTCC_SYNCBUSY 	EQU	0x030 		; Synchronization Busy Register
RTCC_POWERDOWN 	EQU	0x034 		; Retention RAM Power-down Register
RTCC_LOCK 	EQU	0x038 		; Configuration Lock Register
RTCC_EM4WUEN 	EQU	0x03C 		; Wake Up Enable
RTCC_CC0_CTRL 	EQU	0x040 		; CC Channel Control Register
RTCC_CC0_CCV 	EQU	0x044 		; Capture/Compare Value Register
RTCC_CC0_TIME 	EQU	0x048 		; Capture/Compare Time Register
RTCC_CC0_DATE 	EQU	0x04C 		; Capture/Compare Date Register
RTCC_CC1_CTRL 	EQU	0x050 		; CC Channel Control Register
RTCC_CC1_CCV 	EQU	0x054 		; Capture/Compare Value Register
RTCC_CC1_TIME 	EQU	0x058 		; Capture/Compare Time Register
RTCC_CC1_DATE 	EQU	0x05C 		; Capture/Compare Date Register
RTCC_CC2_CTRL 	EQU	0x060 		; CC Channel Control Register
RTCC_CC2_CCV 	EQU	0x064 		; Capture/Compare Value Register
RTCC_CC2_TIME 	EQU	0x068 		; Capture/Compare Time Register
RTCC_CC2_DATE 	EQU	0x06C 		; Capture/Compare Date Register
RTCC_RET0_REG 	EQU	0x104 		; Retention Register
RTCC_RET31_REG 	EQU	0x180 		; Retention Register

;-------- ADC registers ----------------------------------------------------------------------
ADCn_CTRL 	EQU	0x000 		; Control Register
ADCn_CMD 	EQU	0x008 		; Command Register
ADCn_STATUS 	EQU	0x00C 		; Status Register
ADCn_SINGLECTRL EQU	0x010 		; Single Channel Control Register
ADCn_SINGLECTRLX EQU	0x014 		; Single Channel Control Register Continued
ADCn_SCANCTRL 	EQU	0x018 		; Scan Control Register
ADCn_SCANCTRLX 	EQU 	0x01C 		; Scan Control Register Continued
ADCn_SCANMASK 	EQU	0x020 		; Scan Sequence Input Mask Register
ADCn_SCANINPUTSEL EQU	0x024 		; Input Selection Register for Scan Mode
ADCn_SCANNEGSEL EQU	0x028 		; Negative Input Select Register for Scan
ADCn_CMPTHR 	EQU	0x02C 		; Compare Threshold Register
ADCn_BIASPROG 	EQU	0x030		; Bias Programming Register f
ADCn_CAL 	EQU	0x034 		; Calibration Register
ADCn_IF 	EQU	0x038 		; Interrupt Flag Register
ADCn_IFS 	EQU	0x03C 		; Interrupt Flag Set Register
ADCn_IFC 	EQU	0x040 		; Interrupt Flag Clear Register
ADCn_IEN 	EQU	0x044 		; Interrupt Enable Register
ADCn_SINGLEDATA EQU	0x048 		; Single Conversion Result Data
ADCn_SCANDATA 	EQU	0x04C 		; Scan Conversion Result Data
ADCn_SINGLEDATAP EQU	0x050 		; Single Conversion Result Data Peek Register
ADCn_SCANDATAP 	EQU	0x054 		; Scan Sequence Result Data Peek Register
ADCn_SCANDATAX 	EQU	0x068 		; Scan Sequence Result Data + Data Source Register
ADCn_SCANDATAXP EQU	0x06C 		; Scan Sequence Result Data + Data Source Peek Register
ADCn_APORTREQ 	EQU	0x07C 		; APORT Request Status Register
ADCn_APORTCONFLICT EQU	0x080 		; APORT Conflict Status Register
ADCn_SINGLEFIFOCOUNT EQU 0x084 		; Single FIFO Count Register
ADCn_SCANFIFOCOUNT EQU	0x088 		; Scan FIFO Count Register
ADCn_SINGLEFIFOCLEAR EQU 0x08C 		; Single FIFO Clear Register
ADCn_SCANFIFOCLEAR EQU	0x090 		; Scan FIFO Clear Register
ADCn_APORTMASTERDIS EQU	0x094 		; APORT Bus Master Disable Register

;-------- TRNG registers ----------------------------------------------------------------------
TRNGn_CONTROL 	EQU	0x000 		; Main Control Register
TRNGn_FIFOLEVEL EQU	0x004 		; FIFO Level Register
TRNGn_FIFODEPTH EQU	0x00C 		; FIFO Depth Register
TRNGn_KEY0 	EQU	0x010 		; Key Register 0
TRNGn_KEY1 	EQU	0x014 		; Key Register 1
TRNGn_KEY2 	EQU	0x018 		; Key Register 2
TRNGn_KEY3 	EQU	0x01C 		; Key Register 3
TRNGn_TESTDATA 	EQU	0x020 		; Test Data Register
TRNGn_STATUS 	EQU	0x030 		; Status Register
TRNGn_INITWAITVAL EQU	0x034 		; Initial Wait Counter
TRNGn_FIFO 	EQU	0x100 		; FIFO Data

;-------- ARM Core registers -----------------------------------------------------------------
NVIC_ISER0	EQU	0xE000E100	; NVIC SETENA
NVIC_ISER1	EQU	0xE000E104
NVIC_ICER0	EQU	0xE000E180	; NVIC CLRENA
NVIC_ICER1	EQU	0xE000E184
NVIC_ISPR0	EQU	0xE000E200	; NVIC SETPEND
NVIC_ISPR1	EQU	0xE000E204
NVIC_ICPR0	EQU	0xE000E280	; NVIC CLRPEND
NVIC_ICPR1	EQU	0xE000E284

CPACR		EQU	0xE000ED88	; Co-processor config register address

SCB_SCR		EQU	0xE000ED10	; System Control Register
SLEEPDEEP	EQU	0x04		; bits in System Control Register
SLEEPONEXIT	EQU	0x02

	MACRO				; store word data in a given register
	PUTW	$wdata, $reg, $base
	IF	"$base" <> "" 
	ldr	R0, =$base
	ENDIF
	IF	$wdata <= 0xFF
	movs	R1, #$wdata
	ELIF	$wdata <= 0xFFFF
	movw	R1, #$wdata
	ELSE
	ldr	R1, =$wdata
	ENDIF
	str	R1, [R0, #$reg]	
	MEND

	MACRO				; store byte in a given register
	PUTB	$wdata, $reg, $base
	IF	"$base" <> "" 
	ldr	R0, =$base
	ENDIF		
	movs	R1, #$wdata	
	strb	R1, [R0, #$reg]
	MEND

	MACRO				; load a word into R1
	GETW	$reg, $base
	IF	"$base" <> "" 
	ldr	R0, =$base
	ENDIF			
	ldr	R1, [R0, #$reg]	
	MEND
		
	MACRO				; OR a word with data in memory
	OORW	$wdata, $reg, $base
	IF	"$base" <> "" 
	ldr	R0, =$base
	ENDIF
	IF	$wdata <= 0xFF
	movs	R2, #$wdata
	ELIF	$wdata <= 0xFFFF
	movw	R2, #$wdata
	ELSE
	ldr	R2, =$wdata
	ENDIF	
	ldr	R1, [R0, #$reg]
	orr	R1, R2
	str	R1, [R0, #$reg]
	MEND

	MACRO				; OR a halfword with data in memory
	OORH	$wdata, $reg, $base 
	IF	"$base" <> "" 
	ldr	R0, =$base
	ENDIF
	IF	$wdata <= 0xFF
	movs	R2, #$wdata
	ELSE	
	movw	R2, #$wdata
	ENDIF		
	ldrh	R1, [R0, #$reg]
	orr	R1, R2
	strh	R1, [R0, #$reg]
	MEND

	MACRO				; OR a byte with data in memory
	OORB	$wdata, $reg, $base
	IF	"$base" <> "" 
	ldr	R0, =$base
	ENDIF	
	ldrb	R1, [R0, #$reg]
	movs	R2, #$wdata
	strb	R1, [R0, #$reg]
	MEND	

	MACRO				; AND a word with data in memory
	ANDW	$wdata, $reg, $base
	IF	"$base" <> "" 
	ldr	R0, =$base
	ENDIF
	IF	$wdata <= 0xFF
	movs	R2, #$wdata
	ELIF	$wdata <= 0xFFFF
	movw	R2, #$wdata
	ELSE
	ldr	R2, =$wdata
	ENDIF	
	ldr	R1, [R0, #$reg]
	and	R1, R2
	str	R1, [R0, #$reg]
	MEND	
	
	PRESERVE8
	THUMB				; use thumb instruction set	

	END