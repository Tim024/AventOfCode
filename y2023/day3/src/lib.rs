use utils::read_data_matrix;
use std::collections::HashMap;


fn symbol_in_window(
    matrix: &Vec<Vec<char>>, 
    x_l: usize,
    x_r: usize, 
    y_t: usize, 
    y_b: usize,
    symbols: String
) -> bool {
    (x_l..=x_r).any(|x| (y_t..=y_b).any(|y| symbols.contains(matrix[y][x])))
}


pub fn part1() -> String{

    let matrix = read_data_matrix("./day3/src/data.input");
    let siz_x = matrix[0].len();
    let siz_y = matrix.len();

    let mut summ = 0;
    for y in 0..siz_y {
        let mut x = 0;
        while x < siz_x {

            if matrix[y][x].is_digit(10){
                // Read entire number
                let mut c2 = matrix[y][x];
                let mut current_number: Vec<char> = Vec::new();
                while c2.is_digit(10){
                    current_number.push(c2.to_string().chars().next().unwrap());
                    x += 1;
                    if x > siz_x - 1 {break}
                    c2 = matrix[y][x];
                }
                x -= 1;
                
                let siz = current_number.len();
                let x_l = if x < siz {0} else {x - siz};
                let x_r = if x + 1 == siz_x {x} else {x + 1};
                let y_t = if y < 1 {0} else {y - 1};
                let y_b = if y > siz_y - 2 {siz_y - 1} else {y + 1};
    
                // Add if valid
                if symbol_in_window(&matrix, x_l, x_r, y_t, y_b, "/=%@-_!^(&)$+*#".to_string()) {
                    summ += current_number.iter().collect::<String>().parse::<u32>().unwrap();
                }
            }
            x += 1;
        }
    }
    return summ.to_string()
}

pub fn part2() -> String{
    let matrix = read_data_matrix("./day3/src/data.input");
    let siz_x = matrix[0].len();
    let siz_y = matrix.len();

    let mut hashmap = HashMap::new();

    for y in 0..siz_y {
        let mut x = 0;
        while x < siz_x {
            if matrix[y][x].is_digit(10){
                // Read entire number
                let mut c2 = matrix[y][x];
                let mut current_number: Vec<char> = Vec::new();
                while c2.is_digit(10){
                    current_number.push(c2.to_string().chars().next().unwrap());
                    x += 1;
                    if x > siz_x - 1 {break}
                    c2 = matrix[y][x];
                }
                x -= 1;
                
                let siz = current_number.len();
                let x_l = if x < siz {0} else {x - siz};
                let x_r = if x + 1 == siz_x {x} else {x + 1};
                let y_t = if y < 1 {0} else {y - 1};
                let y_b = if y > siz_y - 2 {siz_y - 1} else {y + 1};
                let number: u32 = current_number.iter().collect::<String>().parse::<u32>().unwrap();

                // Scan for symbol:
                for y1 in y_t..=y_b {
                    for x1 in x_l..=x_r {
                        if matrix[y1][x1] == '*' {
                            hashmap
                                .entry((x1, y1))
                                .and_modify(|(v, b)| (*v, *b) = ((*v)*number , true))
                                .or_insert((number, false));
                            }
                        }
                    }
                }
            x += 1;
            }
        }
    let sum = hashmap.values().filter(|(_, b)| *b).map(|(v, _)| v).sum::<u32>();
    return sum.to_string()
}
