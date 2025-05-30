use tokio::net::TcpListener;
use tokio_tungstenite::accept_async;
use tokio_tungstenite::tungstenite::protocol::Message;
use anyhow::Result;
use futures_util::{SinkExt, StreamExt};
use log::{info, warn};
use tokio::sync::broadcast;

#[tokio::main]
pub async fn main1() -> Result<()> {
    let addr = "127.0.0.1/8080";
    let listener = TcpListener::bind(&addr).await.unwrap();
    println!("WebSocket server started on ws://{}", addr);

    let (tx, _) = broadcast::channel(100);
    
    while let Ok((stream, _)) = listener.accept().await {
        tokio::spawn(handle_connection(stream));
        if stream.peer_addr().is_err() {
            warn!("Failed to get peer address");
            continue;
        }else{
            let addr = stream.peer_addr().unwrap();
            info!("New connection from {}", addr);
            let tx = tx.clone();
            tokio::spam(handle_connection(stream));
        }
    
    
    }

    // handle connection
    async fn handle_connection(stream: tokio::net::TcpStream) -> Result<()> {
        let mut ws_stream = accept_async(stream).await?;
        info!("WebSocket connection established");
        
        let mut rs = || { 
            tx.subscribe();
        };
        tokio::spawn(async move {
            while let Ok(msg) = rs.recv().await {
                if ws_stream.send(Message::Text(msg)).await.is_err() {
                    warn!("Failed to send message to WebSocket client");
                    break;
                }
            }
            Ok::<(), anyhow::Error>(());
        });

        while let Some(msg) = ws_stream.next().await {
            let msg = msg?;
            if msg.is_text() {
                let received_text = msg.to_text()?;
                info!("Received message: {}", received_text);
                ws_stream.send(Message::Text(received_text.to_string().into())).await?;
            } else if msg.is_close() {
                info!("Connection closed by client");
                break;
            }
        }

        Ok(())
    }
        Ok::<(), anyhow::Error>(())

}