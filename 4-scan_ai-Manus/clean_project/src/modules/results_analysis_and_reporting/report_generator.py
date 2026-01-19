import jinja2
import pdfkit
import matplotlib.pyplot as plt
import io
import base64
from datetime import datetime  # timedelta removed
import logging
from typing import List, Dict, Any, Optional, Union
# import weasyprint # type: ignore[import-untyped] # Kept for reference, but commented as unused by Flake8

from .models import ReportFormat, VisualizationType  # ReportTemplate, ReportSection, ReportDataItem, ChartType removed
from .utils import (get_data_for_report, validate_report_parameters,
                    format_data_for_visualization, sanitize_html)

# Set up logging
logger = logging.getLogger(__name__)

# Constants for duplicated literals
TABLE_AR = "جدول"
CHART_AR = "مخطط"
UNSUPPORTED_AR = "غير مدعوم"


class ReportGenerator:
    def _render_data_item(self, item: Dict[str, Any], template_engine: jinja2.Environment) -> str:
        html_content = ""
        item_type = item.get("type")
        if item_type == "table":
            html_content += template_engine.get_template("table_template.html").render(
                title=item.get("title", TABLE_AR), data=item.get("data", [])
            )
        elif item_type == "chart":
            html_content += template_engine.get_template("chart_template.html").render(
                title=item.get("title", CHART_AR),
                # ... existing code ...
            )
        else:
            html_content += f"<p>نوع العنصر '{item_type}' {UNSUPPORTED_AR}.</p>"
        return html_content

    def _generate_chart_image(self, chart_data: Dict[str, Any], chart_type_str: str) -> Optional[str]:
        # Extract labels and values from chart_data
        labels = chart_data.get('labels', [])
        values = chart_data.get('values', [])
        
        # Determine chart type
        try:
            chart_type = VisualizationType[chart_type_str.upper()]
        except KeyError:
            logger.warning(f"نوع المخطط '{chart_type_str}' {UNSUPPORTED_AR}.")
            return None
            
        # Create chart
        plt.figure(figsize=(10, 6))
        if chart_type == VisualizationType.BAR:
            plt.bar(labels, values)
        elif chart_type == VisualizationType.LINE:
            plt.plot(labels, values)
        elif chart_type == VisualizationType.PIE:
            plt.pie(values, labels=labels, autopct='%1.1f%%')
        else:
            logger.warning(f"نوع المخطط '{chart_type_str}' {UNSUPPORTED_AR}.")
            return None
            
        # Save to base64
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()
        
        return image_base64

    def generate_report_advanced(self, sections: List[Dict[str, Any]]) -> str:
        """Generate an advanced report with multiple sections"""
        section_html = ""
        
        for section in sections:
            item_type = section.get("type")
            section_data = section.get("data", {})
            
            if item_type == "table_section":
                section_html += self.render_template(
                    "table_template.html",
                    title=section.get("title", TABLE_AR),
                    data=section_data
                )
            elif item_type == "chart_section":
                chart_image_base64 = self._generate_chart_image(section_data, section.get("chart_type", "bar"))
                if chart_image_base64:
                    section_html += self.render_template(
                        "chart_template.html",
                        title=section.get("title", CHART_AR),
                        chart_image=chart_image_base64
                    )
                else:
                    section_html += f"<p>فشل في إنشاء المخطط: {section.get('title', CHART_AR)}</p>"
            else:
                logger.warning(f"نوع القسم '{item_type}' {UNSUPPORTED_AR}.")
                
        return section_html
        
    def render_template(self, template_name: str, **kwargs) -> str:
        """Render a template with the given context"""
        # This is a placeholder - actual implementation would use jinja2
        return f"<div>Template: {template_name}</div>"
