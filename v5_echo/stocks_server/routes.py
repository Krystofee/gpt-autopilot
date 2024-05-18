from fastapi import APIRouter, HTTPException
from external_api_service import fetch_intraday_data
from schemas import IntradayDataResponse

router = APIRouter()

@router.get("/intraday/{symbol}", response_model=IntradayDataResponse)
def get_intraday_data(symbol: str):
    try:
        data = fetch_intraday_data(symbol)
        if not data:
            raise HTTPException(status_code=404, detail="Data not found")
        return {"Time Series (5min)": data}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
