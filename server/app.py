from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from groq import Groq
from dotenv import load_dotenv
import json
import re
 
  
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend communication


GROQ_API_KEY = os.getenv('GROQ_API_KEY')

client = Groq(api_key=GROQ_API_KEY)

def parse_playlist_response(response_text):
    """
    Parse the AI response and extract song information
    Returns a list of dictionaries with song and artist
    """
    playlist = []
    
    # Try to find JSON in the response
    try:
        # Look for JSON array or object in the response
        json_match = re.search(r'\[.*\]', response_text, re.DOTALL)
        if json_match:
            playlist_data = json.loads(json_match.group())
            return playlist_data
    except json.JSONDecodeError:
        pass
    
    # Fallback: Parse line by line
    lines = response_text.strip().split('\n')
    for line in lines:
        line = line.strip()
        if not line or line.startswith('#'):
            continue
            
        # Remove numbering (1., 2., etc.)
        line = re.sub(r'^\d+[\.\)]\s*', '', line)
        
        # Try to split by common delimiters
        if ' - ' in line:
            parts = line.split(' - ', 1)
            if len(parts) == 2:
                playlist.append({
                    'song': parts[0].strip().strip('"\''),
                    'artist': parts[1].strip().strip('"\'')
                })
        elif ' by ' in line.lower():
            parts = re.split(r'\s+by\s+', line, 1, re.IGNORECASE)
            if len(parts) == 2:
                playlist.append({
                    'song': parts[0].strip().strip('"\''),
                    'artist': parts[1].strip().strip('"\'')
                })
    
    return playlist

@app.route('/api/generate-playlist', methods=['POST'])
def generate_playlist():
    """
    Generate a playlist based on the selected genre
    Expected JSON: {"genre": "Pop"}
    Returns: {"playlist": [{"song": "Song Name", "artist": "Artist Name"}, ...]}
    """
    try:
        # Get genre from request
        data = request.get_json()
        
        if not data or 'genre' not in data:
            return jsonify({
                'error': 'Genre is required',
                'message': 'Please provide a genre in the request body'
            }), 400
        
        genre = data['genre']
        
        # Validate genre (optional)
        if not genre or len(genre.strip()) == 0:
            return jsonify({
                'error': 'Invalid genre',
                'message': 'Genre cannot be empty'
            }), 400
        
        # Create prompt for AI
        prompt = f"""Generate a playlist of exactly 5 {genre} songs. 
        
For each song, provide the song title and artist name.

Return ONLY a JSON array in this exact format with no additional text:
[
  {{"song": "Song Title 1", "artist": "Artist Name 1"}},
  {{"song": "Song Title 2", "artist": "Artist Name 2"}},
  {{"song": "Song Title 3", "artist": "Artist Name 3"}},
  {{"song": "Song Title 4", "artist": "Artist Name 4"}},
  {{"song": "Song Title 5", "artist": "Artist Name 5"}}
]

Choose popular and well-known {genre} songs."""

        # Call Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a music expert that provides song recommendations. Always return responses in valid JSON format."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama-3.3-70b-versatile",  # Current production model (Dec 2024)
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract response
        ai_response = chat_completion.choices[0].message.content
        
        # Parse the response
        playlist = parse_playlist_response(ai_response)
        
        # Validate we got 5 songs
        if len(playlist) < 5:
            return jsonify({
                'error': 'Incomplete playlist',
                'message': f'Only generated {len(playlist)} songs. Please try again.',
                'playlist': playlist
            }), 500
        
        # Return only first 5 songs if more were generated
        playlist = playlist[:5]
        
        return jsonify({
            'genre': genre,
            'playlist': playlist,
            'message': f'Successfully generated {len(playlist)} {genre} songs'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Internal server error',
            'message': str(e)
        }), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'Music Playlist Generator API is running'
    }), 200

@app.route('/', methods=['GET'])
def home():
    """Root endpoint with API information"""
    return jsonify({
        'message': 'Music Playlist Generator API',
        'endpoints': {
            '/api/generate-playlist': 'POST - Generate a playlist (requires JSON body with "genre" field)',
            '/api/health': 'GET - Health check'
        },
        'example_request': {
            'method': 'POST',
            'url': '/api/generate-playlist',
            'body': {'genre': 'Pop'}
        }
    }), 200

if __name__ == '__main__':
    # Run the Flask app
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)