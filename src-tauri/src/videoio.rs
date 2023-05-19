use opencv::{core, videoio::VideoWriter, Error, Result};

#[cfg(test)]
mod tests {

    use matches::assert_matches; // a 'dev-dependency' in Cargo.toml

    use super::*;

    #[test]
    pub fn fourcc() -> Result<()> {
        let fourcc = VideoWriter::fourcc('a', 'v', 'c', '1')?;
        assert_eq!(fourcc, 0x31637661);
        let fourcc_error = VideoWriter::fourcc('😀', 'v', 'c', '1');
        assert_matches!(
            fourcc_error,
            Err(Error {
                code: core::StsBadArg,
                ..
            })
        );
        println!("Message from bottom of opencv-rust videoio::fourcc function");
        Ok(())
    }

} // mod tests

