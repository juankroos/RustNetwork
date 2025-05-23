Skip to content

DEV Community


0
Jump to Comments

3
Save

Boost

George O. E. Campbell
George O. E. Campbell
Posted on 30 juil. 2024


6
Websocket starter in Rust with client and server example
#
rust
#
websocket
#
server
#
client
Server code for websockets
(server): https://github.com/campbellgoe/rust_websocket_server

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
Cargo.toml (server):

[dependencies]
tokio = { version = "1.12", features = ["full"] }
tokio-stream = "0.1"
tokio-tungstenite = "0.23.1"
anyhow = "1.0"
futures-util = "0.3"
Client websocket code
(client): https://github.com/campbellgoe/rust_websocket_client

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
client Cargo.toml

[dependencies]
tokio = { version = "1.12", features = ["full"] }
tokio-stream = "0.1"
tokio-tungstenite = "0.23.1"
url = "2"
anyhow = "1.0"
futures-util = "0.3"
You could use this as a starting point for your Rust websocket project.

Top comments (0)

Subscribe
pic
Add to the discussion
Code of Conduct • Report abuse
profile
Datadog
Promoted

Image of Datadog

Keep your GPUs in check
This cheatsheet shows how to use Datadog’s NVIDIA DCGM and Triton integrations to track GPU health, resource usage, and model performance—helping you optimize AI workloads and avoid hardware bottlenecks.

Get the Cheatsheet

Read next
aaravjoshi profile image
Rust Concurrent Data Structures: Building Thread-Safe Collections Without Sacrificing Performance
Aarav Joshi - Apr 4

aaravjoshi profile image
Rust Performance Boost: Building Efficient Caching Systems From Scratch
Aarav Joshi - Mar 29

aaravjoshi profile image
Zero-Copy Parsing in Rust: A Guide to High-Performance Data Processing
Aarav Joshi - Feb 27

d2d_weizhi profile image
The Power of Thinking..."I CAN"
Chen Weizhi - May 16


George O. E. Campbell
Follow
Web developer focused on Next.js, Three.js, JavaScript/TypeScript .
Location
Hereford, United Kingdom
Education
Diploma of Higher Education, Human Geography.
Work
Frontend engineer
Joined
30 juil. 2018
Trending on DEV Community 
Shariful Ehasan profile image
Which JavaScript Loop Do You Use the Most and Why?
#discuss #javascript #programming #webdev
Snappy Tuts profile image
🧬 Programming Languages Are Just Thought Interfaces
#learning #rust #python #programming
Anthony James profile image
Ashkan Rajaee’s Secret Formula for Remote Meetings That Outsmart the Competition
#productivity #remote #business #leadership
profile
AWS
Promoted

AWS Security LIVE! Stream

Stream AWS Security LIVE!
See how AWS is redefining security by design with simple, seamless solutions on Security LIVE!

Learn More

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
💎 DEV Diamond Sponsors

Thank you to our Diamond Sponsors for supporting the DEV Community

Neon - Official Database Partner
Neon is the official database partner of DEV

Algolia - Official Search Partner
Algolia is the official search partner of DEV

DEV Community — A space to discuss and keep up software development and manage your software career

Home
Reading List
Tags
About
Contact
Code of Conduct
Privacy Policy
Terms of use
Built on Forem — the open source software that powers DEV and other inclusive communities.

Made with love and Ruby on Rails. DEV Community © 2016 - 2025.