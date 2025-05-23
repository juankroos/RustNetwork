

use tokio::net::TcpListener;
use tokio_tungstenite::accept_async;
use tokio_tungstenite::tungstenite::protocol::Message;
use anyhow::Result;
use futures_util::{SinkExt, StreamExt};

#[tokio::main]
async fn main() -> Result<()> {
    let addr = "127.0.0.1:8080".to_string();
    let listener = TcpListener::bind(&addr).await?;
    println!("WebSocket server started on ws://{}", addr);

    while let Ok((stream, _)) = listener.accept().await {
        tokio::spawn(handle_connection(stream));
    }

    Ok(())
}

async fn handle_connection(stream: tokio::net::TcpStream) -> Result<()> {
    let mut ws_stream = accept_async(stream).await?;
    println!("WebSocket connection established");

    while let Some(msg) = ws_stream.next().await {
        let msg = msg?;
        if msg.is_text() {
            let received_text = msg.to_text()?;
            println!("Received message: {}", received_text);
            ws_stream.send(Message::Text(received_text.to_string())).await?;
        }
    }

    Ok(())
}

use tokio_tungstenite::connect_async;
use tokio_tungstenite::tungstenite::protocol::Message;
use anyhow::Result;
use futures_util::{SinkExt, StreamExt};
use url::Url;

#[tokio::main]
async fn main() -> Result<()> {
    let url = Url::parse("ws://127.0.0.1:8080")?;
    let (mut ws_stream, _) = connect_async(url.as_str()).await.expect("Failed to connect");
    println!("WebSocket client connected");

    // Sending a message to the server
    let message = "Hello, Server!";
    ws_stream.send(Message::Text(message.into())).await?;

    // Receiving messages from the server
    while let Some(msg) = ws_stream.next().await {
        match msg? {
            Message::Text(text) => {
                println!("Received message from server: {}", text);
            }
            _ => {}
        }
    }

    Ok(())
}

use tokio_tungstenite::connect_async;
use tokio_tungstenite::tungstenite::protocol::Message;
use anyhow::Result;
use futures_util::{SinkExt, StreamExt};
use url::Url;

#[tokio::main]
async fn main() -> Result<()> {
    let url = Url::parse("ws://127.0.0.1:8080")?;
    let (mut ws_stream, _) = connect_async(url.as_str()).await.expect("Failed to connect");
    println!("WebSocket client connected");

    // Sending a message to the server
    let message = "Hello, Server!";
    ws_stream.send(Message::Text(message.into())).await?;

    // Receiving messages from the server
    while let Some(msg) = ws_stream.next().await {
        match msg? {
            Message::Text(text) => {
                println!("Received message from server: {}", text);
            }
            _ => {}
        }
    }

    Ok(())
}
use tokio_tungstenite::connect_async;
use tokio_tungstenite::tungstenite::protocol::Message;
use anyhow::Result;
use futures_util::{SinkExt, StreamExt};
use url::Url;

#[tokio::main]
async fn main() -> Result<()> {
    let url = Url::parse("ws://127.0.0.1:8080")?;
    let (mut ws_stream, _) = connect_async(url.as_str()).await.expect("Failed to connect");
    println!("WebSocket client connected");

    // Sending a message to the server
    let message = "Hello, Server!";
    ws_stream.send(Message::Text(message.into())).await?;

    // Receiving messages from the server
    while let Some(msg) = ws_stream.next().await {
        match msg? {
            Message::Text(text) => {
                println!("Received message from server: {}", text);
            }
            _ => {}
        }
    }

    Ok(())
}
