use std::fs::OpenOptions;
use std::io::Write;
use chrono::Utc;

pub fn init() {
    let mut file = OpenOptions::new()
        .append(true)
        .create(true)
        .open("diagnostics.log")
        .expect("Diagnostics: Unable to open diagnostics.log");
    let now = Utc::now();
    writeln!(file, "{} - Diagnostics initialized.", now).expect("Diagnostics: Unable to write log");
    println!("Diagnostics: Logging system initialized.");
}
