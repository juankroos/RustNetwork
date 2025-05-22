
struct server{
    name: String,
    address: i32,
    status: String,

    /*
    fn connection(&self) {
        println!("{} is connected to {}", self.name, self.address);
    }
    fn disconnect(&self) {
        println!("{} is disconnected from {}", self.name, self.address);
    }

    fn send_message(&self, message: &str) {
        println!("{} sent: {}", self.name, message);
    }*/
}


// users connection handler using tokio

use tokio::net::TcpListener;
use tokio::io::{AsyncReadExt, AsyncWriteExt};

#[tokio::main]
async fn connect_handler( ){
    let conn_listerner = TcpListener::bind("127.0.0.1:0").await.unwrap();
    println!("Server is listening on {}", conn_listerner.local_addr().unwrap());
    loop{
        match conn_listerner.accept().await{
            Ok((mut stream, addr)) => {
                println!("New connection from {} bla bla bla....", addr);
                tokio::spawn(async move {
                    let mut buffer = [0;512];
                    match stream.read(&mut buffer).await{
                        //message send here
                        /*Ok(_) =>{
                            println!("Received: {}", String::from_utf8_lossy(&buffer));
                            stream.write_all(b"HTTP/1.1 200 OK\r\n\r\n").await.unwrap();
                        }
                        Err(e) => {
                            println!("Error reading from stream: {}", e);
                            return;
                        }*/
                    }
                }); 
            }
                Err(e) => {
                    println!("Error accepting connection: {}", e);
                    return;
                }
            }
        
    }
}
