use std::process::exit;

use utils::read_data_lines;

fn parse_input() -> Vec<Vec<i64>> {
    let lines = read_data_lines("./day9/src/data.input");

    return lines
        .iter()
        .map(|line| line.split_whitespace().into_iter().map(|n: &str| n.parse::<i64>().unwrap()).collect())
        .collect::<Vec<Vec<i64>>>();
}

fn reach_zero(data: Vec<i64>) -> Vec<Vec<i64>>{
    let mut current = data.clone();
    let mut diffs = Vec::new();
    loop {
        let mut diff = Vec::with_capacity(current.len() - 1);
        for i in 0..(current.len() - 1) {
            diff.push(current[i + 1] - current[i]);
        }
        if diff.iter().all(|&x| x == 0) {
            break;
        }
        current = diff.clone();
        diffs.push(diff);
    }
    return diffs;
}

pub fn part2() -> String{

    let data = parse_input();

    let mut summ = 0;
    for d in data {
        let mut difs = reach_zero(d.clone());
        difs.reverse();
        let mut diff = 0;
        for difsi in difs {
            diff = difsi[0] - diff;
            // println!("diff: {} {:?}", diff,difsi.clone());
        }
        let val = d[0] - diff;
        summ += val;
    }

    return summ.to_string()
}

pub fn part1() -> String{

    let data = parse_input();

    let mut summ = 0;
    for d in data {
        let mut difs = reach_zero(d.clone());
        difs.reverse();
        let mut diff = 0;
        for difsi in difs {
            let siz = difsi.len();
            diff = difsi[siz-1] + diff;
        }
        let val = d[d.len()-1] + diff;
        summ += val;
    }

    return summ.to_string()
}
