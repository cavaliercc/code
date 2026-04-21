import { useState, useEffect } from "react";
import { invoke } from "@tauri-apps/api/core";
import { open } from "@tauri-apps/plugin-dialog";
import { readFile } from "@tauri-apps/plugin-fs";
import { Upload, FileText, Settings, Activity, CheckCircle } from "lucide-react";
import "./App.css";

interface RecognitionResult {
  document_id: string;
  text_content: string;
  confidence: number;
  engine_used: string;
}

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [selectedFile, setSelectedFile] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [result, setResult] = useState<RecognitionResult | null>(null);
  const [backendStatus, setBackendStatus] = useState(false);

  useEffect(() => {
    checkBackendStatus();
    const interval = setInterval(checkBackendStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  async function checkBackendStatus() {
    try {
      const status = await invoke("check_backend_health");
      setBackendStatus(status as boolean);
    } catch (error) {
      setBackendStatus(false);
    }
  }

  async function greet() {
    const msg = await invoke("greet", { name: "OCR Desktop User" });
    setGreetMsg(msg as string);
  }

  async function selectFile() {
    try {
      const selected = await open({
        multiple: false,
        filters: [
          {
            name: "Image & PDF",
            extensions: ["png", "jpg", "jpeg", "pdf", "bmp", "tiff"],
          },
        ],
      });
      if (selected) {
        setSelectedFile(selected as string);
        setResult(null);
      }
    } catch (error) {
      console.error("File selection failed:", error);
    }
  }

  async function processOCR() {
    if (!selectedFile) return;
    
    setIsProcessing(true);
    try {
      // TODO: Call backend API for OCR
      // For now, simulate processing
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      setResult({
        document_id: `doc_${Date.now()}`,
        text_content: "Sample OCR text content...",
        confidence: 0.95,
        engine_used: "PP-OCRv5",
      });
    } catch (error) {
      console.error("OCR processing failed:", error);
    } finally {
      setIsProcessing(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>OCR Desktop</h1>
        <div className="status">
          <span className={`status-dot ${backendStatus ? "online" : "offline"}`}></span>
          Backend {backendStatus ? "Online" : "Offline"}
        </div>
      </header>

      <main className="main">
        <div className="upload-section">
          <div className="upload-area" onClick={selectFile}>
            <Upload size={48} />
            <p>Click to select file</p>
            <p className="hint">Supports: PNG, JPG, PDF, BMP, TIFF</p>
          </div>
          
          {selectedFile && (
            <div className="file-info">
              <FileText size={20} />
              <span>{selectedFile}</span>
            </div>
          )}
        </div>

        {selectedFile && (
          <button 
            className="process-btn"
            onClick={processOCR}
            disabled={isProcessing}
          >
            {isProcessing ? "Processing..." : "Start OCR"}
          </button>
        )}

        {result && (
          <div className="result-section">
            <h3>Recognition Result</h3>
            <div className="result-card">
              <div className="result-header">
                <CheckCircle size={20} className="success-icon" />
                <span>Document ID: {result.document_id}</span>
              </div>
              <div className="result-stats">
                <div className="stat">
                  <Activity size={16} />
                  <span>Confidence: {(result.confidence * 100).toFixed(1)}%</span>
                </div>
                <div className="stat">
                  <Settings size={16} />
                  <span>Engine: {result.engine_used}</span>
                </div>
              </div>
              <div className="result-content">
                <h4>Extracted Text:</h4>
                <pre>{result.text_content}</pre>
              </div>
            </div>
          </div>
        )}

        <div className="actions">
          <button onClick={greet}>Test Backend</button>
          {greetMsg && <p className="greet-msg">{greetMsg}</p>}
        </div>
      </main>

      <footer className="footer">
        <p>OCR Desktop v0.1.0 - Local OCR with Self-Learning</p>
      </footer>
    </div>
  );
}

export default App;
