import os
import mimetypes
from swe_tools.instance import mcp
from pydantic import BaseModel
from typing import List

class ImageViewerResult(BaseModel):
    path: str
    mime_type: str = None
    error: str = None

@mcp.tool(name="view_images", description="Reads one or more image files from the specified paths and provides them to the AI for multimodal analysis. Use this to allow the AI to see screenshots, diagrams, or other visual information. Input is a comma-separated list of paths.")
def view_images(paths: str) -> List[ImageViewerResult]:
    """
    Validates that paths point to valid image files and returns structured data
    for the client to process.

    Args:
        paths: A comma-separated string of paths to image files.

    Returns:
        A list of ImageViewerResult objects.
    """
    path_list = [p.strip() for p in paths.split(',')]
    results = []
    for path in path_list:
        if not os.path.exists(path):
            results.append(ImageViewerResult(path=path, error="File not found."))
        elif not os.path.isfile(path):
            results.append(ImageViewerResult(path=path, error="Path is a directory."))
        else:
            mime_type, _ = mimetypes.guess_type(path)
            if mime_type and mime_type.startswith('image/'):
                results.append(ImageViewerResult(path=path, mime_type=mime_type))
            else:
                results.append(ImageViewerResult(path=path, error=f"Not a recognized image type ({mime_type})."))
    return results
