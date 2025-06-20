pub fn main_event(){
    let mut input = String::new();
    println!("entrez un mots : ");
    std::io::stdin().read_line(&mut input).expect("Failed to read line");
    println!("le mots est : {:?}", input);
}
pub fn random_ahh(){
    let mut input = u64::new();
    println!("guest the number between 1 and 10");
    let nbr = rand::thread_rng().gen_range(1..10);
    std::io::stdin().read_line(&mut input).expect("Failed to read line");
    
    
}