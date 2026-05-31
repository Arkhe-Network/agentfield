; boot/bootloader_arm64.asm
.global _start

_start:
    /* Carregar kernel via IPFS */
    /* Verificar assinatura via TrustZone / Ed25519 */
    /* Configurar MMU / page tables */
    /* Saltar para kmain */
    b kmain

kmain:
    b .
