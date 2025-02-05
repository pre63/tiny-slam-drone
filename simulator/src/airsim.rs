use log::info;
use reqwest::Error;
use serde::Deserialize;

#[derive(Deserialize, Debug)]
pub struct SensorData {
    pub timestamp: u64,
    pub image_data: Vec<u8>,
    pub imu: (f32, f32, f32),
}

pub fn init() {
    info!("AirSim: Connection established.");
}

pub async fn fetch_sensor_data() -> Result<(), Error> {
    // Actual HTTP call to AirSim API.
    let url = "http://localhost:41451/api/simGetImages";
    let resp = reqwest::get(url).await?;
    if resp.status().is_success() {
        let sensor_data: SensorData = resp.json().await?;
        info!("AirSim: Fetched sensor data: {:?}", sensor_data);
    } else {
        info!("AirSim: HTTP error: {}", resp.status());
    }
    Ok(())
}
