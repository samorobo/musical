from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS module
import replicate
import os
import logging
from dotenv import load_dotenv  # Import load_dotenv

# Load environment variables from the .env file
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/api/playlist/<genre>', methods=['GET'])
def get_playlist(genre):
    # Ensure the Replicate API token is set
    replicate_api_token = os.getenv("REPLICATE_API_TOKEN")
    if not replicate_api_token:
        return jsonify({'error': 'Replicate API token is not set'}), 500

    try:
        os.environ["REPLICATE_API_TOKEN"] = replicate_api_token

        # Initialize model with more specific prompt
        output = replicate.run(
            "meta/meta-llama-3.1-405b-instruct",
            input={
                "prompt": f"""Generate a playlist of 5 {genre} songs in exactly this format:
                Artist Name - Song Title
                Artist Name - Song Title
                Artist Name - Song Title
                Artist Name - Song Title
                Artist Name - Song Title""",
                "max_length": 200,
                "temperature": 0.7,
                "num_return_sequences": 1
            }
        )

        # Convert iterator to list and concatenate tokens
        tokens = list(output)
        full_text = ''.join(tokens)
        logger.info(f"Raw output from model: {full_text}")

        if not full_text:
            logger.error("Empty response from model")
            return jsonify({'error': 'Empty response from model'}), 500

        # Split response into lines and filter empty lines
        songs = [line.strip() for line in full_text.split('\n') if line.strip()]
        logger.info(f"Parsed songs before filtering: {songs}")

        # Parse songs with more detailed error handling
        playlist = []
        for song in songs:
            try:
                if ' - ' in song:
                    # Remove any markdown formatting if present
                    song = song.replace('*', '').strip()
                    # Remove numbered lists if present
                    if '. ' in song:
                        song = song.split('. ', 1)[1]
                    
                    artist, title = song.split(' - ', 1)
                    playlist.append({
                        'artist': artist.strip(),
                        'title': title.strip()
                    })
            except Exception as e:
                logger.error(f"Error parsing song '{song}': {e}")

        if not playlist:
            logger.error("No valid songs found in response")
            return jsonify({'error': 'No valid songs found in response'}), 500

        logger.info(f"Final playlist: {playlist}")
        return jsonify({'playlist': playlist})

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': f'An unexpected error occurred: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(debug=True)