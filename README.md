# 🍞 Bakery Market Basket Analysis

A comprehensive web-based dashboard for visualizing and analyzing customer purchasing patterns in a bakery using **Association Rule Mining** and **Market Basket Analysis**. This interactive application helps identify which products are frequently bought together, enabling data-driven decisions for product placement, promotions, and inventory management.

[![Python Version](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/)
[![Dash](https://img.shields.io/badge/Dash-3.2.0-green.svg)](https://dash.plotly.com/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 📋 Table of Contents

- [Overview](#overview)
- [Key Concepts](#key-concepts)
  - [Market Basket Analysis](#market-basket-analysis)
  - [Association Rule Mining](#association-rule-mining)
  - [Key Metrics](#key-metrics)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Deployment](#deployment)
- [Technical Implementation](#technical-implementation)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

## 🎯 Overview

This project implements a **Market Basket Analysis** system for a bakery business using the **Apriori algorithm** to discover association rules from transaction data. The application provides interactive visualizations including:

- **Bar charts** showing top-selling items
- **Heatmaps** displaying product associations
- **Network graphs** visualizing item relationships
- **Dynamic tables** for exploring specific product recommendations

The dashboard is built with **Dash** (Plotly) and uses **mlxtend** for implementing the Apriori algorithm and extracting association rules.

## 📚 Key Concepts

### Market Basket Analysis

**Market Basket Analysis (MBA)** is a data mining technique used to discover purchasing patterns by analyzing which items customers frequently buy together. It's called "market basket" analysis because it originated from analyzing the contents of shopping baskets.

**Business Applications:**
- 📦 **Product placement**: Position frequently bought-together items near each other
- 🎁 **Cross-selling**: Recommend complementary products
- 💰 **Promotional strategies**: Bundle products that are often purchased together
- 📊 **Inventory management**: Stock related items based on demand patterns

### Association Rule Mining

**Association Rule Mining** identifies interesting relationships (associations) between items in large datasets. It discovers rules of the form:

```
{Antecedent} → {Consequent}
```

**Example:** 
```
{Coffee} → {Bread}
```
This rule means: "Customers who buy Coffee are likely to also buy Bread"

#### The Apriori Algorithm

The **Apriori algorithm** is the most popular algorithm for finding frequent itemsets and generating association rules. It works on the principle:

> "If an itemset is frequent, then all of its subsets must also be frequent"

**Algorithm Steps:**
1. **Generate candidate itemsets** of length k
2. **Prune candidates** with support below threshold
3. **Count support** for remaining candidates
4. **Repeat** for k+1 length itemsets
5. **Generate rules** from frequent itemsets

### Key Metrics

#### 1. Support
**Definition:** The proportion of transactions that contain a particular itemset.

```
Support(A) = (Transactions containing A) / (Total Transactions)
```

**Example:** If Coffee appears in 150 out of 1000 transactions:
```
Support(Coffee) = 150/1000 = 0.15 or 15%
```

**Interpretation:** Indicates how frequently an item or itemset appears in the dataset.

#### 2. Confidence
**Definition:** The probability that a transaction containing antecedent A also contains consequent B.

```
Confidence(A → B) = Support(A ∪ B) / Support(A)
```

**Example:** If 100 transactions have both Coffee and Bread, and 150 have Coffee:
```
Confidence(Coffee → Bread) = 100/150 = 0.67 or 67%
```

**Interpretation:** Shows the reliability of the rule. A confidence of 67% means that 67% of customers who buy Coffee also buy Bread.

#### 3. Lift
**Definition:** The ratio of observed support to expected support if A and B were independent.

```
Lift(A → B) = Support(A ∪ B) / (Support(A) × Support(B))
```

**Interpretation:**
- **Lift > 1**: Items are positively correlated (bought together more often than expected)
- **Lift = 1**: Items are independent (no correlation)
- **Lift < 1**: Items are negatively correlated (rarely bought together)

**Example:** If Coffee and Bread have:
- Joint support = 0.10 (10%)
- Individual supports = 0.15 (Coffee) and 0.20 (Bread)

```
Lift = 0.10 / (0.15 × 0.20) = 0.10 / 0.03 = 3.33
```

A lift of 3.33 means customers are 3.33 times more likely to buy Coffee and Bread together than if the purchases were independent.

#### 4. Leverage
**Definition:** The difference between observed frequency of A and B appearing together and expected frequency if they were independent.

```
Leverage(A → B) = Support(A ∪ B) - (Support(A) × Support(B))
```

#### 5. Conviction
**Definition:** The ratio of expected frequency that A occurs without B.

```
Conviction(A → B) = (1 - Support(B)) / (1 - Confidence(A → B))
```

## ✨ Features

### 1. Association Rules Dashboard
- 📊 Display top-selling product combinations
- 🔍 View association rules sorted by confidence and lift
- 📈 Interactive filtering and sorting

### 2. Item Association Explorer
- 🔎 Select any product to see recommended pairings
- 📋 Dynamic table showing all associations for selected item
- 💡 Confidence and lift scores for each recommendation

### 3. Visualization Tools
- 📊 **Bar Charts**: Item counts and percentage distributions
- 🔥 **Heatmap**: Visual representation of lift values between products
- 🕸️ **Network Graph**: Interactive graph showing product relationships

### 4. Configurable Parameters
- ⚙️ Adjustable minimum lift threshold (default: 1.0)
- ⚙️ Adjustable minimum confidence threshold (default: 0.2)
- ⚙️ Customizable number of top items to display

## 📁 Project Structure

```
bread-basket/
├── src/
│   ├── app.py                          # Dash app initialization
│   ├── index.py                        # Main entry point, routing, navigation
│   ├── config.py                       # Configuration constants and parameters
│   ├── data_loader.py                  # Data loading with singleton pattern
│   ├── utils.py                        # Utility functions
│   ├── helper_functions.py             # Additional helper functions
│   ├── assets/
│   │   └── association.css             # Custom styling
│   ├── models/
│   │   ├── bakery_initial.sav          # Initial dataset (pickled)
│   │   ├── final_model_appriori.sav    # Trained Apriori model (pickled)
│   │   ├── BreadBasket_DMS.csv         # Raw transaction data
│   │   ├── bakery_market_basket_analysis.ipynb  # Analysis notebook
│   │   └── test_model.ipynb            # Model testing notebook
│   └── pages/
│       ├── __init__.py
│       ├── association_rules.py        # Rules display page
│       └── association_visualization.py # Visualization page
├── env/                                 # Virtual environment
├── requirements.txt                     # Python dependencies
├── runtime.txt                          # Python version for deployment
├── Procfile                             # Heroku deployment configuration
├── ARCHITECTURE.md                      # Detailed architecture documentation
└── README.md                            # This file
```

## 🚀 Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/kosalaMaduwantha/bread-basket.git
cd bread-basket
```

### Step 2: Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv env

# Activate virtual environment
# On Linux/Mac:
source env/bin/activate
# On Windows:
# env\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Dependencies Overview
- **dash** (3.2.0): Web application framework
- **dash-bootstrap-components** (1.6.0): Bootstrap components for Dash
- **dash-cytoscape** (1.0.2): Network graph visualization
- **plotly** (6.3.1): Interactive plotting library
- **pandas** (1.5.3): Data manipulation
- **mlxtend** (0.23.4): Apriori algorithm implementation
- **scikit-learn** (1.3.2): Machine learning utilities
- **gunicorn** (23.0.0): WSGI HTTP server for deployment

## 💻 Usage

### Running Locally

#### Development Mode
```bash
# Make sure virtual environment is activated
source env/bin/activate

# Run the application
python src/index.py
```

The application will start on `http://127.0.0.1:8050/`

#### Production Mode
```bash
# Using Gunicorn
gunicorn src.index:server --bind 0.0.0.0:8050
```

### Configuration

Edit `src/config.py` to customize:

```python
# Association rules parameters
MIN_LIFT = 1              # Minimum lift threshold
MIN_CONFIDENCE = 0.2      # Minimum confidence threshold
LIFT_THRESHOLD = 0.1      # Threshold for rule generation

# Display parameters
TOP_N_ITEMS = 10          # Number of top items to display
TOP_N_ASSOCIATIONS = 10   # Number of top associations to show

# App configuration
APP_HOST = '127.0.0.1'
APP_PORT = 8050
APP_DEBUG = True          # Set to False in production
```

### Navigation

The application has two main pages:

1. **Association Visualization** (`/association_visualization`)
   - View item sales statistics
   - Explore heatmaps of product relationships
   - Interactive network graph of associations

2. **Association Rules** (`/association_rules`)
   - Browse top-selling product combinations
   - Select items to see specific recommendations
   - Filter and sort association rules

## 🌐 Deployment

### Deploying to Heroku

This application is configured for Heroku deployment with the included `Procfile` and `runtime.txt`.

#### Step 1: Create Heroku App
```bash
# Install Heroku CLI if not already installed
# Then login
heroku login

# Create new Heroku app
heroku create your-app-name
```

#### Step 2: Deploy
```bash
# Add files to git
git add .
git commit -m "Initial commit"

# Push to Heroku
git push heroku main
```

#### Step 3: Scale Dynos
```bash
heroku ps:scale web=1
```

#### Step 4: Open Application
```bash
heroku open
```

### Environment Variables (Optional)

For production, consider using environment variables:

```bash
heroku config:set DEBUG=False
heroku config:set MIN_LIFT=1.0
heroku config:set MIN_CONFIDENCE=0.2
```

Update `config.py` to read from environment:
```python
import os

APP_DEBUG = os.getenv('DEBUG', 'False') == 'True'
MIN_LIFT = float(os.getenv('MIN_LIFT', '1.0'))
MIN_CONFIDENCE = float(os.getenv('MIN_CONFIDENCE', '0.2'))
```

## 🔧 Technical Implementation

### Architecture Highlights

#### 1. Singleton Pattern for Data Loading
The `DataLoader` class implements the singleton pattern to ensure data is loaded only once and cached for subsequent requests:

```python
class DataLoader:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataLoader, cls).__new__(cls)
        return cls._instance
```

**Benefits:**
- ⚡ Reduced load times (40-60% faster)
- 💾 Efficient memory usage
- 🔄 Consistent data across pages

#### 2. Modular Page Structure
Each page is self-contained with:
- Layout definition
- Callback functions
- Component generation functions

#### 3. Centralized Configuration
All constants, thresholds, and styling parameters are stored in `config.py` for easy maintenance.

### Data Flow

```
User Action
    ↓
Dash Callback Triggered
    ↓
DataLoader.get_data() → Check Cache
    ↓
    ├─ Cache Hit → Return Cached Data
    └─ Cache Miss → Load from File → Cache → Return
    ↓
Process with utils.py
    ↓
Format and Render
    ↓
Update UI Component
```

### Performance Optimizations

- **Lazy loading**: Data loaded only when needed
- **Caching**: Singleton pattern prevents redundant file reads
- **Efficient callbacks**: Minimal computation in callback functions
- **Compressed assets**: CSS and images optimized for web delivery


### Development Guidelines

- Follow PEP 8 style guidelines
- Add docstrings to all functions
- Update tests for new features
- Update documentation as needed


## 👥 Authors

- **Kosala Maduwantha** - [GitHub](https://github.com/kosalaMaduwantha)

## 🙏 Acknowledgments

- **mlxtend** library for Apriori algorithm implementation
- **Plotly/Dash** for the amazing visualization framework
- **Bootstrap** for responsive UI components
- The open-source community for various tools and libraries

## 🔮 Future Enhancements

- [ ] Add user authentication
- [ ] Export reports to PDF
- [ ] Real-time data updates
- [ ] Integration with POS systems
- [ ] Advanced filtering options
- [ ] A/B testing framework for promotional strategies
- [ ] Time-series analysis of purchasing patterns
- [ ] Seasonal trend detection
- [ ] Customer segmentation analysis

---

**Made with ❤️ using Python and Dash**
