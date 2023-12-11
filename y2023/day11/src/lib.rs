use utils::read_data_matrix;
use utils::write_data_matrix;

fn abs_difference(x: usize, y: usize) -> u32 {
    if x < y {
        (y - x) as u32
    } else {
        (x - y) as u32
    }
}

#[derive(Debug, Clone, Copy)]
struct Galaxy
{
    x: usize,
    y: usize,
}

fn manhattan(p1: Galaxy, p2: Galaxy) -> u32 {
    abs_difference(p2.x, p1.x) + abs_difference(p2.y, p1.y)
}

fn expand_space(data: Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut new_data = data.clone();
    let mut new_rows_index = Vec::new();
    let mut new_cols_index = Vec::new();
    for (i, row) in data.iter().enumerate() {
        if row.iter().all(|x| *x == '.') {
            new_rows_index.push(i);
        }
    }
    for (i, col) in data[0].iter().enumerate() {
        if data.iter().all(|x| x[i] == '.') {
            new_cols_index.push(i);
        }
    }
    for i in new_rows_index.iter().rev() {
        let empty_row = vec!['.'; data[0].len()];
        new_data.insert(*i, empty_row)
    }
    for i in new_cols_index.iter().rev() {
        for row in new_data.iter_mut() {
            row.insert(*i, '.')
        }
    }
    new_data
}



pub fn part1() -> String{
    let data = read_data_matrix("./day11/src/data.input");

    let data = expand_space(data);

    let galaxy_positions: Vec<Galaxy> = data.iter().enumerate().flat_map(|(x, row)| {
        row.iter().enumerate().filter_map(move |(y, col)| {
            if *col == '#' {
                Some(Galaxy{x, y})
            } else {
                None
            }
        })
    }).collect();

    let mut distances = Vec::new();
    for (i,g1) in galaxy_positions.iter().enumerate() {
        for (j,g2) in galaxy_positions.iter().enumerate() {
            if j <= i {
                continue;
            }
            distances.push(manhattan(*g1, *g2));
            println!("G1 {i}: {g1:?}, G2 {j}: {g2:?}, Distance: {}", manhattan(*g1, *g2));
        }
    }

    write_data_matrix("./day11/src/data.output", &data);
    let sum_distances: u32 = distances.iter().sum();

    return sum_distances.to_string()
}

pub fn part2() -> String{
    let data = read_data_matrix("./day11/src/data.input");

    let galaxy_positions: Vec<Galaxy> = data.iter().enumerate().flat_map(|(x, row)| {
        row.iter().enumerate().filter_map(move |(y, col)| {
            if *col == '#' {
                Some(Galaxy{x, y})
            } else {
                None
            }
        })
    }).collect();

    let mut distances = Vec::new();
    for (i,g1) in galaxy_positions.iter().enumerate() {
        for (j,g2) in galaxy_positions.iter().enumerate() {
            if j <= i {
                continue;
            }
            distances.push(manhattan(*g1, *g2)); // Change the way to calculate distance
            println!("G1 {i}: {g1:?}, G2 {j}: {g2:?}, Distance: {}", manhattan(*g1, *g2));
        }
    }

    write_data_matrix("./day11/src/data.output", &data);
    let sum_distances: u32 = distances.iter().sum();

    return sum_distances.to_string()
}
