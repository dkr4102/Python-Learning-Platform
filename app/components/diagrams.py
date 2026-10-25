"""
Interactive educational visualizations for Python concept models.
Renders interactive UI diagrams for memory references, control branching, loops, slicing, OOP, and APIs.
"""
from nicegui import ui

def render_memory_pointer_diagram():
    """Interactive visualizer for Python's variable reference memory model."""
    with ui.column().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] rounded-lg p-5 my-4 font-sans"):
        with ui.row().classes("items-center justify-between w-full"):
            with ui.column().classes("gap-0"):
                ui.label("INTERACTIVE CONCEPT MODEL: MEMORY BINDING").classes("text-[10px] tracking-wider text-[#6E8098] font-bold")
                ui.label("Variables as Named Reference Pointers").classes("font-serif text-lg text-[#161616]")
            ui.label("Heap Allocation").classes("text-xs bg-[#EFEAE2] text-[#5E5A55] px-2.5 py-1 rounded")

        ui.label("Click reassign to see how Python variables rebind to new object allocations in memory rather than modifying a fixed memory bucket.").classes("text-xs text-[#5E5A55] mt-1")

        state = {"val": 42, "obj_type": "int", "addr": "0x1048B2A0"}

        with ui.row().classes("w-full justify-around items-center py-6 bg-[#F5F2EC] rounded border border-[#E2DCD2] my-3"):
            # Variable label
            with ui.column().classes("items-center p-4 bg-white border border-[#E2DCD2] rounded shadow-sm min-w-[120px]"):
                ui.label("Identifier Label").classes("text-[10px] text-[#8C857D] uppercase font-bold")
                ui.label("x").classes("font-mono text-2xl font-bold text-[#23342B]")
                ui.label("Variable Name").classes("text-[10px] text-[#5E5A55]")

            # Pointer arrow
            with ui.column().classes("items-center"):
                ui.label("points to (id)").classes("text-[10px] text-[#6E8098] font-mono")
                pointer_label = ui.label(f"──► {state['addr']} ──►").classes("font-mono text-xs text-[#23342B] font-bold")

            # Object in Heap
            with ui.column().classes("items-center p-4 bg-[#23342B] text-white rounded shadow-sm min-w-[140px]"):
                ui.label("Heap Object").classes("text-[10px] text-[#DCC9A3] uppercase font-bold")
                val_label = ui.label(str(state["val"])).classes("font-mono text-2xl font-bold text-[#A3E635]")
                type_label = ui.label(f"<class '{state['obj_type']}'>").classes("text-[10px] text-white/70 font-mono")

        with ui.row().classes("gap-2 items-center justify-center w-full"):
            def set_int():
                state["val"] = 100
                state["obj_type"] = "int"
                state["addr"] = "0x1048B4C8"
                val_label.set_text("100")
                type_label.set_text("<class 'int'>")
                pointer_label.set_text(f"──► {state['addr']} ──►")

            def set_str():
                state["val"] = "'Pip Learn'"
                state["obj_type"] = "str"
                state["addr"] = "0x7FFEE310"
                val_label.set_text("'Pip Learn'")
                type_label.set_text("<class 'str'>")
                pointer_label.set_text(f"──► {state['addr']} ──►")

            def set_float():
                state["val"] = 3.14159
                state["obj_type"] = "float"
                state["addr"] = "0x2A1990F0"
                val_label.set_text("3.14159")
                type_label.set_text("<class 'float'>")
                pointer_label.set_text(f"──► {state['addr']} ──►")

            ui.button("Reassign x = 100 (int)", on_click=set_int).props("size=sm flat").classes("text-xs bg-white border border-[#E2DCD2] text-[#161616]")
            ui.button("Reassign x = 'Pip Learn' (str)", on_click=set_str).props("size=sm flat").classes("text-xs bg-white border border-[#E2DCD2] text-[#161616]")
            ui.button("Reassign x = 3.14159 (float)", on_click=set_float).props("size=sm flat").classes("text-xs bg-white border border-[#E2DCD2] text-[#161616]")


def render_slicing_diagram():
    """Interactive visualizer for Python string and list slicing."""
    with ui.column().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] rounded-lg p-5 my-4 font-sans"):
        ui.label("INTERACTIVE CONCEPT MODEL: SEQUENCE INDEXING & SLICING").classes("text-[10px] tracking-wider text-[#6E8098] font-bold")
        ui.label("List & String Index Coordinate Space").classes("font-serif text-lg text-[#161616]")
        ui.label("Sequence: ['P', 'Y', 'T', 'H', 'O', 'N']").classes("text-xs font-mono text-[#5E5A55] mb-2")

        elements = ["P", "Y", "T", "H", "O", "N"]
        slice_result = ui.label("Slice sequence[1:4] -> ['Y', 'T', 'H'] (indices 1, 2, 3)").classes("font-mono text-sm text-[#23342B] font-bold p-2 bg-[#EFEAE2] rounded w-full text-center")

        with ui.row().classes("w-full justify-center gap-1 my-3 overflow-x-auto"):
            for idx, char in enumerate(elements):
                with ui.column().classes("items-center p-2.5 bg-white border border-[#E2DCD2] rounded min-w-[55px]"):
                    ui.label(f"+{idx}").classes("text-[10px] font-mono text-[#2D6A4F] font-bold")
                    ui.label(char).classes("font-mono text-xl font-bold text-[#161616] my-1")
                    ui.label(f"-{len(elements)-idx}").classes("text-[10px] font-mono text-[#9D3A3A] font-bold")

        with ui.row().classes("w-full justify-center gap-2"):
            ui.button("[:3] (First 3)", on_click=lambda: slice_result.set_text("Slice sequence[:3] -> ['P', 'Y', 'T']")).props("size=sm flat").classes("text-xs bg-white border border-[#E2DCD2]")
            ui.button("[1:4] (Middle)", on_click=lambda: slice_result.set_text("Slice sequence[1:4] -> ['Y', 'T', 'H']")).props("size=sm flat").classes("text-xs bg-white border border-[#E2DCD2]")
            ui.button("[::2] (Step 2)", on_click=lambda: slice_result.set_text("Slice sequence[::2] -> ['P', 'T', 'O']")).props("size=sm flat").classes("text-xs bg-white border border-[#E2DCD2]")
            ui.button("[::-1] (Reverse)", on_click=lambda: slice_result.set_text("Slice sequence[::-1] -> ['N', 'O', 'H', 'T', 'Y', 'P']")).props("size=sm flat").classes("text-xs bg-white border border-[#E2DCD2]")


def render_api_flow_diagram():
    """Visualizer for REST API Request-Response architecture."""
    with ui.column().classes("w-full bg-[#FBF8F3] border border-[#E2DCD2] rounded-lg p-5 my-4 font-sans"):
        ui.label("INTERACTIVE CONCEPT MODEL: REST ARCHITECTURE").classes("text-[10px] tracking-wider text-[#6E8098] font-bold")
        ui.label("HTTP Client-Server Request / Response Flow").classes("font-serif text-lg text-[#161616]")

        with ui.row().classes("w-full justify-between items-center py-4 bg-[#F5F2EC] rounded border border-[#E2DCD2] px-6 my-2"):
            with ui.column().classes("items-center p-3 bg-white border border-[#E2DCD2] rounded min-w-[130px]"):
                ui.icon("terminal", size="24px").classes("text-[#23342B]")
                ui.label("Python Client").classes("font-serif font-bold text-sm")
                ui.label("requests.get()").classes("text-[10px] font-mono text-[#5E5A55]")

            with ui.column().classes("items-center flex-1 px-4"):
                ui.label("1. HTTP GET /forecast?city=Rajkot ──►").classes("text-xs font-mono text-[#23342B] font-bold")
                ui.label("◄── 2. HTTP 200 OK (Content-Type: application/json)").classes("text-xs font-mono text-[#2D6A4F] font-bold mt-2")

            with ui.column().classes("items-center p-3 bg-white border border-[#E2DCD2] rounded min-w-[130px]"):
                ui.icon("cloud", size="24px").classes("text-[#6E8098]")
                ui.label("REST Web Service").classes("font-serif font-bold text-sm")
                ui.label("open-meteo.com").classes("text-[10px] font-mono text-[#5E5A55]")
