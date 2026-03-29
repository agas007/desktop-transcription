import os
import json
from datetime import datetime
from docx import Document
from core.entities.meeting import MeetingData

class FileWriter:
    def __init__(self, base_folder="output/meetings"):
        self.base_folder = base_folder

    def _create_run_folder(self) -> str:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        folder_path = os.path.join(self.base_folder, timestamp)
        os.makedirs(folder_path, exist_ok=True)
        return folder_path

    def write(self, meeting: MeetingData) -> str:
        folder = self._create_run_folder()

        txt_transcript_path = os.path.join(folder, "transcript.txt")
        docx_transcript_path = os.path.join(folder, "transcript.docx")
        
        txt_summary_path = os.path.join(folder, "summary.txt")
        docx_summary_path = os.path.join(folder, "summary.docx")
        
        json_raw_path = os.path.join(folder, "raw.json")

        self._write_txt(txt_transcript_path, meeting.transcript.text)
        self._write_docx(docx_transcript_path, meeting.transcript.text)

        if meeting.summary_text:
            self._write_txt(txt_summary_path, meeting.summary_text)
            self._write_docx(docx_summary_path, meeting.summary_text)

        self._write_json(json_raw_path, meeting)
        
        return folder

    def _write_txt(self, path: str, content: str):
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)

    def _write_docx(self, path: str, content: str):
        doc = Document()
        doc.add_paragraph(content)
        doc.save(path)

    def _write_json(self, path: str, meeting: MeetingData):
        data = {
            "transcript_text": meeting.transcript.text,
            "segments": [{"start": s.start, "end": s.end, "text": s.text, "speaker": s.speaker} for s in meeting.transcript.segments],
            "summary_text": meeting.summary_text
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
