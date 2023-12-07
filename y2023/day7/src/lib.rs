use utils::read_data_lines;

fn get_score(hand: [u64; 5], part_two: bool, original_hand: [char; 5]) -> u64 {
    // Type * 100 * 100 * 100 * 100 * 100 + first card * 100 * 100 * 100 * 100 + second card * 100 * 100 * 100 + third card * 100 * 100 + fourth card * 100 + fifth card
    let mut sorted_hand = hand.clone();
    sorted_hand.sort();

    // dbg!(&sorted_hand);

    // Five of a kind
    let mut type_s: u64 = 0;
    if sorted_hand.iter().all(|&x| x == sorted_hand[0]) {
        type_s = 6;
    }
    // Four of a kind
    else if sorted_hand.iter().filter(|&x| x == &sorted_hand[0]).count() == 4
        || sorted_hand.iter().filter(|&x| x == &sorted_hand[1]).count() == 4
    {
        type_s = 5;
    }
    // Full house
    else if (sorted_hand.iter().filter(|&x| x == &sorted_hand[0]).count() == 3
        && sorted_hand.iter().filter(|&x| x == &sorted_hand[3]).count() == 2
        && &sorted_hand[0] != &sorted_hand[3])
        || (sorted_hand.iter().filter(|&x| x == &sorted_hand[0]).count() == 2
            && hand.iter().filter(|&x| x == &sorted_hand[3]).count() == 3
            && &sorted_hand[0] != &sorted_hand[3])
    {
        type_s = 4;
    }
    // Three of a kind
    else if sorted_hand.iter().filter(|&x| x == &sorted_hand[0]).count() == 3
        || sorted_hand.iter().filter(|&x| x == &sorted_hand[2]).count() == 3
    {
        type_s = 3;
    }
    // Two pairs
    else if (sorted_hand.iter().filter(|&x| x == &sorted_hand[0]).count() == 2
        && sorted_hand.iter().filter(|&x| x == &sorted_hand[2]).count() == 2
        && &sorted_hand[0] != &sorted_hand[2])
        || (sorted_hand.iter().filter(|&x| x == &sorted_hand[0]).count() == 2
            && sorted_hand.iter().filter(|&x| x == &sorted_hand[3]).count() == 2
            && &sorted_hand[0] != &sorted_hand[3])
        || (sorted_hand.iter().filter(|&x| x == &sorted_hand[1]).count() == 2
            && sorted_hand.iter().filter(|&x| x == &sorted_hand[3]).count() == 2
            && &sorted_hand[1] != &sorted_hand[3])
    {
        type_s = 2;
    }
    // One pair
    else if sorted_hand.iter().filter(|&x| x == &sorted_hand[0]).count() == 2
        || sorted_hand.iter().filter(|&x| x == &sorted_hand[1]).count() == 2
        || sorted_hand.iter().filter(|&x| x == &sorted_hand[2]).count() == 2
        || sorted_hand.iter().filter(|&x| x == &sorted_hand[3]).count() == 2
        || sorted_hand.iter().filter(|&x| x == &sorted_hand[4]).count() == 2
    {
        type_s = 1;
    }
    // High card

    let mut hand = hand.clone();
    if part_two {
        // Replace 'J' with 1
        for i in 0..5 {
            if original_hand[i] == 'J' {
                hand[i] = 1;
            }
        }
    }
    let score = (type_s + 1) * 100 * 100 * 100 * 100 * 100
        + hand[0] * 100 * 100 * 100 * 100
        + hand[1] * 100 * 100 * 100
        + hand[2] * 100 * 100
        + hand[3] * 100
        + hand[4];
    return score;
}

pub fn part1() -> String {
    let lines = read_data_lines("./day7/src/data.input");

    let mut scores = Vec::new();
    let mut bids = Vec::new();
    for line in lines {
        let mut hand: [u64; 5] = [0; 5];
        let hand_str = line.split_whitespace().nth(0).unwrap();
        for (i, card) in hand_str.chars().enumerate() {
            if card == 'T' {
                hand[i] = 10;
            } else if card == 'J' {
                hand[i] = 11;
            } else if card == 'Q' {
                hand[i] = 12;
            } else if card == 'K' {
                hand[i] = 13;
            } else if card == 'A' {
                hand[i] = 14;
            } else {
                hand[i] = card.to_digit(10).unwrap() as u64;
            }
        }
        let bid = line
            .split_whitespace()
            .nth(1)
            .unwrap()
            .parse::<u64>()
            .unwrap();
        let score = get_score(
            hand,
            false,
            hand_str.chars().collect::<Vec<char>>().try_into().unwrap(),
        );

        scores.push(score);
        bids.push(bid);
    }
    // Get rank of each score
    let mut ranks = scores
        .iter()
        .enumerate()
        .map(|(i, &x)| (i, x))
        .collect::<Vec<(usize, u64)>>();
    ranks.sort_by(|a, b| a.1.cmp(&b.1));

    let mut total = 0;
    for (i, rank) in ranks.iter().enumerate() {
        total += bids[rank.0] * (i + 1) as u64;
    }

    return total.to_string();
}

pub fn part2() -> String {
    let lines = read_data_lines("./day7/src/data.input");

    let mut scores = Vec::new();
    let mut bids = Vec::new();
    for line in lines {
        let mut hands: Vec<[u64; 5]> = Vec::new();
        let hand_str = line.split_whitespace().nth(0).unwrap();
        for J_value in 2..15 {
            let mut hand: [u64; 5] = [0; 5];
            for (i, card) in hand_str.chars().enumerate() {
                if card == 'T' {
                    hand[i] = 10;
                } else if card == 'J' {
                    hand[i] = J_value;
                } else if card == 'Q' {
                    hand[i] = 12;
                } else if card == 'K' {
                    hand[i] = 13;
                } else if card == 'A' {
                    hand[i] = 14;
                } else {
                    hand[i] = card.to_digit(10).unwrap() as u64;
                }
            }
            hands.push(hand);
        }
        // Remove duplicates
        hands.sort();
        hands.dedup();

        // Find largest score
        let mut max_score = 0;
        for hand in hands {
            let score = get_score(
                hand,
                true,
                hand_str.chars().collect::<Vec<char>>().try_into().unwrap(),
            );
            if score > max_score {
                max_score = score;
            }
        }
        let bid = line
            .split_whitespace()
            .nth(1)
            .unwrap()
            .parse::<u64>()
            .unwrap();

        scores.push(max_score);
        bids.push(bid);
    }
    // Get rank of each score
    let mut ranks = scores
        .iter()
        .enumerate()
        .map(|(i, &x)| (i, x))
        .collect::<Vec<(usize, u64)>>();
    ranks.sort_by(|a, b| a.1.cmp(&b.1));

    let mut total = 0;
    for (i, rank) in ranks.iter().enumerate() {
        total += bids[rank.0] * (i + 1) as u64;
    }

    return total.to_string();
}
