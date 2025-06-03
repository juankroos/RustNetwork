use tokio::net::TcpListener;
use tokio_tungstenite::accept_async;
use tokio_tungstenite::tungstenite::protocol::Message;
use anyhow::Result;
use futures_util::{SinkExt, StreamExt};

#[tokio::main]
async fn main() -> Result<()> {
    let addr = "";
    let url = format!("ws://{}", addr);
    let (mut ws_stream, _) = connect_async(url.as_str()).await.expect("Failed to connect");
    println!("WebSocket client connected to {}", addr);

    // Sending a message to the server
    async fn send_message(){
        println!("Enter a message to send to the server (type 'exit' to quit):");
        io::stdout().flush().unwrap();
        let mut message = String::new();
        io::stdin().read_line(&mut message).expect("Failed to read line");
        let message = message.trim();
        loop{
            println!("Enter a message to send to the server (type 'exit' to quit):");
            io::stdout().flush().unwrap();
            let mut message = String::new();
            io::stdin().read_line(&mut message).expect("Failed to read line");
            let message = message.trim();
            message.to_string();
            ws_stream.send(Message::Text(message.into())).await?;
            if ws_stream.next().await.is_none() {
                println!("Connection closed by server");
                break;
            }
        }
    }

    //_stream.send(Message::Text(message.into())).await?;
fn revieve_message(){
    while let Some(msg) = ws_stream.next().await {
        match msg? {
            //verifying the message type
            Message::Text(text) => {
                println!("Received message from server: {}", text);
            },
            Message::Close(_) => {
                println!("Connection closed by server");
                break;
            },
            _ => {}
        }
    }
    }
}

// Function to send a file
/*
use tokio::fs::File;
use tokio::io::AsyncReadExt;
use tokio_tungstenite::tungstenite::protocol::Message;

async fn send_file(ws_stream: &mut tokio_tungstenite::WebSocketStream<tokio::net::TcpStream>, file_path: &str) -> anyhow::Result<()> {
    let mut file = File::open(file_path).await?;
    let mut buffer = Vec::new();
    file.read_to_end(&mut buffer).await?;
    
    ws_stream.send(Message::Binary(buffer)).await?;
    println!("Fichier {} envoyé", file_path);

    Ok(())
}
*/

// Function to receive a file
/*
use tokio::fs::File;
use tokio::io::AsyncWriteExt;
use tokio_tungstenite::WebSocketStream;
use tokio_tungstenite::tungstenite::protocol::Message;
use anyhow::Result;
use futures_util::stream::StreamExt;

async fn receive_file(ws_stream: &mut WebSocketStream<tokio::net::TcpStream>, save_path: &str) -> Result<()> {
    while let Some(msg) = ws_stream.next().await {
        match msg {
            Ok(Message::Binary(data)) => {
                let mut file = File::create(save_path).await?;
                file.write_all(&data).await?;
                println!("Fichier sauvegardé sous {}", save_path);
                break;
            }
            Err(e) => {
                println!("Erreur de réception : {}", e);
                break;
            }
            _ => {}
        }
    }
    Ok(())
}
*/
