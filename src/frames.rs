pub fn send_frames_to_docker() {
    // Send new frame's ndarray from Rust to Docker container running object detection server
}


// tells node which of their frames must be used for evaluation
// hash the concatenation of the all the CFD's five times();
mod evaluation {
    // pub fn hash_concatenation_of_all_cfds_five_times() {}
    pub fn make_merkle_tree_from_frames();
}



pub fn replace_corners() {
    // Replace four corners of ndarray with a frame shape with the first 12 bytes of a 256 bit sequence
}


// each corner pixel is RGB so 3 x 8 bytes. There are 4 corners so 24 * 4 = 96. So take the first 96 bits of the 256 bit digest. Then pass frame to neural network
pub fn modify_frame_by_changing_pixels_in_four_corners_to_truncated_hash_of_last_frame_digest() {}

