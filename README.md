# 🛢️ Russian Oil Well Production Analytics App

An interactive Streamlit-based analytics application designed to derive actionable insights from time-series production data of an oil well in Russia.
This project demonstrates how data analytics and machine learning can support engineering and operational decision-making in oil and gas production systems.

🔗 Live Application: https://russiaoilwellapp.streamlit.app/

📂 GitHub Repository: https://github.com/olufemiogunwole/Russia-Oil-Well-Production

# 📌 Project Overview

This application analyzes daily production data from Oil Well №807, located in northern Russia. The well produces a mixture of oil, gas, and water under high reservoir pressure and is equipped with artificial lift.

The goal of this project is to:

Move from static dashboards to an interactive analytics platform

Support production monitoring, anomaly detection, and strategic decision-making

Demonstrate how such systems can be extended to real-time database-driven workflows

# 📊 Key Features
📈 Production Trend Analysis

Interactive selection of production metrics

Rolling averages for trend smoothing

Identification of long-term production decline or stability

🏭 Performance Analysis

Segmentation of high vs low production periods

Threshold-based identification of operational inefficiencies

🧠 Operational Regime Clustering

K-Means clustering applied to time-series production metrics

Identification of:

High-output operating states

Stable production regimes

Declining or inefficient production periods

Cluster centroids represent typical operational conditions over time

📌 Strategic Insights

Clear interpretation of analytical outputs

Engineering-focused insights for operational planning and optimization

# 🗄️ Database & Real-Time Readiness

The application is designed to be database-ready.
With integration to a production database (e.g., PostgreSQL, MySQL, or cloud data warehouses), the platform can support:

Live or near real-time production feeds

Continuous monitoring of well performance

Faster detection of anomalies and operational risks

Ongoing decision support without manual data uploads

# 🧰 Tech Stack

Python

Streamlit

Pandas & NumPy

Matplotlib

Scikit-learn (K-Means Clustering)

# 📂 Project Structure
 Oil well website.py      # Main Streamlit application
 Oil well.csv             # Oil well production dataset
 requirements.txt         # Project dependencies
 README.md                # Project documentation
 .vscode/
    settings.json

# ⚙️ Installation & Local Run

1️⃣ Clone the repository:

git clone https://github.com/olufemiogunwole/Russia-Oil-Well-Production.git
cd Russia-Oil-Well-Production


2️⃣ Install dependencies:

pip install -r requirements.txt


3️⃣ Run the application:

streamlit run "Oil well website.py"

# 📈 About the Dataset

The dataset contains daily operational measurements from Oil Well №807, including:

Total fluid production

Oil, gas, and water production rates

Water cut

Dynamic fluid level

Reservoir pressure

These measurements provide a comprehensive view of the well’s production performance and reservoir behaviour over time.

🎯 Key Insights

High water cut dominates production, significantly reducing oil output

Pump performance inefficiencies are observed despite stable fluid levels

Production trends indicate late-stage decline

Clustering reveals distinct operational regimes requiring different intervention strategies

🚀 Future Enhancements

Database integration for real-time data ingestion

Automated anomaly alerts

Advanced time-series forecasting

Multi-well scalability for field-level analysis

# 👤 Author

Olufemi Ogunwole
Data Analytics | Engineering | Machine Learning

# 📜 License

This project is for educational and analytical purposes.
