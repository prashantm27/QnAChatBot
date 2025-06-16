from docling.datamodel.base_models import InputFormat
from docling.datamodel.pipeline_options import EasyOcrOptions, PdfPipelineOptions
from docling.document_converter import DocumentConverter, PdfFormatOption
from dotenv import load_dotenv
import os 

load_dotenv()

artifacts_path = os.getenv("ARTIFACTS_PATH") # path of your doclings models

pipeline_options = PdfPipelineOptions(artifacts_path=artifacts_path)
doc_converter = DocumentConverter(
    format_options={
        InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_options)
    }
)
def extract_text(src_file):
    result = doc_converter.convert(src_file)
    return result.document.export_to_text()