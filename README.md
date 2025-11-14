# ⚙️ ATLAS — Smart Warehouse Management System

## 🎥 Video Documentation
<div align="center">
  <!-- Click the image to open the Drive preview. 
       Ensure screenshots/video.avif (or video.avif) exists in the repo; adjust path if needed. -->
  <a href="https://drive.google.com/file/d/1AziU_eTjwFnQaXtP8V2ilecWmuWdLeLl/preview">
    <img src="screenshots/video.avif" alt="ATLAS video preview — click to open" style="max-width:100%;height:auto;" />
  </a>

  <p>
    <a href="https://drive.google.com/file/d/1AziU_eTjwFnQaXtP8V2ilecWmuWdLeLl/preview">Open video in Google Drive (new tab)</a>
  </p>
</div>

---

## 📌 Overview
ATLAS is a **Next.js-based intelligent inventory management system** designed to help teams track items, manage stock, analyze historical changes, and run advanced simulations to optimize inventory strategies.

The entire project is built with a **scalable architecture**, optimized for **SEO**, and uses **AVIF** images for maximum performance.

---

## 🚀 Features
- Smart **inventory intake, updates, and consumption**
- **Simulation engine** to test stock strategies
- **Full item history timeline**
- **Inventory diff engine** for displaying changes
- **User settings & preferences**
- **Responsive, fast, and SEO-ready**
- Built on **Next.js App Router + Server Actions**

---

## 🧠 Core Algorithms

| Algorithm | Purpose | Description |
|----------|----------|-------------|
| **Stock Level Tracking** | Real-time stock state | Tracks additions/removals using incremental counters. |
| **Demand Forecasting (EMA)** | Predict future consumption | Uses Exponential Moving Average to estimate future depletion rates. |
| **Restock Suggestion Logic** | Automated advice | Suggests reorder quantities by combining safety stock + predicted demand. |
| **Simulation Engine** | Strategy testing | Runs multiple simulated cycles with various parameters to compare outcomes. |
| **History Diff Engine** | Change tracking | Generates field-level diffs between old and new item states. |
| **Low-Stock Alerts** | Warning system | Triggers notifications when thresholds are crossed. |

---

## 🛠️ Tech Stack

![Next.js](https://img.shields.io/badge/Next.js-000000?style=for-the-badge&logo=nextdotjs)  
![React](https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=black)  
![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript)  
![TailwindCSS](https://img.shields.io/badge/TailwindCSS-06B6D4?style=for-the-badge&logo=tailwindcss)  
![Tauri](https://img.shields.io/badge/Tauri-000000?style=for-the-badge&logo=tauri)  
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python)  
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask)  
![Three.js](https://img.shields.io/badge/Three.js-000000?style=for-the-badge&logo=three.js&logoColor=white)  
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql)  

---

## 🗂️ Project Structure

```
/app
/home
/inventory
add/
manage/
take/
/simulation
/history
/settings
/components
/lib
/public/screenshots

```

---

## 📸 Screenshots

| Home                       | History                       |
| -------------------------- | ----------------------------- |
| ![](screenshots/home.avif) | ![](screenshots/history.avif) |

| Add Inventory                       | Manage Inventory                       |
| ----------------------------------- | -------------------------------------- |
| ![](screenshots/inventory-add.avif) | ![](screenshots/inventory-manage.avif) |

| Take Inventory                       | Settings                       |
| ------------------------------------ | ------------------------------ |
| ![](screenshots/inventory-take.avif) | ![](screenshots/settings.avif) |

| 3D Simulation                    |
| -------------------------------- |
| ![](screenshots/simulation.avif) |


---

## 🔧 Installation

```
git clone https://github.com/mohaneddz/Smart-Warehouse-Management-System

cd ATLAS

pnpm install

pnpm run dev
```

---

## 🧪 Simulation Engine — How It Works

The simulation module allows users to test restock strategies by generating multiple virtual cycles.

Each cycle evaluates:

* Starting stock
* Daily usage pattern
* Forecasted usage (EMA)
* Safety stock
* Restock quantity
* Total duration until stockout

The system compares scenarios and highlights the most optimal strategy.

---

## 📄 License

This project is released under the **MIT License**.