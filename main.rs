/* 
mod db;
mod rest;
mod view;

use crate::db::init_db;
use anyhow::Result;
use axum::{Extension, Router};
use sqlx::SqlitePool;
use std::net::SocketAddr;

/// Build the overall web service router.
/// Constructing the router in a function makes it easy to re-use in unit tests.
fn router(connection_pool: SqlitePool) -> Router {
    Router::new()
        // Nest service allows you to attach another router to a URL base.
        // "/" inside the service will be "/books" to the outside world.
        .nest_service("/books", rest::books_service())
        // Add the web view
        .nest_service("/", view::view_service())
        // Add the connection pool as a "layer", available for dependency injection.
        .layer(Extension(connection_pool))
}

#[tokio::main]
async fn main() -> Result<()> {
    // Load environment variables from .env if available
    dotenv::dotenv().ok();

    // Initialize the database and obtain a connection pool
    let connection_pool = init_db().await?;

    // Initialize the Axum routing service
    let app = router(connection_pool);

    // Define the address to listen on (everything)
    let addr = SocketAddr::from(([0, 0, 0, 0], 3001));

    // Start the server
    axum::Server::bind(&addr)
        .serve(app.into_make_service())
        .await?;

    Ok(())
}
*/

use std::io;

fn main() {
    /*
    let x: i32 = -42;
    let y: u64 = 100;
    println!("Signed Integer: {}", x);
    println!(" unsigned integer: {}", y);

    let pi: f64 = 3.14;
    println!("value of pi: {}", pi);

    let is_snowing: bool = true;
    println!("It is snowing,: {}",is_snowing);

    let letter: char = 'a';
    println!("first letter of alphabet: {}", letter);
    */
    let mut guess = String::new();
    //let apples = 5;
    println!("enter something to guess a number");
    let mut secret_number = rand::thread_rng().gen_range(1..=100);
    let mut guess1 = String::new();
    
    io::stdin()
        .read_line(&mut guess1)
        .expect("error reading");
    println!("You guess:{guess1}");
    println!("the secret number is {secret_number}");

    /*0
    io::stdin()

        .read_line(&mut guess)
        .expect("failed to read the line");
    println!("you tap: {}",guess);
    */
    let a = 5;
    let b = 9;
    //println!("the sum of: {} and {} is  {}", a,b,a+b);


}
/* 
fn main(){
    let yo : i32 = 15 ;
    println!("Signed Integer: {}", yo);
} */

//use core::slice;
/*
fn cal(){
    let num : i32 = 2;
    if num < 100 {
        num =  * 2;

    }else{
        println!("end conter");
        println!("  {}", num);
    }
}
*/
/* 
fn main(){

    
    let numbers:[i32; 5] = [1,2,3,4,5];
    println!("Number Array: {:?}", numbers);
    //let mix = [1,2,"apple",true];
    //println!("mix : {:?}", mix)
    let fruits: [&str; 3 ] = ["Apple","Banana", "Orange"];
    println!("Fruits array: {:?}", fruits);
    println!("Fruits array first: {}", fruits[0]);
    println!("Fruits array second: {}", fruits[1]);
    println!("Fruits array thirt: {}", fruits[2]);

    //tuples
    let human: (String,i32,bool) = ("Alice".to_string(),30,false);
    println!("human tuple: {:?}",human);
    let my_mix_tuple = ("Kratos",23,true,[1,2,3,4,5]);
    println!("My mix tuple: {:?}",my_mix_tuple);

    //slices: 
    let number_sclice: &[i32] = &[1,2,3,4,5];
    println!("Number sclice: {:?}", number_sclice);

    let animal_sclice: &[&str] = &["Lion","Elephant","Crocodile"];
    println!("Animal sclice: {:?}", animal_sclice);

    let book_sclice: &[&String] = &[&"IT".to_string(),&"Harry potter".to_string(),&"Zen".to_string()];
    println!("Book sclice: {:?}", book_sclice);
    
    // Strings vs Strings
    let mut stone_cold : String = String:: from("Hell, ");
    stone_cold.push_str("Yeah!");
    println!("Stone cold Says {}", stone_cold);
    let String: String = String::from("Hello world");
    let slice: &str = &String;
    println!("Slice value: {}", slice);

    
 
}*/
/* 
fn main(){
    let aa: i32 = 35645;
    println!("la valeur de aa est : {}",aa);
    let human:  (String,i32,bool) = ("juan".to_string(),65,false);
    println!("tuple list :{:?}", human);
    let mix_tuple = ("alex",564,[1,2,3,4,5],"dimi".to_string(),true);
    println!("tuple mix : {:?}", mix_tuple);
    let name: &[&String] = &[&"juan".to_string(),&"dimi".to_string(),&"lola".to_string()];
    println!("array list :{:?}", name);
}*/

