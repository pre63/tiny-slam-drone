pub fn init() {
    println!("Flight Controller: PWM outputs and motor controllers initialized.");
}

pub fn set_motor_speed(motor: u8, speed: f32) {
    let pwm_value = (speed * 255.0) as u8;
    println!("Flight Controller: Motor {} set to PWM value {}.", motor, pwm_value);
}
