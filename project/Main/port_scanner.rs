use port_scanner::scan_ports;

fn main() {
    let open_ports = scan_ports("192.168.1.1", 1, 65535);
    println!("Ports ouverts : {:?}", open_ports);
}