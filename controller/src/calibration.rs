use opencv::calib3d;
use opencv::core;
use opencv::imgcodecs;
use opencv::imgproc;
use opencv::prelude::*;
use opencv::types::VectorOfPoint2f;

pub fn calibrate() {
    let image_path = "test_data/calibration.jpg";
    let img = imgcodecs::imread(image_path, imgcodecs::IMREAD_COLOR)
        .expect("Calibration: Failed to load image.");
    let mut gray = core::Mat::default();
    imgproc::cvt_color(&img, &mut gray, imgproc::COLOR_BGR2GRAY, 0).unwrap();

    let board_size = core::Size { width: 7, height: 7 };
    let mut corners = VectorOfPoint2f::new();
    let found = calib3d::find_chessboard_corners(&gray, board_size, &mut corners, 0).unwrap();
    if found {
        println!("Calibration: Found {} corners.", corners.len());
        let object_points = vec![vec![(0.0, 0.0, 0.0); 49]];
        let image_points = vec![corners.to_vec()];
        let image_size = gray.size().unwrap();
        let (ret, camera_matrix, dist_coeffs, _, _) = calib3d::calibrate_camera(&object_points, &image_points, image_size, core::Mat::default(), core::Mat::default(), 0).unwrap();
        println!("Calibration: Camera matrix: {:?}", camera_matrix);
        println!("Calibration: Distortion coefficients: {:?}", dist_coeffs);
    } else {
        println!("Calibration: Chessboard pattern not detected.");
    }
}
