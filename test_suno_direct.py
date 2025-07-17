import requests
import json
import time

# SUNO API Configuration
SUNO_API_KEY = "4434867ce3286ce2635056e2b67eef0b"
BASE_URL = "https://api.sunoapi.org/api/v1"

headers = {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
    'Authorization': f'Bearer {SUNO_API_KEY}'
}

def test_suno_generate():
    """Test SUNO music generation"""
    print("🎵 Testing SUNO API Generation...")
    
    payload = {
        "prompt": "A calm and relaxing piano track with soft melodies",
        "style": "Classical",
        "title": "Peaceful Piano Meditation",
        "customMode": True,
        "instrumental": True,
        "model": "V3_5",
        "negativeTags": "Heavy Metal, Upbeat Drums",
        "callBackUrl": "https://api.example.com/callback"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/generate", headers=headers, json=payload)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            task_id = data.get('data', {}).get('taskId')
            print(f"✅ Task ID: {task_id}")
            return task_id
        else:
            print(f"❌ Error: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def check_task_status(task_id):
    """Check the status of a SUNO task using the correct endpoint"""
    print(f"\n🔍 Checking status for task: {task_id}")
    
    # Use the correct endpoint from the documentation
    endpoint = f"{BASE_URL}/generate/record-info?taskId={task_id}"
    
    try:
        response = requests.get(endpoint, headers=headers)
        print(f"Endpoint: {endpoint}")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Success! Data: {json.dumps(data, indent=2)}")
            
            # Check the status
            status = data.get('data', {}).get('status')
            if status:
                print(f"📊 Task Status: {status}")
                
                # Status descriptions
                status_descriptions = {
                    'PENDING': 'Task is waiting to be processed',
                    'TEXT_SUCCESS': 'Lyrics/text generation completed successfully',
                    'FIRST_SUCCESS': 'First track generation completed successfully',
                    'SUCCESS': 'All tracks generated successfully',
                    'CREATE_TASK_FAILED': 'Failed to create the generation task',
                    'GENERATE_AUDIO_FAILED': 'Failed to generate music tracks',
                    'CALLBACK_EXCEPTION': 'Error occurred during callback',
                    'SENSITIVE_WORD_ERROR': 'Content contains prohibited words'
                }
                
                if status in status_descriptions:
                    print(f"📝 Status Description: {status_descriptions[status]}")
                
                # Check if we have results
                if status == 'SUCCESS':
                    results = data.get('data', {}).get('data', [])
                    if results:
                        print(f"🎵 Generated {len(results)} track(s):")
                        for i, track in enumerate(results, 1):
                            print(f"  Track {i}:")
                            print(f"    Title: {track.get('title', 'N/A')}")
                            print(f"    Duration: {track.get('duration', 'N/A')} seconds")
                            print(f"    Audio URL: {track.get('audio_url', 'N/A')}")
                            print(f"    Image URL: {track.get('image_url', 'N/A')}")
            
            return data
        else:
            print(f"❌ Error: {response.status_code}")
            return None
                
    except Exception as e:
        print(f"❌ Exception: {e}")
        return None

def main():
    print("🚀 SUNO API Direct Test")
    print("=" * 50)
    
    # Test generation
    task_id = test_suno_generate()
    
    if task_id:
        print(f"\n⏳ Waiting 10 seconds before checking status...")
        time.sleep(10)
        
        # Check status multiple times
        max_attempts = 5
        for attempt in range(max_attempts):
            print(f"\n🔄 Attempt {attempt + 1}/{max_attempts}")
            status = check_task_status(task_id)
            
            if status:
                task_status = status.get('data', {}).get('status')
                if task_status == 'SUCCESS':
                    print(f"\n🎉 Task completed successfully!")
                    break
                elif task_status in ['CREATE_TASK_FAILED', 'GENERATE_AUDIO_FAILED', 'CALLBACK_EXCEPTION', 'SENSITIVE_WORD_ERROR']:
                    print(f"\n❌ Task failed with status: {task_status}")
                    break
                else:
                    print(f"\n⏳ Task still processing... Status: {task_status}")
                    if attempt < max_attempts - 1:
                        print(f"⏳ Waiting 30 seconds before next check...")
                        time.sleep(30)
            else:
                print(f"\n❌ Failed to get status")
                if attempt < max_attempts - 1:
                    print(f"⏳ Waiting 30 seconds before next check...")
                    time.sleep(30)
    else:
        print(f"\n❌ Failed to create task")

if __name__ == "__main__":
    main() 