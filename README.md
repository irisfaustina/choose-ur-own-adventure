# Choose Your Own Adventure

An interactive story generation application that allows users to create and explore personalized adventures.

## Features

- **Interactive Story Generation**
  - Generate stories based on custom themes
  - Branching narrative paths with multiple choices
  - Dynamic story progression based on user choices

- **Modern Web Interface**
  - Clean and intuitive UI
  - Responsive design for all devices
  - Real-time story loading and updates

- **API-Driven Architecture**
  - RESTful API endpoints
  - Background job processing for story generation
  - Session management

## Tech Stack

### Backend
- **Framework**: FastAPI
- **Database**: SQLAlchemy
- **Job Processing**: Background Tasks
- **Authentication**: Cookie-based sessions

### Frontend
- **Framework**: React
- **Build Tool**: Vite
- **Routing**: React Router
- **State Management**: React Hooks
- **Styling**: CSS Modules

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- PostgreSQL (for production)
- SQLite (for development)

### Installation

#### Backend
```bash
# Navigate to backend directory
cd backend

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python -m alembic upgrade head

# Start the server
uv run main.py
```

#### Frontend
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

## API Documentation

The API is documented using FastAPI's automatic documentation. You can access it at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

#### Stories
- `POST /api/stories/create`: Create a new story
- `GET /api/stories/{id}/complete`: Get complete story tree
- `GET /api/stories/{id}/complete/{node_id}`: Get specific story node

#### Jobs
- `GET /api/jobs/{job_id}`: Get job status

## Project Structure

```
choose-ur-own-adventure/
├── backend/              # Backend application
│   ├── core/            # Core application logic
│   ├── db/              # Database models and migrations
│   ├── models/          # Database models
│   ├── routers/         # API route handlers
│   ├── schemas/         # Pydantic models
│   └── main.py          # FastAPI application
├── frontend/            # Frontend application
│   ├── public/          # Static assets
│   ├── src/             # Source code
│   │   ├── components/  # React components
│   │   ├── styles/      # CSS modules
│   │   └── util/        # Utility functions
│   └── vite.config.js   # Build configuration
└── README.md            # Project documentation
```

## Development

### Code Style
- Follow PEP 8 for Python code
- Use ESLint and Prettier for JavaScript/React code
- Maintain consistent commit messages

### Testing
- Unit tests for backend services
- Integration tests for API endpoints
- E2E tests for frontend components

### Security
- Input validation
- Rate limiting
- CSRF protection
- Secure cookie handling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
