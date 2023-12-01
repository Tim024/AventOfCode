use std::fs;
use std::path;


pub fn read_data(filepath: &str) -> String {
    let path = path::Path::new(filepath);
    // println!("Reading file: {:?}", path);
    let content = fs::read_to_string(path).expect("Couldn't read file");
    content
}

pub fn read_data_lines(filepath: &str) -> Vec<String> {
    let content = read_data(filepath);
    let lines: Vec<String> = content.lines().map(|s| s.to_string()).collect();
    lines
}