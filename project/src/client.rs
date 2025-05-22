struct client{
    name: String,
    address: String,
    message: String,

    fn connection(&self) {
        println!("{} is connected to {}", self.name, self.address);
    }
    fn disconnect(&self) {
        println!("{} is disconnected from {}", self.name, self.address);
    }

    fn send_message(&self, message: &str) {
        println!("{} sent: {}", self.name, message);
    }
}