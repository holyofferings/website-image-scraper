# 🕷️ Website Image Scraper

A powerful and user-friendly web application that crawls entire websites to extract all images from every page and provides them in an organized format with detailed CSV reports.

## ✨ Features

- **Full Website Crawling**: Automatically discovers and crawls all pages within a website (up to 200 pages)
- **Complete Image Extraction**: Finds all images including those in CSS backgrounds and lazy-loaded content
- **Real-time Progress Tracking**: Live updates on scraping progress with detailed statistics
- **Organized Downloads**: Images delivered in a convenient ZIP package with CSV metadata
- **Modern UI**: Beautiful, responsive interface with progress indicators
- **Detailed CSV Reports**: Structured data with page URL, image ID, image URL, and filename
- **Error Handling**: Robust error handling with user-friendly messages
- **Background Processing**: Non-blocking scraping with real-time status updates

## 📋 Requirements

- Python 3.7 or higher
- Internet connection for scraping websites

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
python app.py
```

### 3. Open Your Browser

Navigate to `http://localhost:8080` and start scraping!

## 🎯 How to Use

1. **Enter Website URL**: Input the URL of the website you want to scrape
2. **Start Scraping**: Click the "Start Scraping" button
3. **Monitor Progress**: Watch real-time crawling and download progress with statistics
4. **Download Results**: Once complete, download the ZIP file containing:
   - `images/` folder with all scraped images
   - `image_data.csv` file with metadata
   - `crawl_summary.txt` file with crawling statistics

## 📊 CSV File Structure

The generated CSV file contains the following columns:

| Column | Description |
|--------|-------------|
| PAGE_URL | The original website URL that was scraped |
| IMAGE_ID | Unique identifier for each image (e.g., 0001, 0002) |
| IMAGE_URL | Direct URL to the original image |
| FILENAME | Local filename of the downloaded image |

## 🛠️ Technical Details

### Backend (Python Flask)
- **Web Scraping**: BeautifulSoup for HTML parsing
- **HTTP Requests**: Requests library with proper headers
- **Image Processing**: Supports JPG, PNG, GIF, BMP, WebP, SVG
- **Background Tasks**: Threading for non-blocking operations
- **File Management**: Automatic ZIP creation and cleanup

### Frontend (HTML/CSS/JavaScript)
- **Modern UI**: Responsive design with gradient backgrounds
- **Real-time Updates**: AJAX polling for progress updates
- **Form Validation**: URL validation and error handling
- **Progress Visualization**: Animated progress bars and statistics

### Supported Image Sources
- Standard `<img>` tags with `src` attribute
- Lazy-loaded images with `data-src` or `data-lazy-src`
- CSS background images in `style` attributes
- Various image formats: JPG, JPEG, PNG, GIF, BMP, WebP, SVG

## 🔧 Configuration

### Customizing User Agent
The application uses a Chrome user agent by default. You can modify it in the `headers` dictionary in `app.py`.

### Adjusting Timeout
The default timeout for HTTP requests is 30 seconds. Modify the `timeout` parameter in the `requests.get()` calls.

### Changing Port
To run on a different port, modify the last line in `app.py`:
```python
app.run(debug=True, port=YOUR_PORT)
```

## 🚨 Important Notes

- **Respect robots.txt**: Always check and respect website robots.txt files
- **Rate Limiting**: The application doesn't implement rate limiting - use responsibly
- **Large Websites**: Scraping large websites may take considerable time
- **Legal Compliance**: Ensure you have permission to scrape the target website
- **Storage Space**: Large image collections will require adequate disk space

## 🐛 Troubleshooting

### Common Issues

**Issue**: "No images found on the website"
- **Solution**: The website might use JavaScript to load images. Try a different website or check if images are loaded dynamically.

**Issue**: "Error downloading images"
- **Solution**: Some images might be protected or require authentication. The scraper will skip these and continue with others.

**Issue**: "Connection timeout"
- **Solution**: The website might be slow or blocking requests. Try again or use a different website.

## 📁 Project Structure

```
SCRAPPING AGENT/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Frontend HTML template
├── scrape_results_*/     # Generated folders (auto-cleaned)
└── *.zip                 # Generated ZIP files
```

## 🔄 How It Works

1. **URL Input**: User enters a website URL through the web interface
2. **Request Processing**: Flask backend validates and processes the request
3. **Web Scraping**: BeautifulSoup parses the HTML and extracts image URLs
4. **Image Download**: Each image is downloaded with proper error handling
5. **CSV Generation**: Metadata is compiled into a structured CSV file
6. **ZIP Creation**: All files are packaged into a downloadable ZIP
7. **Cleanup**: Temporary files are managed automatically

## 🎨 UI Features

- **Gradient Backgrounds**: Modern visual design
- **Progress Indicators**: Real-time scraping progress
- **Statistics Cards**: Live count of found and downloaded images
- **Responsive Design**: Works on desktop and mobile devices
- **Error States**: Clear error messages and recovery options
- **Success States**: Celebration UI for completed scrapes

## 🔒 Security Considerations

- Input validation for URLs
- Proper error handling to prevent crashes
- User agent headers to identify requests
- File type validation for downloaded images
- Timeout handling for slow websites

## 📈 Performance

- **Concurrent Downloads**: Images are downloaded sequentially to avoid overwhelming servers
- **Memory Efficient**: Streaming downloads for large images
- **Progress Updates**: Real-time status without blocking the UI
- **Background Processing**: Non-blocking server operations

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the application!

## 📄 License

This project is open source and available under the MIT License. 