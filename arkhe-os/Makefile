.PHONY: all kernel bootloader run clean

all: bootloader kernel

kernel:
	cd kernel && cargo build --release

bootloader:
	# Assume nasm installed for bootloader asm building
	# nasm -f elf64 boot/bootloader.asm -o boot/bootloader.o
	# ld -T boot/bootloader.ld -o boot/bootloader.bin boot/bootloader.o

clean:
	cd kernel && cargo clean
	rm -f boot/*.o boot/*.bin
