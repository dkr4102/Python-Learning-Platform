"""
Artwork integration component.
Handles responsive rendering of the 12 oil painting masterworks from pip-learn-artworks.
"""
from nicegui import ui
from app.config import ARTWORK_MAPPING

def render_artwork(
    artwork_id: str,
    height_px: int = 340,
    show_caption: bool = False,
    overlay_content: callable = None,
    classes: str = ""
):
    """
    Render fine-art landscape oil painting integrated cleanly into the editorial UI.
    """
    info = ARTWORK_MAPPING.get(artwork_id)
    if not info:
        return

    filename = info["filename"]
    title = info["title"]
    img_url = f"/artworks/{filename}"

    with ui.element("div").classes(f"artwork-frame relative w-full overflow-hidden rounded-lg border border-[#E2DCD2] bg-[#EFEAE2] {classes}").style(f"height: {height_px}px; min-height: 200px;"):
        # The painting image with object-cover and crisp center alignment
        ui.image(img_url).props("fit=cover").classes("w-full h-full").style("height: 100%; width: 100%; object-fit: cover; object-position: center 50%;")

        if overlay_content:
            with ui.element("div").classes("absolute inset-0 bg-gradient-to-t from-black/75 via-black/25 to-transparent p-6 md:p-8 flex flex-col justify-end text-white"):
                overlay_content()
        elif show_caption:
            with ui.element("div").classes("absolute bottom-3 left-3 right-3 flex justify-between items-center pointer-events-none"):
                with ui.element("div").classes("artwork-plaque flex items-center justify-between w-full shadow-sm"):
                    ui.label(title).classes("font-serif text-sm font-medium tracking-wide text-[#FBF8F3]")
                    ui.label("Oil on Canvas").classes("text-[10px] text-white/60 font-sans hidden sm:block")


def render_artwork_thumbnail(
    artwork_id: str,
    width_px: int = 240,
    height_px: int = 160,
    classes: str = ""
):
    """
    Render compact artwork thumbnail for module cards without internal production badges.
    """
    info = ARTWORK_MAPPING.get(artwork_id)
    if not info:
        return

    filename = info["filename"]
    img_url = f"/artworks/{filename}"

    with ui.element("div").classes(f"relative overflow-hidden rounded-md border border-[#E2DCD2] bg-[#EFEAE2] flex-shrink-0 {classes}").style(f"width: {width_px}px; height: {height_px}px;"):
        ui.image(img_url).props("fit=cover").classes("w-full h-full").style("height: 100%; width: 100%; object-fit: cover; object-position: center;")
