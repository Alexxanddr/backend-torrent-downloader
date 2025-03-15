import py1337x
from flask import Flask, request, jsonify
from flask_cors import CORS

torrents = py1337x.Py1337x()

app = Flask(__name__)
CORS(app)

@app.route("/search_torrent", methods=["POST"])
def search_anime():
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
def download_anime():
    data = request.json
    magnet_link = data.get("magnet_link")
    category = data.get("category")  # Will be "Film", "TV-Series", or "Other"
    
    if not magnet_link or not category:
        return jsonify({"message": "Missing required parameters"}), 400

    # Add your category handling logic here
    print(f"Downloading {category} with magnet link: {magnet_link}")
    
    # Rest of your download logic
    #torrent_file = TorrentDownloader(magnet_link, '.')
    #asyncio.run(torrent_file.start_download())
    
    return jsonify({"message": f"{category} download started successfully!"}), 200

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port="8081")