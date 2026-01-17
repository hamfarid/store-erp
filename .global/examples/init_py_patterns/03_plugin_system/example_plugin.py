"""Example plugin implementation"""


class ExamplePlugin:
    """Example plugin that demonstrates the plugin interface"""
    
    name = "example"
    version = "1.0.0"
    
    def initialize(self) -> None:
        """Initialize the plugin"""
        print(f"Initializing {self.name} plugin...")
    
    def execute(self, *args, **kwargs):
        """Execute plugin functionality"""
        return f"Example plugin executed with args={args}, kwargs={kwargs}"


def register_plugin():
    """Register this plugin"""
    return ExamplePlugin

