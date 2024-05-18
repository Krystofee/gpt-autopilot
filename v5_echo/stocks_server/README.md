# FastAPI Intraday Data Fetcher

This project is a FastAPI server that fetches intraday stock data from an external API and returns the processed data in the response.

## Getting Started

### Prerequisites

Ensure you have Python installed on your system. Clone the repository and navigate to the project directory.

### Setup

1. **Create a `.env` file** and add the following line to it:

    ```
    API_KEY=V7MX5QSVQ0LT7LSJ
    ```

2. **Install the dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

### Running the Server

To run the FastAPI server, execute the following command:

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

The server will be accessible at `http://0.0.0.0:8000`.

### API Endpoint

You can fetch intraday data for a stock symbol (e.g., `IBM`) by accessing the following endpoint:

```
GET /intraday/{symbol}
```

For example:

```
GET http://0.0.0.0:8000/intraday/IBM
```

### Response
The response will contain the time series data for the given stock symbol:

```json
{
    "Time Series (5min)": {
        "2024-05-17 19:55:00": {
            "1. open": "169.0190",
            "2. high": "169.0190",
            "3. low": "169.0190",
            "4. close": "169.0190",
            "5. volume": "1"
        },
        "2024-05-17 19:50:00": {
            "1. open": "168.9800",
            "2. high": "168.9800",
            "3. low": "168.9700",
            "4. close": "168.9700",
            "5. volume": "156"
        },
        ...
    }
}
```