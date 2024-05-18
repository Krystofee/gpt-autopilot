from pydantic import BaseModel, Field
from typing import Dict

class TimeSeriesData(BaseModel):
    open: str = Field(..., alias='1. open')
    high: str = Field(..., alias='2. high')
    low: str = Field(..., alias='3. low')
    close: str = Field(..., alias='4. close')
    volume: str = Field(..., alias='5. volume')

class IntradayDataResponse(BaseModel):
    time_series: Dict[str, TimeSeriesData] = Field(..., alias='Time Series (5min)')
