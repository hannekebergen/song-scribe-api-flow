SUNO.AI.API DOCUMENTATION

GENERATE MUSIC:
Generate music with or without lyrics using Suno's AI models.

Parameter Usage Guide
When customMode is true (Custom Mode):

If instrumental is true: style and title are required
If instrumental is false: style, prompt, and title are required
Prompt length limit:
For V3_5 and V4 models: 3000 characters
For V4_5 model: 5000 characters
Style length limit:
For V3_5 and V4 models: 200 characters
For V4_5 model: 1000 characters
title length limit: 80 characters
When customMode is false (Non-custom Mode):

Only prompt is required regardless of instrumental setting
prompt length limit: 400 characters
Other parameters should be left empty
Developer Notes
Recommendation for First-Time Users: Start with customMode: false and instrumental: false, and only provide a prompt. This is the simplest setup to quickly test the API and experience the results.
Generated files are retained for 15 days before being deleted
Ensure all required fields are provided based on the customMode and instrumental settings to avoid errors
Respect the character limits for prompt, style, and title to ensure successful processing
Callback process has three stages: text (text generation), first (first track complete), complete (all tracks complete)
You can use the Get Music Generation Details endpoint to actively check task status instead of waiting for callbacks
Request
application/json
Bodyrequired
prompt
string
A description of the desired audio content.

In Custom Mode (customMode: true): Required if instrumental is false. The prompt will be strictly used as the lyrics and sung in the generated track. Character limits by model:
V3_5 & V4: Maximum 3000 characters
V4_5: Maximum 5000 characters
Example: "A calm and relaxing piano track with soft melodies"
In Non-custom Mode (customMode: false): Always required. The prompt serves as the core idea, and lyrics will be automatically generated based on it (not strictly matching the input). Maximum 400 characters.
Example: "A short relaxing piano tune"
Example: A calm and relaxing piano track with soft melodies
style
string
The music style or genre for the audio.

Required in Custom Mode (customMode: true). Examples: "Jazz", "Classical", "Electronic".
For V3_5 and V4 models: Max length: 200 characters.
For V4_5 model: Max length: 1000 characters.
Example: "Classical"
In Non-custom Mode (customMode: false): Leave empty.
Example: Classical
title
string
The title of the generated music track.

Required in Custom Mode (customMode: true). Max length: 80 characters.
Example: "Peaceful Piano Meditation"
In Non-custom Mode (customMode: false): Leave empty.
Example: Peaceful Piano Meditation
customMode
boolean
required
Enables Custom Mode for advanced audio generation settings.

Set to true to use Custom Mode (requires style and title; prompt required if instrumental is false). The prompt will be strictly used as lyrics if instrumental is false.
Set to false for Non-custom Mode (only prompt is required). Lyrics will be auto-generated based on the prompt.
Example: true
instrumental
boolean
required
Determines if the audio should be instrumental (no lyrics).

In Custom Mode (customMode: true):
If true: Only style and title are required.
If false: style, title, and prompt are required (with prompt used as the exact lyrics).
In Non-custom Mode (customMode: false): No impact on required fields (prompt only). Lyrics are auto-generated if instrumental is false.
Example: true
model
string
required
The model version to use for audio generation.

Available options:
V4_5: Superior genre blending with smarter prompts and faster output, up to 8 minutes.
V4: Best audio quality with refined song structure, up to 4 minutes.
V3_5: Solid arrangements with creative diversity, up to 4 minutes.
Possible values: [V3_5, V4, V4_5]

Example: V3_5
negativeTags
string
Music styles or traits to exclude from the generated audio.

Optional. Use to avoid specific styles.
Example: "Heavy Metal, Upbeat Drums"
Example: Heavy Metal, Upbeat Drums
callBackUrl
uri
required
The URL to receive task completion notifications when music extension is complete.

Example: https://api.example.com/callback
Responses
200
500
Request successful

application/json
Schema
Example (auto)
Schema
code
integer
Status Codes
✅ 200 - Request successful
⚠️ 400 - Invalid parameters
⚠️ 401 - Unauthorized access
⚠️ 404 - Invalid request method or path
⚠️ 405 - Rate limit exceeded
⚠️ 413 - Theme or prompt too long
⚠️ 429 - Insufficient credits
⚠️ 455 - System maintenance
❌ 500 - Server error
Possible values: [200, 400, 401, 404, 405, 413, 429, 455, 500]

Example: 200
msg
string
Error message when code != 200

Example: success
data
object
Callbacks
POST audioGenerated
POST
{request.body#/callBackUrl}
System will call this callback when audio generation is complete.

Callback Example
{
  "code": 200,
  "msg": "All generated successfully.",
  "data": {
    "callbackType": "complete",
    "task_id": "2fac****9f72",
    "data": [
      {
        "id": "8551****662c",
        "audio_url": "https://example.cn/****.mp3",
        "source_audio_url": "https://example.cn/****.mp3",
        "stream_audio_url": "https://example.cn/****",
        "source_stream_audio_url": "https://example.cn/****",
        "image_url": "https://example.cn/****.jpeg",
        "source_image_url": "https://example.cn/****.jpeg",
        "prompt": "[Verse] Night city lights shining bright",
        "model_name": "chirp-v3-5",
        "title": "Iron Man",
        "tags": "electrifying, rock",
        "createTime": "2025-01-01 00:00:00",
        "duration": 198.44
      },
      {
        "id": "bd15****1873",
        "audio_url": "https://example.cn/****.mp3",
        "source_audio_url": "https://example.cn/****.mp3",
        "stream_audio_url": "https://example.cn/****",
        "source_stream_audio_url": "https://example.cn/****",
        "image_url": "https://example.cn/****.jpeg",
        "source_image_url": "https://example.cn/****.jpeg",
        "prompt": "[Verse] Night city lights shining bright",
        "model_name": "chirp-v3-5",
        "title": "Iron Man",
        "tags": "electrifying, rock",
        "createTime": "2025-01-01 00:00:00",
        "duration": 228.28
      }
    ]
  }
}

application/json
Body
code
integer
Status code

Example: 200
msg
string
Response message

Example: All generated successfully

EXTEND MUSIC:
Extend or modify existing music tracks.

Parameter Usage Guide
When defaultParamFlag is true (Custom Parameters):

prompt, style, title and continueAt are required
prompt length limit: 3000 characters
style length limit: 200 characters
title length limit: 80 characters
When defaultParamFlag is false (Use Default Parameters):

Only audioId is required
Other parameters will use the original audio's parameters
Developer Notes
Generated files are retained for 15 days
Model version must be consistent with the source music
This feature is ideal for creating longer compositions by extending existing tracks
Request
application/json
Bodyrequired
defaultParamFlag
boolean
required
Controls parameter usage mode.

true: Use custom parameters (requires continueAt, prompt, style, and title).
false: Use original audio parameters (only audioId is required).
Example: true
audioId
string
required
Audio ID of the track to extend. This is the source track that will be continued.

Example: 5c79****be8e
prompt
string
Description of how the music should be extended. Required when defaultParamFlag is true.

Example: Extend the music with more relaxing notes
style
string
Music style, e.g., Jazz, Classical, Electronic

Example: Classical
title
string
Music title

Example: Peaceful Piano Extended
continueAt
number
The time point (in seconds) from which to start extending the music.

Required when defaultParamFlag is true.
Value range: greater than 0 and less than the total duration of the generated audio.
Specifies the position in the original track where the extension should begin.
Example: 60
model
string
required
Model version to use, must be consistent with the source audio.

Available options:
V4_5: Superior genre blending with smarter prompts and faster output, up to 8 minutes.
V4: Best audio quality with refined song structure, up to 4 minutes.
V3_5: Solid arrangements with creative diversity, up to 4 minutes.
Possible values: [V3_5, V4, V4_5]

Example: V3_5
negativeTags
string
Music styles to exclude from generation

Example: Relaxing Piano
callBackUrl
uri
required
The URL to receive task completion notifications when music extension is complete.

Example: https://api.example.com/callback
Responses
200
500
Request successful

application/json
Schema
Example (auto)
Schema
code
integer
Status Codes
✅ 200 - Request successful
⚠️ 400 - Invalid parameters
⚠️ 401 - Unauthorized access
⚠️ 404 - Invalid request method or path
⚠️ 405 - Rate limit exceeded
⚠️ 413 - Theme or prompt too long
⚠️ 429 - Insufficient credits
⚠️ 455 - System maintenance
❌ 500 - Server error
Possible values: [200, 400, 401, 404, 405, 413, 429, 455, 500]

Example: 200
msg
string
Error message when code != 200

Example: success
data
object
Callbacks
POST audioExtend
POST
{$request.body#/callBackUrl}
System will call this callback when audio generation is complete.

Callback Example
{
  "code": 200,
  "msg": "All generated successfully.",
  "data": {
    "callbackType": "complete",
    "task_id": "2fac****9f72",
    "data": [
      {
        "id": "8551****662c",
        "audio_url": "https://example.cn/****.mp3",
        "source_audio_url": "https://example.cn/****.mp3",
        "stream_audio_url": "https://example.cn/****",
        "source_stream_audio_url": "https://example.cn/****",
        "image_url": "https://example.cn/****.jpeg",
        "source_image_url": "https://example.cn/****.jpeg",
        "prompt": "[Verse] Night city lights shining bright",
        "model_name": "chirp-v3-5",
        "title": "Iron Man",
        "tags": "electrifying, rock",
        "createTime": "2025-01-01 00:00:00",
        "duration": 198.44
      }
    ]
  }
}

application/json
Body
code
integer
Status code

Example: 200
msg
string
Response message

Example: All generated successfully
data
object

GET MUSIC GENERATION DETAILS:
Get Music Generation Details
GET
https://api.sunoapi.org/api/v1/generate/record-info
Retrieve detailed information about a music generation task, including status, parameters, and results.

Status Descriptions
PENDING: Task is waiting to be processed
TEXT_SUCCESS: Lyrics/text generation completed successfully
FIRST_SUCCESS: First track generation completed successfully
SUCCESS: All tracks generated successfully
CREATE_TASK_FAILED: Failed to create the generation task
GENERATE_AUDIO_FAILED: Failed to generate music tracks
CALLBACK_EXCEPTION: Error occurred during callback
SENSITIVE_WORD_ERROR: Content contains prohibited words
Developer Notes
For instrumental tracks (instrumental=true), no lyrics data will be included in the response
Use this endpoint to check task status instead of waiting for callbacks
Request
Query Parameters
taskId
string
required
The task ID returned from the Generate Music or Extend Music endpoints. Used to identify the specific generation task to query.

Example: 5c79****be8e
Responses
200
500
Request successful

application/json
Schema
Example (auto)
Example
Schema
code
integer
Status Codes
✅ 200 - Request successful
⚠️ 400 - Invalid parameters
⚠️ 401 - Unauthorized access
⚠️ 404 - Invalid request method or path
⚠️ 405 - Rate limit exceeded
⚠️ 413 - Theme or prompt too long
⚠️ 429 - Insufficient credits
⚠️ 455 - System maintenance
❌ 500 - Server error
Possible values: [200, 400, 401, 404, 405, 413, 429, 455, 500]

Example: 200
msg
string
Error message when code != 200

Example: success