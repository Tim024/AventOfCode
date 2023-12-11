use utils::read_data_matrix;
use utils::write_data_matrix;

fn abs_difference(x: i64, y: i64) -> u64 {
    (x - y).abs() as u64
}

#[derive(Debug, Clone, Copy)]
struct Galaxy {
    x: i64,
    y: i64,
}

fn empty_spaces(data: &[Vec<char>]) -> (Vec<u64>, Vec<u64>) {
    let new_rows_index = data
        .iter()
        .enumerate()
        .filter(|&(_, row)| row.iter().all(|&x| x == '.'))
        .map(|(i, _)| i as u64)
        .collect();
    let new_cols_index = (0..data[0].len())
        .filter(|&i| data.iter().all(|x| x[i] == '.'))
        .map(|i| i as u64)
        .collect();

    (new_rows_index, new_cols_index)
}

fn generate_galaxy_positions(data: &[Vec<char>]) -> Vec<Galaxy> {
    data.iter()
        .enumerate()
        .flat_map(|(x, row)| {
            row.iter().enumerate().filter_map(move |(y, &col)| {
                if col == '#' {
                    Some(Galaxy {
                        x: x as i64,
                        y: y as i64,
                    })
                } else {
                    None
                }
            })
        })
        .collect()
}

fn calc_distance(
    p1: Galaxy,
    p2: Galaxy,
    new_rows_index: &[u64],
    new_cols_index: &[u64],
    mult: u64,
) -> u64 {
    let base_distance = abs_difference(p1.x, p2.x) + abs_difference(p1.y, p2.y);
    let x_range = p1.x.min(p2.x) as u64..p1.x.max(p2.x) as u64;
    let y_range = p1.y.min(p2.y) as u64..p1.y.max(p2.y) as u64;

    let n_empty_rows = new_rows_index
        .iter()
        .filter(|&&x| x_range.contains(&x))
        .count() as u64;
    let n_empty_cols = new_cols_index
        .iter()
        .filter(|&&y| y_range.contains(&y))
        .count() as u64;

    base_distance + (n_empty_rows + n_empty_cols) * mult
}

fn solve(empty_space: u64) -> String {
    let data = read_data_matrix("./day11/src/data.input");
    let (new_rows_index, new_cols_index) = empty_spaces(&data);

    let galaxy_positions = generate_galaxy_positions(&data);

    let sum_distances: u64 = galaxy_positions
        .iter()
        .enumerate()
        .flat_map(|(i, &g1)| {
            let new_rows_index_clone = new_rows_index.clone();
            let new_cols_index_clone = new_cols_index.clone();
            galaxy_positions
                .iter()
                .enumerate()
                .skip(i + 1)
                .map(move |(_, &g2)| {
                    calc_distance(
                        g1,
                        g2,
                        &new_rows_index_clone,
                        &new_cols_index_clone,
                        empty_space,
                    )
                })
        })
        .sum();

    sum_distances.to_string()
}

pub fn part1() -> String {
    solve(1)
}

pub fn part2() -> String {
    solve(999_999)
}
