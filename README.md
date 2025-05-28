# Random Forest ML Web Application

A full-stack web application that automatically analyzes datasets using Random Forest algorithm. Upload any CSV file and get instant insights, metrics, and visualizations.

## Features

- 📊 Automatic problem type detection (Classification/Regression)
- 🔍 Domain inference from dataset features
- 🌳 Random Forest model training and evaluation
- 📈 Comprehensive performance metrics
- 📊 Interactive visualizations
- 📱 Responsive design

## Tech Stack

### Backend

- FastAPI (Python)
- scikit-learn
- pandas
- numpy
- matplotlib/seaborn

### Frontend

- React
- Tailwind CSS
- Chart.js
- Axios

## Project Structure

```
random-forest/
├── backend/           # FastAPI backend
│   ├── app/
│   │   ├── models/    # ML models and utilities
│   │   ├── routes/    # API endpoints
│   │   └── utils/     # Helper functions
│   └── requirements.txt
├── frontend/          # React frontend
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── utils/
│   └── package.json
└── README.md
```

## Setup Instructions

### Prerequisites

- Python 3.8 or higher
- Node.js 14 or higher
- npm 6 or higher

### Backend Setup

1. Create a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   cd backend
   pip install -r requirements.txt
   ```

3. Run the server:
   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. Install dependencies:

   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm start
   ```

### Running Both Servers

You can use the root package.json to run both servers concurrently:

```bash
# Install root dependencies
npm install

# Run both servers
npm run dev
```

## Usage

1. Open your browser and navigate to `http://localhost:3000`
2. Upload a CSV file using the drag-and-drop interface or file selector
3. Wait for the analysis to complete
4. View the results, including:
   - Problem type (Classification/Regression)
   - Domain detection
   - Performance metrics
   - Feature importance plot
   - Confusion matrix (for classification)
   - ROC curve (for classification)

## API Documentation

Once the backend is running, visit `http://localhost:8000/docs` for the interactive API documentation.

## Example Dataset

A sample dataset is provided in `backend/test_data/sample.csv` for testing purposes. This dataset contains information about loan approvals with the following features:

- age
- income
- education_level
- employment_status
- credit_score
- loan_approved (target variable)

## License

MIT
cd backend : uvicorn app.main:app --reload -; uvicorn app.main:app --reload --port 8001
