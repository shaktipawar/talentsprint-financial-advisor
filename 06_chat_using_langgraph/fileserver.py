from flask import Flask, send_from_directory

app = Flask(__name__)

#Serve static files from the assets folder.
@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('assets',filename)

if __name__ == "__main__":
    app.run(port = 5000, debug=True)