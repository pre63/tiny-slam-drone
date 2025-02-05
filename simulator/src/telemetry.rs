use log::info;
use tokio::time::{sleep, Duration};

pub async fn simulate_telemetry() {
    info!("Telemetry: Starting transmission...");
    for i in 1..=10 {
        info!("Telemetry: Packet {}", i);
        sleep(Duration::from_secs(1)).await;
    }
    info!("Telemetry: Transmission complete.");
}
