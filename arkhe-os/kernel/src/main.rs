#![no_std]
#![no_main]

use core::panic::PanicInfo;

mod axiarchy;
mod ipc;
mod isolation;
mod memory;
mod scheduler;
mod syscalls;
mod temporal;

#[no_mangle]
pub extern "C" fn kmain() -> ! {
    // Inicialização do kernel
    loop {}
}

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}
