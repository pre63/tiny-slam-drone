mod flight_controller;
mod sensor_fusion;
mod slam;
mod navigation;
mod calibration;
mod diagnostics;

fn main() {
    env_logger::init();
    println!("Initializing Drone Controller...");

    calibration::calibrate();
    flight_controller::init();
    sensor_fusion::init();
    slam::init();
    navigation::init();
    diagnostics::init();

    for motor in 0..4 {
        flight_controller::set_motor_speed(motor, 0.75);
    }
    sensor_fusion::update();
    slam::process_frame();
    navigation::plan_path("target_waypoint");

    println!("Drone Controller loop executed.");
}
