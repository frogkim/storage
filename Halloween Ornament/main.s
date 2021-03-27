; turn on red LED with BUTTON0, turn it off with BUTTON1

	INCLUDE EFR32MG12.inc		; CPU register definitions
	EXPORT  main	
	IMPORT	GPIO_setup
	IMPORT	LETIMER_setup	
		
;RED_LED		EQU	1<<8			; red LED at PD8
BUTTON0		EQU	1<<14			; BUTTON0 at PD14	
BUTTON1		EQU	1<<15			; BUTTON1 at PD15

RGB_LED0	EQU	1				; defines for 4 RGB leds on board
RGB_LED1	EQU	1<<1
RGB_LED2	EQU	1<<2
RGB_LED3	EQU	1<<3	

RED_LED		EQU	1<<11				; RGB LED control pins at PD
GREEN_LED	EQU	1<<12
BLUE_LED	EQU	1<<13
YELLOW_LED	EQU	RED_LED+GREEN_LED
CION_LED	EQU	GREEN_LED+BLUE_LED
PURPLE_LED	EQU	RED_LED+BLUE_LED
WHITE_LED	EQU	BLUE_LED+GREEN_LED+RED_LED	
;-------------------------------------	; DATA segment in RAM
	AREA	RAM, DATA, NOINIT, READWRITE, ALIGN=3
shiftReg0	SPACE 1			; button shift register for BUTTON0
butState0	SPACE 1			; button state (1=OFF, 0=ON)
butEvent0	SPACE 1			; button event (1 = pressed)	
shiftReg1	SPACE 1			; button shift register for BUYYON1
butState1	SPACE 1			; button state (1=OFF, 0=ON)
butEvent1	SPACE 1			; button event (1 = pressed)		
	
;-------------------------------------	; CODE segment in flash (ROM)
	AREA    |.text|, CODE, READONLY
main	PROC				; main user code
	bl	GPIO_setup
	bl	LETIMER_setup
	
	ldr 	R0, =shiftReg0		; initializa RAM variables
	movs	R1, #0xFF
	strb	R1, [R0]		; shiftReg0 = 0xFF	
	strb	R1, [R0, #1]		; butState0 = 0xFF
	strb	R1, [R0, #3]		; shiftReg1 = 0xFF
	strb	R1, [R0, #4]		; butState1 = 0xFF
	movs	R5, #0
	movs	R6, #0

loop
	cmp	R6, #252
	blt	passsubs
	subs	R6, #252
	
passsubs
	adds	R6, #1
	cbz	R5, passthrough
	bl	BlingBling
	
passthrough	
	GETW	LETIMERn_IF, LETIMER0	; R1 = LETIMER flags
	ands	R1, #0x04		; check COMP0 flag
	beq	loop
	PUTW	0x1F, LETIMERn_IFC	; clear LETIMER flags	

	GETW	GPIO_PD_DIN, GPIO	; R1 = button values
	mov	R2, R1			; save values in R2	
	
	ldr	R0, =shiftReg0		; debounce BUTTON0
	and	R1, R2, #BUTTON0	; R1 = current button value	
	bl	Debounce		
		
	ldr	R0, =shiftReg1		; debounce BUTTON1
	and	R1, R2, #BUTTON1	; R1 = current button value
	bl	Debounce		
					
	ldr	R0, =butEvent0
	ldrb	R1, [R0]		; R1 = butEvent0
	cbz	R1, L1			; BUTTON0 pressed?
	movs	R5, #1
	bl	TurnOn
	
L1	ldr	R0, =butEvent1
	ldrb	R1, [R0]		; R1 = butEvent1
	tst	R1, #1			; BUTTON1 pressed?
	beq	loop			; NO  - wait for button press
	movs	R5, #0
	bl	TurnOff
	ANDW	~(RGB_LED0+RGB_LED1+RGB_LED2+RGB_LED3), GPIO_PI_DOUT	; turn off both LEDs
	
	b	loop			; loop back	

	ENDP

;------------------------------------
BlingBling	PROC
	push	{LR, R4, R5}
	movs	R4, #7		; divider
	udiv	R5, R6, R4	; R5 - quotient
	mls	R5, R4, R5, R6  ; R6 = R6 - R4 * R5 

	PUTW	RED_LED, GPIO_PD_DOUT, GPIO  	; set color 
	cmp	R5, #0
	beq	GotoBB
	
	PUTW	GREEN_LED, GPIO_PD_DOUT, GPIO  	; set color 
	cmp	R5, #1
	beq	GotoBB

	PUTW	BLUE_LED, GPIO_PD_DOUT, GPIO  	; set color 
	cmp	R5, #2
	beq	GotoBB

	PUTW	YELLOW_LED, GPIO_PD_DOUT, GPIO  	; set color 
	cmp	R5, #3
	beq	GotoBB

	PUTW	CION_LED, GPIO_PD_DOUT, GPIO  	; set color 
	cmp	R5, #4
	beq	GotoBB

	PUTW	PURPLE_LED, GPIO_PD_DOUT, GPIO  	; set color 
	cmp	R5, #5
	beq	GotoBB

	PUTW	WHITE_LED, GPIO_PD_DOUT, GPIO  	; set color 
	cmp	R5, #6
	beq	GotoBB


GotoBB
	movs	R4, #4		; divider
	udiv	R5, R6, R4	; R5 - quotient
	mls	R5, R4, R5, R6  ; R6 = R6 - R4 * R5 

	cmp	R5, #0
	beq	BB0
	cmp	R5, #1
	beq	BB1
	cmp	R5, #2
	beq	BB2
	b	BB3

BB0	
	PUTW	RGB_LED0, GPIO_PI_DOUT, GPIO 	; enable LED0
	b	BBEND
BB1	
	PUTW	RGB_LED1, GPIO_PI_DOUT, GPIO 	; enable LED1
	b	BBEND
BB2	
	PUTW	RGB_LED2, GPIO_PI_DOUT, GPIO 	; enable LED2
	b	BBEND
BB3	
	PUTW	RGB_LED3, GPIO_PI_DOUT, GPIO 	; enable LED3

BBEND	bl	delay
	pop	{LR, R4, R5}
	bx	LR
	ENDP

;------------------------------------
TurnOn	PROC
	push	{LR, R5}
	movs	R5, #5
	PUTW	RED_LED, GPIO_PD_DOUT, GPIO  ; set YELLOW_LED 
	
LoopTurnOn
	PUTW	RGB_LED0, GPIO_PI_DOUT, GPIO 	; enable LED0
	bl	onoff
	PUTW	RGB_LED1, GPIO_PI_DOUT, GPIO 	; enable LED1
	bl	onoff
	PUTW	RGB_LED2, GPIO_PI_DOUT, GPIO 	; enable LED0
	bl	onoff
	PUTW	RGB_LED3, GPIO_PI_DOUT, GPIO 	; enable LED1
	bl	onoff
	subs	R5, #1
	bne	LoopTurnOn
	
	pop	{LR, R5}
	bx	LR
	ENDP
;------------------------------------
TurnOff	PROC
	push	{LR, R5}
	movs	R5, #5
	PUTW	BLUE_LED, GPIO_PD_DOUT, GPIO  ; set YELLOW_LED 
	
LoopTurnOff
	PUTW	RGB_LED0, GPIO_PI_DOUT, GPIO 	; enable LED0
	bl	onoff
	PUTW	RGB_LED1, GPIO_PI_DOUT, GPIO 	; enable LED1
	bl	onoff
	PUTW	RGB_LED2, GPIO_PI_DOUT, GPIO 	; enable LED0
	bl	onoff
	PUTW	RGB_LED3, GPIO_PI_DOUT, GPIO 	; enable LED1
	bl	onoff
	subs	R5, #1
	bne	LoopTurnOff
	
	pop	{LR, R5}
	bx	LR
	ENDP

;------------------------------------
Debounce	PROC			; R0 = &shiftReg, R1 = current button value
	push	{R1, R2}
	movs	R2, #0
	strb	R2, [R0, #2]		; clear button event
	ldrb	R2, [R0]		; R2 = shiftReg value
	lsrs	R2, #1			
	cmp	R1, #0			; check current button state
	addne	R2, #0x80		; R2 = updated shiftReg
	strb	R2, [R0]		; save it in RAM
	
	ldrb	R1, [R0, #1]		; R1 = old button state
	cbz	R1, deb1		; proceed to deb1 if old state is pressed
	cmp	R2, #0x3F		; shiftReg <= 0x3F?
	bgt	deb2			; NO  - exit		
	movs	R1, #0 			; YES - set new button state to ON
	strb	R1, [R0, #1]		; save updated state in RAM 
	ldrb	R1, [R0, #2]		; R1 = button event
	orr	R1, #1			; set event bit
	strb	R1, [R0, #2]		; save event in RAM
	b	deb2			; exit

deb1	cmp	R2, #0xFC		; shiftReg >= release threschold?
	blt	deb2			; NO  - exit		
	movs	R1, #1			; YES - set new button state to OFF
	strb	R1, [R0, #1]		; save updated status in RAM
	nop				; button release action (none)	
deb2	pop	{R1, R2}
	bx	LR			; return						
	ENDP
;==================================================================
delay	PROC				; software delay for about 1 sec
	push	{R0}
	ldr 	R0, =1500000
dl	subs	R0, #1
	bne	dl
	pop	{R0}
	bx	LR
	ENDP
;==================================================================
onoff	PROC				; software delay for about 1 sec
	push	{R0}
	ldr 	R0, =250000
lonoff	subs	R0, #1
	bne	lonoff
	pop	{R0}
	bx	LR
	ENDP
;===========================================================		
	ALIGN
	END	