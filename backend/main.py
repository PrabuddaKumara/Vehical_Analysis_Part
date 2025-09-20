from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
from typing import List, Dict
from crew_manager import VehicleAnalysisCrew

app = FastAPI(title="Vehicle Analyzer API", version="1.0.0")

# CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VehicleRequest(BaseModel):
    vehicle1: str
    vehicle2: str

class VehicleResponse(BaseModel):
    comparison: Dict
    ads: List[Dict]
    status: str

@app.get("/")
async def root():
    return {"message": "Vehicle Analyzer API is running!"}

@app.post("/api/v1/analyze-vehicles", response_model=VehicleResponse)
async def analyze_vehicles(request: VehicleRequest):
    try:
        print(f"Analyzing vehicles: {request.vehicle1} vs {request.vehicle2}")
        
        # Initialize crew manager
        crew = VehicleAnalysisCrew()
        
        # Run analysis
        result = await crew.run_analysis(request.vehicle1, request.vehicle2)
        
        return VehicleResponse(
            comparison=result["comparison"],
            ads=result["ads"],
            status="success"
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "message": "API is working properly"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)