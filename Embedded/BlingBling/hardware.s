	INCLUDE EFR32MG12.inc			; CPU register definitions	
		
	AREA    |.text|, CODE, READONLY	; another section in the CODE area	
;-------------------------------------------------------------------------------
GPIO_setup	PROC				; I/O Ports configuration
	EXPORT	GPIO_setup
	OORW	1<<3, CMU_HFBUSCLKEN0, CMU	; enable clock to GPIO
	OORW	(0x11<<24), GPIO_PD_MODEH, GPIO	; configure PD14,15 for digital input
	OORW	4<<24, GPIO_PJ_MODEH, GPIO
	OORW	1<<14, GPIO_PJ_DOUT		; turn on DC/DC converter
	OORW	0x4444, GPIO_PI_MODEL		; enable RGB COMs
	OORW	0x444000, GPIO_PD_MODEH		; enable RGB LEDs	
	;OORW	0x44, GPIO_PD_MODEH		; congigure PD8,9 for RG LED
	bx	LR
	ENDP	

;-------------------------------------------------------------------------------
LETIMER_setup	PROC ; 2^16 = 32768 = 1000 ms period
	EXPORT	LETIMER_setup
	PUTW	1, CMU_LFACLKEN0, CMU		; enable LFA clock for LETIMER
	PUTW	1<<9, LETIMERn_CTRL, LETIMER0	; set period	
	PUTW	600, LETIMERn_COMP0		; ~20 ms period : ~~ 600000 / 32768
	PUTW	0x1F, LETIMERn_IFC		; clear all IF	
	PUTW	5, LETIMERn_CMD, LETIMER0	; start timer
	bx	LR
	ENDP
	ALIGN
	END
	