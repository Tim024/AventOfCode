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
    let lines = read_data_lines("./day8/src/data.input");

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


pub fn part2() -> String {
    let (instructions, nodes) = parse_input();

    let mut period = 1;
    let mut offset = 0;
    let starting_nodes: Vec<String> = nodes.keys().filter(|k| k.ends_with("A")).map(|k| k.clone()).collect();

    for n in starting_nodes.iter(){
        let mut current_node = n.clone();
        let mut i = 0;
        let mut step = 0;
        let mut loop_steps = 0;
        let mut loop_start = false;
        loop {
            if loop_start {
                loop_steps += 1;
            } else{
                step += 1;
            }
    
            let c = instructions.chars().nth(i).unwrap();
            if c == 'L' {
                current_node = nodes.get(&current_node).unwrap().child_l.clone();
            } else if c == 'R' {
                current_node = nodes.get(&current_node).unwrap().child_r.clone();
            }
    
            // dbg!(current_node.clone(), loop_steps, step, i, c);
            i = (i + 1) % instructions.len();
    
            if current_node.ends_with("Z") {
                if loop_start {
                    break;
                }
                loop_start = true;
            }
        }

        offset = (step - loop_steps).max(offset);
        period = lcm(period, loop_steps);
    }
    

    return (offset + period).to_string();
}
