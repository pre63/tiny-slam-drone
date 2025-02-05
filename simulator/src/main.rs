mod airsim;
mod px4_integration;
mod telemetry;

#[tokio::main]
async fn main() {
    env_logger::init();
    println!("Starting AirSim Simulator Integration...");

    airsim::init();
    // Continuously fetch sensor data from AirSim.
    tokio::spawn(async {
        loop {
            if let Err(e) = airsim::fetch_sensor_data().await {
                eprintln!("Error fetching sensor data: {:?}", e);
            }
            tokio::time::sleep(tokio::time::Duration::from_millis(100)).await;
        }
    });
    px4_integration::init();
    telemetry::simulate_telemetry().await;
    println!("AirSim Simulator Integration terminated.");
}
