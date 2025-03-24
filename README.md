# Warehouse Management AI App

## 📌 Project Overview
This project is a **Warehouse Management Application** that utilizes **AI-powered pathfinding** and **optimal storage positioning** to streamline warehouse operations. The app features **3D warehouse visualization, statistical analysis, and real-time optimization**. Built with **Tauri, React, TypeScript, Tailwind CSS, and Three.js**, and backed by **PostgreSQL** for data storage.

## 🚀 Features
- **AI-powered shortest pathfinding** for efficient navigation
- **Optimized storage allocation** for better inventory management
- **3D warehouse visualization** using Three.js
- **Advanced statistical analysis** with dynamic charts
- **PostgreSQL database** for structured, scalable data storage
- **Tauri integration** for cross-platform desktop application support
- **Flask API** for backend interactions
- **Responsive UI** with Tailwind CSS

## 🏗 Tech Stack
- **Frontend:** React, TypeScript, Tailwind CSS
- **Backend:** Tauri (Rust), Flask (Python), PostgreSQL
- **3D Visualization:** Three.js
- **AI Algorithms:** Custom pathfinding and storage optimization logic

## 📂 Project Structure
```
warehouse/
├── src/
│   ├── components/       # Reusable UI components (buttons, cards, modals, etc.)
│   ├── pages/            # Main application pages (Dashboard, Storage, Analytics, etc.)
│   ├── assets/           # Static files (icons, images, etc.)
│   ├── utils/            # Helper functions and utilities
│   ├── lib/              # API calls and database interactions
│   ├── main.tsx          # App entry point
│   └── App.tsx           # Main application component
│
├── src-tauri/
│   ├── db/               # Database interactions (PostgreSQL)
│   │   ├── schema.sql    # Database schema definitions
│   │   ├── queries.rs    # SQL queries and models
│   │   └── config.rs     # Database connection settings
│   ├── src/
│   │   ├── main.rs       # Tauri backend entry point (Rust)
│   │   └── config.rs     # Environment and config settings
│   └── Cargo.toml        # Rust dependencies
│
├── flask-api/
│   ├── app/
│   │   ├── routes/       # Flask API endpoints
│   │   ├── services/     # Business logic for AI & optimization
│   │   └── __init__.py   # Flask app initialization
│   ├── run.py            # Main entry point for Flask server
│   └── requirements.txt  # Python dependencies
│
├── public/               # Static public files
├── tauri.conf.json       # Tauri configuration file
├── package.json          # Node.js dependencies
├── tailwind.config.js    # Tailwind CSS configuration
├── tsconfig.json         # TypeScript configuration
├── .env                  # Environment variables
├── README.md             # Project documentation (this file!)
├── .gitignore            # Git ignored files
└── pyproject.toml        # Python project configuration
```

## ⚡ Installation & Setup
### Prerequisites
- **Node.js** (Latest LTS)
- **Rust & Cargo** (for Tauri backend)
- **PostgreSQL** (Database)
- **Python 3 & pip** (for Flask API)

### 1️⃣ Clone the Repository
```sh
git clone https://github.com/your-repo/warehouse-management-ai.git
cd warehouse-management-ai
```

### 2️⃣ Install Dependencies
```sh
npm install  # Install frontend dependencies
cargo build  # Compile Tauri backend
pip install -r flask-api/requirements.txt  # Install Flask dependencies
```

### 3️⃣ Set Up Database
1. Start PostgreSQL and create a database:
```sql
CREATE DATABASE warehouse_db;
```
2. Configure the `.env` file:
```
DATABASE_URL=postgresql://user:password@localhost:5432/warehouse_db
```
3. Run database migrations:
```sh
cargo run --bin migrate
```

### 4️⃣ Start the App
```sh
npm run dev  # Start frontend
cargo tauri dev  # Start Tauri backend
python flask-api/run.py  # Start Flask API
```

## 📊 Future Enhancements
- 🔄 **Real-time warehouse tracking** with AI-powered predictions
- 📡 **Cloud-based synchronization** for multi-device access
- 🔥 **Machine learning optimization** for demand forecasting

## 🤝 Contributing
Contributions are welcome! Feel free to fork the repo and submit pull requests. 🚀

## 📜 License
This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

