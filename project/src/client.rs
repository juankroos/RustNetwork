use std::io::{prelude::*, BufReader};
use std::net::{ TcpStream};
use std::net::{IpAddr, Ipv4Addr, Ipv6Addr};



struct client{
    name: String,
    address: String,
    message: String,
    server_ip: Int ,
    status: String,
    stream: TcpStream,
}

impl Client{

    fn connection(&self) -> std::io::Result<()> {
        match Tcpstream::connect("address/port"){
            Ok(stream) => println!("{} is connected to {}", self.name, self.address),
            Err(e) => {
                println!("Failed to connect: {}", e);
                return Err(e);
            }
        }
    }

    fn disconnect(&self) {
        drop(self.stream);
        //println!("{} is disconnected from {}", self.name, self.address);
    }

    fn send_message(&self, server_ip: IpAddr) {
        //we wait for the user to send a message
        let mut message = String::new();
        println!(" Write ---> ");
        loop {
            message.clear();
            io::stdin()
                .read_line(&mut message)
                .execpt("Failed to read line");
            if disconnect(){
                break;
            }
        }

        println!("{} sent: {}", self.name, message);
    }
    }
    
