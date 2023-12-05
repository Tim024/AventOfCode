use std::process::exit;

use utils::read_data_lines;

fn parse_lines_to_vec(start: usize, end: usize, lines: &[String]) -> Vec<Vec<i64>> {
    (start..end + 1)
        .into_iter()
        .map(|i| {
            lines[i]
                .split_whitespace()
                .map(|x| x.parse::<i64>().unwrap())
                .collect::<Vec<i64>>()
        })
        .collect()
}

#[derive(Copy, Clone, Debug)]
struct Interval {
    start: i64,
    end: i64,
    offset: i64,
}

struct Map {
    offsets: Vec<Interval>,
}

impl Map {
    fn create(data: Vec<Vec<i64>>) -> Map {
        let mut m = Map {
            offsets: Vec::new(),
        };
        for d in data.iter() {
            m.add(d[1], d[1] + d[2], d[0]- d[1]);
        }
        m
    }

    fn add(&mut self, start: i64, end: i64, offset: i64) {
        self.offsets.push(Interval { start, end, offset });
    }

    fn split_interval(&self, interval: &Interval) -> Vec<Interval> {
        let mut result = Vec::new();
        for i in self.offsets.iter() {
            if i.start > interval.start && i.start < interval.end {
                println!("Interval is contained in {i:?}");
                // interval is split
                result.push(Interval {
                    start: interval.start,
                    end: i.start,
                    offset: 0,
                });
                result.push(Interval {
                    start: i.start,
                    end: interval.end,
                    offset: i.offset,
                });
            } else if i.end > interval.start && i.end < interval.end {
                println!("Interval is contained in {i:?}.");
                // interval is split
                result.push(Interval {
                    start: interval.start,
                    end: i.end,
                    offset: 0,
                });
                result.push(Interval {
                    start: i.end,
                    end: interval.end,
                    offset: i.offset,
                });
           }
        }
        if result.len() == 0 {
            result.push(*interval);
        }
        // Remove empty intervals
        result = result.into_iter().filter(|x| x.start != x.end).collect();
        // Remove identical intervals
        result = result.into_iter().fold(Vec::new(), |mut acc, x| {
            if acc.iter().find(|y| y.start == x.start && y.end == x.end).is_none() {
                acc.push(x);
            }
            acc
        });
        result
    }

    fn apply(&self, interval: Interval) -> Vec<Interval> {
        let mut result = Vec::new();

        let splitted_interval = self.split_interval(&interval);
        // dbg!(&splitted_interval);

        for si in splitted_interval.iter() {
            let mut interval_contained = false;
            for i in self.offsets.iter() {
                // Each interval is start, end, offset value

                // println!("Checking if {si:?} is contained in {i:?}", si=si, i=i);
                if si.start >= i.start && si.end <= i.end {
                    // interval is fully contained
                    // println!("Interval is fully contained!");
                    result.push(Interval {
                        start: si.start + i.offset,
                        end: si.end + i.offset,
                        offset: 0,
                    });
                    interval_contained = true;
                    break;
                }
            }
            if !interval_contained {
                // println!("Interval is not contained!");
                result.push(*si);
            }
        }

        // dbg!(&result);
        result
    }
}

fn parse_puzzle() -> (Vec<i64>, Vec<Map>) {
    let lines = read_data_lines("./day5/src/data.input");

    let seeds: Vec<i64> = lines[0]
        .split(":")
        .nth(1)
        .unwrap()
        .split_whitespace()
        .map(|x| x.parse::<i64>().unwrap())
        .collect();

    //Example ranges
    // let see_to_soi = parse_lines_to_vec(3, 4, &lines);
    // let soi_to_fer = parse_lines_to_vec(7, 9, &lines);
    // let fer_to_wat = parse_lines_to_vec(12, 15, &lines);
    // let wat_to_lig = parse_lines_to_vec(18, 19, &lines);
    // let lig_to_tem = parse_lines_to_vec(22, 24, &lines);
    // let tem_to_hum = parse_lines_to_vec(27, 28, &lines);
    // let hum_to_loc = parse_lines_to_vec(31, 32, &lines);

    let see_to_soi = parse_lines_to_vec(3, 39, &lines);
    let soi_to_fer = parse_lines_to_vec(42, 71, &lines);
    let fer_to_wat = parse_lines_to_vec(74, 112, &lines);
    let wat_to_lig = parse_lines_to_vec(115, 139, &lines);
    let lig_to_tem = parse_lines_to_vec(142, 158, &lines);
    let tem_to_hum = parse_lines_to_vec(161, 191, &lines);
    let hum_to_loc = parse_lines_to_vec(194, 236, &lines);

    let chain_map = vec![
        Map::create(see_to_soi), 
        Map::create(soi_to_fer), 
        Map::create(fer_to_wat),
        Map::create(wat_to_lig),
        Map::create(lig_to_tem),
        Map::create(tem_to_hum),
        Map::create(hum_to_loc),
    ];

    (seeds, chain_map)
}

pub fn part1() -> String {
    let (seeds, chain_map) = parse_puzzle();

    let mut min_value: u64 = u64::MAX;
    for s in seeds {
        let mut interval = Interval {
            start: s,
            end: s + 1,
            offset: 0,
        };

        // dbg!(&interval);
        for map in chain_map.iter() {
            // println!("Applying map...");
            interval = map.apply(interval)[0];
        }
        // dbg!(&interval);
        min_value = min_value.min(interval.start as u64);
    }
    return min_value.to_string();
}

pub fn part2() -> String {
    let (seeds, chain_map) = parse_puzzle();

    let seeds = (0..seeds.len()/2 as usize).into_iter()
        .map(|i| (seeds[i*2], seeds[i*2+1]))
        .collect::<Vec<(i64, i64)>>();



    let mut min_value: u64 = u64::MAX;
    for (s, sr) in seeds {
        let interval = Interval {
            start: s,
            end: s + sr,
            offset: 0,
        };

        let mut intervals = Vec::new();
        intervals.push(interval);

        for map in chain_map.iter() {
            let mut next_intervals = Vec::new();
            for itv in intervals.iter() {
                // println!("Applying map...");
                let res = map.apply(*itv);
                next_intervals.extend(res);
            }
            // dbg!(&interval);
            intervals = next_intervals;

            exit(1);
        }
        min_value = min_value.min(intervals.iter().map(|x| x.start).min().unwrap() as u64);
    }
    return min_value.to_string();
}
