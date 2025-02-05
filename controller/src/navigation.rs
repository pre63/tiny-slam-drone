use std::collections::{BinaryHeap, HashMap};

#[derive(Copy, Clone, Eq, PartialEq)]
struct Node {
    x: i32,
    y: i32,
    cost: i32,
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> std::cmp::Ordering {
        other.cost.cmp(&self.cost)
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<std::cmp::Ordering> {
        Some(self.cmp(other))
    }
}

pub fn init() {
    println!("Navigation: Path planning system initialized.");
}

pub fn plan_path(goal: &str) {
    let start = (0, 0);
    let goal_coord = (4, 4);
    let mut open_set = BinaryHeap::new();
    open_set.push(Node { x: start.0, y: start.1, cost: 0 });
    let mut came_from = HashMap::new();
    let mut cost_so_far = HashMap::new();
    cost_so_far.insert(start, 0);

    let directions = [(1,0), (-1,0), (0,1), (0,-1)];
    while let Some(current) = open_set.pop() {
        if (current.x, current.y) == goal_coord { break; }
        for &(dx, dy) in directions.iter() {
            let neighbor = (current.x + dx, current.y + dy);
            if neighbor.0 < 0 || neighbor.0 > 4 || neighbor.1 < 0 || neighbor.1 > 4 { continue; }
            let new_cost = cost_so_far[&(current.x, current.y)] + 1;
            if !cost_so_far.contains_key(&neighbor) || new_cost < cost_so_far[&neighbor] {
                cost_so_far.insert(neighbor, new_cost);
                let priority = new_cost + heuristic(neighbor, goal_coord);
                open_set.push(Node { x: neighbor.0, y: neighbor.1, cost: priority });
                came_from.insert(neighbor, (current.x, current.y));
            }
        }
    }
    let mut path = vec![goal_coord];
    let mut current = goal_coord;
    while current != start {
        current = came_from[&current];
        path.push(current);
    }
    path.reverse();
    println!("Navigation: Calculated path: {:?}", path);
}

fn heuristic(a: (i32, i32), b: (i32, i32)) -> i32 {
    (a.0 - b.0).abs() + (a.1 - b.1).abs()
}
