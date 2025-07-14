# 🏗️ WMS Automation - Full-Stack Assignment

This is a Warehouse Management System (WMS) MVP built as part of the AI-Powered Full-Stack Developer assignment.

It supports:
- ✅ SKU to MSKU mapping
- ✅ Combo product decomposition
- ✅ Sales data processing from multiple marketplaces (Amazon, Flipkart, Meesho, etc.)
- ✅ Inventory update and subtraction logic
- ✅ Visual dashboard (via Airtable)
- ✅ AI queries over data (Airtable AI prompts)
- ✅ Drag-and-drop interface for non-tech users
- ✅ Deployed web app via Streamlit

---

## 🚀 Demo

**🔗 Live App:** [https://your-streamlit-link](https://wms-app.streamlit.app/)
**📊 Airtable Dashboard:** [https://airtable.com/appHaexhstXF6RdbF/tblpC2fwllaI60zX3/viwb1uHCXNOLmCvEm?blocks=biplmQjaMLblqjfgd](https://airtable.com/appHaexhstXF6RdbF/tblpC2fwllaI60zX3/viwb1uHCXNOLmCvEm?blocks=biplmQjaMLblqjfgd)  

---

## 🧠 Features Overview

### 🔹 Part 1: Python + Streamlit App
- Upload sales report (CSV/XLSX)
- Upload WMS Excel file (SKU–MSKU mapping, combo sheet, inventory)
- Automatically:
  - Maps SKUs to MSKUs
  - Handles combo decomposition
  - Subtracts quantities from stock
  - Logs missing/unmapped SKUs
- Exports updated inventory with remaining stock

### 🔹 Part 2: Airtable Dashboard
- Inventory and Sales data organized relationally
- MSKU-linked tables
- Grouped by marketplace
- Filtered views and summary charts

### 🔹 Part 3: Drag-and-Drop UI
- Web-based upload interface via Streamlit
- Accepts multiple sales files (multi-marketplace)
- Designed for non-technical users

### 🔹 Part 4: AI Over Data Layer
- Used **Airtable AI Prompting**
  - Example: “Show SKUs with stock < 5”
  - Example: “Top 5 SKUs sold on Amazon last week”
- Charts and summaries generated automatically

---

## 🛠️ Tech Stack

| Layer         | Tools/Frameworks                          |
|--------------|--------------------------------------------|
| Frontend      | Streamlit (Python-based UI)               |
| Backend       | Python (Pandas for processing)            |
| Dashboard     | Airtable (linked relational tables)       |
| AI Layer      | Airtable AI (for query prompts)           |
| Deployment    | Streamlit Cloud                           |
| Extra Tools   | GitHub, VS Code, Excel, CSV               |

---

## 📂 Folder Structure

wms-assignment/                                                                                                                                                 
├── app.py                                                                                                                                                 
├── mapping_utils.py                                                                                                                                                 
├── requirements.txt                                                                                                                                                 
├── data/                                                                                                                                                 
│ ├── Amazon.csv                                                                                                                                                 
│ ├── Flipkart.csv                                                                                                                                                 
│ ├── Meesho.csv                                                                                                                                                 
│ └── ...                                                                                                                                                 
├── output/                                                                                                                                                 
│ └── updated_inventory.csv                                                                                                                                                 
└── README.md                                                                                                                                                 

---

## 🚀 Getting Started

### 📦 Local Setup

1. Clone this repo
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

Run the Streamlit app:

streamlit run app.py


🧾 Output

Updated inventory table with updated_qty

Log of unmapped/missing SKUs

Exportable CSV


📝 Notes

Uses intelligent column detection for mapping SKUs from various sales formats

Handles inventory across multiple warehouses

Combos are flattened using melt → grouped by MSKU

App is modular and easily extendable


🤝 Contribution

Built by Aishvariya Senaiyar

LinkedIn - [https://www.linkedin.com/in/aishvariya-s](https://www.linkedin.com/in/aishvariya-s)

GitHub - [https://github.com/Aishvariya-03](https://github.com/Aishvariya-03)

Email: [aishvariya19703@gmail.com](aishvariya19703@gmail.com)
