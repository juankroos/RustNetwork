use std::io::{prelude::*, BufReader};
use std::net::{ TcpStream};


struct client{
    name: String,
    address: String,
    message: String,
    server_ip: Int ,
    status: String,
}

impl Client{

    fn connection(&self) -> std::io::Result<()> {
        match Tcpstream::connect(self.address){
            Ok(stream) => println!("{} is connected to {}", self.name, self.address),
            Err(e) => {
                println!("Failed to connect: {}", e);
                return Err(e);
            }
        }
    }

    fn disconnect(&self) {
        println!("{} is disconnected from {}", self.name, self.address);
    }

    fn send_message(&self, message: &str) {
        println!("{} sent: {}", self.name, message);
    }
    }
    fn send_message(&self, message: &str) {
        let stream = TcpStream::connect(self.address).unwrap();
        stream.write_all(message.as_bytes()).unwrap();
        println!("{} sent: {}", self.name, message);
    }
