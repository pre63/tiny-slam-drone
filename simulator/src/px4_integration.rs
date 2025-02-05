use log::info;
use mavlink::{MavHeader, common::MavMessage, MavConnection};
use std::net::UdpSocket;

pub fn init() {
    // Open a UDP socket for MAVLink messages.
    let socket = UdpSocket::bind("0.0.0.0:14550").expect("Failed to bind UDP socket");
    socket.set_nonblocking(true).expect("Failed to set nonblocking");
    info!("PX4 Integration: UDP socket bound on 14550.");
}

pub fn send_control_command(command: &str) {
    info!("PX4 Integration: Sending control command: {}", command);
    let socket = UdpSocket::bind("0.0.0.0:0").expect("Failed to bind UDP socket for sending");
    let target = "127.0.0.1:14550";
    let payload = command.as_bytes();
    socket.send_to(payload, target).expect("Failed to send control command");
}
