import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import "./App.css";
import Button from "./components/Button";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
    setGreetMsg(await invoke("greet", { name }));
  }

  return (
    <main className="w-screen h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-500 to-slate-700">
      <h1 className="font-black text-5xl text-slate-400">HELLO WORLD!</h1>
    </main>
  );
}

export default App;
