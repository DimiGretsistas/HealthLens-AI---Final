import os
import gradio as gr

from backend.video_processor import process_video
from backend.agent import health_agent
import backend.state as state


def gradio_process_video(youtube_url):
    if not youtube_url or not youtube_url.strip():
        return "Please paste a YouTube URL first."
    try:
        return process_video(youtube_url.strip())
    except Exception as e:
        return f"Error while processing video: {e}"


def gradio_ask_question(user_question):
    if state.current_video_id is None:
        return "Please process a YouTube video first.", ""

    if not user_question or not user_question.strip():
        return "Please ask a question first.", ""

    try:
        result = health_agent(user_question.strip())
        response = result.get("response", result)

        if isinstance(response, dict):
            answer = response.get("answer", str(response))
            sources = response.get("sources", [])
        else:
            answer = str(response)
            sources = []

        sources_text = ""
        for source in sources:
            time_value = source.get("time", "")
            url_value = source.get("url", "")
            sources_text += f"• {time_value} → {url_value}\n"

        return answer, sources_text if sources_text else "No sources returned."
    except Exception as e:
        return f"Error while answering question: {e}", ""


custom_css = """
.gradio-container {
    max-width: 1100px !important;
    margin: auto !important;
}

#main-title {
    text-align: center;
    padding: 24px 0 10px 0;
}

#main-title h1 {
    font-size: 42px;
    font-weight: 800;
}

#main-title p {
    font-size: 16px;
    opacity: 0.8;
}
"""

custom_theme = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="indigo",
    neutral_hue="slate"
)

with gr.Blocks(
    title="YouTube Health Video Q&A Assistant",
    theme=custom_theme,
    css=custom_css
) as demo:
    gr.Markdown(
        """
        <div id="main-title">
            <h1>YouTube Health Video Q&A Assistant</h1>
            <p>Process any YouTube health video, ask questions, and get timestamped answers.</p>
        </div>
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 1. Process Video")

            youtube_url = gr.Textbox(
                label="YouTube Video URL",
                placeholder="Paste a YouTube URL here..."
            )

            process_button = gr.Button(
                "Process Video",
                variant="primary"
            )

            process_output = gr.Textbox(
                label="Processing Status",
                lines=3
            )

        with gr.Column(scale=1):
            gr.Markdown("### 2. Ask Questions")

            question = gr.Textbox(
                label="Your Question",
                placeholder="Example: What are the main health warnings?",
                lines=3
            )

            ask_button = gr.Button(
                "Ask AI",
                variant="primary"
            )

    gr.Markdown("### Answer")

    answer_output = gr.Textbox(
        label="AI Answer",
        lines=10
    )

    sources_output = gr.Textbox(
        label="Sources / YouTube Timestamps",
        lines=6
    )

    process_button.click(
        fn=gradio_process_video,
        inputs=youtube_url,
        outputs=process_output
    )

    ask_button.click(
        fn=gradio_ask_question,
        inputs=question,
        outputs=[answer_output, sources_output]
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print(f"Launching on 0.0.0.0:{port}", flush=True)
    demo.queue().launch(
        server_name="0.0.0.0",
        server_port=port,
        show_error=True
    )