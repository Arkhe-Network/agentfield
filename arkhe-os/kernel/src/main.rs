#![no_std]
#![no_main]

use core::panic::PanicInfo;

pub mod memory;
pub mod scheduler;
pub mod syscalls;
pub mod ipc;
pub mod isolation;
pub mod temporal;
pub mod axiarchy;

#[no_mangle]
pub extern "C" fn kmain() -> ! {
    // Initialize memory, scheduler, IPC, isolation, temporal chain, and axiarchy verifier.
    loop {}
}

#[panic_handler]
fn panic(_info: &PanicInfo) -> ! {
    loop {}
}
