use std::fs;
use std::path;
use std::io::prelude::*;

pub fn write_data_matrix(filepath: &str, data: &Vec<Vec<char>>) {
    let mut file = std::fs::File::create(filepath).unwrap();
    let x_max = data.len();
    let y_max = data[0].len();
    for x in 0..x_max {
        for y in 0..y_max {
            write!(file, "{}", data[x][y]).unwrap(); // Added space after {}
        }
        write!(file, "\n").unwrap();
    }
}

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

pub fn read_data_matrix(filepath: &str) -> Vec<Vec<char>> {
    let content = read_data(filepath);
    let lines: Vec<Vec<char>> = content.lines().map(|s| s.chars().collect()).collect();
    lines
}