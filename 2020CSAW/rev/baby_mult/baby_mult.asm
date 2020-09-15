section .text:
	global _start

	_start:
		push	rbp
		mov    	rbp,rsp
		sub    	rsp,0x18
		mov    	QWORD [rbp-0x8],0x4f
		mov		rax,0x14be74f15
		mov    	QWORD [rbp-0x10],rax
		mov    	QWORD [rbp-0x18],0x4
		mov    	QWORD [rbp-0x20],0x3
		mov    	QWORD [rbp-0x28],0x13
		mov    	QWORD [rbp-0x30],0x115
		mov		rax,0x77cf4b645b61
		mov    	QWORD [rbp-0x38],rax
		mov    	QWORD [rbp-0x40],0x2
		mov    	QWORD [rbp-0x48],0x11
		mov    	QWORD [rbp-0x50],0x21c1
		mov    	QWORD [rbp-0x58],0x182265e9
		mov    	QWORD [rbp-0x60],0x833
		mov    	QWORD [rbp-0x68],0xaab
		mov    	QWORD [rbp-0x70],0x8daaad
		mov    	rax,QWORD [rbp-0x8]
		imul   	rax,QWORD [rbp-0x10]
		mov    	QWORD [rbp-0x78],rax
		mov    	rax,QWORD [rbp-0x18]
		imul   	rax,QWORD [rbp-0x20]
		imul   	rax,QWORD [rbp-0x28]
		imul   	rax,QWORD [rbp-0x30]
		imul   	rax,QWORD [rbp-0x38]
		mov    	QWORD [rbp-0x80],rax
		mov    	rax,QWORD [rbp-0x40]
		imul   	rax,QWORD [rbp-0x48]
		imul   	rax,QWORD [rbp-0x50]
		imul   	rax,QWORD [rbp-0x58]
		mov    	QWORD [rbp-0x88],rax
		mov    	rax,QWORD [rbp-0x60]
		imul   	rax,QWORD [rbp-0x68]
		imul   	rax,QWORD [rbp-0x70]
		mov    	QWORD [rbp-0x90],rax
		mov     rax, 1
        mov     rdi, 1
        lea     rsi,[rbp-0x90]
        mov     rdx, 0x20
        syscall
		mov    	eax,0x0
		leave
