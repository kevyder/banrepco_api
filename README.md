# BanRepCo API

A FastAPI-based API that provides access to Bank of the Republic of Colombia (BanRep) data, inflation rates and TRM (Representative Market Rate) exchange rate data.

## Features

- Historical inflation rates data
- TRM (Representative Market Rate) exchange rate data
- Filter data by date ranges
- Get specific records by date
- Real-time TRM data updates from Banco de la República
- SQLite database with Turso integration
- Containerized deployment on Cloudflare

## Requirements

- Python 3.13+
- Node 22.16.0+
- Turso CLI (for database management)
- Docker (for local development)
- Cloudflare account (for deployment)

## Local Development Setup

To run the project locally, check out the [API README](./api/README.md).

### Running with Wrangler

1. Install dependencies
```bash
npm install
```

2. Run the development server
```bash
npm run dev
```

Server will be available at `http://localhost:8787`.

## Cloudflare Deployment

### Prerequisites

1. Install Wrangler CLI (if not already installed)
```bash
npm install -g wrangler
```

2. Login to Cloudflare
```bash
wrangler login
```

### Deployment

To deploy to Cloudflare the Cloudflare workers paid plan is required
```bash
# Deploy the container
npm run deploy
```

## API Documentation

Once the server is running, you can access:
- API documentation: `/docs`
- Alternative documentation: `/redoc`

### Available Endpoints

#### Inflation Endpoints
- `GET v1/inflation`: Get paginated inflation data
- `GET v1/inflation/date-range`: Get inflation data by date range
- `GET v1/inflation/{year}/{month}`: Get specific inflation record

#### TRM (Exchange Rate) Endpoints
- `GET v1/trm`: Get paginated TRM data with optional sorting
- `GET v1/trm/by-date-range`: Get TRM data within a specified date range
- `GET v1/trm/by-date`: Get TRM data for a specific date

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests (if available)
5. Submit a pull request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.
