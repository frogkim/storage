	INCLUDE EFR32MG12.inc		; CPU register definitions
;  Stack Configuration
Stack_Size      EQU     0x00001000
                AREA    STACK, NOINIT, READWRITE, ALIGN=3
Stack_Mem       SPACE   Stack_Size
__initial_sp

;  Heap Configuration
Heap_Size       EQU     0x00001000
                AREA    HEAP, NOINIT, READWRITE, ALIGN=3
__heap_base
Heap_Mem        SPACE   Heap_Size
__heap_limit

	PRESERVE8
	THUMB

; Vector Table Mapped to Address 0 at Reset
	AREA    RESET, DATA, READONLY, ALIGN=8
                
__Vectors
	DCD     __initial_sp           	; Top of Stack
        DCD     Reset_Handler          	; Reset Handler
        DCD     Default_Handler        	; NMI Handler
        DCD     Default_Handler        	; Hard Fault Handler
        DCD     Default_Handler        	; MPU Fault Handler
        DCD     Default_Handler        	; Bus Fault Handler
        DCD     Default_Handler        	; Usage Fault Handler
        DCD     0                      	; Reserved
        DCD     0                      	; Reserved
        DCD     0                      	; Reserved
        DCD     0                     	; Reserved
	DCD     Default_Handler       	; SVCall Handler
	DCD     Default_Handler        	; Debug Monitor Handler
	DCD     0                     	; Reserved
	DCD     Default_Handler       	; PendSV Handler
	DCD     Default_Handler        	; SysTick Handler

	; External Interrupts
	DCD     Default_Handler       	;  0: EMU Interrupt
	DCD     Default_Handler        	;  1: FRC_PRI Interrupt
	DCD     Default_Handler        	;  2: WDOG0 Interrupt
	DCD     Default_Handler       	;  3: WDOG1 Interrupt
	DCD     Default_Handler        	;  4: FRC Interrupt
	DCD     Default_Handler        	;  5: MODEM Interrupt
	DCD     Default_Handler        	;  6: RAC_SEQ Interrupt
	DCD     Default_Handler        	;  7: RAC_RSM Interrupt
	DCD     Default_Handler        	;  8: BUFC Interrupt
	DCD     Default_Handler        	;  9: LDMA Interrupt
	DCD     Default_Handler      	; 10: GPIO_EVEN Interrupt
	DCD     Default_Handler         ; 11: TIMER0 Interrupt
	DCD     Default_Handler      	; 12: USART0_RX Interrupt
	DCD     Default_Handler      	; 13: USART0_TX Interrupt
	DCD     Default_Handler       	; 14: ACMP0 Interrupt
	DCD     Default_Handler        	; 15: ADC0 Interrupt
	DCD     Default_Handler        	; 16: IDAC0 Interrupt
	DCD     Default_Handler        	; 17: I2C0 Interrupt
	DCD     Default_Handler       	; 18: GPIO_ODD Interrupt
	DCD     Default_Handler         ; 19: TIMER1 Interrupt
	DCD     Default_Handler      	; 20: USART1_RX Interrupt
	DCD     Default_Handler      	; 21: USART1_TX Interrupt
	DCD     Default_Handler        	; 22: LEUART0 Interrupt
	DCD     Default_Handler       	; 23: PCNT0 Interrupt
	DCD     Default_Handler       	; 24: CMU Interrupt
	DCD     Default_Handler        	; 25: MSC Interrupt
	DCD     Default_Handler        	; 26: CRYPTO0 Interrupt
	DCD     Default_Handler    	; 27: LETIMER0 Interrupt
	DCD     Default_Handler        	; 28: AGC Interrupt
	DCD     Default_Handler       	; 29: PROTIMER Interrupt
	DCD     Default_Handler       	; 30: RTCC Interrupt
	DCD     Default_Handler       	; 31: SYNTH Interrupt
			
	DCD     Default_Handler      	;  0: CRYOTIMER Interrupt
	DCD     Default_Handler        	;  1: RFSENSE Interrupt
	DCD     Default_Handler         ;  2: FPUEH Interrupt
	DCD     Default_Handler       	;  3: SMU Interrupt
	DCD     Default_Handler    	;  4: WTIMER0 Interrupt
	DCD     Default_Handler    	;  5: WTIMER1 Interrupt
	DCD     Default_Handler      	;  6: PCNT1 Interrupt
	DCD     Default_Handler     	;  7: PCNT2 Interrupt
	DCD     Default_Handler    	;  8: USART2_RX Interrupt
	DCD     Default_Handler   	;  9: USART2_TX Interrupt
	DCD     Default_Handler    	; 10: I2C1 Interrupt
	DCD     Default_Handler  	; 11: USART3_RX Interrupt
	DCD     Default_Handler  	; 12: USART3_TX Interrupt
	DCD     Default_Handler   	; 13: VDAC0 Interrupt
	DCD     Default_Handler  	; 14: CSEN Interrupt
	DCD     Default_Handler   	; 15: LESENSE Interrupt
	DCD     Default_Handler   	; 16: CRYPTO1 Interrupt
	DCD     Default_Handler   	; 17: TRNG0 Interrupt
	DCD     0                    	; 18: Reserved
__Vectors_End
__Vectors_Size  EQU     __Vectors_End - __Vectors

	AREA    |.text|, CODE, READONLY
Reset_Handler   PROC				; Reset Handler
	EXPORT  Reset_Handler             
	IMPORT  main
	PUTW	0x02, EMU_PWRCFG, EMU		; unlock DCDC registers
	OORW	15<<16, EMU_DCDCMISCCTRL	; set 320mA current limit
	OORW	1<<13, EMU_DCDCCLIMCTRL		; enable current limiter
	PUTW	0, EMU_DCDCCTRL			; bypass DCDC
	PUTW	1<<10, EMU_PWRCTRL		; power analog blocks from DVDD
	
	PUTW	0x190, CMU_OSCENCMD, CMU	; enable LFXO
rh1	
	GETW	CMU_STATUS			; R1 = status
	ands	R1, #(1<<9)
	beq	rh1				; wait for LFXO stabilize
	
	PUTW	1, CMU_HFCLKSEL			; select 19 MHz HFRCO as closk source
	OORW	1<<2, CMU_HFBUSCLKEN0		; enable LE clock access
	PUTW	2, CMU_LFACLKSEL		; set LFXO as LFA
	PUTW	2, CMU_LFECLKSEL	

	ldr	R0, =main			; pass control to main
	bx	R0
	ENDP

;--------------------------------------------------------------------
Default_Handler	PROC				; default ISR placeholder
	b	.
	ENDP
		
 	EXPORT  __initial_sp
	EXPORT  __heap_base
	EXPORT  __heap_limit
	EXPORT  __Vectors
	EXPORT  __Vectors_End
	EXPORT  __Vectors_Size	

	ALIGN
	END
