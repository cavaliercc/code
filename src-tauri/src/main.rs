// Prevents additional console window on Windows in release
#![cfg_attr(not(debug_assertions), windows_subsystem = "windows")]

use tauri::{Manager, Window};
use std::process::Command;
use std::thread;
use std::time::Duration;

// Learn more about Tauri commands at https://tauri.app/v1/guides/features/command
#[tauri::command]
fn greet(name: &str) -> String {
    format!("Hello, {}! You've been greeted from Rust!", name)
}

#[tauri::command]
async fn start_python_backend() -> Result<String, String> {
    // Start Python FastAPI backend
    thread::spawn(|| {
        let _ = Command::new("python")
            .arg("-m")
            .arg("uvicorn")
            .arg("python-api.main:app")
            .arg("--host")
            .arg("127.0.0.1")
            .arg("--port")
            .arg("8000")
            .arg("--reload")
            .current_dir("..")
            .spawn();
    });
    
    // Wait for backend to start
    thread::sleep(Duration::from_secs(2));
    
    Ok("Python backend started".to_string())
}

#[tauri::command]
async fn check_backend_health() -> Result<bool, String> {
    // Check if Python backend is running
    let client = reqwest::Client::new();
    match client.get("http://127.0.0.1:8000/health").send().await {
        Ok(response) => Ok(response.status().is_success()),
        Err(_) => Ok(false),
    }
}

fn main() {
    tauri::Builder::default()
        .invoke_handler(tauri::generate_handler![
            greet,
            start_python_backend,
            check_backend_health
        ])
        .run(tauri::generate_context!())
        .expect("error while running tauri application");
}
