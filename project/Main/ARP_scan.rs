use std::net::{IpAddr, UdpSocket};

fn get_local_ip() -> std::io::Result<IpAddr> {
    let socket = UdpSocket::bind("0.0.0.0:0")?;
    socket.connect("8.8.8.8:80")?;
    Ok(socket.local_addr()?.ip())
}

fn main() {
    match get_local_ip() {
        Ok(ip) => println!("Adresse IP locale de la machine : {}", ip),
        Err(e) => eprintln!("Erreur : {}", e),
    }
}