use nalgebra::{Vector3, Matrix3};

pub struct KalmanFilter {
    pub state: Vector3<f32>,
    pub covariance: Matrix3<f32>,
    pub process_noise: Matrix3<f32>,
    pub measurement_noise: Matrix3<f32>,
}

impl KalmanFilter {
    pub fn new() -> Self {
        Self {
            state: Vector3::new(0.0, 0.0, 9.81),
            covariance: Matrix3::identity() * 1.0,
            process_noise: Matrix3::identity() * 0.01,
            measurement_noise: Matrix3::identity() * 0.1,
        }
    }

    pub fn predict(&mut self, control: Vector3<f32>) {
        self.state += control;
        self.covariance += self.process_noise;
    }

    pub fn update(&mut self, measurement: Vector3<f32>) {
        let k = self.covariance * (self.covariance + self.measurement_noise).try_inverse().unwrap();
        self.state += k * (measurement - self.state);
        self.covariance = (Matrix3::identity() - k) * self.covariance;
    }
}

pub fn init() {
    println!("Sensor Fusion: Kalman filter initialized.");
}

pub fn update() {
    let mut kf = KalmanFilter::new();
    let control = Vector3::new(0.0, 0.0, 0.0);
    kf.predict(control);
    let measurement = Vector3::new(0.0, 0.0, 9.81);
    kf.update(measurement);
    println!("Sensor Fusion: Updated state: {:?}", kf.state);
}
