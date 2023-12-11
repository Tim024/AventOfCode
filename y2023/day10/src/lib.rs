use utils::read_data_matrix;


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

fn solve() -> (usize, Vec<Vec<char>>, Vec<Vec<char>>) {
    // let data = read_data_matrix("./day10/src/data.input");
    // let starting_position: (isize, isize) = (58, 51);
    let data = read_data_matrix("./day10/src/data.example");
    let starting_position: (isize, isize) = (4, 12);

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

    (steps, new_data, data.clone())
}

pub fn part1() -> String {

    let (steps, _new_data, _) = solve();
    let solution = (steps+1)/2;

    return solution.to_string();
}

pub fn part2() -> String {

    fn fill_with_O(old_data: Vec<Vec<char>>, new_data: &mut Vec<Vec<char>>, updown: bool, position: (usize, usize), k: &mut usize){
        let char = new_data[position.0][position.1];
        let old_char = old_data[position.0][position.1];
        if char == 'O' || char == 'I' {
            return;
        }
        if char == 'X' {
            if updown && (old_char == '|' || old_char == 'F' || old_char == '7' || old_char == 'J' || old_char == 'L' || old_char == 'S') {
                *k += 1;
                *k %= 2;
            }
            if !updown && (old_char == '-' || old_char == 'F' || old_char == '7' || old_char == 'J' || old_char == 'L' || old_char == 'S') {
                *k += 1;
                *k %= 2;
            }
            return;
        }
        if *k == 0 {
            new_data[position.0][position.1] = 'O';
        } else {
            new_data[position.0][position.1] = 'I';
        }
    }

    let (steps, new_data, old_data) = solve();
    let mut new_data = new_data;

    let x_max = new_data.len();
    let y_max = new_data[0].len();
    // Fill borders with O
    for x in 0..x_max {
        let mut k = 0;
        for y in 0..y_max {
            fill_with_O(old_data.clone(), &mut new_data, true, (x, y), &mut k);
        }
        // break;
    }

    // Count elements that are not O or X:
    let solution = new_data.iter().flatten().filter(|&x| *x != 'O' && *x != 'X').count();


    return solution.to_string();
}
