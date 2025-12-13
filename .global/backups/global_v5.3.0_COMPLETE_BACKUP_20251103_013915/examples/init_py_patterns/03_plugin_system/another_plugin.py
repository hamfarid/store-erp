"""Another example plugin"""


class AnotherPlugin:
    """Another plugin example"""
    
    name = "another"
    version = "2.0.0"
    
    def initialize(self) -> None:
        """Initialize the plugin"""
        print(f"Initializing {self.name} plugin...")
        self.data = []
    
    def execute(self, *args, **kwargs):
        """Execute plugin functionality"""
        self.data.append({"args": args, "kwargs": kwargs})
        return f"Another plugin executed. Total executions: {len(self.data)}"


def register_plugin():
    """Register this plugin"""
    return AnotherPlugin

