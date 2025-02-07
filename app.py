import os
import streamlit as st
import subprocess
import tempfile

st.title("YouTube to MP3 Converter (yt-dlp)")

st.write("Enter a YouTube URL below to convert its audio to an MP3 file.")

# Input for the YouTube URL
url = st.text_input("YouTube URL:")

if st.button("Convert"):
    if not url.strip():
        st.warning("Please enter a valid YouTube URL.")
    else:
        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                st.info("Downloading and converting...")

                # Set up the output template: this will create a file with the video title as its name.
                output_template = os.path.join(tmpdir, '%(title)s.%(ext)s')

                # Build the yt-dlp command:
                command = [
                    'yt-dlp',
                    '--extract-audio',
                    '--audio-format', 'mp3',
                    '--output', output_template,
                    url
                ]

                # Run the command using subprocess
                result = subprocess.run(command, capture_output=True, text=True)

                if result.returncode != 0:
                    st.error(f"yt-dlp error: {result.stderr}")
                else:
                    # Find the resulting mp3 file in the temporary directory
                    mp3_files = [f for f in os.listdir(tmpdir) if f.endswith('.mp3')]
                    if not mp3_files:
                        st.error("Could not locate the converted MP3 file.")
                    else:
                        mp3_file_path = os.path.join(tmpdir, mp3_files[0])
                        st.success("Conversion successful!")
                        with open(mp3_file_path, 'rb') as mp3_file:
                            st.download_button(
                                label="Download MP3",
                                data=mp3_file,
                                file_name=mp3_files[0],
                                mime="audio/mpeg"
                            )
        except Exception as e:
            st.error(f"An error occurred: {e}")
