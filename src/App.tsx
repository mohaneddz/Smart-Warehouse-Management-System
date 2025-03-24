import { useState } from "react";
import { invoke } from "@tauri-apps/api/core";
import "./App.css";

function App() {
  const [greetMsg, setGreetMsg] = useState("");
  const [name, setName] = useState("");

  async function greet() {
    // Learn more about Tauri commands at https://tauri.app/develop/calling-rust/
    setGreetMsg(await invoke("greet", { name }));
  }

  return (
    <main className="w-screen h-screen flex flex-col items-center justify-center bg-gradient-to-b from-slate-500 to-slate-700">
      <div className="">
        <h1 className="font-black text-5xl text-slate-300">Hello World!</h1>
        <h3 className=""></h3>
      </div>
    </main>
  );
}

export default App;
