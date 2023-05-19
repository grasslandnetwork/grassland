use opencv::{
	core::{self, Moments, Point2f, RotatedRect, Scalar, Size2f, Vec3b, CV_32S, CV_64F, CV_8U, CV_MAKETYPE},
	prelude::*,
	types::VectorOfMat,
	Result,
};


#[cfg(test)]
mod tests {

    use super::*;

    #[test]
    pub fn make_type() {
        assert_eq!(8, CV_MAKETYPE(CV_8U, 2));
        assert_eq!(20, CV_MAKETYPE(CV_32S, 3));
        assert_eq!(6, CV_MAKETYPE(CV_64F, 1));
        println!("Message from bottom of opencv-rust core::make_type function");
    }

} // mod tests
