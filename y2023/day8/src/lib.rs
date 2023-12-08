use regex::Regex;
use std::collections::HashMap;
use utils::read_data_lines;

#[derive(Debug, Clone)]
struct Node {
    // name: String,
    child_l: String,
    child_r: String,
}

fn parse_elements(input: &str) -> Option<(String, String, String)> {
    let re = Regex::new(r"(\w+) = \((\w+), (\w+)\)").unwrap();
    re.captures(input)
        .map(|cap| (cap[1].to_string(), cap[2].to_string(), cap[3].to_string()))
}

fn parse_input() -> (String, HashMap<String, Node>) {
    println!("Building...");
    let lines = read_data_lines("./day8/src/data.example");

    let instruction = lines.first().unwrap().clone();
    let mut nodes = HashMap::new();

    // dbg!(instruction);

    for l in lines {
        if let Some((name, child_l, child_r)) = parse_elements(&l) {
            if !(nodes.contains_key(&name)) {
                nodes.insert(name, Node { child_l, child_r });
            }
        }
    }

    println!("Done!");
    (instruction, nodes)
}

const fn gcd(mut a: usize, mut b: usize) -> usize {
    while b != 0 {
        (a, b) = (b, a % b);
    }
    a
}

const fn lcm(a: usize, b: usize) -> usize {
    a / gcd(a, b) * b
}

pub fn part1() -> String {
    let (instructions, nodes) = parse_input();

    let mut current_node = "AAA".to_string();
    let mut i = 0;
    let mut step = 0;
    loop {
        step += 1;
        let c = instructions.chars().nth(i).unwrap();
        if c == 'L' {
            current_node = nodes.get(&current_node).unwrap().child_l.clone();
        } else if c == 'R' {
            current_node = nodes.get(&current_node).unwrap().child_r.clone();
        }

        i += 1;
        if i == instructions.len() {
            i = 0;
        }
        if current_node == "ZZZ" {
            break;
        }
    }

    return step.to_string();
}

/**
 *
L
11A = (11B, XXX)
11B = (11C, XXX)
11C = (11D, XXX)
11D = (11Z, XXX)
11Z = (11A, XXX)
12A = (12B, XXX)
12B = (12Z, XXX)
12Z = (12A, XXX)
13A = (13B, XXX)
13B = (13C, XXX)
13C = (13D, XXX)
13D = (13E, XXX)
13E = (13Z, XXX)
13Z = (13A, XXX)
XXX = (XXX, XXX)

LR
11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)

 * 
 * 
 */

pub fn part2() -> String {
    "Not yet".to_string()
}



