use utils::read_data_lines;
use std::collections::HashMap;


fn parse_game(line: &str) -> HashMap<String, u32>{
    let mut game_hashmap:HashMap<String, u32> = HashMap::new();

    let l1:Vec<&str> = line.split(":").collect();
    let l2:Vec<&str> = l1[1].split(";").collect();
    for l3 in l2 {
        let l4:Vec<&str> = l3.split(",").collect();
        // dbg!(&l4);
        for l5 in l4{
            let l6:Vec<&str> = l5.split_whitespace().collect();
            // dbg!(&l6);
            let amount:u32 = l6[0].parse().unwrap();
            let color = l6[1].to_string();

            game_hashmap.entry(color).and_modify(|e| *e = (*e).max(amount)).or_insert(amount);
        }
    }
    game_hashmap
}

pub fn part1() -> String{
    let games = read_data_lines("./day2/src/data.input");

    let mut requirements: HashMap<String, u32> = HashMap::new();
    requirements.insert("red".to_string(), 12);
    requirements.insert("green".to_string(), 13);
    requirements.insert("blue".to_string(), 14);

    let mut sum_possible_games = 0;
    let mut game_id = 1;
    for g in games {
        let mut possible_game = true;
        // dbg!(game_id, &g);
        let hashmap = parse_game(&g);
        // dbg!(&hashmap);
        for (color, amount) in hashmap {
            if amount > *requirements.get(&color).unwrap_or(&0) {
                possible_game = false;
                break;
            }
        }
        if possible_game {
            sum_possible_games += game_id;
        }
        // dbg!(possible_game, sum_possible_games);
        game_id += 1;
    }

    return sum_possible_games.to_string()
}

pub fn part2() -> String{
    let games = read_data_lines("./day2/src/data.input");

    let mut power_sum = 0;
    for g in games {
        let hashmap = parse_game(&g);
        let power:u32 = hashmap.values().product();
        power_sum += power;
    }
    return power_sum.to_string();   
}
