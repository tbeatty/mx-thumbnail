# mx-thumbnail

This project uses ImageMagick to generate pdf thumbnails.

### Configuration

Function output is configured in the `config.json` file.

### Deployment

```bash
gcloud functions deploy pdf-thumbnail \
  --runtime python37 \
  --memory 2048MB \
  --trigger-bucket gs://mx-docs \
  --entry-point handle_message
```

### View Log Output

```bash
gcloud functions logs read pdf-thumbnail
```

### Testing

The current version of the `wand` Python library requires ImageMagick 6.

To install ImageMagick 6 on OSX:

```bash
brew install imagemagick@6
```

Define `MAGICK_HOME` in your shell profile (e.g., `.bashrc`, `.zshrc`) or in your launch profile if using an IDE.

```bash
export MAGICK_HOME=/usr/local/opt/imagemagick@6
```
