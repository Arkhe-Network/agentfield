; boot/bootloader_arm64.asm
.global _start

.extern kmain

.section .text
_start:
    // Carregar kernel ELF do IPFS
    // Verificar assinatura Ed25519
    // Configurar MMU e EL (Exception Level)
    // Saltar para kmain
    b kmain
