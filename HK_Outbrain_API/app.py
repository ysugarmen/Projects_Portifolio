from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import os
from werkzeug.utils import secure_filename
from main import main  # Import your existing script functions
import logging

app = Flask(__name__)
app.secret_key = "your_secret_key"
app.config['UPLOAD_FOLDER'] = 'uploads'
LOG_FOLDER = 'logs'


# Ensure the uploads and logs directories exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(LOG_FOLDER, exist_ok=True)
# Setup logging
log_file = os.path.join(LOG_FOLDER, 'api_logs.log')
logging.basicConfig(filename=log_file, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        campaigns_file = request.files.get('campaigns_file')
        promoted_links_file = request.files.get('promoted_links_file')

        if not campaigns_file or not promoted_links_file:
            flash("Please upload both CampaignsData and PromotedLinksData files.", "danger")
            return redirect(url_for('index'))

        # Save files
        campaigns_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(campaigns_file.filename))
        promoted_links_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(promoted_links_file.filename))
        campaigns_file.save(campaigns_path)
        promoted_links_file.save(promoted_links_path)

        try:
            logs = main(campaigns_path, promoted_links_path, logger)  # Pass logger and get filtered logs
            flash("Campaigns and promoted links created successfully!", "success")
            return render_template('index.html', logs=logs)
        except Exception as e:
            flash(f"An error occurred: {str(e)}", "danger")
            return render_template('index.html', logs=[])

    return render_template('index.html', logs=[])


if __name__ == '__main__':
    app.run(debug=True)
