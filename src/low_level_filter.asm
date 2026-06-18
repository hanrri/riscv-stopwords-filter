.data
    entrada: .asciz "data/input_clean.txt"
    saida:   .asciz "data/output_riscv.txt"
    buffer: .space 20000
    buffer_saida: .space 20000
    temp_palavra: .space 256
    erro_msg: .asciz "Erro ao abrir arquivo\n"

    sw_1:  .asciz "o"
    sw_2:  .asciz "a"
    sw_3:  .asciz "os"
    sw_4:  .asciz "as"
    sw_5:  .asciz "um"
    sw_6:  .asciz "uma"
    sw_7:  .asciz "de"
    sw_8:  .asciz "do"
    sw_9:  .asciz "da"
    sw_10: .asciz "em"
    sw_11: .asciz "para"
    sw_12: .asciz "com"
    sw_13: .asciz "por"
    sw_14: .asciz "e"
    sw_15: .asciz "ou"
    sw_16: .asciz "mas"
    sw_17: .asciz "que"
    sw_18: .asciz "se"

    .align 2

    stopwords: .word sw_1, sw_2, sw_3, sw_4, sw_5, sw_6, sw_7, sw_8, sw_9, sw_10, sw_11, sw_12, sw_13, sw_14, sw_15, sw_16, sw_17, sw_18
    num_sw: .word 18

.text
.globl main

main:
    li a7, 1024
    la a0, entrada
    li a1, 0
    ecall
    
    bltz a0, erro_abertura
    mv s0, a0

    li a7, 63
    mv a0, s0
    la a1, buffer
    li a2, 20000
    ecall
    
    mv s5, a0
    la t0, buffer
    add t0, t0, s5
    sb zero, 0(t0)

    li a7, 57
    mv a0, s0
    ecall

    la s1, buffer
    la s3, buffer_saida
    li s2, 0

proxima_palavra:
    la s4, temp_palavra

le_char:
    lbu t2, 0(s1)
    addi s1, s1, 1
    beqz t2, delimitador_encontrado

    li t3, 48
    blt t2, t3, nao_alfanumerico
    li t3, 57
    ble t2, t3, armazena_char

    li t3, 65
    blt t2, t3, nao_alfanumerico
    li t3, 90
    ble t2, t3, converte_minusculo

    li t3, 97
    blt t2, t3, nao_alfanumerico
    li t3, 122
    ble t2, t3, armazena_char

nao_alfanumerico:
    j delimitador_encontrado

converte_minusculo:
    addi t2, t2, 32

armazena_char:
    sb t2, 0(s4)
    addi s4, s4, 1
    j le_char

delimitador_encontrado:
    sb zero, 0(s4)
    mv s6, t2

    la t4, temp_palavra
    beq s4, t4, verifica_fim_texto

    la a0, temp_palavra
    call verifica_sw
    bnez a0, verifica_fim_texto

    la t4, temp_palavra

copia_saida:
    lbu t5, 0(t4)
    beqz t5, fim_copia
    sb t5, 0(s3)
    addi t4, t4, 1
    addi s3, s3, 1
    addi s2, s2, 1
    j copia_saida

fim_copia:
    li t5, 32
    sb t5, 0(s3)
    addi s3, s3, 1
    addi s2, s2, 1

verifica_fim_texto:
    beqz s6, fim_processamento
    j proxima_palavra

fim_processamento:
    li a7, 1024
    la a0, saida
    li a1, 1
    ecall
    mv s0, a0

    li a7, 64
    mv a0, s0
    la a1, buffer_saida
    mv a2, s2
    ecall

    li a7, 57
    mv a0, s0
    ecall

    li a7, 10
    ecall

verifica_sw:
    la t3, stopwords
    lw t4, num_sw
    mv t5, a0

loop_dicionario:
    beqz t4, fim_nao_encontrou
    lw t6, 0(t3)
    mv a2, t5
    mv a3, t6

loop_compara_chars:
    lbu a4, 0(a2)
    lbu a5, 0(a3)
    bne a4, a5, proxima_stopword
    beqz a4, fim_encontrou
    addi a2, a2, 1
    addi a3, a3, 1
    j loop_compara_chars

proxima_stopword:
    addi t3, t3, 4
    addi t4, t4, -1
    j loop_dicionario

fim_encontrou:
    li a0, 1
    ret

fim_nao_encontrou:
    li a0, 0
    ret

erro_abertura:
    li a7, 4
    la a0, erro_msg
    ecall
    
    li a7, 10
    ecall