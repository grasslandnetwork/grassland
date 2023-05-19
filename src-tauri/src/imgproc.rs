use opencv::{
	core::{Mat_AUTO_STEP, Point, Point2f, Scalar, Size, Vec2f},
	imgproc,
	prelude::*,
	types::VectorOfPoint,
	Result,
};


#[cfg(test)]
mod tests {

    use super::*;
    
    #[test]
    pub fn min_enclosing() -> Result<()> {
        let mut pts = Mat::new_rows_cols_with_default(1, 2, Vec2f::opencv_type(), Scalar::default())?;
        let points = pts.at_row_mut::<Vec2f>(0)?;
        points[0].copy_from_slice(&[10., 10.]);
        points[1].copy_from_slice(&[20., 10.]);

        let mut center = Point2f::default();
        let mut radius = 0.;
        imgproc::min_enclosing_circle(&pts, &mut center, &mut radius)?;
        assert_eq!(radius, 5.0001);
        assert_eq!(center, Point2f::new(15., 10.));
        println!("Message from bottom of opencv-rust imgproc::min_enclosing function");
        Ok(())
    }

} // mod tests
