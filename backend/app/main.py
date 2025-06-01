from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import pandas as pd # used for data manipulation & analysis
import numpy as np # used for numerical operations
from typing import Dict, Any
import io
import json
from .models.ml_processor import MLProcessor
from .utils.domain_detector import detect_domain
from .utils.data_processor import preprocess_data

app = FastAPI(
    title="Random Forest ML API",
    description="API for automatic dataset analysis using Random Forest algorithm",
    version="1.0.0"
)

# Configure CORS - more permissive for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/analyze")
async def analyze_dataset(file: UploadFile = File(...)) -> Dict[str, Any]:
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        # Read the uploaded CSV file
        contents = await file.read()
        df = pd.read_csv(io.BytesIO(contents))
        
        if df.empty:
            raise HTTPException(status_code=400, detail="The uploaded file is empty")
        
        # Detect domain
        domain = detect_domain(df.columns)
        
        # Preprocess data
        df_processed, target_column = preprocess_data(df)
        
        # Initialize ML processor
        ml_processor = MLProcessor(df_processed, target_column)
        
        # Get analysis results
        results = ml_processor.analyze()
        
        # Add domain information
        results['domain'] = domain
        
        return JSONResponse(content=results)
        
    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=400, detail="The uploaded file is empty or invalid")
    except pd.errors.ParserError:
        raise HTTPException(status_code=400, detail="Invalid CSV file format")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy"} 