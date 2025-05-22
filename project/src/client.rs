use std::io::{prelude::*, BufReader};
use std::net::{ TcpStream};


struct client{
    name: String,
    address: String,
    message: String,
    server_ip: Int ,
    status: String,

    fn connection(&self) -> std::io::Result<()> {
        let mut stream = TcpStream::connect(self.address)?;
        stream.write(&[1]?);
        stream.read(&mut [0; 128])?;
        Ok(())
        println!("{} is connected to {}", self.name, self.address);
    }
    fn disconnect(&self) {
        println!("{} is disconnected from {}", self.name, self.address);
    }

    fn send_message(&self, message: &str) {
        println!("{} sent: {}", self.name, message);
    }
}