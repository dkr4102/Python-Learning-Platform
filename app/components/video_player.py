"""
Pip Learn 2.0 - Reusable Shared Video Player Component
Fixed 16:9 geometry, zero-layout-shift layer swap, YouTube-inspired compact play overlay.
"""
from html import escape
from typing import Callable, Optional
from nicegui import ui
from app.curriculum.videos import LessonVideo


def render_video_player(
    video_info: Optional[LessonVideo],
    saved_video_status: str = "not_started",
    on_playback_started: Optional[Callable[[], None]] = None,
    on_status_change: Optional[Callable[[str], None]] = None,
) -> dict:
    """
    Renders a strictly layout-stable 16:9 video player with a compact YouTube-inspired
    Play overlay that swaps in-place for the native YouTube iframe on click.

    Returns dict with references to container and controllers.
    """
    video_container = ui.element("div").classes("video-frame-container")

    with video_container:
        if video_info:
            # 1. Poster Layer with Compact 68x48 YouTube-Style Play Overlay
            poster_layer = ui.element("div").classes("video-poster-layer")
            poster_layer.props('tabindex="0" role="button" aria-label="Play video tutorial" @keydown.enter="$el.click()" @keydown.space.prevent="$el.click()"')

            with poster_layer:
                # Video Poster Image (100% cover, fixed 16:9, no dimming)
                ui.html(
                    f'<img src="https://i.ytimg.com/vi/{video_info.video_id}/hqdefault.jpg" '
                    f'alt="{escape(video_info.title)}" class="video-poster-img" />',
                    sanitize=False,
                )

                # Compact YouTube-style Play Overlay (68x48px, rounded rect, centered white triangle)
                ui.html(
                    '<button type="button" class="video-play-btn" aria-label="Play video" tabindex="-1">'
                    '<svg width="22" height="22" viewBox="0 0 24 24" fill="#FFFFFF" style="margin-left: 2px;">'
                    '<path d="M8 5v14l11-7z"/>'
                    '</svg>'
                    '</button>',
                    sanitize=False,
                )

            # 2. Player Layer (Houses the genuine YouTube iframe upon activation)
            player_layer = ui.element("div").classes("video-player-layer hidden")

            # 3. Error Fallback Layer (Revealed if YouTube emits embed playback error)
            error_layer = ui.element("div").classes("video-error-layer hidden").props('id="video-error-banner"')
            with error_layer:
                with ui.column().classes("video-error-content items-center text-center p-6 gap-3"):
                    ui.icon("error_outline", size="2.5rem", color="amber-7")
                    ui.label("Playback unavailable in embedded frame").classes("text-sm font-semibold text-stone-200")
                    ui.label(
                        "This video may have embed restrictions enabled by YouTube or your network. "
                        "You can watch it directly on YouTube without losing your lesson progress."
                    ).classes("text-xs text-stone-300 max-w-sm leading-relaxed")
                    ui.link(
                        "Open on YouTube ↗",
                        f"https://www.youtube.com/watch?v={video_info.video_id}",
                        new_tab=True,
                    ).classes("btn-blue text-xs font-semibold px-4 py-2 mt-1")

            def start_youtube_playback():
                # In-place layer activation: hide poster, reveal player iframe
                poster_layer.classes(add="hidden")
                player_layer.classes(remove="hidden")

                with player_layer:
                    ui.html(
                        f'<iframe id="youtube-player-iframe" class="youtube-frame" '
                        f'src="https://www.youtube-nocookie.com/embed/{video_info.video_id}'
                        f'?autoplay=1&controls=1&playsinline=1&rel=0&enablejsapi=1" '
                        f'title="{escape(video_info.title)}" '
                        f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                        f'allowfullscreen '
                        f'referrerpolicy="strict-origin-when-cross-origin"></iframe>',
                        sanitize=False,
                    )

                # Set up postMessage error listener for YouTube iframe error codes (100, 101, 150)
                ui.run_javascript(
                    """
                    if (!window.__pipYoutubeListenerAttached) {
                        window.__pipYoutubeListenerAttached = true;
                        window.addEventListener('message', function(event) {
                            try {
                                var data = typeof event.data === 'string' ? JSON.parse(event.data) : event.data;
                                if (data && (data.event === 'onError' || (data.info && [2, 5, 100, 101, 150].indexOf(data.info) !== -1))) {
                                    var errBox = document.getElementById('video-error-banner');
                                    if (errBox) errBox.classList.remove('hidden');
                                }
                            } catch(e) {}
                        });
                    }
                    """
                )

                if on_playback_started:
                    on_playback_started()
                if on_status_change:
                    on_status_change("Status: Video active in embedded YouTube player")

            # Click anywhere on poster layer activates playback
            poster_layer.on("click", lambda _: start_youtube_playback())

            def handle_keydown(e):
                key = getattr(e, "key", None)
                if key is None and hasattr(e, "args") and isinstance(e.args, dict):
                    key = e.args.get("key")
                if key in ("Enter", " ", "Spacebar"):
                    start_youtube_playback()

            poster_layer.on("keydown", handle_keydown)

        else:
            with ui.column().classes("video-poster-layer items-center justify-center p-6 text-center"):
                ui.icon("play_disabled", size="3rem", color="grey-6")
                ui.label("No direct video available for this lesson.").classes("text-sm text-stone-300 mt-2")
                ui.label("Continue directly to Experiment and Practice stages.").classes("text-xs text-stone-400")

    return {
        "container": video_container,
    }
