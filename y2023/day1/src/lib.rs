use utils::read_data_lines;

fn parse_digits(t_num: &str) -> Vec<u32> {
    t_num
        .chars()
        .filter_map(|a| a.to_digit(10))
        .collect()
}

fn parse_written_digits_and_digits(line: &str) -> Vec<u32> {
    let mut digits = Vec::new();
    let stri_siz_di = [
        ("zero", 4, 0), 
        ("one", 3 ,1), 
        ("two", 3, 2), 
        ("three", 5, 3), 
        ("four", 4, 4), 
        ("five", 4, 5), 
        ("six", 3, 6), 
        ("seven", 5, 7), 
        ("eight", 5, 8), 
        ("nine", 4, 9)
    ];
    
    for (i, c) in line.chars().enumerate() {
        if c.to_digit(10).is_some() {
            digits.push(c.to_digit(10).unwrap());
        } else {
            for (word, siz, di) in stri_siz_di.iter() {
                if line.len() < i+siz {
                    continue;
                }
                if line[i..i+siz].eq(*word) {
                    digits.push(*di);
                    break;
                }
            }
        }
    }
    digits
}

pub fn part1() -> String{
    let lines = read_data_lines("./day1/src/data.input");
    
    let mut sum = 0;
    for line in lines {
        let digits = parse_digits(&line);
        let first_digit = digits.first().unwrap();
        let last_digit = digits.last().unwrap();
        let number = first_digit*10 + last_digit;
        // dbg!(line, digits, number);
        sum += number;
    }

    return sum.to_string()
}

pub fn part2() -> String{
    let lines = read_data_lines("./day1/src/data.input");
    // let lines = input.lines();
    
    let mut sum = 0;
    for line in lines {
        let digits = parse_written_digits_and_digits(&line);
        let first_digit = digits.first().unwrap();
        let last_digit = digits.last().unwrap();
        let number = first_digit*10 + last_digit;
        // println!("{line} -> {digits:?} -> {number}");
        sum += number;
    }
    
    return sum.to_string()
}
