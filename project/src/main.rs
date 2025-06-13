use std::thread;
extern crate websocket;
//use hex;
//hex::encode(bytes);


//#[path = "E:/RustNetwork/project/Main/server.rs"]
//mod server;
 fn main(){
    websocket::websocket::client::main();
    websocket::websocket::server::main();

    /*thread::spawn(f);
    thread::spawn(f);
    thread::spawn(s);

    println!(" the main thread is running");
    let numbers = vec![1, 2, 3];


    thread::scope(|s|{
        s.spawn(||{
            println!("length: {}", numbers.len());
        });
        s.spawn(||{
            for n in &numbers {
                println!("number: {}", n);
            }
        })
    })*/
    
    //server::main1();
    /*let water  = Some("water");
    let lemonade = Some("lemonade");
    let void  = None;

    give_adult(water);
    give_adult(lemonade);
    give_adult(void);

    let coffee = Some("coffee");
    let nothing = None;

    drink(coffee);
    drink(nothing);
    */
    /* 
    let mut input = String::new();
    let mut array = Vec::<String>::new();
    println!("enter some texte:");
    std::io::stdin().read_line(&mut input);
    for (a, b) in input.chars().enumerate() {
        array.push(a.to_string());
        array.push(b.to_string());
        println!("{}: {}", a, b);

    }
    println!("the array is: {:?}", array);

    println!("The has is : {:?} ", simple_hash(&input));
    println!("The has is : {:x} ", simple_hash(&input));
    */
 }

 fn give_adult(drink: Option<&str>) {
    match drink{
        Some("lemonade") => println!("you! too sugary."),
        Some(inner) => println!("{}? how nice.", inner),
        None => println!("no drink? on well."),
    }
 }

 fn drink(drink: Option<&str>) {
    let inside = drink.unwrap();
    if inside =="lemonade" {panic!("AAAaaaaaa!!!!");}
    println!("I love {}s is a nice drink.", inside);
 }

 fn f(){
    println!(" the thread is running");
    let id = thread::current().id();
    println!(" the thread id is {:?}", id);
 }
 fn s(){
    println!(" the thread is running");
    let id = thread::current().id();
    println!(" the thread id is {:?}", id);
    
 }
 
 fn simple_hash(input1: &str) -> u64 {
    let mut hash: u64 = 0;
    for (i, c) in input1.chars().enumerate() {
        hash += (c as u64) * (i as u64 + 1);
        hash ^= hash.rotate_left(13);
    }
    hash
    
}