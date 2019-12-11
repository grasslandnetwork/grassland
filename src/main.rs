mod settings;
mod videostream;
mod neural_network;
use std::process::Child;
use std::process::{Command};
use std::process::Stdio;
use std::io::{self, BufReader, Write};
use std::env;

fn main() {

    let args: Vec<String> = env::args().collect();
    
    // Get detection server settings
    let detection_server_meta: settings::DetectionServerMeta = settings::get_detection_server_meta();

    println!("detection server settings = {:?}", detection_server_meta);

    // Create connection to detection server
    let mut detect_stream = neural_network::detection::server::connect(&detection_server_meta);

    // Start pulling in frames from video stream
    videostream::start_frame_capture(&mut detect_stream, &args[1]);
 
}

