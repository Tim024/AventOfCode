use utils::read_data_matrix;
use std::fs::File;
use std::io::prelude::*;

fn moveit(current_pipe: char, pipe: char, direction: (isize, isize)) -> bool {
    match direction {
        (1, 0) => match current_pipe {
            '|' => match pipe {
                '|' => return true,
                'J' => return true,
                'L' => return true,
                _ => return false,
            }
            '7' => match pipe {
                '|' => return true,
                'J' => return true,
                'L' => return true,
                _ => return false,
            }
            'F' => match pipe {
                '|' => return true,
                'J' => return true,
                'L' => return true,
                _ => return false,
            },
            'S' => match pipe {
                '|' => return true,
                'J' => return true,
                'L' => return true,
                _ => return false,
            }
            _ => return false,
        },
        (0, 1) => match current_pipe {
            '-' =>match pipe {
                '-' => return true,
                '7' => return true,
                'J' => return true,
                _ => return false,
            },
            'F' => match pipe {
                '-' => return true,
                '7' => return true,
                'J' => return true,
                _ => return false,
            },
            'L' =>match pipe {
                '-' => return true,
                '7' => return true,
                'J' => return true,
                _ => return false,
            }
            'S' =>match pipe {
                '-' => return true,
                '7' => return true,
                'J' => return true,
                _ => return false,
            }
            _ => return false,   
        },
        (-1, 0) => match current_pipe {
            '|' => match pipe {
                '|' => return true,
                '7' => return true,
                'F' => return true,
                _ => return false,
            },
            'L' => match pipe {
                '|' => return true,
                '7' => return true,
                'F' => return true,
                _ => return false,
            },
            'J' => match pipe {
                '|' => return true,
                '7' => return true,
                'F' => return true,
                _ => return false,
            }
            'S' => match pipe {
                '|' => return true,
                '7' => return true,
                'F' => return true,
                _ => return false,
            }
            _ => return false,
        },
        (0, -1) => match current_pipe {
            '-' => match pipe {
                '-' => return true,
                'F' => return true,
                'L' => return true,
                _ => return false,
            },
            '7' => match pipe {
                '-' => return true,
                'F' => return true,
                'L' => return true,
                _ => return false,
            },
            'J' => match pipe {
                '-' => return true,
                'F' => return true,
                'L' => return true,
                _ => return false,
            }
            'S' => match pipe {
                '-' => return true,
                'F' => return true,
                'L' => return true,
                _ => return false,
            }
            _ => return false,
        },
        _ => return false,
    }
}

static ALL_DIRECTIONS: [(isize, isize); 4] = [(0, 1), (1, 0), (0, -1), (-1, 0)];

fn solve() -> (usize, Vec<Vec<char>>) {
    // let data = read_data_matrix("./day10/src/data.input");
    // let starting_position: (isize, isize) = (58, 51);
    let data = read_data_matrix("./day10/src/data.example");
    let starting_position: (isize, isize) = (0, 4);

    let mut new_data = data.clone();

    dbg!(starting_position, data[starting_position.0 as usize][starting_position.1 as usize]);

    assert!(data[starting_position.0 as usize][starting_position.1 as usize] == 'S', "Starting position is not a S!");

    let mut steps = 0;
    let mut position = starting_position;
    let mut possible_directions: Vec<&(isize, isize)> = Vec::from_iter(ALL_DIRECTIONS.iter());

    loop {
        let pipe = data[position.0 as usize][position.1 as usize];

        // println!(
        //     "Position: {position:?}, Pipe: {pipe}, Possible directions: {possible_directions:?}",
        //     position = position,
        //     pipe = pipe,
        //     possible_directions = possible_directions
        // );
        let mut new_possible_directions: Vec<&(isize, isize)> =
            Vec::from_iter(ALL_DIRECTIONS.iter());
        for d in &possible_directions {
            new_data[position.0 as usize][position.1 as usize] = 'X';
            let direction = **d;

            if position.0 + direction.0 < 0
                || position.0 + direction.0 >= data.len() as isize
                || position.1 + direction.1 < 0
                || position.1 + direction.1 >= data[0].len() as isize
            {
                // println!("\t{direction:?} is out of bounds!", direction = direction);
                continue;
            }
            let next_pipe = data[(position.0 + direction.0) as usize]
                [(position.1 + direction.1) as usize];
            // println!(
            //     "\t{pipe} -> {next_pipe} Trying direction: {direction:?} {tmp}",
            //     tmp = moveit(pipe, next_pipe, direction)
            // );
            if moveit(pipe, next_pipe, direction) {
                position.0 += direction.0;
                position.1 += direction.1;
                new_possible_directions.retain(|&x| !(x.0 == -d.0 && x.1 == -d.1));
                steps += 1;
                println!("\t\tDirection chosen: {direction:?}, Steps: {steps}");
                break;
            }
        }
        possible_directions = new_possible_directions;
        if possible_directions.len() == 4 {
            println!("No possible directions!");
            break;
        }
    }

    (steps, new_data)
}

pub fn part1() -> String {

    let (steps, _new_data) = solve();
    let solution = (steps+1)/2;

    return solution.to_string();
}

pub fn part2() -> String {

    let (steps, new_data) = solve();
    let mut new_data = new_data;

    let x_max = new_data.len();
    let y_max = new_data[0].len();
    // Fill borders with O
    for x in 0..x_max {
        if new_data[x][0] != 'X' {
            new_data[x][0] = 'O';
        }
        if new_data[x][y_max -1] != 'X' {
            new_data[x][y_max -1] = 'O';
        }
    }
    for y in 0..y_max {
        if new_data[0][y] != 'X' {
            new_data[0][y] = 'O';
        }
        if new_data[x_max - 1][y] != 'X' {
            new_data[x_max - 1][y] = 'O';
        }
    }

    for inc in 1..x_max/2 {
        for x in inc..x_max - inc {
            // Check if adjacent tiles are filled with O:
            if new_data[x][inc-1] == 'O' {
                if new_data[x][inc] != 'X' {
                    new_data[x][inc] = 'O';
                }
            }
            if new_data[x][y_max - inc] == 'O' {
                if new_data[x][y_max -1 - inc] != 'X' {
                    new_data[x][y_max -1 - inc] = 'O';
                }
            }
        }
        for y in inc..y_max-inc {
            if new_data[inc-1][y] == 'O' {
                if new_data[inc][y] != 'X' {
                    new_data[inc][y] = 'O';
                }
            }
            if new_data[x_max - inc][y] == 'O' {
                if new_data[x_max - 1 - inc][y] != 'X' {
                    new_data[x_max - 1 - inc][y] = 'O';
                }
            }
        }
    }

    // Count elements that are not O or X:
    let solution = new_data.iter().flatten().filter(|&x| *x != 'O' && *x != 'X').count();

    // Write to file:
    let mut file = std::fs::File::create("./day10/src/data.output").unwrap();
    for x in 0..x_max {
        for y in 0..y_max {
            write!(file, "{} ", new_data[x][y]).unwrap(); // Added space after {}
        }
        write!(file, "\n").unwrap();
    }


    return solution.to_string();
}
