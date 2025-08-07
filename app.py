from flask import Flask, render_template, request, jsonify, send_file
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse
import os
import csv
import zipfile
from datetime import datetime
import threading
import time
import uuid
from collections import deque

app = Flask(__name__)

# Global variable to store scraping progress
scraping_status = {}

def is_valid_image_url(url):
    """Check if URL is a valid image URL"""
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp', '.svg')
    return url.lower().endswith(image_extensions)

def is_same_domain(url1, url2):
    """Check if two URLs are from the same domain"""
    domain1 = urlparse(url1).netloc.lower()
    domain2 = urlparse(url2).netloc.lower()
    return domain1 == domain2

def normalize_url(url):
    """Normalize URL by removing fragments and query parameters for deduplication"""
    parsed = urlparse(url)
    return urlunparse((parsed.scheme, parsed.netloc, parsed.path, '', '', ''))

def get_all_links(soup, base_url):
    """Extract all valid links from a page"""
    links = set()
    
    # Find all anchor tags with href
    for link in soup.find_all('a', href=True):
        href = link['href']
        full_url = urljoin(base_url, href)
        
        # Only include links from the same domain
        if is_same_domain(base_url, full_url):
            normalized_url = normalize_url(full_url)
            # Exclude common file types that aren't web pages
            if not normalized_url.lower().endswith(('.pdf', '.doc', '.docx', '.zip', '.exe', '.dmg')):
                links.add(normalized_url)
    
    return links

def download_image(img_url, folder_path, img_id):
    """Download individual image"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(img_url, headers=headers, timeout=30, stream=True)
        response.raise_for_status()
        
        # Get file extension
        parsed_url = urlparse(img_url)
        path = parsed_url.path
        if '.' in path:
            extension = path.split('.')[-1].lower()
            if extension not in ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'webp', 'svg']:
                extension = 'jpg'
        else:
            extension = 'jpg'
        
        filename = f"image_{img_id}.{extension}"
        file_path = os.path.join(folder_path, filename)
        
        with open(file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        return filename
    except Exception as e:
        print(f"Error downloading {img_url}: {str(e)}")
        return None

def scrape_page_images(url, headers):
    """Scrape images from a single page"""
    try:
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find all image tags
        img_tags = soup.find_all('img')
        
        # Also look for images in CSS background-image properties
        style_tags = soup.find_all(['div', 'section', 'header', 'span'], style=True)
        
        image_urls = []
        
        # Extract URLs from img tags
        for img in img_tags:
            src = img.get('src') or img.get('data-src') or img.get('data-lazy-src')
            if src:
                full_url = urljoin(url, src)
                if is_valid_image_url(full_url):
                    image_urls.append(full_url)
        
        # Extract URLs from CSS background-image
        for element in style_tags:
            style = element.get('style', '')
            if 'background-image' in style:
                # Extract URL from background-image: url(...)
                start = style.find('url(')
                if start != -1:
                    start += 4
                    end = style.find(')', start)
                    if end != -1:
                        bg_url = style[start:end].strip('\'"')
                        full_url = urljoin(url, bg_url)
                        if is_valid_image_url(full_url):
                            image_urls.append(full_url)
        
        # Get all links for further crawling
        page_links = get_all_links(soup, url)
        
        return list(set(image_urls)), page_links
        
    except Exception as e:
        print(f"Error scraping page {url}: {str(e)}")
        return [], set()

def scrape_images(url, task_id):
    """Main scraping function that crawls all pages"""
    try:
        scraping_status[task_id] = {
            'status': 'running',
            'progress': 0,
            'total_images': 0,
            'downloaded': 0,
            'pages_found': 0,
            'pages_scraped': 0,
            'message': 'Starting crawl...'
        }
        
        # Create directories
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_folder = f"scrape_results_{timestamp}"
        images_folder = os.path.join(base_folder, "images")
        os.makedirs(images_folder, exist_ok=True)
        
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        
        # Initialize crawling
        visited_urls = set()
        urls_to_visit = deque([normalize_url(url)])
        all_image_urls = []
        csv_data = []
        
        scraping_status[task_id]['message'] = 'Discovering pages...'
        
        # Crawl all pages found on the website (no artificial limit)
        # Safety: Stop if we've been crawling for too long (prevent infinite loops)
        max_crawl_time = 3600  # 1 hour maximum crawl time
        start_time = time.time()
        
        while urls_to_visit:
            # Safety check: Stop if crawling too long
            if time.time() - start_time > max_crawl_time:
                scraping_status[task_id]['message'] = f'Crawl time limit reached (1 hour). Processed {len(visited_urls)} pages.'
                break
                
            current_url = urls_to_visit.popleft()
            
            if current_url in visited_urls:
                continue
                
            visited_urls.add(current_url)
            
            scraping_status[task_id].update({
                'pages_found': len(visited_urls) + len(urls_to_visit),
                'pages_scraped': len(visited_urls),
                'message': f'Crawling page {len(visited_urls)}: {current_url[:50]}...'
            })
            
            # Scrape current page
            page_images, page_links = scrape_page_images(current_url, headers)
            
            # Add images from this page
            for img_url in page_images:
                if img_url not in [item['IMAGE_URL'] for item in csv_data]:
                    all_image_urls.append(img_url)
                    csv_data.append({
                        'PAGE_URL': current_url,
                        'IMAGE_ID': f"{len(csv_data)+1:04d}",
                        'IMAGE_URL': img_url,
                        'FILENAME': ''  # Will be filled when downloaded
                    })
            
            # Add new links to visit
            for link in page_links:
                if link not in visited_urls and link not in urls_to_visit:
                    urls_to_visit.append(link)
            
            # Small delay to be respectful to the server
            time.sleep(0.5)
        
        total_images = len(all_image_urls)
        scraping_status[task_id].update({
            'total_images': total_images,
            'pages_found': len(visited_urls) + len(urls_to_visit),
            'pages_scraped': len(visited_urls),
            'message': f'Found {total_images} images across {len(visited_urls)} pages. Starting downloads...'
        })
        
        if total_images == 0:
            scraping_status[task_id].update({
                'status': 'completed',
                'message': f'No images found across {len(visited_urls)} pages.'
            })
            return
        
        # Download images
        downloaded_count = 0
        
        for i, img_url in enumerate(all_image_urls):
            img_id = f"{i+1:04d}"
            
            scraping_status[task_id].update({
                'progress': int((i / total_images) * 100),
                'message': f'Downloading image {i+1} of {total_images}...'
            })
            
            filename = download_image(img_url, images_folder, img_id)
            
            if filename:
                downloaded_count += 1
                # Update CSV data with filename
                for item in csv_data:
                    if item['IMAGE_URL'] == img_url and not item['FILENAME']:
                        item['FILENAME'] = filename
                        break
            
            scraping_status[task_id]['downloaded'] = downloaded_count
        
        # Create CSV file
        csv_file_path = os.path.join(base_folder, 'image_data.csv')
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['PAGE_URL', 'IMAGE_ID', 'IMAGE_URL', 'FILENAME']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows([item for item in csv_data if item['FILENAME']])  # Only include successfully downloaded images
        
        # Create a summary file
        summary_file_path = os.path.join(base_folder, 'crawl_summary.txt')
        with open(summary_file_path, 'w', encoding='utf-8') as f:
            f.write(f"Website Crawl Summary\n")
            f.write(f"===================\n\n")
            f.write(f"Root URL: {url}\n")
            f.write(f"Crawl Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Pages Discovered: {len(visited_urls) + len(urls_to_visit)}\n")
            f.write(f"Pages Scraped: {len(visited_urls)}\n")
            f.write(f"Images Found: {total_images}\n")
            f.write(f"Images Downloaded: {downloaded_count}\n\n")
            f.write("Pages Visited:\n")
            for i, page_url in enumerate(sorted(visited_urls), 1):
                f.write(f"{i}. {page_url}\n")
        
        # Create ZIP file
        zip_file_path = f"{base_folder}.zip"
        with zipfile.ZipFile(zip_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add all files in base_folder to zip
            for root, dirs, files in os.walk(base_folder):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, base_folder)
                    zipf.write(file_path, arcname)
        
        scraping_status[task_id].update({
            'status': 'completed',
            'progress': 100,
            'message': f'Successfully crawled {len(visited_urls)} pages and downloaded {downloaded_count} images!',
            'zip_file': zip_file_path,
            'base_folder': base_folder
        })
        
    except Exception as e:
        scraping_status[task_id].update({
            'status': 'error',
            'message': f'Error: {str(e)}'
        })

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/scrape', methods=['POST'])
def start_scrape():
    data = request.get_json()
    url = data.get('url')
    
    if not url:
        return jsonify({'error': 'URL is required'}), 400
    
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Start scraping in background thread
    thread = threading.Thread(target=scrape_images, args=(url, task_id))
    thread.daemon = True
    thread.start()
    
    return jsonify({'task_id': task_id})

@app.route('/status/<task_id>')
def get_status(task_id):
    status = scraping_status.get(task_id, {'status': 'not_found'})
    return jsonify(status)

@app.route('/download/<task_id>')
def download_results(task_id):
    status = scraping_status.get(task_id)
    if not status or status['status'] != 'completed':
        return jsonify({'error': 'Results not ready'}), 404
    
    zip_file = status.get('zip_file')
    if not zip_file or not os.path.exists(zip_file):
        return jsonify({'error': 'Download file not found'}), 404
    
    return send_file(zip_file, as_attachment=True, download_name=f'scraped_images_{task_id[:8]}.zip')

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, host='0.0.0.0', port=port) 