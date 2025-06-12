fn simple_hash(input: &str) -> u64 {
    let mut hash: u64 = 0;
    for (i, c) in input.chars().enumerate() {
        hash += (c as u64) * (i as u64 + 1);
        //hash ^= hash.rotate_left(7);
    }
    hash
}
// ******Total incorporation******
// To take  the  nessesary information from the input to hash
fn input_hash( input: &str) -> u64 {
    let mut enu = input.chars.enumerate();
    let mut length = input.len();
    let mut size = mem::size_of(&input);
    let mut info: Vec<String>::new();
    info.push(length.to_string());
    info.push(size.to_string());
    info.push(enu.to_string());
    info;
}

// A more complex hash fucntion that uses a prime number and a vector to store characters
fn complexe_hash(input: &str) ->u64 {
    let mut hash : u64 = 0;
    let mut prime: u64 = 31;
    let mut array: Vec::<String>::new();
    let mut char: Vec::<String>::new();
    let mut index: Vec::<usize>::new();
    for (a,b) in input.chars().enumerate() {
        array.push(a.to_string());
        index.push(a);
        char.push(b.to_string());
        array.push(b.to_string());
    }
    
}

fn main() {
    let message = "Hello, Rust!";
    println!("Hash personnalisé de merde : {}", simple_hash(message));
}