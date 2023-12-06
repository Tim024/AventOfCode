use utils::read_data_lines;

fn parse_input(lines: Vec<String>) -> (Vec<u64>, Vec<u64>, usize) {
    let times = lines
        .first()
        .unwrap()
        .split(":")
        .nth(1)
        .unwrap()
        .split_whitespace()
        .map(|x| x.parse::<u64>().unwrap())
        .collect::<Vec<u64>>();

    let distances = lines
        .last()
        .unwrap()
        .split(":")
        .nth(1)
        .unwrap()
        .split_whitespace()
        .map(|x| x.parse::<u64>().unwrap())
        .collect::<Vec<u64>>();

    let n_races = times.len();

    (times, distances, n_races)
}

fn parse_input_part2(lines: Vec<String>) -> (u64, u64) {
    fn remove_whitespace(s: &mut String) {
        s.retain(|c| !c.is_whitespace());
    }

    let times = lines.first().unwrap().split(":").nth(1).unwrap();

    let mut times: String = times.to_string();
    remove_whitespace(&mut times);
    let times = times.parse::<u64>().unwrap();

    let distances = lines.last().unwrap().split(":").nth(1).unwrap();

    let mut distances: String = distances.to_string();
    remove_whitespace(&mut distances);
    let distances = distances.parse::<u64>().unwrap();

    (times, distances)
}

fn calc_distances(max_time: u64) -> Vec<u64> {
    let mut dists = Vec::new();
    for hold in 1..max_time {
        dists.push((max_time - hold) * hold); // speed is equal to hold
    }
    dists
}

pub fn part1() -> String {
    let lines = read_data_lines("./day6/src/data.input");

    let (times, distances, n_races) = parse_input(lines);

    let mut counts = 1;
    for i in 0..n_races {
        let max_min_time = times[i];
        let min_distance = distances[i];
        let dists = calc_distances(max_min_time);
        let count = dists.iter().filter(|x| **x > min_distance).count();
        counts *= count;
    }

    return counts.to_string();
}

pub fn part2() -> String {
    let lines = read_data_lines("./day6/src/data.input");

    let (max_time, min_distance) = parse_input_part2(lines);

    let dists = calc_distances(max_time);
    let count = dists.iter().filter(|x| **x > min_distance).count();

    return count.to_string();
}
