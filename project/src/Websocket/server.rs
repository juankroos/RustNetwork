use wrap::filter;
use std::sync::{Arc, Mutex};
use tokio::sync::broadcast;

mod ws_handler;

#[tokio::main]
async fn main() {
    let tx = Arc::new(Mutex::new(broadcast::channel(100).0));
    let tx_ws = tx.clone();
    let ws_route = warp::path("ws")
        .and(warp::ws())
        .map(move |ws: warp::ws::Ws| {
            let tx = tx_ws.clone();
            // Handle the WebSocket connection
            ws.on_upgrade(move |websocket| ws_handler::handle_connection(websocket, tx))
        });
        warp::serve(ws_route)
        .run(([127, 0, 0, 1], 8080))
        .await;
    println!("Server is running on ws://");
}