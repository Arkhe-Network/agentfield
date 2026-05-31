.PHONY: all kernel bootloader servers tools

all: bootloader kernel servers tools

bootloader:
	@echo "Building bootloader..."
	nasm -f elf64 boot/bootloader.asm -o boot/bootloader.o
	ld -T boot/bootloader.ld boot/bootloader.o -o boot/bootloader.bin

kernel:
	@echo "Building kernel..."
	cd kernel && cargo build --release

servers:
	@echo "Building servers..."
	cargo build --workspace --exclude kernel --release

tools:
	@echo "Building tools..."
	cargo build --workspace --exclude kernel --release

clean:
	cargo clean
	rm -f boot/*.o boot/*.bin
