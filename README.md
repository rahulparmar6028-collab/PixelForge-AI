# PixelForge AI

A sleek, decentralized AI image generator built with **Streamlit** and powered by the **AI Horde** community GPU cluster.

## Features

- 🎨 **Neural Vision Prompts**: Describe what you want to generate in natural language
- 🎭 **Multiple Art Styles**: Cinematic, Anime, 3D Render, Cyberpunk, Fantasy, Oil Paint, Vaporwave, Sketch, Steampunk
- 📐 **Custom Canvas Ratios**: Generate images in 1:1, 16:9, or 9:16 aspect ratios
- 🔧 **Advanced Controls**: Adjust neural intensity (CFG scale) from 1.0 to 20.0
- 🎬 **Variant Generation**: Re-forge images with the same settings for variation
- 💾 **Export Support**: Download generated images as PNG
- 🌓 **Dark/Light Mode**: Toggle between theme preferences
- 📊 **System Console**: Real-time logs of generation status and queue times

## Prerequisites

- Python 3.8+
- Active AI Horde account (free)

## Setup

### 1. Get an AI Horde API Key

1. Visit [https://aihorde.net/](https://aihorde.net/)
2. Sign up for a free account (or use an existing one)
3. Navigate to your account settings
4. Copy your API key

### 2. Clone & Install

```bash
# Clone the repository
git clone <your_repo_url>
cd PixelForge

# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Key

There are two ways to set your API key:

#### Option A: Using `.env` file (Recommended)

1. Copy the example file:
   ```bash
   cp .env.example .env
   ```

2. Open `.env` and replace `your_api_key_here` with your actual API key:
   ```
   HORDE_API_KEY=your_actual_api_key_here
   ```

3. Save and close the file (`.env` is git-ignored)

#### Option B: Using Environment Variable

Alternatively, set the environment variable directly:

**Windows (PowerShell):**
```powershell
$env:HORDE_API_KEY = "your_api_key_here"
streamlit run app.py
```

**macOS/Linux:**
```bash
export HORDE_API_KEY="your_api_key_here"
streamlit run app.py
```

## Running the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Enter a Prompt**: Describe the image you want to generate
2. **Add Negative Directives** (optional): Specify what to exclude
3. **Select Canvas Ratio**: Choose the image dimensions
4. **Pick a Neural Theme**: Apply an art style filter
5. **Adjust Intensity**: Control how strictly the AI follows your prompt (CFG scale)
6. **Execute Forge**: Click to submit the generation request
7. **Wait**: The app polls the AI Horde cluster for your generation
8. **Export**: Download the generated image or generate variants

## Example Prompts

- "A futuristic city with neon lights at night, cyberpunk aesthetic"
- "A serene landscape with mountains, forests, and a lake, oil painting style"
- "A cute anime girl with long blue hair, magical sparkles around her"
- "A steampunk airship with gears and brass, intricate details"

## Troubleshooting

### "CRITICAL: HORDE_API_KEY not found"

**Solution**: Ensure you have:
1. Created a `.env` file in the project root
2. Added `HORDE_API_KEY=your_key` to the file
3. Saved the file
4. Restarted the Streamlit app

### Generation takes too long

- AI Horde is a decentralized, community-powered service
- During peak hours, queue times may be longer
- Check the System Console at the bottom of the app for queue status

### "Image retrieval failed" or Network errors

- Verify your internet connection
- Check if AI Horde is online: https://aihorde.net/status
- Ensure your API key is valid
- Try again in a few moments

### My generated images look low quality

- Try adjusting the **Neural Intensity** slider (higher = stricter adherence to prompt)
- Refine your prompt with more descriptive keywords
- Try a different art style
- Increase the prompt length for more detail

## Architecture

- **Frontend**: Streamlit (Python web framework)
- **Backend**: AI Horde API (decentralized GPU cluster)
- **Image Processing**: Pillow
- **HTTP Requests**: Requests library

### Key Files

- `app.py`: Main Streamlit application with UI and logic
- `requirements.txt`: Python dependencies
- `.env.example`: Template for environment variables
- `.gitignore`: Git configuration to ignore sensitive files

## Advanced Features (Future)

- Session history and thumbnails
- Batch generation presets
- Custom seed control
- Multiple sampler options
- Export with metadata

## Legal & Attribution

- **AI Horde**: https://aihorde.net/
- Generated images are produced by the AI Horde cluster
- Respect copyright and content policies when generating images
- AI Horde reserves the right to refuse service for inappropriate use

## License

This project is provided as-is for educational and personal use.

## Support

For issues with:
- **PixelForge App**: Check the troubleshooting section above or open an issue on GitHub
- **AI Horde Service**: Visit https://aihorde.net/ or join their Discord community

---

**Happy Forging!** 🎨✨
