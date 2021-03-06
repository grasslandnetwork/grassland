

pub fn check_detection_size() {
    //Check that the size of a stream of bytes is 2532 bytes long
}

use duct::cmd;
use hex;
use std::io::Read;
use std::thread;
use std::time::{Duration, Instant};

use std::process::Stdio;

use std::sync::mpsc;
use std::marker::Send;

use std::net::{TcpListener, TcpStream, Shutdown};

pub fn start_frame_capture(mut detect_stream: &mut TcpStream, video_stream: &str) {

    // Start frame capture on child Python process

    // Create a simple streaming channel
    let (frame_tx, frame_rx) = mpsc::channel();

    // Start frame server and send transmitter to frame server so it can send back frames
    let frame_server_thread_handle = thread::spawn(move|| {
      frame_server(frame_tx);  
    });

    thread::sleep(Duration::from_millis(2000));
    
    let mut get_frames_reader = cmd!("python3", "python/get_frames.py", video_stream).reader().unwrap();

    let mut count = 0;
    for frame_vec in frame_rx { // should run as long as there are frames

        count += 1;

        if count < 300 {

            send_frame_to_detection_server(&mut detect_stream, frame_vec);
        } 

    }

    
    // Join thread. Because of the kill() above, both threads will exit
    // quickly.
    frame_server_thread_handle.join().unwrap();
    
    // FUNCTION::replace_corners();
}


pub fn send_frame_to_detection_server(detect_stream: &mut TcpStream, frame_vec: Vec<u8>) {

    // println!("about to send frame to detection server");
    
    detect_stream.write(&frame_vec).unwrap();
    detect_stream.flush().unwrap();

    // println!("frames sent to detection server");
    

    let mut buffer = vec![0; 6000];
    let mut unparsed: Vec<u8> = vec![];


    loop {


        let count = detect_stream.read(&mut buffer).unwrap();
        if count > 0 {
            unparsed.extend(buffer[0..count].iter());
            if unparsed.len() >= 2532 {
                let result = digest::digest(&digest::SHA256, &unparsed);
                println!("sha256 hash of detections_and_digests_encoded = {:?}", result);

                break;

            }
        } else {
            println!("Unexpected End of File");
            break;
        }
    }


}


use std::process::Child;


use std::io::{self, BufReader, Write};
use std::thread::JoinHandle;
use std::io::prelude::*;

use ring::{digest, test};

const frame_size: usize = 6220800; // usize because it's used to index a vector
const frame_checksum_size: usize = 32;
// const total_bytes: usize = frame_size + frame_checksum_size;
const total_bytes: usize = frame_size;

use std::sync::mpsc::Sender;

pub fn frame_server(tx: Sender<Vec<u8>>) {

    // 'ring' Test
    // let expected_hex = "09ca7e4eaa6e8ae9c7d261167129184883644d07dfba7cbfbc4c8a2e08360d5b";
    // let expected: Vec<u8> = test::from_hex(expected_hex).unwrap();
    // let actual = digest::digest(&digest::SHA256, b"hello, world");
    // assert_eq!(&expected, &actual.as_ref());

    let listener = TcpListener::bind("127.0.0.1:4442").unwrap();

    let mut now = Instant::now();
    let mut frame_count = 0;
    for stream in listener.incoming() {

        // println!("new stream");
        let stream = stream.unwrap();
        
        match handle_connection(stream) {
            Ok(frame_vec) => {

                // increment frame count to check FPS transfer rate
                frame_count += 1;

                tx.send(frame_vec);

            },
            Err(e) => {
                println!("{}", e);
            }
        };

        // println!("FRAME SERVER: current duration = {}", now.elapsed().as_secs());
        
        if now.elapsed().as_secs() > 50 {
            let this_secs = now.elapsed().as_secs();
            println!("FRAME SERVER: frame_count/per second = {}", frame_count/this_secs);
            frame_count = 0;
            
            now = Instant::now();
            // println!("FRAME SERVER: new system duration = {}", now.elapsed().as_secs());
        }
    }
    
}


fn handle_connection(mut stream: TcpStream) -> Result<Vec<u8>, &'static str> {
    // continuously return serialized numpy ndarray of frames to rust

    let mut buffer = vec![0; total_bytes];
    let mut unparsed: Vec<u8> = vec![];

    // let mut count = 0;
    loop {

        let count = stream.read(&mut buffer).unwrap();
        if count > 0 {
            unparsed.extend(buffer[0..count].iter());
            if unparsed.len() >= total_bytes {

                // return frame's bytes 
                return Ok(unparsed);
            }
        } else {
            return Err("Unexpected End of File");
        }
    }

}



pub fn node_creates_p2sh_out_of_the_htcoardt() {
}

