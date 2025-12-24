# Torrent Search & Download API

A Flask-based REST API for searching and downloading torrents from 1337x. The API provides endpoints to search for torrents and initiate downloads with automatic organization by category.

## Features

- **Search Torrents**: Search 1337x by query with pagination support
- **Sorted Results**: Results automatically sorted by number of seeders
- **Organized Downloads**: Automatic categorization into Film, TV-Series, or Other directories
- **Background Downloads**: Non-blocking torrent downloads using async execution
- **CORS Enabled**: Ready for frontend integration

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

### Option 1: Local Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <project-directory>
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Run the Flask application:
```bash
python app.py
```

The server will start on `http://0.0.0.0:8080`

### Option 2: Docker Installation

1. Build the Docker image:
```bash
docker build -t torrent-api .
```

2. Run the container:
```bash
docker run -d \
  -p 8080:8080 \
  -v /path/to/downloads:/Film \
  -v /path/to/downloads:/Serie \
  -v /path/to/downloads:/Other \
  --name torrent-api \
  torrent-api
```

Replace `/path/to/downloads` with your desired download location on the host machine.

## Usage

### API Endpoints

#### 1. Search Torrents

**Endpoint**: `POST /search_torrent`

**Request Body**:
```json
{
  "query": "movie name",
  "page": 1
}
```

**Response**:
```json
{
  "movies": [
    {
      "torrent_id": "...",
      "name": "...",
      "seeders": 100,
      "leechers": 10,
      "magnet_link": "...",
      ...
    }
  ],
  "current_page": 1,
  "total_pages": 10
}
```

#### 2. Download Torrent

**Endpoint**: `POST /download_torrent`

**Request Body**:
```json
{
  "magnet_link": "magnet:?xt=urn:btih:...",
  "category": "Film",
  "short_name": "optional-folder-name"
}
```

**Parameters**:
- `magnet_link` (required): The magnet link of the torrent
- `category` (required): Download category - must be one of:
  - `"Film"` - Downloads to `/Film/` directory
  - `"TV-Series"` - Downloads to `/Serie/` directory
  - `"Other"` - Downloads to `/Other/` directory
- `short_name` (optional): Custom folder name. If not provided, extracts name from magnet link

**Response**:
```json
{
  "message": "Film download started successfully!"
}
```

## Download Organization

Downloads are automatically organized into category-specific directories:

```
/Film/
  └── movie-name/
/Serie/
  └── tv-show-name/
/Other/
  └── other-content/
```

## Configuration

To modify download paths, edit the `category_paths` dictionary in the code:

```python
category_paths = {
    "Film": "/Film/",
    "TV-Series": "/Serie/",
    "Other": "/Other/"
}
```

## Dependencies

- **py1337x**: 1337x torrent site scraper
- **Flask**: Web framework
- **flask-cors**: Cross-Origin Resource Sharing support
- **torrentp**: Torrent download manager

## Notes

- Downloads run in background threads to prevent blocking
- Folders are created automatically if they don't exist
- Search results are sorted by seeders for best download speeds
- The API uses CORS, making it accessible from web frontends

## Example Usage

### Using cURL

Search for torrents:
```bash
curl -X POST http://localhost:8080/search_torrent \
  -H "Content-Type: application/json" \
  -d '{"query": "inception", "page": 1}'
```

Download a torrent:
```bash
curl -X POST http://localhost:8080/download_torrent \
  -H "Content-Type: application/json" \
  -d '{
    "magnet_link": "magnet:?xt=urn:btih:...",
    "category": "Film",
    "short_name": "Inception"
  }'
```

## Docker Configuration

The included Dockerfile creates a lightweight Alpine-based image with:
- Python 3.12
- Non-root user (`downloader`) for security
- Exposed port 8080
- All required dependencies from `requirements.txt`

### Docker Volumes

Mount volumes to persist downloaded content:
- `/Film` - Movies directory
- `/Serie` - TV series directory
- `/Other` - Other content directory

## License

MIT License

Copyright (c) 2024

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Disclaimer

This tool is for educational purposes only. Ensure you have the legal right to download any content. The authors are not responsible for any misuse of this software.
