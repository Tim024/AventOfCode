use utils::read_data_lines;

fn parse_card(card: String) -> (Vec<u32>, Vec<u32>){
    let g = card.split(':').nth(1).unwrap();
    let m = g.split("|").collect::<Vec<&str>>();
    let parse_numbers = |x: &str| x.split_whitespace().map(|x| x.parse::<u32>().unwrap()).collect::<Vec<u32>>();
    let winning_numbers = parse_numbers(m.first().unwrap());
    let my_numbers = parse_numbers(m.last().unwrap());

    return (winning_numbers, my_numbers)
}

pub fn part1() -> String{
    let cards = read_data_lines("./day4/src/data.input");

    let mut total_score = 0;

    for card in cards{

        let (winning_numbers, my_numbers) = parse_card(card);

        let mut score = 0.5;
        for n in my_numbers{
            if winning_numbers.contains(&n){
                score = score*2.0;
            }
        }
        total_score += score as u32;
    }
    return total_score.to_string()
}

pub fn part2() -> String{
    let cards = read_data_lines("./day4/src/data.input");

    let mut nb_of_cards = 0;
    let mut extra_cards = vec![0; 24];

    for card in cards{
        let copies = 1 + extra_cards.remove(0);
        nb_of_cards += copies;
        extra_cards.push(0);

        let (winning_numbers, my_numbers) = parse_card(card.clone());
        let nb_win = my_numbers.iter().filter(|x| winning_numbers.contains(x)).count();

        for n in 0..nb_win{
            extra_cards[n] += copies;
        }
    }
    return nb_of_cards.to_string()
}
