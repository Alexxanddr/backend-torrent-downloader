import py1337x
from flask import Flask, request, jsonify
from flask_cors import CORS
import asyncio
from torrentp import TorrentDownloader
import os
import re
import asyncio
import concurrent.futures


torrents = py1337x.Py1337x()

app = Flask(__name__)
CORS(app)

def download_in_background(magnet_link, download_path):
    torrent_file = TorrentDownloader(magnet_link, download_path)
    asyncio.run(torrent_file.start_download())

@app.route("/search_torrent", methods=["POST"])
def search_torrent():
    data = request.get_json()
    query = data.get("query", "").lower()
    page = data.get("page", 1)
    print(data.get("page"))
    results = torrents.search(query, page=page, sort_by=py1337x.sort.SEEDERS)

    res = []
    for result in results.items:
        torrent = torrents.info(torrent_id=result.torrent_id)
        info_dict = torrent.to_dict()
        res.append(info_dict)

    return jsonify({
        "movies": res,
        "current_page": results.current_page,  
        "total_pages": results.page_count     
    })

@app.route("/download_torrent", methods=["POST"])
def download_torrent():
    data = request.json
    magnet_link = data.get("magnet_link")
    category = data.get("category")  # "Film", "TV-Series", "Other"
    short_name = data.get('short_name', '').strip()  # Aggiungi un default vuoto e rimuovi gli spazi

    if not short_name:
        match = re.search(r'dn=([^&]+)', magnet_link)
        if not match:
            return jsonify({"message": "Invalid magnet link format"}), 400
        folder_name = match.group(1)
    else:
        folder_name = short_name

    if not magnet_link or not category:
        return jsonify({"message": "Missing required parameters"}), 400

    # Mappatura delle categorie a percorsi specifici
    category_paths = {
        "Film": "/Film/",
        "TV-Series": "/Serie/",
        "Other": "/Other/"
    }
    # category_paths = {
    #     "Film": "Film/",
    #     "TV-Series": "Serie/",
    #     "Other": "Other/"
    # }

    # Percorso per la categoria scelta
    category_path = category_paths.get(category)

    download_path = os.path.join(category_path, folder_name)

    # Creazione della cartella se non esiste
    os.makedirs(download_path, exist_ok=True)
    print(f"Downloading {category} with magnet link: {magnet_link} to {download_path}")
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(download_in_background, magnet_link, download_path)

    return jsonify({"message": f"{category} download started successfully!"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8080")